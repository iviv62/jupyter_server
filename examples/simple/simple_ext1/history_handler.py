import os
import json
import datetime
from tornado import web
from jupyter_server.extension.handler import ExtensionHandlerMixin
from jupyter_server.base.handlers import JupyterHandler

HISTORY_DIR = "/home/jovyan/notebook_history"

class NotebookHistoryHandler(ExtensionHandlerMixin, JupyterHandler):
    @web.authenticated
    async def post(self):
        data = self.get_json_body()
        path = data.get("path")
        content = data.get("content")
        if not path or not content:
            self.set_status(400)
            self.finish({"error": "Missing path or content"})
            return
        os.makedirs(HISTORY_DIR, exist_ok=True)
        base = os.path.basename(path)
        if base.endswith('.ipynb'):
            base = base[:-6]
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        history_file = os.path.join(HISTORY_DIR, f"{base}-{timestamp}.ipynb")
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(content, f)
        self.finish({"status": "saved", "history_file": history_file})

    @web.authenticated
    async def get(self):
        path = self.get_argument("path", None)
        if not path:
            self.set_status(400)
            self.finish({"error": "Missing path"})
            return
        base = os.path.basename(path)
        if not os.path.exists(HISTORY_DIR):
            self.finish({"versions": []})
            return
        if base.endswith('.ipynb'):
            base = base[:-6]
        files = [f for f in os.listdir(HISTORY_DIR) if f.startswith(base + "-") and f.endswith('.ipynb')]
        files.sort(reverse=True)
        versions = []
        for f in files:
            versions.append({
                "file": f,
                "timestamp": f.split(".")[1] if "." in f else ""
            })
        self.finish({"versions": versions})
