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
- The images or video feed (frames) should be taken such that the pupil becomes the darker region, one of the ways to achieve that is to use the light source and the camera at a different location
- Make sure the ROI (Region of Intrest) is the eye, hence place the camera such that only the eye is in the frame, and all the portions of the eye are well illuminated, avoid any other darker shades formation
- If some darker areas are unavoidable use the *threshold_correction* parameter during the calibration to get the pupil detected
- Use of a macro camera is advisable
- The above same procedure can be used using an IR camera and IR source
> **Warning** Long-term exposure of IR waves may be dangerous to the eye, make proper research before procedding 

# Pupil detection diver code for a given image
> **Note** Make sure the image resides in the same directory in which this code is, or else provide the absolute path of the image

    # read the image
    image = cv.imread("IR.jpg")

    # create a PupilDetector object
    PD = PupilDetector()

    # get the x-y coordinate, the radius and the image of the detected pupil 
    (x, y, r), pupil = PD.detect(image)
    print("x:{}, y:{}, r:{}".format(x, y, r))

    # display the frame
    cv.imshow("final", pupil)
    cv.waitKey(0)

# Pupil detection diver code for a video feed
> **Note**
 - Make sure the video files reside in the same directory in which this code is, or else provide the absolute path of the image
 - The credit for the video used in the driver code goes to the video available on YouTube [Link](https://youtu.be/vAgGeLJ37iU)


        # open the video file 
        cap = cv.VideoCapture('1.mp4')
        
        # create the PupilDetector object
        PD = PupilDetector()
        
        # some properties
        status = True
        radius = None
        font = cv.FONT_HERSHEY_SIMPLEX
        org = (180, 220)
        fontScale = 1
        thickness = 2
        
        # runs until the video file is opened  
        while cap.isOpened():
        ret, frame = cap.read()
        # check whether there is any frame to read or not
        if ret:
            (x, y, r), pupil = PD.detect(frame)
        
            # serves the purpose of saving the size of a pupil
            if status:
                radius = r
                status = False
        
            # if the currently detected pupil radius is 10 more or less than the original
            # considered as not pupil
            if abs(r - radius) >= 10:
                cv.putText(pupil, 'No Pupil', org, font, fontScale, (255, 255, 255), thickness, cv.LINE_AA)
            else:
                cv.putText(pupil, 'Pupil', org, font, fontScale, (255, 255, 255), thickness, cv.LINE_AA)
            cv.imshow("Pupil detection", pupil)
        else:
            break
        
        # Breaks the while loop when the letter 'q' is pressed 
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        cap.release()
        cv.destroyAllWindows()

# Pupil Detector

## PupilDetector() | return type: None
This is the constructor of the pupil detector class.    
>**Note** Make sure the image resides in the same directory in which this code is, or else provide the absolute path of the image

    # Read the image
    imageMatrix = cv.imread("IR.jpg")
    
    # PupilDetector object
    PD = PupilDetector()

## detect(*imageMatrix*, *threshold_correction = 10*) | return type: (*int* x, *int* y, *int* radius), *numpy 2d array* imageMatrix
It is a function inside the PupilDetector class to automate the process of pupil detection. It expects the <kbd> imageMatrix </kbd> (**BGR color matrix of the image and not the image file name or path**). There is also an optional parameter <kbd>threshold_correction</kbd> whose default value is set to 10. This parameter be changed only when the pupil is not detected during the calibration phase due to darker regions in the <kbd> imageMatrix </kbd> (originally in the frames). 

This function needs to be called explicitly to initiate pupil detection. It returns the detected pupils (circular shape) x-y coordinate of the center, its radius, and the imageMatrix with the detected pupil

    
    # Read the image
    imageMatrix = cv.imread("IR.jpg")
    
    # PupilDetector object
    PD = PupilDetector()
    (x, y, radius), pupil = PD.detect(image)

## getMinThreshold() | return type: (int minThreshold)
According to the camera placement relative to the eye, as described in the **Important Instructions**, the pupil is supposed to be the darkest region in the grayscale image. 

Directly hardcoding the intensity value for pupil region works only in some idle environments, but different environment conditions will lead to different light exposure which will deviate the pupils' intensity value. Hence in every image/frame, the darkest pixel value is obtained. 

That value is the minimum threshold value and again pupil will be a significantly larger darker region so there might be some variation in intensity therefore a *threshold correction* is added to the in minimum threshold value, which can be adjusted through <kbd> detect() </kbd>function.

## thresholding(int threshold = 127, int maxValue = 255) | return type: (*numpy 2d array* thresholdedImage)
## getContours(*numpy 2d array* thresholdedImage) | return type: (*numpy 3d array* contours)
## findPupil((*numpy 3d array* contours) | return type: (int x, int y, int radius)
