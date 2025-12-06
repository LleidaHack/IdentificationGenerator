# IdentificationGenerator

A FastAPI-based service for generating identification cards for hackathon events. This application creates personalized ID cards with QR codes for contestants, mentors, organizers, volunteers, companies, and guests.

## Features

- 🎫 Generate ID cards for multiple user types
- 🔲 QR code generation for each participant
- 📄 PDF export functionality
- 🔥 Firebase integration for data storage
- 🚀 FastAPI REST API
- 🐳 Docker support for easy deployment

## Prerequisites

- Docker and Docker Compose (for containerized deployment)
- OR Python 3.12+ and uv (for local development)

## Quick Start with Docker

### Production Deployment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd IdentificationGenerator
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the API**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Development Mode

For development with hot-reload:

```bash
docker-compose -f docker-compose.dev.yml up
```

This will mount your source code into the container, enabling live reload on code changes.

## Docker Commands

### Build the image
```bash
docker build -t identification-generator .
```

### Run a container
```bash
docker run -d -p 8000:8000 --name id-gen identification-generator
```

### View logs
```bash
docker-compose logs -f
```

### Stop containers
```bash
docker-compose down
```

### Rebuild after changes
```bash
docker-compose up -d --build
```

### Access container shell
```bash
docker exec -it identification-generator-api /bin/bash
```

## Local Development (without Docker)

### Setup

1. **Install uv** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Run the application**
   ```bash
   uv run uvicorn main:app --reload
   ```

## Configuration

### Firebase Setup

1. Obtain your Firebase service account credentials
2. Save the JSON file as `resources/2019_firebase_cert.json`
3. Update the path in `Config.py` if needed

### Environment Variables

Create a `.env` file based on `.env.example`:

- `EDITION`: The year/edition of the event (default: 2025)
- `TEST`: Set to `True` for test mode, `False` for production

## API Endpoints

- `GET /` - Health check
- `GET /docs` - Interactive API documentation
- `/contestants/*` - Contestant management endpoints
- `/companies/*` - Company/sponsor endpoints
- `/guests/*` - Guest management
- `/mentors/*` - Mentor management
- `/organizers/*` - Organizer management
- `/volunteers/*` - Volunteer management

## Project Structure

```
.
├── main.py                 # FastAPI application entry point
├── Config.py              # Configuration settings
├── dependencies.py        # Dependency injection
├── models/                # Data models
├── repositories/          # Data access layer
├── routers/              # API route handlers
├── services/             # Business logic
├── resources/            # Static resources (fonts, templates)
├── tests/                # Test suite
└── docker-compose.yml    # Docker orchestration
```

## Generated Files

Generated ID cards are stored in the `generated_cards/` directory (mounted as `_out_/` inside the container).

## Testing

Run tests with:

```bash
# With uv
uv run pytest

# In Docker
docker-compose exec api uv run pytest
```

## Production Deployment

### Using Docker Compose

1. Update `docker-compose.yml` with production settings
2. Set up proper secrets management for Firebase credentials
3. Configure nginx reverse proxy (optional, template included)
4. Set up SSL certificates
5. Deploy:
   ```bash
   docker-compose up -d
   ```

### Health Checks

The Docker container includes a health check that pings the API every 30 seconds.

## Troubleshooting

### Container won't start
- Check logs: `docker-compose logs api`
- Verify all required files are present
- Ensure Firebase credentials are properly mounted

### Permission issues with generated files
- Check volume mount permissions
- Ensure the `generated_cards/` directory exists and is writable

### Missing fonts or resources
- Verify the `resources/` directory is properly mounted
- Check that all required fonts are in `resources/fonts/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

[Add your license here]

## Support

For issues and questions, please open an issue on GitHub.