FROM python:3.12.3
ENV PYTHONDONTWRITEVYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /mysite/mysite/weatherapi

COPY requirements.txt /mysite/mysite/weatherapi
RUN apt-get update && apt-get install -y nodejs npm
RUN pip install -r requirements.txt

COPY . /mysite/mysite/weatherapi
