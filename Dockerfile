FROM python:3.9.15-alpine3.16

WORKDIR /app

RUN apk update && apk add tesseract-ocr
RUN apk add --no-cache \
    blas-dev \
    cargo \
    g++ \
    gcc \
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

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py
RUN pip install pyopenssl

RUN pip install -U pip setuptools wheel cython
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["python", "main.py"]
