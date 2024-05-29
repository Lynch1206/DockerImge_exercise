import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Reshape, BatchNormalization, Conv2D, Conv2DTranspose, LeakyReLU
import numpy as np
import matplotlib.pyplot as plt
import os, sys

# Function to build the generator
def build_generator():
    model = Sequential()
    model.add(Dense(256, input_dim=100))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Dense(1024))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Dense(28 * 28 * 1, activation='tanh'))
    model.add(Reshape((28, 28, 1)))
    return model

# Function to build the discriminator
def build_discriminator():
    model = Sequential()
    model.add(Flatten(input_shape=(28, 28, 1)))
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(256))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(1, activation='sigmoid'))
    return model

# Training function for GAN
def train_gan(generator, discriminator, gan, epochs=10000, batch_size=64):
    (X_train, _), (_, _) = tf.keras.datasets.mnist.load_data()
    X_train = X_train / 127.5 - 1.0
    X_train = np.expand_dims(X_train, axis=3)
    half_batch = batch_size // 2
    train_d_loss =[]
    epoch_ = []
    train_g_loss = []
    accuracy = []
    for epoch in range(epochs):
        idx = np.random.randint(0, X_train.shape[0], half_batch)
        real_images = X_train[idx]
        noise = np.random.normal(0, 1, (half_batch, 100))
        fake_images = generator.predict(noise)
        
        d_loss_real = discriminator.train_on_batch(real_images, np.ones((half_batch, 1)))
        d_loss_fake = discriminator.train_on_batch(fake_images, np.zeros((half_batch, 1)))
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

        noise = np.random.normal(0, 1, (batch_size, 100))
        valid_y = np.array([1] * batch_size)
        g_loss = gan.train_on_batch(noise, valid_y)

        if epoch % 1000 == 0:
            print(f"{epoch} [D loss: {d_loss[0]}, acc.: {100*d_loss[1]}] [G loss: {g_loss}]")
            train_d_loss.append(d_loss[0])
            accuracy.append(d_loss[1])
            train_g_loss.append(g_loss)
            epoch_.append(epoch)
    return train_d_loss, train_g_loss, accuracy, epoch_


    

# Build and compile the discriminator
discriminator = build_discriminator()
discriminator.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Build the generator
generator = build_generator()

# The generator takes noise as input and generates images
z = tf.keras.Input(shape=(100,))
img = generator(z)

# For the combined model, we will only train the generator
discriminator.trainable = False

# The discriminator takes generated images as input and determines validity
valid = discriminator(img)

# The combined model (stacked generator and discriminator)
gan = tf.keras.Model(z, valid)
gan.compile(loss='binary_crossentropy', optimizer='adam')

# Train the GAN
train_d_loss, train_g_loss, accuracy, epoch_ = train_gan(generator, discriminator, gan)
print('Python version: ', sys.version)
# plot training result
plt.plot(epoch_, train_d_loss, label='Discriminator Loss')
plt.plot(epoch_, train_g_loss, label='Generator Loss')
plt.plot(epoch_, accuracy, label='Accuracy')
plt.legend()
# save the image at local directory
route = os.getcwd()
plt.savefig(os.path.join(route, 'training_result.png'))
plt.show()