# Yummy Noodle Demo Web Client #

Web client that pulls Menu data from the Yummy Noodle Python Service and allows customers to create orders, orders are created and stored in a Firebse database, they can then be seen in the Orders page and actioned from there by the kitchen

To run locally run

```bash
$ cd html
$ pyhton -m http.server
```


Build the image using the following command

```bash
$ docker build -t yummy-web-client:latest .
```

Run the Docker container using the command shown below.

```bash
$ docker run docker run -d -p 8080:80 yummy-web-client
```

To determine the ip address of the docker machine execute

```bash
$ docker-machine default ip
```