FROM python:3.7.1-alpine3.7

ADD requirements.txt requirements.txt
RUN apk update && \
    apk add --update --no-cache python-dev build-base linux-headers pcre-dev && \
    pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /tmp/* /root/.cache

ADD app.py app.py
ADD characters.json characters.json
ADD templates templates

EXPOSE 6060/tcp

ENTRYPOINT ["uwsgi"]
CMD ["--http", "0.0.0.0:6060", "--master", "--processes", "2", "--module", "app:app"]