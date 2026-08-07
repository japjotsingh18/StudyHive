.DEFAULT_GOAL := help
SHELL := /bin/sh

.PHONY: help bootstrap dev down lint format typecheck test build check db-upgrade

help: ## Show repository commands.
	@awk 'BEGIN {FS = ":.*## "; printf "StudyHive commands:\n"} /^[a-zA-Z0-9_-]+:.*## / {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

bootstrap: ## Install pinned dependencies, create local config, and configure hooks.
	@./scripts/bootstrap.sh

dev: ## Start the complete local development stack.
	@./scripts/dev.sh

down: ## Stop the local development stack.
	@docker compose -f docker/compose.yaml down

lint: ## Run Python and TypeScript lint checks.
	@pnpm lint
	@./scripts/uv.sh run ruff check .
	@./scripts/uv.sh run black --check .

format: ## Format Python, TypeScript, styles, and documentation.
	@pnpm format
	@./scripts/uv.sh run ruff check --fix .
	@./scripts/uv.sh run black .

typecheck: ## Run strict Python and TypeScript type checks.
	@pnpm typecheck
	@./scripts/uv.sh run mypy

test: ## Run web, package, and API tests.
	@pnpm test
	@./scripts/uv.sh run pytest

build: ## Verify production web and API package builds.
	@pnpm build
	@./scripts/uv.sh build --package studyhive-api

check: ## Run the same required checks as CI.
	@$(MAKE) lint
	@pnpm format:check
	@$(MAKE) typecheck
	@$(MAKE) test
	@$(MAKE) build

db-upgrade: ## Apply all local Alembic migrations.
	@./scripts/uv.sh run --package studyhive-api alembic --config apps/api/alembic.ini upgrade head
