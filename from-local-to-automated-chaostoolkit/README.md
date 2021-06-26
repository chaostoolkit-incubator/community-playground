# From solo Chaos Engineer to organization Chaos Engineering capability

This simple demo will walk you through how you can benefit from the Chaos
Toolkit to start on your journey and get to a team Chaos Engineering
capability.

Chaos Engineering is practice as much as a discipline, it takes trials to get
your own approach of the topic right. Chaos Toolkit aims at providing a protocol
as well as a platform to put you on the right track.

## Overview

This demo is purposefully simple from an application perspective so that we
can focus on the Chaos Engineering side.

### Application Design

The application is a simple HTTP endpoint that, when called, returns a JSON
payload:

```json
{
  "svc": "service1",
  "version": "1",
  "timestamp": 1558335507.2725668,
  "count": 2752
}
```

The `count` value is an integer that is incremented by the service every time
you call the endpoint.

Initially, the service, called `service1`, generates the value on its own.
But in a second version, we decide to have another service, called `service2`,
that generates the value while `service1` then calls it internally over HTTP
to fetch that value to pass it back to the user.

```json
{
  "svc": "service1",
  "version": "2",
  "timestamp": 1558335867.205336,
  "count": 2802
}
```

```json
{
  "svc": "service2",
  "version": "1",
  "last": 2802
}
```

Both services expose as well:

* a `/health` endpoint for probing the health of the service
* a `/metrics` endpoint for collecting metrics (from Prometheus)


### Operational Design

We use Kubernetes to manage our application's lifecycle. Both have their
own deployment strategies.

When a new version is rolled out, Kubernetes waits up to a certain amount of
time before accepting that the new version is allowed to take trafic in.

This allows us to reduce the impact on our users should a new version break
on deployment.

This demo is going to focus on scenarios around rollouts essentially.

## Setup your Environment

This demo is not really difficult to deploy but hasn't been tested against all
environments yet. So please report any issue you might encounter.

### Create a Kubernetes cluster

You obviously need to start with running a Kubernetes cluster. It does not
have to be very powerful as we will run a minimal set of pods in there. Our
applications have resource limits which are fairly low.

The demo has been tested on Ubuntu 19.04 against a local Kubernetes cluster
deployed with [microk8s][].

[microk8s]: https://microk8s.io/

As this only works on Linux, you might want to try [minikube][], [k3s][] or
a cloud offering.

[minikube]: https://kubernetes.io/docs/setup/minikube/
[k3s]: https://k3s.io/

Make sure `~/.kube/config` is properly configured so that you can query the
cluster from your local machine.

### Install system dependencies

This demo is concerned about showing you how Chaos Toolkit can integrate
smoothly with your existing tooling (observability, CI/CD...). For the purpose
of the demo, please install Jaeger and Prometheus in your cluster:

```
$ kubectl apply -f https://raw.githubusercontent.com/jaegertracing/jaeger-kubernetes/master/all-in-one/jaeger-all-in-one-template.yml
```

```
git clone https://github.com/coreos/kube-prometheus.git
cd kube-prometheus
kubectl apply -f manifests/
```

### Configure your shell environment

Once deployed and running, please make sure the following variables are
populated anywhere you will be running Chaos Toolkit:

```
export JAEGER_HOST=$(kubectl get pods -o=jsonpath='{.items[0].status.podIP}' -l app=jaeger)
export PROMETHEUS_URL="http://$(kubectl -n monitoring get svc prometheus-k8s -o=jsonpath='{.spec.clusterIP}'):9090"
```

In addition, the demo may send logs to a central logging service, such as
[Humio](https://www.humio.com/). Please set these two variables:

```
export HUMIO_INGEST_TOKEN=
export HUMIO_DATASPACE=
```

If you do not have an account with Humio, or do not wish to create one, simply
leave these variables empty.

Finally, we pretend to have a domain called `counter.dev` pointing at
`service1`. If you run everything locally, please add the following entry to
your `/etc/hosts` file.

```
127.0.0.1 counter.dev
```

Then export the following variable:

```
export COUNTER_URL=http://counter.dev/
```


### Deploy the application resources

The last thing is to deploy some resources we'll need for the demo:

```
$ kubectl apply --record \
    -f manifests/ingress/ \
    -f manifests/prometheus/
```

### Install Chaos Toolkit dependencies

You will need to install the Chaos Toolkit and then its dependencies for this
demo:

```
$ pip3 install -U experiments/requirements.txt
```

## Get Started

### A single service...

First, we'll be deploying v1 of our `service1`. That version generates the
counter value on its own.

```
$ kubectl apply --record \
    -f manifests/deployment/service1.yaml \
    -f manifests/service/service1.yaml
```

Once deployed, check you can call the service:

```
$ curl --silent $COUNTER_URL
{"svc":"service1","version":"1","timestamp":1558339816.4258926,"count":1}
```

You should see traces for this service in Jaeger's UI.

![Jaeger Service1 v1](/from-local-to-automated-chaostoolkit/assets/screenshots/service1-v1-jaeger.png)

### A microservice architecture !

We are now moving to a microservice architecture whereby a second service is
deployed to actually manage the counter. The first service simply calls that
new service to fetch the value and pass it along to users.


```
$ kubectl apply --record \
    -f manifests/deployment/service2.yaml \
    -f manifests/service/service2.yaml
```

```
export SVC2="http://$(kubectl get svc service2 -o=jsonpath='{.spec.clusterIP}'):8000"
```

```
$ curl --silent $SVC2
{"svc":"service2","version":"1","count":1}
```

However, for now our first service is not aware of the new service. We update
`service1`'s code and deploy v2.

```
$ kubectl set image deployment service1 service1=lawouach/service1:v2
```


You should see traces for both services in Jaeger's UI.

![Jaeger Service1 v2](/from-local-to-automated-chaostoolkit/assets/screenshots/service1-v2-jaeger.png)

At this stage, we are now ready to try various Chaos Engineering scenarios 
which will surface potential issues when rolling out new versions of `service2`
and how this impacts `service1`, potentially thus our users.

## Run Chaos Engineering experiments with the Chaos Toolkit

### Can we roll the same version of a service without problem?

The hypothesis here is the null hypothesis. Do we impact anyone when we rollout
the same version of a service?

The experiment is `experiments/rollout-v1-service2.json`, run it as follows:

```
$ cd experiments
$ chaos run --journal-path=v1.json rollout-v1-service2.json
```

This experiment shows that we do not hurt our users, nor `service1` when
we rollout the same version which is already running of `service2`.

### Can we roll a new version of a service without problem?

Do we impact anyone when we rollout a newer version of a service?

The experiment is `experiments/rollout-v2-service2.json`, run it as follows:

```
$ cd experiments
$ chaos run --journal-path=v2.json rollout-v2-service2.json
```

This experiment shows that we do not hurt our users, nor `service1` when
we rollout a new version of `service2`.

### Can we roll a new version of an unhealthy service without problem?

Do we impact anyone when we rollout a newer version of a service that reports
being unhealthy to Kubernetes?

The experiment is `experiments/rollout-v3-service2.json`, run it as follows:

```
$ cd experiments
$ chaos run --journal-path=v3.json rollout-v3-service2.json
```

This experiment shows that we do not hurt our users, nor `service1` when
we rollout a new version of `service2` if that new version reports being
unhealthy. Kubernetes won't let it be deployed.

### Can we roll a new version of a slow service without problem?

Do we impact anyone when we rollout a newer version of a service that reports
being healthy to Kubernetes, even if it is too slow and adds latency?

The experiment is `experiments/rollout-v4-service2.json`, run it as follows:

```
$ cd experiments
$ chaos run --journal-path=v4.json rollout-v4-service2.json
```

This experiment shows that *we do hurt our users* and `service1` when
we rollout a new version of `service2` if that new version reports being
healthy but is actually broken because it is now too slow and the latency is
not tolerated by `service1` which expects a faster response.

![Jaeger Service1 v4](/from-local-to-automated-chaostoolkit/assets/screenshots/run-v4-jaeger.png)

![Humio v4](/from-local-to-automated-chaostoolkit/assets/screenshots/run-v4-humio.png)

## Generate a PDF report

You can now generate a [report][] from all those runs:

[report]: https://github.com/chaostoolkit/chaostoolkit-reporting

```
$ cd experiments
$ docker run \
    --user `id -u` \
    -v `pwd`:/tmp/result \
    -it \
    chaostoolkit/reporting -- report --export-format=pdf v?.json report.pdf
```

## Automate running the experiments with a Kubernetes Job

Finally, you may decide to run the Chaos Toolkit automatically as a
[Kubernetes Job](kubejob), or from your CI/CD for instance.

[kubejob]: https://github.com/chaostoolkit-incubator/kubernetes-job

```
$ kubectl apply -f manifests/job/toolkit-as-kubejob.yaml
$ kubectl apply -f manifests/job/chaostoolkit-rollout-v2-service2.yaml
$ kubectl -n chaostoolkit logs -c chaostoolkit -l app=chaostoolkit
```
