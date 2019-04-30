## Deploying the application on Kubernetes

The application can be orchestrated by Kubernetes on your local machine.

### Requirements

To run this demo, you must install:

* Docker
* [kubectl][]
* [microk8s][microk8s]
* [snap][]

[snap]: https://docs.snapcraft.io/installing-snapd/6735
[kubectl]: https://kubernetes.io/docs/tasks/tools/install-kubectl/
[microk8s]: https://microk8s.io/

### Deploy using microk8s (Linux only)

[microk8s][microk8s] is a tool that installs Kubernetes directly on your local
machine without a VM. This means you have a single-node Kubernetes environment.

Please amend the `scripts/deploy-minikube.sh` accordingly if you want different
settings.

Once ready, simply run the following:

```
$ ./scripts/deploy-microk8s.sh
```

This will do the following:

* deploy Kubernetes on your machine
* package each microservice into a container image using the Docker daemon
  ran by microk8s
* deploy all the Kubernetes manifests
* configure your `~/.kube/config` so you can use the native `kubectl`

Please note, refer to the [microk8s documentation][microdoc] for various corner
cases that the provided script cannot provision for.

[microdoc]: https://github.com/ubuntu/microk8s#troubleshooting

### Undeploy

Run the following:

```
$ ./scripts/undeploy-microk8s.sh
```
