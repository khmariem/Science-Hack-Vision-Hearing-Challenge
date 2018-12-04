
from threading import Thread, Lock
import numpy as np
import cv2

import sys
sys.path.append("./object_detection")
import matplotlib.pyplot as plt
from object_detection.notebooks import visualization
from object_detection.feat import FeatureVectors
from audio import mix
from subprocess import Popen

class WebcamVideoStream :
    def __init__(self, src=1, width=300, height=200) :
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
    oldprocesses = []
    processes = []
    names = []
    try:
        while True :
            frame = vs.read()
            fv = fv.update(frame)

            features, rbboxes, rclasses, rscores = fv.read()
            # print(features)
            # print(rclasses)
            for f, rcl in zip(features,rclasses):
                names.append(mix(f,rcl))
            if processes:
                for p in processes: p.kill()
                # oldprocesses = processes
                processes = []
            for n in names:
                print(n)
                processes.append(Popen(['ffplay', "-nodisp", "-autoexit", "-hide_banner", n]))

            print("rboxes: " + str(rbboxes))
            img = visualization.plt_bboxes(frame, rclasses, rscores, rbboxes)
            cv2.imshow('webcam', img)
            if cv2.waitKey(1) == 27:
                break
    except Exception as e:
        fv.stop()   
        vs.stop()
        cv2.destroyAllWindows()
        for p in processes: p.kill()
        for p in oldprocesses: p.kill()
        raise e
    fv.stop()   
    vs.stop()
    cv2.destroyAllWindows()
    for p in processes: p.kill()
    for p in oldprocesses: p.kill()



