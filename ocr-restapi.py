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
    myconfig = r"--oem 3 --psm 6"
    return pytesseract.image_to_string(image, config=myconfig, lang='ind')


def findTotal(text):
    for word in text.lower().split("\n"):
        if 'total' in word:
            removeChars = re.sub("[^\s\.,\d]", "", word).replace(
                " ", "")
            regexAmount = re.search(
                r'^(0|[1-9][0-9]{0,2})([\.,]\d{3})*(\.\d{1,2})?$', removeChars)
            return regexAmount.group()
        elif 'subtotal' in word:
            removeChars = re.sub("[^\s\.,\d]", "", word).replace(
                " ", "")
            regexAmount = re.search(
                r'^(0|[1-9][0-9]{0,2})([\.,]\d{3})*(\.\d{1,2})?$', removeChars)
            return regexAmount.group()

@app.route('/', methods=['GET'])
def index():
    return 'Team Pawang OCR 2022'

@app.route('/scan', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']

        # create a secure filename
        filename = secure_filename(f.filename)

        # save file to /static/uploads
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # load the example image and convert it to grayscale
        image = cv2.imread(filepath, 0)

        # save the processed image in the /static/uploads directory
        ofilename = os.path.join(
            app.config['UPLOAD_FOLDER'], "{}.png".format(os.getpid()))
        cv2.imwrite(ofilename, image)

        # perform OCR on the processed image
        final_amounts = findTotal(ocrOCR(image))

        # remove the processed image
        os.remove(ofilename)

        if len(final_amounts) != 0:
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
    app.run(host="0.0.0.0", port=8080, debug=False)
