FROM --platform=linux/arm64 python:latest

LABEL maintainer "Edmund Bennett"
LABEL repository "Financial"
LABEL entrypoint "test_cronjob.py"

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV MESON_SKIP_TESTS=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    software-properties-common \
    wget \
    git \
    cmake \
    gfortran \
    pkg-config \
    libopenblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src /code/src

COPY test_cronjob.py /code/

RUN chmod +x /code/test_cronjob.py

ENTRYPOINT ["python", "test_cronjob.py"]