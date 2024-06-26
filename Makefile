SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.DEFAULT_GOAL := help
.PHONY: help
help: ## Display this help section
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z\$$/]+.*:.*?##\s/ {printf "\033[36m%-38s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install
install: ## Install depenedencies
	uv pip install -r requirements/dev.txt

.PHONY: up
up: ## Start docker containers
	docker compose up

.PHONY: build
build: ## Build docker images
	docker compose build

.PHONY: enter
enter: ## Enter django container
	docker compose exec django sh

.PHONY: lint
lint: ## Run pre-commit checks
	pre-commit run --all-files
