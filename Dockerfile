# Use the official Jupyter base-notebook as a base image
FROM jupyter/base-notebook:latest

# Set a working directory for notebooks
WORKDIR /home/jovyan/work

# (Optional) Install additional Python packages here
# RUN pip install <package-name>

# Copy any local files (e.g., requirements.txt, notebooks) if needed
# COPY requirements.txt ./
# RUN pip install -r requirements.txt

# Expose the default Jupyter port
EXPOSE 8888

# Start Jupyter Server with a preset token for easy access
CMD ["start-notebook.sh", "--NotebookApp.token=devtoken"]
