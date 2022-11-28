FROM python:slim-buster
WORKDIR /app
RUN apt-get update -y
RUN apt-get install -y python3-pip python3 tesseract-ocr ffmpeg libsm6 libxext6

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000
CMD [ "uvicorn main:app --reload" ]
