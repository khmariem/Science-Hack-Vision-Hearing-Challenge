from object_detection.detection import detection
from object_detection.classify import classify
from skimage.transform import resize
import numpy as np


def feat_vecs(image):
    features=[]
    rbboxes,rclasses,rscores = detection(image)
    height, width = image.shape[:2]
    for bbx in rbboxes:
        image_bbx = image[int(height*bbx[0]):int(height*bbx[2]),int(width*bbx[1]):int(width*bbx[3]),:]
        image_bbx = resize(image_bbx,(224,224), anti_aliasing=True)
        image_bbx = np.expand_dims(image_bbx, axis=0)
        feature = classify(image_bbx)
        features.append(feature)
    return features, rbboxes, rclasses, rscores




