#!/bin/bash

# Ensure kubectl is installed and configured
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed or not in PATH."
    exit 1
fi

# Check if jq is installed for JSON parsing
if ! command -v jq &> /dev/null; then
    echo "jq is not installed. Please install it to use this script."
    exit 1
fi

# Fetch all LoadBalancer services and display the required details
echo "Fetching LoadBalancer services..."
echo -e "NAMESPACE\tNAME\tEXTERNAL-IP:PORT\tSTATUS"

kubectl get svc --all-namespaces -o json | jq -r '
    .items[] | 
    select(.spec.type == "LoadBalancer") | 
    [
        .metadata.namespace,
        .metadata.name,
        (.status.loadBalancer.ingress[0].ip // .status.loadBalancer.ingress[0].hostname // "Pending"),
        (.spec.ports[0].port | tostring + ":" + (.spec.ports[0].targetPort | tostring)),
        (.status.conditions // "Unknown")
    ] | @tsv
' | while IFS=$'\t' read -r namespace name external_ip_port status; do
    echo -e "$namespace\t$name\t$external_ip_port\t$status"
done
