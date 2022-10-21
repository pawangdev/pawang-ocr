FROM python:slim-buster
WORKDIR /app
RUN apt-get update -y
RUN apt-get install -y python3-pip python3 tesseract-ocr tesseract-ocr-ind ffmpeg libsm6 libxext6

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8080
CMD [ "python3", "ocr-restapi.py" ]