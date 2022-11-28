FROM python:latest

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN apt-get update -y
RUN apt-get install -y libleptonica-dev leptonica-progs liblept5 ffmpeg libsm6 libxext6
RUN apt-get install -y automake
RUN apt-get install -y pkg-config
RUN apt-get install -y libsdl-pango-dev
RUN apt-get install -y libicu-dev
RUN apt-get install -y libcairo2-dev
RUN apt-get install -y bc
RUN apt-get install -y zip unzip


RUN wget https://github.com/tesseract-ocr/tesseract/archive/refs/tags/5.2.0.zip
RUN unzip 5.2.0.zip
WORKDIR /app/tesseract-5.2.0
RUN sh autogen.sh
RUN sh configure
RUN make
RUN make install
RUN ldconfig
RUN make training
RUN make training-install
WORKDIR /app/tesseract-5.2.0/tessdata
RUN wget https://github.com/tesseract-ocr/tessdata_best/raw/main/eng.traineddata
RUN wget https://github.com/tesseract-ocr/tessdata_best/raw/main/ind.traineddata
RUN wget https://github.com/tesseract-ocr/tessdata_best/raw/main/osd.traineddata
RUN export TESSDATA_PREFIX=$(pwd)
RUN tesseract --list-langs


RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

COPY . /app

CMD ["python", "main.py"]
