FROM tiangolo/uvicorn-gunicorn:python3.7-alpine3.8

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"



RUN pip install starlette aiofiles jinja2

# COPY requirements.txt .
# RUN pip3 install -r requirements.txt



COPY ./app /app
COPY ./statics /app/statics
COPY ./templates /app/templates