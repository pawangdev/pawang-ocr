FROM python:3.9-bullseye

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN sudo apt install tesseract-ocr curl wget
RUN sudo apt install libtesseract-dev

RUN wget https://github.com/tesseract-ocr/tessdata_best/raw/main/ind.traineddata -o /usr/share/tesseract-ocr/tessdata/ind.traineddata
RUN wget https://github.com/tesseract-ocr/tessdata_best/raw/main/ind.traineddata -o /usr/share/tessdata/ind.traineddata
RUN wget https://github.com/tesseract-ocr/tessdata_best/raw/main/ind.traineddata -o /usr/share/tesseract-ocr/4.00/tessdata/ind.traineddata

RUN pip install --upgrade pip setuptools wheel
RUN pip install opencv-python
RUN pip install -U numpy
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["python", "main.py"]
