from flask import Flask, jsonify, request
from PIL import Image
from matplotlib.pyplot import text
from werkzeug.utils import secure_filename
from pytesseract import Output
import pytesseract
import cv2
import os


app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

@app.route("/")
def index():
    return "Halo"

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

@app.route('/uploader', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']

        # create a secure filename
        filename = secure_filename(f.filename)

        # save file to /static/uploads
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        f.save(filepath)
        
        # load the example image and convert it to grayscale
        image = cv2.imread(filepath, 0)

        # save the processed image in the /static/uploads directory
        ofilename = os.path.join(app.config['UPLOAD_FOLDER'],"{}.png".format(os.getpid()))
        cv2.imwrite(ofilename, image)
        
        # perform OCR on the processed image
        myconfig = r"--psm 11 --oem 3"
        data = pytesseract.image_to_data(image, config=myconfig, output_type=Output.DICT)
        amount_boxes = len(data['text'])
        texts = []

        for i in range(amount_boxes):
            if float(data['conf'][i]) > 75:
                (x, y, width, height) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                image = cv2.rectangle(image, (x, y), (x+width, y+height), (0,255,0), 2)
                texts.append(data['text'][i])
        if len(texts) == 0:
            texts.append((pytesseract.image_to_string(Image.open(ofilename))).split())
        
        final_amounts = findAmount(texts)

        # remove the processed image
        os.remove(ofilename)

        if len(final_amounts) != 0:
            data_returned = {
                "message" : "1",
                "amounts" : final_amounts,
            }
        else:
            data_returned = {
                "message" : "0",
                "amounts" : final_amounts,
            }

        return jsonify(data_returned)

if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))
    app.run(host="127.0.0.1", port=8080, debug=True)