# Deploying with minikube

## Requirements

- [minikube](https://minikube.sigs.k8s.io/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

## Build docker images

- Build the docker image for the django app

```bash
docker build -t django-app:latest .
```

- Build the docker image for the django proxy

```bash
docker build -f proxy/Dockerfile -t django-proxy:latest ./proxy/
```

## Deploy

- Deploy the django app and db

```bash
kubectl apply -k deploy/minikube/
```

### Check the deployment

- Get all the pods

```bash
kubectl get pods
```

- Check logs from a specific pod

```bash
kubectl logs <pod-name>
```

### Check minikube dashboard

```bash
minikube dashboard
```

### Check the web site

```bash
kubectl apply -k deploy/minikube/
```
