# library files
import cv2 as cv
import numpy as np

class PupilDetector:
    def __init__(self) -> None:
        pass

    def detect(self, image_matrix, threshold_correction = 10):
        # the original image matrix in BGR color mode
        self.image_matrix = image_matrix

        # coverting the BGR image matrix to gray 
        self.gray_matrix = cv.cvtColor(self.image_matrix, cv.COLOR_BGR2GRAY)
        self.threshold_correction = threshold_correction

        # threshold value for 
        threshold = self.getMinThreshold()

        # thresholding the gray image
        thresh = self.thresholding(threshold = threshold)

        # finding the contours in the thresholded image
        contours = self.getContours(thresh)

        # the center cordinate and the radius of pupil enclosing minimum circle 
        x, y, radius = self.findPupil(contours)
        return (x, y, radius), self.image_matrix
    
    def getMinThreshold(self):
        # the pupil is suppose to be the darkest region in the gray image
        # finding the darkest cell intensity and adding a threshold correction 
        # for error in colour gradient within the pupil
        min_threshold = 255
        for i in range(len(self.gray_matrix)):
            for j in range(len(self.gray_matrix[0])):
                min_threshold = min(min_threshold, self.gray_matrix[i][j])
        return min_threshold + self.threshold_correction
    
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
        cv.circle(self.image_matrix, (x, y), radius,(255,153,153), 2)
        return x, y, radius

# # driver code
# image = cv.imread("IR.jpg")
# PD = PupilDetector()
# (x, y, r), pupil = PD.detect(image)
# print("x:{}, y:{}, r:{}".format(x, y, r))
# cv.imshow("final", pupil)
# cv.waitKey(0)

# video driver code
# pupil video credit: https://youtu.be/vAgGeLJ37iU
cap = cv.VideoCapture('1.mp4')
PD = PupilDetector()
status = True
radius = None
font = cv.FONT_HERSHEY_SIMPLEX
org = (180, 220)
fontScale = 1
thickness = 2
while cap.isOpened():
    ret, frame = cap.read()
    # check whether ther is any frame to read or not
    if ret:
        (x, y, r), pupil = PD.detect(frame)
        if status:
            radius = r
            status = False
        if abs(r - radius) >= 10:
            cv.putText(pupil, 'No Pupil', org, font, fontScale, (255, 255, 255), thickness, cv.LINE_AA)
        else:
            cv.putText(pupil, 'Pupil', org, font, fontScale, (255, 255, 255), thickness, cv.LINE_AA)
        cv.imshow("Pupil detection", pupil)
    else:
        break
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()