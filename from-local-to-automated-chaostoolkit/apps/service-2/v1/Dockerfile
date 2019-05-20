FROM python:3.7-alpine

RUN adduser -D svc

ADD requirements.txt requirements.txt
RUN apk update && \
    apk add --virtual build-deps gcc g++ libffi-dev linux-headers python3-dev libstdc++ make && \
    pip install -q -U pip && \
    pip install -q -r requirements.txt && \
    apk del build-deps && \
    rm -rf /tmp/* /root/.cache

USER svc
EXPOSE 8000/tcp

ADD metrics.py metrics.py
ADD tracing.py tracing.py
ADD app.py app.py

ENTRYPOINT ["python3"]
CMD ["app.py"]
