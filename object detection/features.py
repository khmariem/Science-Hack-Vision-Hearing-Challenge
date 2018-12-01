from detection import detection
from classify import classify
from skimage.transform import resize


def feat_vecs(image):
    features=[]
    rbboxes,rclasses,rscores = detection(image)
    height, width = image.shape[:2]
    for bbx in rbboxes:
        image_bbx = image[int(height*bbx[0]):int(height*bbx[2]),int(width*bbx[1]):int(width*bbx[3]),:]
        image_bbx = resize(image_bbx,(224,224), anti_aliasing=True)
        feature = classify(image_bbx)
        features.append(feature)
    return features




