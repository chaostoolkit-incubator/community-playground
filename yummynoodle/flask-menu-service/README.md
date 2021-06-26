# Python Flask Menu Service #

This is a first version of the menu service in Python Flask, it is
currently using static data but it will evolve to use some form of document
database probably firebase.

To run locally run

```bash
$ python app.py
```

Build the image using the following command

```bash
$ docker build -t flask-menu-service:latest .
```

Run the Docker container using the command shown below.

```bash
$ docker run docker run -d -p 5000:5000 flask-menu-service
```
To determine the ip address of the docker machine execute
```bash
$ docker-machine default ip
```

The application will be accessible at the given ip address and can be tested with curl using:

```bash
$ curl -i http://<IP_ADDRESS>:5000/menu/api/v1.0/menus
```
for the full menu and

```bash
$ curl -i http://<IP_ADDRESS>:5000/menu/api/v1.0/menu/2
```

For a single menu entry.
