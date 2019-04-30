## Deploying the application on Kubernetes

The application can be orchestrated by Kubernetes on your local machine.

### Requirements

To run this demo, you must install:

* Docker
* [kubectl][]
* [Minikube][minikube]

[kubectl]: https://kubernetes.io/docs/tasks/tools/install-kubectl/
[minikube]: https://kubernetes.io/docs/setup/minikube/

### Deploy using minikube

[Minikube][minikube] is a tool that creates a VM on your machine and deploy
Kubernetes on that VM. This means you have a single-node Kubernetes environment.

By default, the VM created uses 4Gb of memory and 4vCPUs. It also the KVM2
hypervisor to create the virtual machine, not VirtualBox.

Please amend the `scripts/deploy-minikube.sh` accordingly if you want different
settings.

Once ready, simply run the following:

```
$ ./scripts/deploy-minikube.sh
```

This will do the following:

* create the VM
* deploy Kubernetes on it
* package each microservice into a container image using the Docker installed
  inside the VM
* deploy all the Kubernetes manifests

Please note, since everything runs in the VM, your services are not accessible
from outside your machine by default. Also, they are not accessible from
`127.0.0.1`, which we used from our experiments.
One approach is to enable port-forwarding to the reverse-proxy we deploy in
front of our services. You can do this by running the next script from a
different terminal.

```
$ ./scripts/port-forward-to-minikube.sh
```

Your application will be available on your machine's address on port 30280.

### Undeploy

Run the following:

```
$ ./scripts/undeploy-minikube.sh
```
