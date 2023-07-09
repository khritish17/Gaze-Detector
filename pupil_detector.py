# library files
import cv2 as cv
import numpy as np

class PupilDetector:
    def __init__(self, image_matrix) -> None:
        self.image_matrix = image_matrix
        # converting the image matrix to gray scale
        self.gray_matrix = cv.cvtColor(image_matrix, cv.COLOR_BGR2GRAY)

    def detect(self):
        threshold = self.getMinThreshold()
        thresh = self.thresholding(threshold = threshold)
        contours = self.getContours(thresh)
        x, y, radius = self.findPupil(contours)
        return (x, y, radius), self.image_matrix
    
    def getMinThreshold(self):
        min_threshold = 255
        for i in range(len(self.gray_matrix)):
            for j in range(len(self.gray_matrix[0])):
                min_threshold = min(min_threshold, self.gray_matrix[i][j])
        return min_threshold + 10
    
    def thresholding(self, threshold = 127, maxValue = 255):
        ret, thresh = cv.threshold(self.gray_matrix, threshold, maxValue, cv.THRESH_BINARY)
        return thresh
    
    def getContours(self, thresh):
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        return contours
    
    def findPupil(self, contours):
        # Finding the max and the second max contour in terms of area
        # The second max is required as pupil is suppose to be the second max contour
        # The First max is the boundary of the image (openCV property) 
        A1, A2 = cv.contourArea(contours[0]), cv.contourArea(contours[1])
        max_area = None
        second_max = None
        if A1 >= A2: 
            max_area = [A1, contours[0]]
            second_max = [A2, contours[1]]
        else:
            max_area = [A2, contours[1]]
            second_max = [A1, contours[0]]

        for i in range(2, len(contours)):
            cnt = contours[i]
            area = cv.contourArea(cnt)
            if area >= max_area[0]:
                second_max = max_area
                max_area = [area, cnt]
            elif area >= second_max[0]:
                second_max = [area, cnt]

        # Approximating the pupil with a circle
        # finding it's center co-ordinate (x, y) and its radius  
        (x, y), radius = cv.minEnclosingCircle(second_max[1])
        x, y, radius = int(x), int(y), int(radius)
        cv.circle(self.image_matrix, (x, y), radius,(0,255,0), 2)
        return x, y, radius


# driver code
image = cv.imread("IR.jpg")
PD = PupilDetector(image)
(x, y, r), pupil = PD.detect()
print("x:{}, y:{}, r:{}".format(x, y, r))
cv.imshow("final", pupil)
cv.waitKey(0)