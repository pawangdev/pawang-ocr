FROM tiangolo/meinheld-gunicorn-flask:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip tesseract-ocr ffmpeg libsm6 libxext6

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app
