# Starlink TAM Analysis Platform - Makefile
# Professional development workflow with Docker
.PHONY: help build up down shell test lint format clean logs demo jupyter

# Default target
.DEFAULT_GOAL := help

# Variables
DOCKER_COMPOSE := docker-compose -f docker/docker-compose.yml
PROJECT_NAME := starlink-tam
DEV_CONTAINER := starlink-tam-dev
JUPYTER_CONTAINER := starlink-tam-jupyter

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

## Display this help message
help:
	@echo "$(GREEN)🚀 Starlink TAM Analysis Platform$(NC)"
	@echo "$(YELLOW)================================$(NC)"
	@echo "Available commands:"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(YELLOW)Quick Start:$(NC)"
	@echo "  make build    # Build Docker images"
	@echo "  make shell    # Start development environment"
	@echo "  make demo     # Run demo analysis"
	@echo ""

## Build all Docker images
build:
	@echo "$(GREEN)Building Docker images...$(NC)"
	$(DOCKER_COMPOSE) build --parallel
	@echo "$(GREEN)✅ Build complete!$(NC)"

## Start all services in the background
up:
	@echo "$(GREEN)Starting services...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)✅ Services started!$(NC)"
	@echo "Access Jupyter Lab: http://localhost:8888 (token: starlink-tam-token)"
	@echo "Access Grafana: http://localhost:3000 (admin/starlink_admin)"

## Stop all services
down:
	@echo "$(YELLOW)Stopping services...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✅ Services stopped!$(NC)"

## Start development shell (interactive)
shell:
	@echo "$(GREEN)Starting development shell...$(NC)"
	$(DOCKER_COMPOSE) up -d starlink-dev
	$(DOCKER_COMPOSE) exec starlink-dev bash

## Run the demo analysis
demo:
	@echo "$(GREEN)Running Starlink TAM demo...$(NC)"
	$(DOCKER_COMPOSE) up -d starlink-dev
	$(DOCKER_COMPOSE) exec starlink-dev python demo.py

## Run basic TAM analysis
analyze:
	@echo "$(GREEN)Running TAM analysis...$(NC)"
	$(DOCKER_COMPOSE) up -d starlink-dev
	$(DOCKER_COMPOSE) exec starlink-dev starlink-tam analyze --output /app/output/analysis.json

## Run Monte Carlo simulation
monte-carlo:
	@echo "$(GREEN)Running Monte Carlo simulation...$(NC)"
	$(DOCKER_COMPOSE) up -d starlink-dev
	$(DOCKER_COMPOSE) exec starlink-dev starlink-tam monte-carlo --simulations 1000 --output /app/output/simulation.csv

## Show top markets analysis
top-markets:
	@echo "$(GREEN)Analyzing top markets...$(NC)"
	$(DOCKER_COMPOSE) up -d starlink-dev
	$(DOCKER_COMPOSE) exec starlink-dev starlink-tam top-markets --metric tam --top-n 10

## Run full test suite
test:
	@echo "$(GREEN)Running tests...$(NC)"
	$(DOCKER_COMPOSE) up -d starlink-dev
	$(DOCKER_COMPOSE) exec starlink-dev pytest tests/ -v --cov=starlink_tam --cov-report=term-missing

## Run linting checks
lint:
	@echo "$(GREEN)Running linting checks...$(NC)"
	$(DOCKER_COMPOSE) up -d starlink-dev
	$(DOCKER_COMPOSE) exec starlink-dev flake8 starlink_tam/
	$(DOCKER_COMPOSE) exec starlink-dev mypy starlink_tam/
	@echo "$(GREEN)✅ Linting complete!$(NC)"

## Format code with black and isort
format:
	@echo "$(GREEN)Formatting code...$(NC)"
	$(DOCKER_COMPOSE) up -d starlink-dev
	$(DOCKER_COMPOSE) exec starlink-dev black starlink_tam/ tests/
	$(DOCKER_COMPOSE) exec starlink-dev isort starlink_tam/ tests/
	@echo "$(GREEN)✅ Code formatted!$(NC)"

## Start Jupyter Lab
jupyter:
	@echo "$(GREEN)Starting Jupyter Lab...$(NC)"
	$(DOCKER_COMPOSE) up -d starlink-jupyter
	@echo "$(GREEN)✅ Jupyter Lab started!$(NC)"
	@echo "Access at: http://localhost:8888 (token: starlink-tam-token)"

## View logs from all services
logs:
	@echo "$(GREEN)Showing logs...$(NC)"
	$(DOCKER_COMPOSE) logs -f

## View logs from development container only
logs-dev:
	@echo "$(GREEN)Showing development logs...$(NC)"
	$(DOCKER_COMPOSE) logs -f starlink-dev

## Clean up containers, volumes, and images
clean:
	@echo "$(YELLOW)Cleaning up Docker resources...$(NC)"
	$(DOCKER_COMPOSE) down -v --remove-orphans
	docker system prune -f
	@echo "$(GREEN)✅ Cleanup complete!$(NC)"

## Hard reset - remove everything including volumes
reset:
	@echo "$(RED)⚠️  Hard reset - removing all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \\
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \\
		$(DOCKER_COMPOSE) down -v --remove-orphans; \\
		docker volume prune -f; \\
		docker image rm -f $$(docker images "$(PROJECT_NAME)*" -q) 2>/dev/null || true; \\
		echo "$(GREEN)✅ Hard reset complete!$(NC)"; \\
	else \\
		echo "$(YELLOW)Reset cancelled.$(NC)"; \\
	fi

## Install pre-commit hooks
install-hooks:
	@echo "$(GREEN)Installing pre-commit hooks...$(NC)"
	$(DOCKER_COMPOSE) up -d starlink-dev
	$(DOCKER_COMPOSE) exec starlink-dev pre-commit install
	@echo "$(GREEN)✅ Hooks installed!$(NC)"

## Run security scan with bandit
security:
	@echo "$(GREEN)Running security scan...$(NC)"
	$(DOCKER_COMPOSE) up -d starlink-dev
	$(DOCKER_COMPOSE) exec starlink-dev bandit -r starlink_tam/ -f json -o /app/output/security-report.json
	@echo "$(GREEN)✅ Security scan complete! Check output/security-report.json$(NC)"

## Generate documentation
docs:
	@echo "$(GREEN)Generating documentation...$(NC)"
	$(DOCKER_COMPOSE) up -d starlink-dev
	$(DOCKER_COMPOSE) exec starlink-dev python -m pydoc -w starlink_tam
	@echo "$(GREEN)✅ Documentation generated!$(NC)"

## Show container status
status:
	@echo "$(GREEN)Container Status:$(NC)"
	$(DOCKER_COMPOSE) ps
	@echo ""
	@echo "$(GREEN)Volume Usage:$(NC)"
	@docker volume ls | grep starlink

## Quick development setup
dev-setup: build
	@echo "$(GREEN)✅ Development environment ready!$(NC)"
	@echo "Run 'make shell' to start coding"

## Show system resource usage
resources:
	@echo "$(GREEN)System Resources:$(NC)"
	@docker stats --no-stream

## Interactive Python shell in container
python:
	@echo "$(GREEN)Starting Python shell...$(NC)"
	$(DOCKER_COMPOSE) up -d starlink-dev
	$(DOCKER_COMPOSE) exec starlink-dev ipython

## Run specific country analysis
country:
	@read -p "Enter country codes (comma-separated, e.g., US,CA,UK): " countries; \\
	echo "$(GREEN)Analyzing countries: $$countries$(NC)"; \\
	$(DOCKER_COMPOSE) up -d starlink-dev; \\
	$(DOCKER_COMPOSE) exec starlink-dev starlink-tam analyze --countries $$countries --output /app/output/country-analysis.json
