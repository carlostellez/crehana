# Crehana TodoList GraphQL API

A TodoList GraphQL API built with FastAPI and Strawberry GraphQL following clean architecture principles.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.8+ (recommended: 3.11)

### Run with Docker
```bash
# Clone and start
git clone https://github.com/carlostellez/crehana.git
cd crehana
docker-compose up --build

# Access the API
# GraphQL Playground: http://localhost:8000/graphql
# API Documentation: http://localhost:8000/docs
# Health Check: http://localhost:8000/health
```

### Local Development
```bash
# Create virtual environment
python3.11 -m venv .env
source .env/bin/activate

# Install dependencies and run
make install
make dev
```

## 🛠️ Tech Stack

- **Backend**: FastAPI + Strawberry GraphQL
- **Architecture**: Clean Architecture (Models → Services → GraphQL)
- **Testing**: pytest + httpx + pytest-cov
- **Code Quality**: flake8 + black + isort + pylint
- **Containerization**: Docker & Docker Compose
- **Data Storage**: In-memory (starts empty)

## 📊 GraphQL Operations

### Queries
- `tasks` - Get all tasks
- `task(taskId: Int!)` - Get a task by ID

### Mutations
- `createTask(taskInput: TaskInput!)` - Create a new task
- `updateTask(taskId: Int!, taskInput: TaskUpdateInput!)` - Update a task
- `deleteTask(taskId: Int!)` - Delete a task

### Example Usage (GraphQL Playground)

**Create a task:**
```graphql
mutation {
  createTask(taskInput: {
    title: "Learn GraphQL"
    description: "Study Strawberry GraphQL with FastAPI"
    completed: false
  }) {
    id
    title
    description
    completed
  }
}
```

**Get all tasks:**
```graphql
query {
  tasks {
    id
    title
    description
    completed
  }
}
```

## 📁 Project Structure

```
crehana/
├── app/
│   ├── main.py                   # FastAPI application
│   ├── models/task.py            # Pydantic models
│   ├── services/task_service.py  # Business logic
│   └── graphql/                  # GraphQL layer
│       ├── types.py              # GraphQL types
│       ├── resolvers.py          # Queries & mutations
│       └── schema.py             # Schema definition
├── tests/                        # Test suite
├── docker-compose.yml            # Docker configuration
├── Dockerfile                    # Container definition
├── Makefile                      # Development commands
└── requirements.txt              # Dependencies
```

## 🧪 Development Workflow

### Available Commands
Use `make help` to see all available commands. Key commands:

```bash
# Development
make dev           # Start development server
make install       # Install dependencies

# Testing & Quality
make test          # Run tests
make test-cov      # Run tests with coverage
make check         # Run all quality checks (lint + format + test)

# Docker
make docker-up     # Start Docker services
make docker-check  # Run all checks in Docker
```

### Testing
- **Unit tests**: Service layer business logic
- **Integration tests**: GraphQL operations
- **Coverage**: 99% code coverage achieved

### Code Quality
- **Linting**: flake8 for code style
- **Analysis**: pylint for advanced code analysis  
- **Formatting**: black + isort for consistent formatting
- **Type checking**: mypy for type safety

## 🎯 API Endpoints

- **GraphQL Playground**: http://localhost:8000/graphql (recommended)
- **GraphQL Query**: http://localhost:8000/graphql-query (for Swagger)
- **FastAPI Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔧 Development Features

- ✅ Type-safe GraphQL with Strawberry
- ✅ Clean Architecture with separated layers
- ✅ Comprehensive test suite (22 tests)
- ✅ Code quality tools integration
- ✅ Docker containerization
- ✅ Hot reload for development
- ✅ GraphQL Playground interface
- ✅ Health checks and monitoring
- ✅ Modern Pydantic v2 configuration
- ✅ Updated Strawberry GraphQL configuration

## 🔧 Troubleshooting

### IDE Import Errors
If you see import errors in your IDE:

1. **Configure Python interpreter** to use `.env/bin/python`
2. **Recreate virtual environment** if needed:
   ```bash
   rm -rf .env && python3.11 -m venv .env && source .env/bin/activate && make install
   ```
3. **Use Docker** as alternative: `make docker-check`

### Verify Installation
```bash
source .env/bin/activate
python -c "import fastapi, pytest, pylint; print('✅ All imports OK')"
```

## 📝 Notes

- **Data Storage**: In-memory, starts empty (create tasks via GraphQL)
- **Python Compatibility**: 3.8+ (Docker uses 3.11-slim)
- **Architecture**: Models → Services → GraphQL → FastAPI
- **Testing**: Unit tests for services, integration tests for GraphQL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run quality checks: `make check`
5. Submit a pull request
