# DockerImage exercise
I am a fresh new Docker learner.

## Goal1
Build a docker image and deploy it to train an easy GAN model. 
> This exercise is not about how good the model is.
- [ ] The purpose of the exercise is to build and deploy a docker image for python training.
- [ ] User can export the training result to the local device.


## Run down
1. Build a [Dockerfile script](./Dockerfile).
2. Build docker image with `conda` environment and specify environment with [`.yml` file](./environment.yml).
   - Activate the environment.
   - Build with [shell script](./build.sh).
3. Run the [`train_gan.py`](./train_gan.py) script with the environment, invoking with [run.sh](./run.sh) script.
4. Assign local path in train file and shell script.

## Goal2
Interacting with sql database software. (see [folder](./Postergresql/document.md))
- [ ] Parse data and save data in the container.
- [ ] Export the container as a docker image.