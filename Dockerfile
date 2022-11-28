# FROM python:slim-buster

# WORKDIR /app

# RUN apt-get update -y
# RUN apt-get install -y python3-pip python3 tesseract-ocr ffmpeg libsm6 libxext6

# COPY . /app
# RUN pip install -r requirements.txt

# EXPOSE 8000
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

RUN apt-get update -y
RUN apt-get install -y python3-pip python3 tesseract-ocr ffmpeg libsm6 libxext6

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app
