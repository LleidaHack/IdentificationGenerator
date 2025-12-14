.PHONY: help build up down logs shell test clean dev prod restart

# Default target
help:
	@echo "Available commands:"
	@echo "  make build       - Build Docker images"
	@echo "  make up          - Start containers in production mode"
	@echo "  make down        - Stop and remove containers"
	@echo "  make logs        - View container logs"
	@echo "  make shell       - Access container shell"
	@echo "  make test        - Run tests in container"
	@echo "  make clean       - Remove containers, images, and volumes"
	@echo "  make dev         - Start in development mode with hot-reload"
	@echo "  make prod        - Start in production mode"
	@echo "  make restart     - Restart containers"

# Build Docker images
build:
	docker-compose build

# Start containers (production)
up:
	docker-compose up -d

# Start containers (production, foreground)
prod:
	docker-compose up

# Start containers (development with hot-reload)
dev:
	docker-compose -f docker-compose.dev.yml up

# Stop containers
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Access container shell
shell:
	docker exec -it identification-generator-api /bin/bash

# Run tests
test:
	docker-compose exec api uv run pytest

# Restart containers
restart:
	docker-compose restart

# Clean everything (containers, images, volumes)
clean:
	docker-compose down -v --rmi all
	rm -rf generated_cards/*

# Rebuild and restart
rebuild: down build up

# Check container status
status:
	docker-compose ps

# View API documentation
docs:
	@echo "API Documentation available at:"
	@echo "  - Swagger UI: http://localhost:8000/docs"
	@echo "  - ReDoc: http://localhost:8000/redoc"
