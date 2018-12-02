#!/usr/bin/env python

from threading import Thread, Lock
import numpy as np
import cv2

import sys
sys.path.append("./object_detection")
import matplotlib.pyplot as plt
from object_detection.notebooks import visualization
from object_detection.feat import FeatureVectors

class WebcamVideoStream :
    def __init__(self, src = 0, width = 320, height = 240) :
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, width)
        self.stream.set(4, height)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self) :
        if self.started :
            print ("already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self) :
        while self.started :
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self) :
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame

    def stop(self) :
        self.started = False
        if self.thread.is_alive():
            self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback) :
        self.stream.release()

if __name__ == "__main__" :
    vs = WebcamVideoStream().start()
    fv = FeatureVectors().start()
    while True :
        frame = vs.read()
        fv = fv.update(frame)

        features, rbboxes, rclasses, rscores = fv.read()

        print(rbboxes)
        img = visualization.plt_bboxes(frame, rclasses, rscores, rbboxes)
        cv2.imshow('webcam', img)
        if cv2.waitKey(1) == 27 :
            break

    fv.stop()   
    vs.stop()
    cv2.destroyAllWindows()



