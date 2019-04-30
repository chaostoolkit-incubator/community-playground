# SuperPower Microservice and Chaos Engineering Demo

Welcome to this simple demo of an application based on a microservice
architecture to explore Chaos Engineering experiments using the
[chaostoolkit][].

[chaostoolkit]: https://chaostoolkit.org/

## Overview

The architecture of our application is as follows:

![Architecture](https://github.com/chaosiq/superpower-demo/raw/master/data/arch.png "Architecture")

As you can see, it's really simple. Users talk to the superpower service which
talks to the powersource service.

The superpower service asks the powersource for data before returning it to the
user in HTML or JSON format.

The presentation for this demo can be found [here](https://www.slideshare.net/Lawouach/chaos-engineering-and-systems-reliability)
and the talk [here](https://skillsmatter.com/skillscasts/12908-distributed-system-reliability-through-chaos-engineering).

### Application Promises

Our application makes two promises to users:

* each time you come back to it, you will get the same superpower (you can turn from hero to vilain suddenly)
* the latency to receive your superpower should be under a second

Our experiments will keep those promises in mind to understand how failures
or changes impact our users.

## Chaos Engineering Experiments

We are going to explore various scenarios that will help us learn how such a
simple architecture copes with degraded conditions.

## Collect data

The data used by this demo is under copyright by [Marvel][]. For this reason,
you need to collect the data yourself prior to running this demo.

To achieve that, you must first create an [API key][apikey] and store it into
the following variables:

```
$ export MARVEL_API_PUBLIC_KEY=...
$ export MARVEL_API_PRIVATE_KEY=...
```

[Marvel]: https://developer.marvel.com/
[apikey]: https://developer.marvel.com/documentation/getting_started

Next, you must have [Python 3.5+][py3] installed:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -U -r scripts/requirements.txt
$ python scripts/collect-characters.py
$ python scripts/collect-images.py
```

Be aware, this will take a few minutes to complete so go grab a coffee :)

## Deploying the application

You can deploy and run the application using one of the followings:

* [Local](https://github.com/chaosiq/superpower-demo/blob/master/docs/local.md): Run natively on your local machine
* [Kubernetes (minikube)](https://github.com/chaosiq/superpower-demo/blob/master/docs/minikube.md): Run in Kubernetes in a VM on your local machine
* [Kubernetes (microk8s)](https://github.com/chaosiq/superpower-demo/blob/master/docs/microk8s.md): Run in Kubernetes natively on your local machine (Linux only)


## Access the application

After deploying the application, you should be able to access it at:

```
http://127.0.0.1:30280
```

## Run Chaos Engineering Experiments

Now that you have your application, you can start performing Chaos Engineering
experiments.

### Requirements

Before you run them, please source the following script:

```
$ . scripts/prepare-experiments-env.sh
```

Note that this is indeed source this script, not running it.

You should also install [vegeta][].

[vegeta]: https://github.com/tsenart/vegeta

### Experiment 1: Lose Half of the PowerSource service fleet

What if 50% of your fleet of powersource service instances were going down?
Would this impact the promises you made to your users?

Such a scenario is declared in `experiments/lose-half-of-powersources.json`
and can be executed as such (use the one for your deployment):

```
$ chaos run --journal-path experiments/journal-1.json experiments/kubernetes/lose-half-of-powersources.json
$ chaos run --journal-path experiments/journal-1.json experiments/local/lose-half-of-powersources.json
```

[See it](https://asciinema.org/a/209775) in action.

### Experiment 2: Lose the entire PowerSource service fleet

What if 100% of your fleet of powersource service instances were going down?
Would this impact the promises you made to your users?

Such a scenario is declared in `experiments/lose-all-of-powersources.json`
and can be executed as such (use the one for your deployment):

```
$ chaos run --journal-path experiments/journal-2.json experiments/kubernetes/lose-all-of-powersources.json
$ chaos run --journal-path experiments/journal-2.json experiments/local/lose-all-of-powersources.json
```

[See it](https://asciinema.org/a/209776) in action.

### Experiment 3: Superpower latency should not be impacted by high-load

How does our service perform under heavy load?
Would this impact the promises you made to your users?

Such a scenario is declared in
`experiments/latency-should-remain-sane-under-heavy-load.json` and can be
executed as such (use the one for your deployment):

```
$ chaos run --journal-path experiments/journal-3.json experiments/kubernetes/latency-should-remain-sane-under-heavy-load.json
$ chaos run --journal-path experiments/journal-3.json experiments/local/latency-should-remain-sane-under-heavy-load.json
```

[See it](https://asciinema.org/a/209786) in action.

## Generate Chaos Engineering Reports

You may generate a single report of all your experiments as follows:

```
$ docker run \
    --user `id -u` \
    -v `pwd`/experiments:/tmp/result \
    -it \
    chaostoolkit/reporting:0.11.0 -- report --export-format=pdf journal-*.json report.pdf
```
