FROM python:latest

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN apt-get update -y
RUN apt-get install -y python3-pip tesseract-ocr libtesseract4 libtesseract-dev libleptonica-dev tesseract-ocr-ind-best ffmpeg libsm6 libxext6 automake pkg-config pango-devel cairo-devel icu-devel

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["python", "main.py"]
