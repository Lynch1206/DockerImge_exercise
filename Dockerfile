# Use the official Anaconda base image
FROM continuumio/anaconda3

# Set the working directory in the container
WORKDIR /app

# Copy the environment.yml file into the container at /app
COPY environment.yml /app/environment.yml

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libhdf5-dev

# Create the conda environment based on the environment.yml file
RUN conda env create -f /app/environment.yml
RUN conda env activate myenv

# Ensure the shell uses the new environment
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Install any additional packages with pip if necessary
# RUN pip install --no-cache-dir tensorflow keras jupyter
RUN pip install --no-cache-dir tensorflow keras

# Copy the current directory contents into the container at /app
COPY . /app

# Set the environment variable for the Anaconda environment
ENV PATH /opt/conda/envs/myenv/bin:$PATH

# Expose port for Jupyter Notebook
# EXPOSE 8888

# # Command to run Jupyter Notebook
# CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]

# Command to run your GAN training script
CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "train_gan.py"]