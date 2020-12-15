
from fastai.vision.all import *
import cv2
import pathlib

import fastai.losses
import fastai.layers

fastai.layers.BaseLoss = fastai.losses.BaseLoss
fastai.layers.CrossEntropyLossFlat = fastai.losses.CrossEntropyLossFlat
fastai.layers.BCEWithLogitsLossFlat = fastai.losses.BCEWithLogitsLossFlat
fastai.layers.BCELossFlat = fastai.losses.BCELossFlat
fastai.layers.MSELossFlat = fastai.losses.MSELossFlat
fastai.layers.L1LossFlat = fastai.losses.L1LossFlat
fastai.layers.LabelSmoothingCrossEntropy = fastai.losses.LabelSmoothingCrossEntropy
fastai.layers.LabelSmoothingCrossEntropyFlat = fastai.losses.LabelSmoothingCrossEntropyFlat

class predictor():

    def __init__(self, fn='export_orig.pkl', cpu=True):
        self.predictor = load_learner(fn, cpu=cpu)
    def approxPoints(self, mask):
        contours = cv2.findContours(mask.copy().astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
        contours = sorted(contours, key=cv2.contourArea)[-1]
        return self.approxContour(contours)

    def approxContour(self, cnt, eps=0.001):
        arclen = cv2.arcLength(cnt, True)
        epsilon = arclen * eps
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        return approx

    def predict(self, img):
        pred = self.predictor.predict(img)
        mask = cv2.resize(pred[1].float().numpy().astype(np.float32), img.shape[:2])
        points = self.approxPoints(mask)

        return points.squeeze()

