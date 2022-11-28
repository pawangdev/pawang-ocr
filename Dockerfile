FROM python:alpine3.16

WORKDIR /app

RUN apk update && apk add tesseract-ocr

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["python", "main.py"]
