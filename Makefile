SHELL := bash
IMG_TAG ?= latest
DOCKER_USERNAME ?= ""
DOCKER_PASSWORD ?= ""
IMG_NAME := airflow-git-sync
ENV ?= dev

.PHONY: docker-build
docker-build:
	@echo "✅ Building the container image for airflow-git-sync ===============>"
	@docker build . -t $(DOCKER_USERNAME)/$(IMG_NAME):$(IMG_TAG)

.PHONY: docker-login
docker-login:
	@echo "✅ Authenticating to Docker Registry ===============>"
	@echo $(DOCKER_PASSWORD) |  docker login -u $(DOCKER_USERNAME) --password-stdin

.PHONY: docker-push
docker-push:
	@echo "✅ Pushing to the Docker Registry ===============>"
	@docker push $(DOCKER_USERNAME)/$(IMG_NAME):$(IMG_TAG)

.PHONY: deploy-argocd-crds
deploy-argocd-crds:
	@echo "✅ Deploying ArgoCD CRDs for $(ENV) ===============>"
	@pushd "argocd"; kubectl apply -f crd; popd

.PHONY: deploy-argocd-operator
deploy-argocd-operator:
	@echo "✅ Deploying ArgoCD Operator for $(ENV) ===============>"
	@pushd "argocd"; kubectl apply -f operator; popd

.PHONY: deploy-argocd-app
deploy-argocd-app:
	@echo "✅ Deploying ArgoCD Application for $(ENV) ===============>"
	@pushd "argocd/applications"; kubectl apply -f airflow-$(ENV); popd

.PHONY: deploy-airflow
deploy-airflow:
	@echo "✅ Deploying Airflow for $(ENV) ===============>"
	@pushd "airflow/overlays"; kustomize build $(ENV) | kubectl apply -f -; popd

.PHONY: cleanup
cleanup:
	@echo "✅ Deleting Airflow for $(ENV) ===============>"
	@pushd "airflow/overlays"; kustomize build $(ENV) | kubectl delete -f -; popd
	@sleep 1
	@echo "✅ Deleting ArgoCD for $(ENV) ===============>"
	@pushd "argocd"; kubectl delete -f crd; popd
	@pushd "argocd"; kubectl delete -f operator; popd
	@pushd "argocd/applications"; kubectl delete -f airflow-$(ENV); popd