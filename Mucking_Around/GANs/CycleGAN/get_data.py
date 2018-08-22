import cv2
import os
import numpy as np
#import matplotlib.pyplot as plt


def get_data(base_dir = 'zebrahorse/horse2zebra', type='train'):

    horses = [
        cv2.resize(cv2.imread(base_dir + '/' + type +'A/' + img), (128,128))
        for img in os.listdir(base_dir + '/' + type + 'A')
    ]

    zebras = [
        cv2.resize(cv2.imread(base_dir + '/' + type +'B/' + img), (128,128))
        for img in os.listdir(base_dir + '/' + type + 'B')
    ]


    return horses, zebras

def check_size(dataset, channels = 3):
    consistant = True
    for i in range(channels):
        max_val = np.max([x[i] for x in [np.shape(x) for x in dataset]])
        min_val = np.min([x[i] for x in [np.shape(x) for x in dataset]])

        if max_val != min_val:
            consistant = False
            print('sizes in-consistant in channel %i' % i)

    if consistant:
        print('Sizes all consistant')
