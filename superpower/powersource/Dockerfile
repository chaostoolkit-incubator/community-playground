FROM python:3.7.1-alpine3.7

ADD requirements.txt requirements.txt
RUN apk update && \
    apk add --update --no-cache python-dev build-base linux-headers pcre-dev && \
    pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /tmp/* /root/.cache

ADD . .

EXPOSE 6061/tcp

#ENTRYPOINT ["gunicorn"]
#CMD ["--workers=2", "-b", "0.0.0.0:6061", "--preload", "app:app"]


ENTRYPOINT ["uwsgi"]
CMD ["--http", "0.0.0.0:6061", "--master", "--processes", "2", "--module", "app:app"]