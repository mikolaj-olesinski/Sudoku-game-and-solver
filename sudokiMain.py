import os
import cv2
import numpy as np
from tools import *

def setup():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    pathImage = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Resources/1.jpg'))
    heightImg = 450
    widthImg = 450
    model = intializePredectionModel()  # LOAD THE CNN MODEL
    return pathImage, heightImg, widthImg, model

def prepareImage(pathImage, heightImg, widthImg):
    img = cv2.imread(pathImage)
    img = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
    imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)  # CREATE A BLANK IMAGE FOR TESTING DEBUGGING IF REQUIRED
    imgThreshold = preProcess(img)
    return img, imgBlank, imgThreshold

def findContours(img):
    imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3) # DRAW ALL DETECTED CONTOURS
    return imgContours, imgBigContour, contours

def processSudoku(img, biggest, widthImg, heightImg):
    if biggest.size != 0:
        biggest = reorder(biggest)
        imgBigContour = cv2.drawContours(img, biggest, -1, (0, 0, 255), 25) # DRAW THE BIGGEST CONTOUR
        pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2) # GER
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        imgDetectedDigits = imgBlank.copy()
        imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
        return imgBigContour, imgDetectedDigits, imgWarpColored
    else:
        print("No Sudoku Found")
        return None

def splitAndDetectDigits(imgWarpColored, model, imgBlank):
    imgSolvedDigits = imgBlank.copy()
    imgDetectedDigits = imgBlank.copy()  # Initialize imgDetectedDigits here
    boxes = splitBoxes(imgWarpColored)
    numbers = getPrediction(boxes, model)
    imgDetectedDigits = displayNumbers(imgDetectedDigits, numbers, color=(255, 0, 255))
    numbers = np.asarray(numbers)
    posArray = np.where(numbers > 0, 0, 1)
    print(numbers)
    return imgDetectedDigits, numbers, posArray


# Wywołanie funkcji setup
pathImage, heightImg, widthImg, model = setup()

# Wywołanie funkcji prepareImage
img, imgBlank, imgThreshold = prepareImage(pathImage, heightImg, widthImg)

# Wywołanie funkcji findContours
imgContours, imgBigContour, contours = findContours(imgThreshold)

# Wywołanie funkcji biggestContour
biggest, maxArea = biggestContour(contours)

# Wywołanie funkcji processSudoku
if biggest is not None:
    imgBigContour, imgDetectedDigits, imgWarpColored = processSudoku(img, biggest, widthImg, heightImg)

# Wywołanie funkcji splitAndDetectDigits
if imgDetectedDigits is not None:
    imgDetectedDigits, numbers, posArray = splitAndDetectDigits(imgWarpColored, model, imgBlank)

