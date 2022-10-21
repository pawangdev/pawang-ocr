from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import pytesseract
import cv2
from PIL import Image
import io
import os
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def ocrOCR(image):
    myconfig = r"--oem 3 --psm 11"
    return list(pytesseract.image_to_string(Image.open(io.BytesIO(image)), config=myconfig, lang='ind').split("\n"))


def findTotal(text):
    flag = 0
    tempAmount = []
    finalAmount = 0

    # remove all empty string in the list
    while("" in text):
        text.remove("")

    # finding total's index
    for index, word in enumerate(text):
        word = word.lower()
        if ('total' in word) and (word.__eq__('subtotal') == False):
            flag = index
            # print('masuk pak eko')
            # print('flag: {}'.format(flag))
            # print('text[flag]: {}'.format(text[flag]))

    # finding the total amount
    for word in text[flag:]:
        word = word.lower()

        # remove special characters
        word = re.sub('[^A-Za-z0-9]+', '', word)
        # print('word mu i lo {}'.format(word))
        
        # remove RP
        if 'rp' in word:
            word = re.sub('rp', '', word)
        # print('word phase 2 :{}'.format(word))
        
        # check is it number
        amount = re.search(r'^\d+(?:,\d*)?$', word)
        # print("amount : {}".format(amount))
        
        if amount is None:
          if len(tempAmount) >= 1:
            break
          else:
            continue
        else: 
            # print("ndek kene bro dee")
            tempAmount.append(amount.group())
    
    if len(tempAmount) > 1:
        finalAmount = int(''.join(tempAmount))
    elif len(tempAmount) == 0:
        finalAmount = 0
    else:
        finalAmount = int(tempAmount[0])

    return finalAmount

@app.route('/', methods=['GET'])
def index():
    return 'Team Pawang OCR 2022'

@app.route('/scan', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        image = request.files['file'].read()

        # perform OCR on the processed image
        final_amounts = findTotal(ocrOCR(image))

        if final_amounts != 0:
            data_returned = {
                "status": "true",
                "amounts": final_amounts,
            }
        else:
            data_returned = {
                "status": "false",
                "amounts": final_amounts,
            }

        return jsonify(data_returned)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
