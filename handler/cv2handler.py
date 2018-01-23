import cv2
import numpy as np
from matplotlib import pyplot as plt


class cv2Handler:
    def __init__(self):
        ...

    @staticmethod
    def matchAndGetCoords(img1, img2, minMatchThreshold=10):
        MIN_MATCH_COUNT = minMatchThreshold
        img1 = cv2.imread(img1, 0)
        img2 = cv2.imread(img2, 0)
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        flann = cv2.FlannBasedMatcher(dict(algorithm=0, trees=5),
                                      dict(checks=50))
        matches = flann.knnMatch(des1, des2, k=2)

        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            center = sum(dst) / 4
            center = tuple(center[0])
            return center
        else:
            print("[cv2] Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
            return None

    @staticmethod
    def testMatching(self, img1, img2, minMatchThreshold=10):
        MIN_MATCH_COUNT = minMatchThreshold
        img1 = cv2.imread(img1, 0)
        img2 = cv2.imread(img2, 0)
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        flann = cv2.FlannBasedMatcher(dict(algorithm=0, trees=5),
                                      dict(checks=50))
        matches = flann.knnMatch(des1, des2, k=2)

        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) > MIN_MATCH_COUNT:
            return True
        else:
            return False


if __name__ == '__main__':
    ...