# EduProof Makefile
# Common commands for development

.PHONY: help install dev test build deploy clean

help:
	@echo "EduProof Development Commands"
	@echo ""
	@echo "  make install    - Install all dependencies"
	@echo "  make dev        - Start development servers"
	@echo "  make test       - Run all tests"
	@echo "  make build      - Build for production"
	@echo "  make deploy     - Deploy to production"
	@echo "  make clean      - Clean build artifacts"

# Install dependencies
install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install
	cd mobile && npm install
	cd ai && pip install -r requirements.txt

# Development servers (use with docker-compose or manually)
dev:
	docker-compose -f cloud/docker/docker-compose.yml up

# Run tests
test:
	cd backend && pytest
	cd frontend && npm test
	cd ai && pytest

# Build for production
build:
	cd frontend && npm run build
	docker build -t eduproof-backend ./backend
	docker build -t eduproof-ai ./ai

# Clean
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name node_modules -exec rm -rf {} +
	find . -type d -name dist -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
