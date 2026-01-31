.PHONY: help build up down restart logs shell clean clean-data clean-reports clean-all info

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build the Docker image
	docker-compose build

up: ## Run the application
	docker-compose run --rm agent-availability

down: ## Stop and remove containers (volumes persist locally)
	docker-compose down

restart: down up ## Restart the application

logs: ## View application logs
	docker-compose logs -f

shell: ## Open a shell in the container
	docker-compose run --rm agent-availability /bin/bash

clean: ## Remove all generated files (local only)
	@echo "Cleaning up generated files..."
	@rm -rf data/*
	@rm -rf reports/*
	@rm -rf *.xlsx *.docx
	@echo "Cleanup complete!"

clean-data: ## Remove persistent database only
	@echo "Removing persistent database..."
	@rm -rf data/agent_baseline.db
	@echo "Database removed!"

clean-reports: ## Remove reports only
	@echo "Removing reports..."
	@rm -rf reports/*
	@echo "Reports removed!"

clean-all: clean ## Clean everything including Docker images
	@echo "Cleaning everything including Docker images..."
	docker-compose down
	docker-compose rm -f
	docker rmi agent-availability-app 2>/dev/null || true
	@echo "Full cleanup complete!"

info: ## Show database and reports info
	@echo "=== Persistent Data Info ==="
	@echo "Database: data/agent_baseline.db"
	@if [ -f "data/agent_baseline.db" ]; then \
		echo "Size: $$(du -sh data/agent_baseline.db | cut -f1)"; \
		echo "Modified: $$(stat -f '%Sm' -t '%Y-%m-%d %H:%M:%S' data/agent_baseline.db 2>/dev/null || stat -c '%y' data/agent_baseline.db)"; \
	else \
		echo "Status: No database found"; \
	fi
	@echo ""
	@echo "Reports directory: reports/"
	@echo "Report count: $$(ls reports/* 2>/dev/null | wc -l | tr -d ' ')"
