snap install microk8s --classic --channel=1.12/stable
sleep 10

microk8s.enable dns dashboard

cd superpower
microk8s.docker build -t mucon/superpower:v0.1.0 .
cd ../superpower-static
microk8s.docker build -t mucon/superpower-static:v0.1.0 .
cd ../powersource
microk8s.docker build -t mucon/powersource:v0.1.0 .
cd ..

microk8s.kubectl apply -f manifests/namespace/
microk8s.kubectl apply -f manifests/rbac/ -f manifests/sa/ -f manifests/configmap/
microk8s.kubectl apply -f manifests/service/ -f manifests/ingress/
microk8s.kubectl apply -f manifests/deployment/

microk8s.kubectl cluster-info

# add entries to the kubectl configuration file so we can directly use
# the kubectl CLI
CLUSTER_NAME=$(microk8s.kubectl config view -o=jsonpath='{.clusters[0].name}')
CLUSTER_URL=$(microk8s.kubectl config view -o=jsonpath='{.clusters[0].cluster.server}')
kubectl config set-cluster ${CLUSTER_NAME} --server=${CLUSTER_URL}

CREDS_NAME=$(microk8s.kubectl config view -o=jsonpath='{.users[0].name}')
CREDS_USERNAME=$(microk8s.kubectl config view -o=jsonpath='{.users[0].user.username}')
kubectl config set-credentials ${CREDS_NAME} --username=${CREDS_USERNAME}

CONTEXT_NAME=$(microk8s.kubectl config view -o=jsonpath='{.contexts[0].name}')
CONTEXT_USER=$(microk8s.kubectl config view -o=jsonpath='{.contexts[0].context.user}')
kubectl config set-context ${CONTEXT_NAME} --cluster=${CLUSTER_NAME} --user=${CONTEXT_USER}

kubectl config use-context ${CONTEXT_NAME}

kubectl get --all-namespaces all
