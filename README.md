# Gaze-Detector
Official Documentation of the Gaze Detection

> **Note** The project is currently active, there may be some updates where the old API may be changed according to the requirement. Hence always look out for updates. Once the project gets finalized this NOTE will be removed.

### Description:

To detect the direction of gaze or focus of a human eye using OpenCV, computer vision, and image processing techniques. This project expects to have a good IR (infrared) image of an eye. 

### Prerequisites

- Install the latest version of Python, make sure to install the PIP pipeline 
- Install Numpy library
- Install the latest version of openCV

### Installation

- Clone the project from [GITLINK](https://github.com/khritish17/Gaze-Detector.git)

### Contact

### Author: Khritish Kumar Behera

### Email: khritish.official[at]gmail.com

### Important instruction
- The IR images or video feed (frames) should be taken such that the pupil becomes the darker region, one of the ways to achieve that is to use the IR source and the IR camera at a different location
- Make sure the ROI (Region of Intrest) is the eye, hence place the camera such that only the eye is in the frame, and all the portions of the eye are well illuminated (by IR waves), avoid any other darker shades formation
- If some darker areas are unavoidable use the *threshold_correction* parameter during the calibration to get the pupil detected
- Use of a NIR (Near Infrared) camera is advisable for keeping the eye as the ROI

# Pupil Detector

## PupilDetector( *imageMatrix*, *threshold_correction = 10* ) | return type: None
This is the constructor of the pupil detector class. It expects the <kbd> imageMatrix </kbd> (BGR color matrix of the image and not the image file name or path). There is also an optional parameter <kbd>threshold_correction</kbd> whose default value is set to 10. This parameter be changed only when the pupil is not detected during the calibration phase due to darker regions in the <kbd> imageMatrix </kbd> (originally in the frames) 
>**Note** Make sure the image resides in the same directory in which this code is, or else provide the absolute path of the image     

    # Read the image
    imageMatrix = cv.imread("IR.jpg")
    
    # PupilDetector object
    PD = PupilDetector(imageMatrix)

## detect() | return type: (x, y, radius), imageMatrix
It is a function inside the PupilDetector class to automate the process of pupil detection. This function needs to be called explicitly to initiate pupil detection. It returns the detected pupils (circular shape) x-y coordinate of the center, its radius, and the imageMatrix with the detected pupil
>**Note** Make sure the image resides in the same directory in which this code is, or else provide the absolute path of the image 
    
    # Read the image
    imageMatrix = cv.imread("IR.jpg")
    
    # PupilDetector object
    PD = PupilDetector(imageMatrix)
    (x, y, radius), pupil = PD.detect()
