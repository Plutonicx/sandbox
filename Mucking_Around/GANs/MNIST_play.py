import numpy as np
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt

# making sure libraries work.
image = cv2.imread("clouds.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

#plt.imshow(image)

# get mnist data
mnist = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0


plt.imshow(x_train[2], cmap='gray')

# test model
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(25, activation=tf.nn.relu),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)
model.evaluate(x_test, y_test)

# Building a GAN
from keras.layers import Input, LSTM, Dense, Conv2D, Conv2DTranspose, Reshape
from keras.layers import BatchNormalization, Concatenate, LeakyReLU
from keras.activations import relu, tanh, sigmoid
from keras.models import Model

# start with the generator.

generator_length = 100

gen_input = Input(
    shape=(generator_length,),
    dtype='float32',
    name="generator_input"
)

# layer 1
gen_layer_1 = Dense(
    units = 7*7*256
)(gen_input)

gen_layer_1 = Reshape(
    target_shape=(7,7,256,)
)(gen_layer_1)

gen_layer_1 = BatchNormalization()(gen_layer_1)

gen_layer_1 = relu(gen_layer_1)

# layer 2

gen_layer_2 = Conv2DTranspose(
    filters = 128,
    kernel_size=5,
    strides=(2,2,),
    padding="same"
)(gen_layer_1)

gen_layer_2 = BatchNormalization()(gen_layer_2)

gen_layer_2 = relu(gen_layer_2)

# layer 3

gen_layer_3 = Conv2DTranspose(
    filters = 64,
    kernel_size=5,
    strides=(2,2,),
    padding="same"
)(gen_layer_2)

gen_layer_3 = BatchNormalization()(gen_layer_3)

gen_layer_3 = relu(gen_layer_3)

# layer 4

gen_final = Conv2DTranspose(
    filters = 1,
    kernel_size=5,
    strides=(2,2,),
    padding="same"
)(gen_layer_3)

gen_final = tanh(gen_final)

gen_final = Reshape(
    target_shape=(28,28,1,)
)(gen_final)
# now for the discriminator.

main_input = Input(
    shape=(28,28,1,),
    dtype='float32',
    name='main_input'
)

disc_input = Concatenate(axis=-1)([
    main_input,
    gen_final
])


def discriminator(input):

    main_layer_1 = Conv2D(
        filters=64,
        kernel_size=(3,3,)
    )(input)

    main_layer_1 = BatchNormalization()(main_layer_1)
    main_layer_1 = LeakyReLU(alpha=0.2)(main_layer_1)

    main_layer_2 = Conv2D(
        filters=128,
        kernel_size=(3,3,)
    )(main_layer_1)

    main_layer_2 = BatchNormalization()(main_layer_2)
    main_layer_2 = LeakyReLU(alpha=0.2)(main_layer_2)


    main_layer_3 = Reshape(target_shape=(24*24*128,))(main_layer_2)

    decision = Dense(10, activation='sigmoid')(main_layer_3)

    return decision

combined_discriminator = discriminator(disc_input)
generator_discriminator = discriminator(gen_final)

main_disc = discriminator(main_input)


model = Model(
    inputs=[gen_input],
    outputs=[generator_discriminator]
)





gan = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(25, activation=tf.nn.relu),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
