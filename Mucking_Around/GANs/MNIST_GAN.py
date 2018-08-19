import numpy as np
import time
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Reshape
from keras.layers import Conv2D, Conv2DTranspose, UpSampling2D
from keras.layers import LeakyReLU, Dropout, ReLU
from keras.layers import BatchNormalization
from keras.optimizers import Adam, RMSprop

import matplotlib.pyplot as plt

# creating discriminator (just a regular classifier)
discriminator = Sequential()

depth = 64
dropout = 0.4
# In: 28 x 28 x 1, depth = 1
# Out: 14 x 14 x 1, depth=64
input_shape = (28, 28, 1)

discriminator.add(Conv2D(depth*1, 5, strides=2, input_shape=input_shape,padding='same'))
discriminator.add(LeakyReLU(alpha=0.2))
discriminator.add(Dropout(dropout))

discriminator.add(Conv2D(depth*2, 5, strides=2, padding='same'))
discriminator.add(LeakyReLU(alpha=0.2))
discriminator.add(Dropout(dropout))

discriminator.add(Conv2D(depth*4, 5, strides=2, padding='same'))
discriminator.add(LeakyReLU(alpha=0.2))
discriminator.add(Dropout(dropout))

discriminator.add(Conv2D(depth*8, 5, strides=1, padding='same'))
discriminator.add(LeakyReLU(alpha=0.2))
discriminator.add(Dropout(dropout))

# Out: 1-dim probability
discriminator.add(Flatten())
discriminator.add(Dense(1))
discriminator.add(Activation('sigmoid'))

# build the generator
generator = Sequential()

dropout = 0.4
depth = 64*4
dim = 7
# In: 100
# Out: dim x dim x depth
generator.add(Dense(dim*dim*depth, input_dim=100))
generator.add(BatchNormalization(momentum=0.9))
generator.add(Activation('relu'))
generator.add(Reshape((dim, dim, depth)))
generator.add(Dropout(dropout))

# In: dim x dim x depth
# Out: 2*dim x 2*dim x depth/2
generator.add(UpSampling2D())
generator.add(Conv2DTranspose(int(depth/2), 5, padding='same'))
generator.add(BatchNormalization(momentum=0.9))
generator.add(Activation('relu'))

generator.add(UpSampling2D())
generator.add(Conv2DTranspose(int(depth/4), 5, padding='same'))
generator.add(BatchNormalization(momentum=0.9))
generator.add(Activation('relu'))

generator.add(Conv2DTranspose(int(depth/8), 5, padding='same'))
generator.add(BatchNormalization(momentum=0.9))
generator.add(Activation('relu'))

# Out: 28 x 28 x 1 grayscale image [0.0,1.0] per pix
generator.add(Conv2DTranspose(1, 5, padding='same'))
generator.add(Activation('sigmoid'))


# build discriminator model
disc_model = Sequential()
disc_model.add(discriminator)
disc_model.compile(
    loss='binary_crossentropy',
    optimizer=RMSprop(lr=0.0002, decay=6e-8),
    metrics=['accuracy']
)

# build adveserial model
adv_model = Sequential()
adv_model.add(generator)
adv_model.add(discriminator)
adv_model.compile(
    loss='binary_crossentropy',
    optimizer=RMSprop(lr=0.0001, decay=3e-8),
    metrics=['accuracy']
)


# visualise models
#SVG(model_to_dot(discriminator).create(prog='dot', format='svg'))
#SVG(model_to_dot(generator).create(prog='dot', format='svg'))


# get data
mnist = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0


x_train = x_train.reshape(-1, 28,28, 1).astype(np.float32)


def plot_images(generator, save2file=False, fake=True, samples=16, gen_input=None, step=0):
    filename = 'mnist.png'
    if fake:
        if gen_input is None:
            gen_input = np.random.uniform(-1.0, 1.0, size=[samples, 100])
        else:
            filename = "mnist_%d.png" % step
        images = generator.predict(gen_input)
    else:
        i = np.random.randint(0, x_train.shape[0], samples)
        images = x_train[i, :, :, :]

    plt.figure(figsize=(10,10))
    for i in range(images.shape[0]):
        plt.subplot(4, 4, i+1)
        image = images[i, :, :, :]
        image = np.reshape(image, [28, 28])
        plt.imshow(image, cmap='gray')
        plt.axis('off')
    plt.tight_layout()
    if save2file:
        plt.savefig(filename)
        plt.close('all')
    else:
        plt.show()


# train params
train_steps = 5000
batch_size = 512
smooth = 0.0

disc_records = []
adv_records = []

# start training
for i in range(train_steps):
    # create batch and generate images
    images_train = x_train[
        np.random.randint(0,x_train.shape[0], size=batch_size),
        :,
        :,
        :
    ]

    gen_input = np.random.uniform(-1, 1, size=[batch_size, 100])

    images_fake = generator.predict(gen_input)

    # build dataset and do grad-descent on the discriminator model
    x = np.concatenate((images_train, images_fake))
    y = np.ones([2*batch_size, 1])*(1-smooth)

    y[batch_size:, :] = 0
    disc_loss = disc_model.train_on_batch(x, y)

    # build dataset and do grad-descent on the adveserial model
    y = np.ones([batch_size, 1])
    gen_input = np.random.uniform(-1, 1, size=[batch_size, 100])
    adv_loss = adv_model.train_on_batch(gen_input, y)

    disc_records.append({
        "loss" : disc_loss[0],
        "acc" : disc_loss[1]
    })
    adv_records.append({
        "loss" : adv_loss[0],
        "acc" : adv_loss[1]
    })

    log_mesg = "%d: [D loss: %f, acc: %f]" % (
        i,
        disc_loss[0],
        disc_loss[1]
    )

    log_mesg = "%s  [A loss: %f, acc: %f]" % (
        log_mesg,
        adv_loss[0],
        adv_loss[1]
    )
    if i % 100 == 0:
        print(log_mesg)


plot_images(generator, fake=True)

from plotly import graph_objs as go
from plotly import figure_factory as ff
from plotly.offline import iplot
import pandas as pd

disc_df = pd.DataFrame(disc_records)
adv_df = pd.DataFrame(adv_records)

data = [
    go.Scatter(
        x = disc_df.index,
        y = disc_df['acc'].rolling(window=20).mean(),
        name = 'Discriminator Accuracy Rolling Mean'
    ),
    go.Scatter(
        x = adv_df.index,
        y = adv_df['acc'].rolling(window=20).mean(),
        name = 'Adveserial Accuracy Rolling Mean'
    )
]

layout = go.Layout(
    title = 'GAN Accuracies',
    xaxis = dict(title = 'Batch Num'),
    yaxis = dict(title = 'Accuracy')
)

fig = go.FigureWidget(data = data, layout = layout)
iplot(fig)
