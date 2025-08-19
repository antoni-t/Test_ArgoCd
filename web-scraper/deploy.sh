#!/bin/bash

eval $(minikube docker-env)

docker build -t web-scraper .
docker build -t stromapp-frontend ./frontend

helm dependency update ./helm/web-scraper

if helm list | grep -q "web-scraper"; then
    echo "Upgrading existing web-scraper..."
    helm upgrade web-scraper ./helm/web-scraper
else
    echo "Installing web-scraper..."
    helm install web-scraper ./helm/web-scraper
fi

if helm list | grep -q "stromapp-frontend"; then
    echo "Upgrading existing stromapp-frontend..."
    helm upgrade stromapp-frontend ./helm/stromapp-frontend
else
    echo "Installing stromapp-frontend..."
    helm install stromapp-frontend ./helm/stromapp-frontend
fi

echo "Applying ArgoCD Applications..."
kubectl apply -f argo-web-scraper.yaml -n argocd
kubectl apply -f argo-frontend.yaml -n argocd