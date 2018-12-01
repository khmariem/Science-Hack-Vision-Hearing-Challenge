import cv2
import os

camera = cv2.VideoCapture(1)
rc, img = camera.read()
camera.set(3,1920)
rc, img = camera.read()
f = 'img'
n = f +'\\'+ str(max([1]+[int(i[:-4]) for i in os.listdir(f) if i[-4:] == '.jpg'])+1) + '.jpg'
cv2.imwrite(n,img)
cv2.destroyAllWindows()