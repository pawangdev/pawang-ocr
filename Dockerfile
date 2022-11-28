FROM python:3.9-bullseye

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN apt-get update -y
RUN apt-get install -y python3-pip tesseract-ocr libtesseract-dev ffmpeg libsm6 libxext6
RUN apt-get install autoconf automake libtool -y
RUN apt-get install autoconf-archive -y
RUN apt-get install pkg-config -y
RUN apt-get install libpng12-dev -y
RUN apt-get install libjpeg8-dev -y
RUN apt-get install libtiff5-dev -y
RUN apt-get install zlib1g-dev -y
RUN apt-get install libicu-dev -y
RUN apt-get install libpango1.0-dev -y
RUN apt-get install libcairo2-dev -y


RUN wget https://github.com/tesseract-ocr/tessdata_best/raw/main/ind.traineddata -o /usr/share/tesseract-ocr/4.00/tessdata/ind.traineddata

RUN pip install --upgrade pip setuptools wheel
RUN pip install opencv-python
RUN pip install -U numpy
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["python", "main.py"]
