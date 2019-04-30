REMOTE_IP=$(kubectl -n mucon get svc traefik-ingress-service -o jsonpath='{.spec.clusterIP}')

eval "$(ssh-agent -s)"
ssh -i $(minikube ssh-key) docker@$(minikube ip) -L 0.0.0.0:30280:${REMOTE_IP}:80
