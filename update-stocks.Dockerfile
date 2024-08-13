FROM python:latest

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src /code/src

CMD ["python", "--version"]