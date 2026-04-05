# Sentinel AI - AI-Powered Incident Management System

Sentinel AI is an intelligent incident management platform that uses AI agents to diagnose, plan, execute, and evaluate remediation for infrastructure incidents.

## Features

- **AI-Powered Diagnosis**: Intelligent analysis of incidents and root cause detection
- **Automated Remediation**: Automated execution of remediation actions
- **Workflow Orchestration**: Complex workflow management and execution
- **Audit Trail**: Complete audit logging for compliance and review
- **Vector Search**: Semantic search over incident documentation
- **Scalable Architecture**: Built with FastAPI, Celery, and PostgreSQL

## Architecture

### Core Components

- **API Layer** (`app/api/`): FastAPI endpoints for incident and ingestion management
- **Agents** (`app/agents/`): AI agents for various incident management tasks
  - `DiagnosisAgent`: Analyzes incidents and identifies root causes
  - `PlannerAgent`: Creates remediation action plans
  - `ExecutorAgent`: Executes planned remediation actions
  - `EvaluatorAgent`: Validates remediation outcomes

- **Orchestration** (`app/orchestration/`): Workflow engine and capability registry
- **Tools** (`app/tools/`): Action execution tools (restart containers, check metrics, etc.)
- **Storage** (`app/storage/`): Repository pattern for data persistence
- **LLM Integration** (`app/llm/`): Model routing and embeddings

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd sentinel-ai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
sqlite migrations/init.sql  # Or use your database
```

### Running Locally

1. Start the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

2. View API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Running with Docker

1. Build and start all services:
```bash
docker-compose -f docker/docker-compose.yml up -d
```

2. View logs:
```bash
docker-compose -f docker/docker-compose.yml logs -f
```

## API Endpoints

### Health Checks
- `GET /health` - Health check
- `GET /ready` - Readiness check

### Incidents
- `GET /incidents/` - List incidents
- `GET /incidents/{incident_id}` - Get incident details
- `POST /incidents/` - Create incident
- `PUT /incidents/{incident_id}` - Update incident
- `DELETE /incidents/{incident_id}` - Delete incident

### Ingestion
- `POST /ingestion/documents` - Ingest documents
- `POST /ingestion/incidents` - Ingest incident data
- `GET /ingestion/status` - Get ingestion status

## Testing

Run tests with:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

## Development

### Project Structure

```
sentinel-ai/
├── app/                    # Main application code
│   ├── api/               # FastAPI routes
│   ├── agents/            # AI agents
│   ├── orchestration/     # Workflow engine
│   ├── tools/             # Action tools
│   ├── ingestion/         # Data ingestion
│   ├── llm/               # LLM integration
│   ├── storage/           # Data repositories
│   ├── core/              # Core utilities
│   ├── schemas/           # Pydantic models
│   ├── services/          # Business logic
│   └── main.py            # Application entry point
├── migrations/            # Database migrations
├── docker/                # Docker configuration
├── tests/                 # Unit and integration tests
├── scripts/               # Utility scripts
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

### Coding Standards

- Use async/await for I/O operations
- Follow PEP 8 style guide
- Add docstrings to all functions
- Write unit tests for new functionality

## Configuration

Configuration is managed through environment variables. See `app/core/config.py`:

- `DATABASE_URL`: Database connection string
- `LLM_MODEL`: LLM model to use (default: gpt-4)
- `LLM_API_KEY`: API key for LLM provider
- `CELERY_BROKER_URL`: Redis connection for Celery
- `DEBUG`: Enable debug mode
- `ENV`: Environment (development, production, testing)

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.
