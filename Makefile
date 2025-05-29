.PHONY: help install test test-cov lint format format-check clean docker-build docker-up docker-down docker-test dev check pylint docker-check

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install --upgrade pip
	pip install -r requirements.txt

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage
	pytest --cov=app --cov-report=html --cov-report=term

lint:  ## Run linting with flake8
	flake8 app tests

pylint:  ## Run pylint for advanced code analysis
	pylint app tests

format:  ## Format code with black and isort
	black app tests
	isort app tests

format-check:  ## Check code formatting
	black --check app tests
	isort --check-only app tests

clean:  ## Clean cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage

docker-build:  ## Build Docker image
	docker-compose build

docker-up:  ## Start Docker services
	docker-compose up -d

docker-down:  ## Stop Docker services
	docker-compose down

docker-test:  ## Run tests in Docker
	docker-compose exec web pytest

dev:  ## Start development server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

check:  ## Run all quality checks (lint + format + test)
	flake8 app tests
	pylint app tests
	black --check app tests
	isort --check-only app tests
	pytest

docker-check:  ## Run all quality checks in Docker
	docker-compose exec web flake8 app tests
	docker-compose exec web pylint app tests
	docker-compose exec web black --check app tests
	docker-compose exec web isort --check-only app tests
	docker-compose exec web pytest 