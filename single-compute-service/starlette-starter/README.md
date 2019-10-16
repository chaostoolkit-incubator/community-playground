# Python Starlete Web App Starter Kit

Simple stateless web application using [Starlette][https://www.starlette.io/]

## To run the app locally with Python

```bash
$ python app/main.py
```
### Test the application is running

When the image is running you should be able to access the running server  from  curl

`curl http://localhost:8000/msg` - should give a json response of {"message":"Hello world! From Starlette running on Uvicorn with Gunicorn in Alpine. Using Python 3.7"}

`curl http://localhost:8000/dt` - should give a json response of {"hello":"world","now":"2019-10-03 09:31:22.163548"}

The app home page can also be seen in a browser [App link](http://localhost:8000)


## To run the app with Docker

The app can also run as a Docker image. The docker image is based on [uvicorn-gunicorn-starlettedocker image](https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-starlette/)

to build:

`docker build -t imageTag .`

 to run locally on docker

 `docker run --name demo -p 80:80 imageTag`

When the image is running you should be able to access the running server  from  curl

`curl http://localhost/msg` - should give a json response of {"message":"Hello world! From Starlette running on Uvicorn with Gunicorn in Alpine. Using Python 3.7"}
`curl http://localhost/dt` - should give a json response of {"hello":"world","now":"2019-10-03 09:31:22.163548"}

to upload the image on to docker hub

`docker push username/imageTag:v1`

The image uploaded to docker hub is used in the [kubernetes deployment file](./deployment.yaml) to deploy to google cloud


