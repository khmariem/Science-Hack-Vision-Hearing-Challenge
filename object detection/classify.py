from keras.applications.inception_v3 import InceptionV3
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K
import numpy as np
import matplotlib.pyplot as plt

#creating the pre-trained model
base_model = InceptionV3(weights='imagenet')

#Cutting the model until the required layers needed for extraction (predictions in this case, i.e last layer)
model = Model(inputs=base_model.input, outputs=base_model.get_layer('predictions').output)

def classify(img):

    prediction_features=model.predict(img)

    return prediction_features




