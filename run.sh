#!/bin/bash
# get local directory
current_dir=$(pwd)
echo "Current directory: $current_dir"
docker run -it --rm -v $current_dir:/app my-gan-trainer
# docker run -it --rm my-gan-trainer