FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN pip install --no-cache-dir -U pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app
