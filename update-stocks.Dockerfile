FROM python:latest

LABEL maintainer "Edmund Bennett"
LABEL repository "Financial"
LABEL entrypoint "update_stocks.py"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    wget \
    git \
    cmake \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

RUN apt install cmake

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src /code/src

COPY update_stocks.py /code/

RUN chmod +x /code/update_stocks.py

CMD ["python", "update_stocks.py"]