# Deploying with minikube

## Requirements

- [k3d](https://k3d.io/)

## Build docker images

- Build the docker image for the django app

```bash
docker build -t django-app:latest .
```

- Build the docker image for the django proxy

```bash
docker build -f proxy/Dockerfile -t django-proxy:latest ./proxy/
```

- Import the images using K3D

```bash
k3d image import django-app:latest
k3d image import django-proxy:latest
```

- Forward app port

```bash
kubectl -n default port-forward svc/django 8000:8000
```

## Deploy

- Deploy the django app and db

```bash
kubectl apply -k deploy/k3d/solution
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

- SSH access

```bash
kubectl exec -it <pod-name> -- /bin/bash
```
