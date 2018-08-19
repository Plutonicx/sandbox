import numpy as np
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import pydot

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
from keras.layers import BatchNormalization, Concatenate, LeakyReLU, Flatten, ReLU
from keras.activations import relu, tanh, sigmoid
from keras.models import Model, Sequential

# start with the generator.

generator_length = 100

gen_input = Input(
    shape=(generator_length,),
    dtype='float32',
    name='gen_input'
)

# layer 1
gen_layer_1 = Dense(
    units = 7*7*256
)(gen_input)

gen_layer_1 = Reshape(
    target_shape=(7,7,256,)
)(gen_layer_1)

gen_layer_1 = BatchNormalization()(gen_layer_1)

gen_layer_1 = ReLU()(gen_layer_1)



# layer 2

gen_layer_2 = Conv2DTranspose(
    filters = 128,
    kernel_size=5,
    strides=(2,2,),
    padding="same"
)(gen_layer_1)

gen_layer_2 = BatchNormalization()(gen_layer_2)

gen_layer_2 = ReLU()(gen_layer_2)

# layer 3

gen_layer_3 = Conv2DTranspose(
    filters = 64,
    kernel_size=5,
    strides=(2,2,),
    padding="same"
)(gen_layer_2)

gen_layer_3 = BatchNormalization()(gen_layer_3)

gen_layer_3 = ReLU()(gen_layer_3)


# layer 4

gen_final = Conv2DTranspose(
    filters = 1,
    kernel_size=5,
    strides=(1,1,),
    padding="same",
    activation="tanh"
)(gen_layer_3)

#gen_final = tanh(gen_final)

gen_final = Reshape(
    target_shape=(28,28,1,)
)(gen_final)
# now for the discriminator.

main_input = Input(
    shape=(28,28,1,),
    dtype='float32',
    name='main_input'
)

disc_merge = Concatenate(axis=0)([
    main_input,
    gen_final
])



disc_input = Input(
    shape=(28,28,1,),
    dtype='float32',
    name='main_input'
)

shared_layer = Conv2D(
    filters=64,
    kernel_size=(3,3,),
    name='conv_layer_1'
)

main_layer_1_a = shared_layer(disc_merge)
main_layer_1_b = shared_layer(gen_final)

shared_norm = BatchNormalization(name='batch_layer_1')

main_layer_1_a = shared_norm(main_layer_1_a)
main_layer_1_b = shared_norm(main_layer_1_b)

shared_leak = LeakyReLU(alpha=0.2, name='lrelu_layer_1')

main_layer_1_a = shared_leak(main_layer_1_a)
main_layer_1_b = shared_leak(main_layer_1_b)

shared_conv = Conv2D(
    filters=128,
    kernel_size=(3,3,)
)

main_layer_2_a = shared_conv(main_layer_1_a)
main_layer_2_b = shared_conv(main_layer_1_b)

shared_batch_2 = BatchNormalization()

main_layer_2_a = shared_batch_2(main_layer_2_a)
main_layer_2_b = shared_batch_2(main_layer_2_b)

shared_leak_2 = LeakyReLU(alpha=0.2)

main_layer_2_a = shared_leak_2(main_layer_2_a)
main_layer_2_b = shared_leak_2(main_layer_2_b)

main_layer_3_a = Reshape(target_shape=(24*24*128,))(main_layer_2_a)
main_layer_3_b = Reshape(target_shape=(24*24*128,))(main_layer_2_b)

shared_dense = Dense(10, activation='sigmoid')

discriminator_a = shared_dense(main_layer_3_a)
discriminator_b = shared_dense(main_layer_3_b)



model = Model(
    inputs=[gen_input, main_input],
    outputs=[discriminator_a,discriminator_b]
)

# loss functions and outputs..

# for the combined discriminator the output needs to be
# gen_discriminator - output = 1
# combined_discriminator - output = 1*(1 - smooth) for smoothing parameter ~ 0.1,
# when input is from the actual dataset, and 0 when the data is from the generated
# dataset.

# For all cases the loss is cross entropy and can try & use equal weights for
# the outputs.

smooth = 0.1

generator_input = [
    np.random.normal(0,1,generator_length)
    for x in range(len(x_train))
]

generator_output = [1 for x in range(len(x_train))]

discriminator_output = [
    1 - smooth for x in range(len(x_train))
] + [
    0 for x in range(len(x_train))
]


# train the model.

from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot

SVG(model_to_dot(model).create(prog='dot', format='svg'))

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])



gan = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(25, activation=tf.nn.relu),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
