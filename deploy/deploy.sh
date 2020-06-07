#! /usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
az account set --subscription development
echo "Logging in to ACR"
az acr login --name delphaidevelopment
docker build -t delphaidevelopment.azurecr.io/metadata-finder $DIR/..
docker push delphaidevelopment.azurecr.io/metadata-finder
kubectx delphai-development
terraform init
terraform apply -auto-approve