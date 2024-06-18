import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os 

def intializePredectionModel():
    """
    Initialize and load a pre-trained CNN model for digit recognition.

    Returns:
    - TensorFlow/Keras model: Loaded CNN model for digit recognition.
    """
    path = os.path.abspath(os.path.join('constants', 'images', 'myModel.h5'))
    model = load_model(path)
    return model

def preProcess(img):
    """
    Preprocesses an image for Sudoku puzzle extraction.

    Args:
    - img (numpy.ndarray): Input image (BGR color format).

    Returns:
    - numpy.ndarray: Processed binary image after grayscale conversion, Gaussian blur, and adaptive thresholding.
    """
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)
    return imgThreshold

def reorder(myPoints):
    """
    Reorders a set of points to standardize their order for perspective transformation.

    Args:
    - myPoints (numpy.ndarray): Input points to be reordered.

    Returns:
    - numpy.ndarray: Reordered points in a specific format suitable for perspective transformation.
    """
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew

def biggestContour(contours):
    """
    Finds the largest contour in a list of contours assumed to be the Sudoku puzzle.

    Args:
    - contours (list): List of contours detected in the image.

    Returns:
    - numpy.ndarray: Biggest contour representing the Sudoku puzzle.
    - float: Area of the biggest contour.
    """
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest, max_area

def splitBoxes(img):
    """
    Splits the Sudoku puzzle image into 81 individual cells (boxes).

    Args:
    - img (numpy.ndarray): Input Sudoku puzzle image.

    Returns:
    - list: List of 81 numpy arrays, each representing an individual cell (box) of the Sudoku puzzle.
    """
    rows = np.vsplit(img, 9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 9)
        for box in cols:
            boxes.append(box)
    return boxes

def getPrediction(boxes, model):
    """
    Predicts digits present in each cell (box) of the Sudoku puzzle.

    Args:
    - boxes (list): List of 81 numpy arrays, each representing an individual cell (box) of the Sudoku puzzle.
    - model (tensorflow.keras.Model): Trained CNN model for digit recognition.

    Returns:
    - list: List of integers representing the predicted digits for each cell in the Sudoku puzzle.
    """
    result = []
    for image in boxes:
        img = np.asarray(image)
        img = img[4:img.shape[0] - 4, 4:img.shape[1] - 4]
        img = cv2.resize(img, (28, 28))
        img = img / 255
        img = img.reshape(1, 28, 28, 1)
        predictions = model.predict(img)
        classIndex = np.argmax(predictions, axis=-1)
        probabilityValue = np.amax(predictions)
        if probabilityValue > 0.8:
            result.append(classIndex[0])
        else:
            result.append(0)
    return result
