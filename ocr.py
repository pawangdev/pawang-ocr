import pytesseract
import cv2
import numpy as np
import re
import string
import io


def get_string(img_path):
    # Read image with opencv
    image = cv2.imread(img_path)

    # Adaptive thresholding
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Scale and pad image
    factor = 1000 / thresh.shape[0]
    thresh = cv2.resize(thresh, None, fx=factor, fy=factor)
    thresh = cv2.copyMakeBorder(thresh, 10, 10, 10, 10,
                                cv2.BORDER_CONSTANT, value=[255, 255, 255])

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    thresh = cv2.erode(thresh, kernel, iterations=1)

    # OCR
    data = pytesseract.image_to_string(
        thresh, lang='ind', config='--psm 6 --oem 3 --tessdata-dir ./tessdata')
    return data


def text_preprocessing(data):
    # String Lower
    data = data.lower()

    # String Punctuation
    data = re.sub(r'[^\w\s]', '', data)

    # String Strip
    data = data.strip()

    # String Delete Blankspaces
    data = re.sub(' +', ' ', data)

    # String Split
    data = data.split("\n")

    # String Delete Blankspaces
    data = [x.strip() for x in data]

    return data


def find_amount(data):
    for text in data:
        total = 0
        if text.startswith('total'):
            # Delete Total
            deleteTotal = re.sub(r'total', '', text).strip()

            # Delete Total Item (Alfamart)
            deleteTotal = re.sub(
                r'([a-zA-Z]+\s+[0-9]+\s)||([a-zA-Z]+\s)', '', deleteTotal)

            # Replace Space
            deleteTotal = deleteTotal.replace(" ", "")

            total = int(deleteTotal)

            return total
        elif text.startswith('tunai'):
            deleteTotal = re.sub(r'tunai', '', text).strip()

            # Replace Space
            deleteTotal = deleteTotal.replace(" ", "")

            total = int(deleteTotal)

            return total
