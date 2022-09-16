from tokenize import Double
from flask import Flask, jsonify, request
from PIL import Image
from matplotlib.pyplot import text
from werkzeug.utils import secure_filename
from pytesseract import Output
import pytesseract
import cv2
import os
import re


app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    return "Pawang OCR Service"


def containsNumber(value):
    if True in [char.isdigit() for char in value]:
        return True
    return False

# def getAmountData(text):
#     total = []
#     temp = text.split()
#     for element in temp:
#         if "total" in element.lower():
#             flag = True
#         else:
#             flag = False
#         if flag:
#             total.append(element)
#             if containsNumber(element):
#                 break

#     return total


def findAmount(total):
    temp = []
    for element in total:
        if containsNumber(element):
            temp.append(element)

    if len(temp) > 1:
        amount = ""
        for element in temp:
            amount = amount + element
        return amount
    else:
        return temp


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


@app.route('/scan', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']

        # create a secure filename
        filename = secure_filename(f.filename)

        # save file to /static/uploads
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(filepath)

        # load the example image and convert it to grayscale
        image = cv2.imread(filepath, 0)

        # save the processed image in the /static/uploads directory
        ofilename = os.path.join(
            app.config['UPLOAD_FOLDER'], "{}.png".format(os.getpid()))
        cv2.imwrite(ofilename, image)

        # perform OCR on the processed image
        myconfig = r"--oem 3 --psm 6"
        data = pytesseract.image_to_string(
            image, config=myconfig, lang='ind')

        # for i in range(amount_boxes):
        #     if float(data['conf'][i]) > 75:
        #         (x, y, width, height) = (
        #             data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        #         image = cv2.rectangle(
        #             image, (x, y), (x+width, y+height), (0, 255, 0), 2)
        #         texts.append(data['text'][i])
        # if len(texts) == 0:
        #     texts.append((pytesseract.image_to_string(
        #         Image.open(ofilename))).split())

        final_amounts = 0
        final_amounts = findTotal(data)

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
    # port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=8080, debug=True)
