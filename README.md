# Crehana TodoList GraphQL API

A TodoList GraphQL API built with FastAPI and Strawberry GraphQL following modern development practices.

## 🚀 Features

- **Complete GraphQL API** with queries and mutations for tasks
- **Strawberry GraphQL** for type-safe GraphQL implementation
- **FastAPI** framework for high performance
- **Clean Architecture** with separated layers (Models, Services, GraphQL)
- **Comprehensive Testing** with pytest (unit and integration tests)
- **Code Quality Tools** (flake8, black, isort)
- **Docker & Docker Compose** for containerization
- **In-memory data storage** for rapid prototyping
- **GraphQL Playground** for interactive API exploration
- **Health checks** and monitoring endpoints
- **CORS** support for frontend integration

## 🛠️ Tech Stack

- **Backend**: FastAPI + Strawberry GraphQL
- **GraphQL**: Strawberry GraphQL with type safety
- **Architecture**: Clean Architecture (Models → Services → GraphQL)
- **Data Storage**: In-memory (for development/prototyping)
- **Testing**: pytest + httpx + pytest-cov
- **Code Quality**: flake8 + black + isort + mypy
- **Containerization**: Docker & Docker Compose
- **Documentation**: English docstrings and comprehensive README

## 📋 Prerequisites

- Docker and Docker Compose installed
- Python 3.11
- Git

## 🐍 Python Version Compatibility

This project supports the following Python versions:

### ✅ Supported Versions
- **Python 3.8** (minimum required)
- **Python 3.9** 
- **Python 3.10** 
- **Python 3.11** (recommended for production)

### 🎯 Recommendations
- **For local development**: Python 3.10 or 3.11 (better performance and features)
- **For production**: Python 3.11 (as used in Docker container)
- **Minimum compatibility**: Python 3.8

### 📦 Dependencies Compatibility
All major dependencies support Python 3.8+:
- FastAPI 0.104.1
- Strawberry GraphQL 0.214.0
- Pydantic 2.5.0
- Uvicorn 0.24.0
- pytest 7.4.3

### ⚠️ Important Notes
- **Python 3.12+**: May have compatibility issues with some dependencies
- **Python < 3.8**: Not supported
- The Docker container uses **Python 3.11-slim** for optimal performance

### 🔍 Check Your Python Version
```bash
python --version
# or
python3 --version
```

### 🛠️ Troubleshooting Import Issues

If you encounter import errors like `Unable to import 'fastapi'` or `ModuleNotFoundError: No module named 'strawberry'`:

#### **1. Virtual Environment Issues**
```bash
# Check current Python version
python --version

# If using wrong version, recreate virtual environment
rm -rf .venv
python3.11 -m venv .venv  # Use Python 3.11
source .venv/bin/activate

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### **2. IDE Configuration**
- **VS Code**: `Cmd+Shift+P` → "Python: Select Interpreter" → choose `.venv/bin/python`
- **PyCharm**: Settings → Project → Python Interpreter → Add → Existing Environment → `.venv/bin/python`

#### **3. Verify Installation**
```bash
# Activate virtual environment
source .venv/bin/activate

# Test imports
python -c "from fastapi.testclient import TestClient; print('✅ FastAPI OK')"
python -c "import strawberry; print('✅ Strawberry OK')"
python -c "from app.main import app; print('✅ App OK')"
```

#### **4. Common Solutions**
```bash
# Clean installation
make clean
make install

# Or manual cleanup
rm -rf .venv __pycache__ .pytest_cache
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/carlostellez/crehana.git
cd crehana
```

### 2. Build and run with Docker Compose
```bash
# Build and start the service
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### 3. Access the API
- **GraphQL Playground**: http://localhost:8000/graphql
- **FastAPI Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
crehana/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application with GraphQL
│   ├── models/                 # Data models and Pydantic schemas
│   │   ├── __init__.py
│   │   └── task.py            # Task models and schemas
│   ├── services/              # Business logic layer
│   │   ├── __init__.py
│   │   └── task_service.py    # Task business logic
│   └── graphql/               # GraphQL layer
│       ├── __init__.py
│       ├── types.py           # GraphQL types and inputs
│       ├── resolvers.py       # GraphQL queries and mutations
│       └── schema.py          # GraphQL schema definition
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_graphql.py        # Integration tests for GraphQL API
│   └── test_services.py       # Unit tests for services
├── docker-compose.yml          # Docker services configuration
├── Dockerfile                  # Application container
├── requirements.txt            # Python dependencies
├── pytest.ini                 # Pytest configuration
├── .flake8                    # Flake8 linting configuration
├── pyproject.toml             # Black and other tool configurations
├── Makefile                   # Development commands
└── README.md                  # Project documentation
```

## 🏗️ Architecture Layers

### 1. **Models Layer** (`app/models/`)
- **Purpose**: Data models and validation schemas
- **Components**: Pydantic models for Task
- **Features**: Input validation, serialization, type safety

### 2. **Services Layer** (`app/services/`)
- **Purpose**: Business logic and data operations
- **Components**: TaskService
- **Features**: CRUD operations, business rules, data validation

### 3. **GraphQL Layer** (`app/graphql/`)
- **Purpose**: GraphQL API with type-safe operations
- **Components**: Types, Resolvers, Schema
- **Features**: Query/mutation handling, type safety, introspection

### 4. **API Layer** (`app/main.py`)
- **Purpose**: FastAPI application with GraphQL integration
- **Components**: FastAPI app with Strawberry GraphQL router
- **Features**: CORS, health checks, GraphQL playground

## 📊 GraphQL API Operations

The API provides the following GraphQL operations:

### Queries
- `tasks` - Get all tasks
- `task(taskId: Int!)` - Get a task by ID

### Mutations
- `createTask(taskInput: TaskInput!)` - Create a new task
- `updateTask(taskId: Int!, taskInput: TaskUpdateInput!)` - Update a task
- `deleteTask(taskId: Int!)` - Delete a task

### Task Data Format
Each task has the following structure:
```graphql
type Task {
  id: Int!
  title: String!
  description: String!
  completed: Boolean!
}

input TaskInput {
  title: String!
  description: String!
  completed: Boolean = false
}

input TaskUpdateInput {
  title: String
  description: String
  completed: Boolean
}
```

## 🔧 Local Development Setup

### 1. Create virtual environment
```bash
python3.11 -m venv .env
source .env/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
# or
make install
```

### 3. Run the application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# or
make dev
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest
# or
make test

# Run tests with coverage
pytest --cov=app --cov-report=html --cov-report=term
# or
make test-cov

# Run specific test file
pytest tests/test_graphql.py
pytest tests/test_services.py

# Run tests in Docker
docker-compose exec web pytest
# or
make docker-test
```

### Test Coverage
The test suite includes:
- **Unit tests** for TaskService class (`tests/test_services.py`)
- **Integration tests** for all GraphQL operations (`tests/test_graphql.py`)
- **Error handling tests** for non-existent resources
- **CRUD operation tests** for all GraphQL mutations and queries

### Test Configuration
- Configuration in `pytest.ini`
- Test markers for unit/integration/slow tests
- Coverage reporting with HTML output

## 🔍 Code Quality

### Linting with flake8
```bash
# Run linting
flake8 app tests
# or
make lint
```

### Code Formatting with black
```bash
# Format code
black app tests
# or
make format

# Check formatting
black --check app tests
# or
make format-check
```

### Import Sorting with isort
```bash
# Sort imports
isort app tests

# Check import sorting
isort --check-only app tests
```

### All Quality Checks
```bash
# Run all quality checks
make check
```

### Configuration Files
- `.flake8` - Flake8 configuration with project-specific rules
- `pyproject.toml` - Black, isort, and other tool configurations
- Line length: 88 characters (black standard)
- Import order: Google style

## 🐳 Docker

### Build and Run
```bash
# Build the application
docker-compose build
# or
make docker-build

# Start services
docker-compose up
# or
make docker-up

# Stop services
docker-compose down
# or
make docker-down
```

### Docker Services
- **web**: FastAPI application with GraphQL

### Docker Commands
```bash
# View logs
docker-compose logs -f web

# Execute commands in container
docker-compose exec web bash

# Run tests in container
docker-compose exec web pytest
```

## 📈 GraphQL Examples

### Query All Tasks
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

### Query Single Task
```graphql
query {
  task(taskId: 1) {
    id
    title
    description
    completed
  }
}
```

### Create Task
```graphql
mutation {
  createTask(taskInput: {
    title: "Complete project documentation"
    description: "Write comprehensive documentation"
    completed: false
  }) {
    id
    title
    description
    completed
  }
}
```

### Update Task
```graphql
mutation {
  updateTask(taskId: 1, taskInput: {
    title: "Updated task title"
    completed: true
  }) {
    id
    title
    description
    completed
  }
}
```

### Delete Task
```graphql
mutation {
  deleteTask(taskId: 1)
}
```

## 📈 Monitoring

- **Health Check**: `GET /health`
- **GraphQL Introspection**: Available through GraphQL playground
- **Metrics**: Available through FastAPI metrics
- **Logs**: Structured logging with Docker

## 🎯 Development Commands

Use the Makefile for common development tasks:

```bash
make help          # Show available commands
make install       # Install dependencies
make test          # Run tests
make test-cov      # Run tests with coverage
make lint          # Run linting
make format        # Format code
make format-check  # Check code formatting
make clean         # Clean cache files
make docker-build  # Build Docker image
make docker-up     # Start Docker services
make docker-down   # Stop Docker services
make docker-test   # Run tests in Docker
make dev           # Start development server
make check         # Run all quality checks
```

## 🔄 Data Persistence

Currently, the API uses in-memory data storage for rapid prototyping. Data will be reset when the application restarts. To add persistent storage:

1. Add a database service to `docker-compose.yml`
2. Update `requirements.txt` with database dependencies
3. Create database models with SQLAlchemy
4. Update services to use database operations
5. Add database migrations with Alembic

## 🎯 GraphQL Features

This implementation provides:

### ✅ Core GraphQL Features
- [x] **Type-safe Schema** - Complete GraphQL schema with Strawberry
- [x] **Queries and Mutations** - Full CRUD operations via GraphQL
- [x] **Input Validation** - Automatic validation through GraphQL types
- [x] **Introspection** - Schema introspection for development tools
- [x] **GraphQL Playground** - Interactive API exploration interface
- [x] **Error Handling** - Proper GraphQL error responses

### 📊 Task Operations
The API supports all standard task operations through GraphQL:
- ✅ Create tasks with validation
- ✅ Read single task or all tasks
- ✅ Update tasks with partial updates
- ✅ Delete tasks with confirmation
- ✅ Type-safe operations with Strawberry

### 🔧 Development Features
- ✅ Hot reload during development
- ✅ Comprehensive test suite for GraphQL operations
- ✅ Code quality tools integration
- ✅ Docker containerization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run quality checks: `make check`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please open an issue in the repository.