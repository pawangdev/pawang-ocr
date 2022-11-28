FROM python:3.9.15-alpine3.16

WORKDIR /app

RUN apk update && apk add tesseract-ocr
RUN apk add --no-cache \
    blas-dev \
    cargo \
    g++ \
    gcc \
    curl \
    jpeg-dev \
    lapack-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    make \
    openblas-dev \
    openssl-dev \
    py3-pip \
    python3-dev \
    zlib-dev

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip setuptools wheel
RUN pip install pip install opencv-python==4.5.3.56
RUN pip install -U numpy
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["python", "main.py"]
