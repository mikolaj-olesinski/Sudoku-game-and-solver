print('Setting UP')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from model.PhotoDetection.tools import *
import numpy as np
import cv2

def get_sudoku_from_image(path):
    """
    Process an image of a Sudoku puzzle to extract digits.

    Parameters
    ----------
    path : str
        Path to the image file containing the Sudoku puzzle.

    Returns
    -------
    list
        List of integers representing the digits extracted from the Sudoku puzzle.

    """
    pathImage = os.path.abspath(path)
    heightImg = 450
    widthImg = 450
    model = intializePredectionModel()  

    img = cv2.imread(pathImage)
    img = cv2.resize(img, (widthImg, heightImg))  
    imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8) 
    imgThreshold = preProcess(img)

    imgContours = img.copy()
    imgBigContour = img.copy() 
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)

    biggest, maxArea = biggestContour(contours) 
    if biggest.size != 0:
        biggest = reorder(biggest)
        cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 25)
        pts1 = np.float32(biggest) 
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)

        boxes = splitBoxes(imgWarpColored)
        numbers = getPrediction(boxes, model) 

    else:
        print("No Sudoku Found")
        numbers = []

    return numbers

