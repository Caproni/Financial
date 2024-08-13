FROM python:latest

LABEL maintainer "Edmund Bennett"
LABEL repository "Financial"
LABEL entrypoint "update_stocks.py"

ENV DEBIAN_FRONTEND=noninteractive
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

COPY update_stocks.py /code/

RUN chmod +x /code/update_stocks.py

CMD ["python", "update_stocks.py"]