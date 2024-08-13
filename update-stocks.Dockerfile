FROM python:latest

LABEL maintainer "Edmund Bennett"
LABEL repository "Financial"
LABEL entrypoint "update_stocks.py"

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src /code/src

COPY update_stocks.py /code/

RUN chmod +x /code/update_stocks.py

CMD ["python", "update_stocks.py"]