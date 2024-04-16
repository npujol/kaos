# Deploying with minikube

## Requirements:
- [minikube](https://minikube.sigs.k8s.io/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

## Build docker images
- Build the docker image for the django app
```
docker build -t django-app:latest .
```
- Build the docker image for the django proxy
```
docker build -f proxy/Dockerfile -t django-proxy:latest ./proxy/
```

## Deploy
- Deploy the django app and db
```
kubectl apply -k deploy/minikube/
```

# Check the deployment
- Get all the pods
```
kubectl get pods
```
- Check logs from a specific pod
```
kubectl logs <pod-name>
```

# Check minikube dashboard
```
minikube dashboard
```

# Check the web site
```
kubectl apply -k deploy/minikube/
```
