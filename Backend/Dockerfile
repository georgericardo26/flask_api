FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y libpq-dev
RUN mkdir -p /code
WORKDIR /code
COPY . ./
RUN pip install --no-cache-dir -r requirements.txt