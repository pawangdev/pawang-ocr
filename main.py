from flask import Flask, request
from werkzeug.utils import secure_filename
import os
import cv2
import ocr

app = Flask(__name__)
UPLOAD_FOLDER = 'images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    return {'message': 'Team Pawang OCR Service'}


@app.route('/receipt', methods=['POST'])
def receipt():
    if 'file' not in request.files:
        return {'status': False, 'message': 'FILE_NOT_FOUND'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'status': False, 'message': 'FILE_NOT_FOUND'}, 400
    if file and allowed_file(file.filename):
        # Save File
        filename = secure_filename(file.filename)
        # Save File to /images
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        data = ocr.get_string(filepath)
        print(data)
        data = ocr.text_preprocessing(data)
        amount = ocr.find_amount(data)

        if amount == None:
            return {'status': False, 'message': 'AMOUNT_NOT_FOUND'}, 400

        return {'status': True, 'amount': amount}, 200
    return {'status': False, 'message': 'FILE_IMAGE_ONLY'}, 400
