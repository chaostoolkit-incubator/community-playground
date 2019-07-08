FROM python:3.7-rc-alpine

ADD requirements.txt requirements.txt
RUN apk update && \
    pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /tmp/* /root/.cache

ADD . .

EXPOSE 8080/tcp

ENTRYPOINT ["python"]
CMD ["app.py"]