# Deploy to Google Cloud Platform Kubernetes

This deployment option requires you to have a Kubernetes Cluster to deploy the services to.

### If you don't have a Kubernetes Cluster/Project already

Create a new project called something like "Yummy Noodle Staging" to keep everything isolated from any other clusters and systems you may be running. Wait for it to initialize.

Create a cluster, 3 nodes is the norm. Wait for it to become available.

```bash
$ export PROJECT_ID="$(gcloud config get-value project -q)"
$ docker build -t gcr.io/${PROJECT_ID}/menu-app:0.1.1 .
$ gcloud auth configure-docker
$ docker push gcr.io/${PROJECT_ID}/menu-app:0.1.1
```
