minikube start --cpus=4 --memory=4096
minikube ip

eval $(minikube docker-env)
cd superpower
docker build -t mucon/superpower:v0.1.0 .
cd ../superpower-static
docker build -t mucon/superpower-static:v0.1.0 .
cd ../powersource
docker build -t mucon/powersource:v0.1.0 .
cd ..

kubectl apply -f manifests/namespace
kubectl apply -f manifests/sa
kubectl apply -f manifests/rbac
kubectl apply -f manifests/configmap
kubectl apply -f manifests/deployment
kubectl apply -f manifests/service
kubectl apply -f manifests/ingress

kubectl get --all-namespaces all

minikube service list