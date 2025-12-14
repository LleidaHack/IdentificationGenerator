# Docker Quick Start Guide

This guide will help you get the IdentificationGenerator API up and running with Docker.

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (usually comes with Docker Desktop)
- Git (to clone the repository)

## Quick Start

### 1. Setup Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env if needed (optional for basic testing)
# nano .env
```

### 2. Start the Application

**Option A: Using Make (Recommended)**
```bash
# View available commands
make help

# Start in production mode (background)
make up

# Or start in development mode (with hot-reload)
make dev
```

**Option B: Using Docker Compose directly**
```bash
# Production mode
docker-compose up -d

# Development mode
docker-compose -f docker-compose.dev.yml up
```

### 3. Verify It's Running

Open your browser and visit:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

You should see the API documentation and be able to test endpoints.

### 4. View Logs

```bash
# Using Make
make logs

# Using Docker Compose
docker-compose logs -f
```

## Common Tasks

### Access Container Shell

```bash
# Using Make
make shell

# Using Docker Compose
docker exec -it identification-generator-api /bin/bash
```

### Run Tests

```bash
# Using Make
make test

# Using Docker Compose
docker-compose exec api uv run pytest
```

### Stop the Application

```bash
# Using Make
make down

# Using Docker Compose
docker-compose down
```

### Rebuild After Code Changes

```bash
# Using Make
make rebuild

# Using Docker Compose
docker-compose up -d --build
```

## Development Workflow

### Hot-Reload Development

1. Start in development mode:
   ```bash
   make dev
   ```

2. Edit your code - changes will automatically reload

3. View logs in real-time to see the reload happening

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
docker-compose exec api uv run pytest tests/test_specific.py

# Run with verbose output
docker-compose exec api uv run pytest -v
```

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:

1. Edit `docker-compose.yml`
2. Change `"8000:8000"` to `"8080:8000"` (or another available port)
3. Access the API at http://localhost:8080

### Container Won't Start

```bash
# Check logs
make logs

# Common issues:
# 1. Missing dependencies - rebuild the image
make rebuild

# 2. Permission issues - check file permissions
ls -la

# 3. Port conflicts - change the port in docker-compose.yml
```

### Generated Files Not Appearing

The generated ID cards are saved to `./generated_cards/` on your host machine.

If files aren't appearing:
1. Check if the directory exists: `ls -la generated_cards/`
2. Check container logs for errors: `make logs`
3. Verify volume mount in docker-compose.yml

### Firebase Connection Issues

If you see Firebase-related errors:

1. Ensure you have the Firebase credentials file
2. Place it at `resources/2019_firebase_cert.json`
3. Uncomment the volume mount in `docker-compose.yml`:
   ```yaml
   - ./resources/2019_firebase_cert.json:/app/resources/2019_firebase_cert.json:ro
   ```
4. Restart: `make restart`

## File Structure

```
IdentificationGenerator/
├── docker-compose.yml          # Production configuration
├── docker-compose.dev.yml      # Development configuration
├── Dockerfile                  # Production image
├── Dockerfile.dev             # Development image
├── .dockerignore              # Files to exclude from build
├── .env.example               # Environment template
├── .env                       # Your environment (git-ignored)
├── Makefile                   # Convenient commands
├── generated_cards/           # Output directory (created automatically)
└── resources/                 # Templates, fonts, etc.
```

## Next Steps

- Read the main [README.md](README.md) for API documentation
- Check out the interactive API docs at http://localhost:8000/docs
- Explore the different endpoints for contestants, mentors, etc.
- Set up your Firebase credentials for full functionality

## Getting Help

- Check the logs: `make logs`
- View container status: `docker-compose ps`
- Access the shell for debugging: `make shell`
- Review the main README.md for more details

## Clean Up

To completely remove all containers, images, and generated files:

```bash
make clean
```

**Warning:** This will delete all generated ID cards and Docker resources!
