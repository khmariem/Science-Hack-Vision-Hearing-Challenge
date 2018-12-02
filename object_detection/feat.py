from threading import Thread, Lock
from object_detection.detection import detection
from object_detection.classify import classify
from skimage.transform import resize
import numpy as np

class FeatureVectors :

    def __init__(self) :
        self.features=[]
        self.rbboxes = [] 
        self.rclasses = []
        self.rscores = []
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

    def update(self,image) :
        if self.started:
            self.rbboxes, self.rclasses, self.rscores = detection(image)
            height, width = image.shape[:2]
            for bbx in self.rbboxes:
                image_bbx = image[int(height*bbx[0]):int(height*bbx[2]),int(width*bbx[1]):int(width*bbx[3]),:]
                image_bbx = resize(image_bbx,(224,224), anti_aliasing=True)
                image_bbx = np.expand_dims(image_bbx, axis=0)
                feature = classify(image_bbx)
                self.features.append(feature)
            
        return self


    def read(self) :
        self.read_lock.acquire()
        features = self.features.copy()
        rbboxes = self.rbboxes.copy()
        rclasses = self.rclasses.copy()
        rscores = self.rscores.copy()
        self.read_lock.release()
        return features, rbboxes, rclasses, rscores

    def stop(self) :
        self.started = False
        if self.thread.is_alive():
            self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback) :
        self.stream.release()





