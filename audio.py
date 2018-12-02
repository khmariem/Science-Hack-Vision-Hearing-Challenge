
import os
import numpy as np
import pysine

def play_feature_vector(vector):
    print("feature vector shape")
    print(vector.shape)
    vector = vector.flatten()
    print(vector.shape)
    for element in range(2):
        if element < len(vector):
            print("frequency: " + str(vector[element] * 1000))
            pysine.add_frequency(vector[element] * 1000)

    pysine.play()
