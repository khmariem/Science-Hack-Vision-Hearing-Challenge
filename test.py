import cv2
import numpy as np

import sys
sys.path.append("./object_detection")
import matplotlib.pyplot as plt
from object_detection.notebooks import visualization
from object_detection.features import feat_vecs

camera = cv2.VideoCapture(1)


def grab_frame(cap):
    ret, frame = cap.read()
    rc, img = camera.read()
    l, rbboxes, rclasses, rscores = feat_vecs(img)

    img = visualization.plt_bboxes(img, rclasses, rscores, rbboxes)

    # print(l)
    if len(l) > 0:
        print(np.max(l[0]))

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)



#create two subplots
ax1 = plt.subplot(1,2,1)

#create two image plots
im1 = ax1.imshow(grab_frame(camera))

plt.ion()

while True:
    im1.set_data(grab_frame(camera))
    plt.pause(0.2)

plt.ioff() # due to infinite loop, this gets never called.
plt.show()