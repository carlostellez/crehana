# Crehana GraphQL API

A modern GraphQL API built with FastAPI, Strawberry GraphQL, and Docker for the Crehana platform.

## 🚀 Features

- **GraphQL API** with Strawberry GraphQL
- **FastAPI** framework for high performance
- **Docker & Docker Compose** for containerization
- **In-memory data storage** for rapid prototyping
- **Redis** for caching and session management
- **GraphQL Playground** for API exploration
- **Automatic API documentation** with FastAPI
- **Health checks** and monitoring endpoints
- **CORS** support for frontend integration

## 🛠️ Tech Stack

- **Backend**: FastAPI + Strawberry GraphQL
- **Data Storage**: In-memory (for development/prototyping)
- **Cache**: Redis 7
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest + httpx

## 📋 Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)
- Git

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone <repository-url>
cd crehana
```

### 2. Set up environment variables
```bash
cp env.example .env
# Edit .env with your configuration
```

### 3. Build and run with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### 4. Access the API
- **GraphQL Endpoint**: http://localhost:8000/graphql
- **GraphQL Playground**: http://localhost:8000/graphql (when DEBUG=True)
- **External GraphQL Playground**: http://localhost:4000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
crehana/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   └── graphql/
│       ├── __init__.py
│       └── schema.py           # GraphQL schema with in-memory data
├── docker-compose.yml          # Docker services configuration
├── Dockerfile                  # Application container
├── requirements.txt            # Python dependencies
├── env.example                 # Environment variables template
└── README.md                   # Project documentation
```

## 🔧 Development

### Local Development Setup

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Commands

```bash
# Build the application
docker-compose build

# Start services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f web

# Execute commands in container
docker-compose exec web bash
```

## 📊 GraphQL Examples

### Sample Queries

```graphql
# Simple hello query
query Hello {
  hello
}

# Get all users
query GetUsers {
  users {
    id
    name
    email
    createdAt
    isActive
  }
}

# Get specific user
query GetUser($id: Int!) {
  user(id: $id) {
    id
    name
    email
    createdAt
  }
}

# Get all courses
query GetCourses {
  courses {
    id
    title
    description
    instructor
    durationHours
    isPublished
  }
}
```

### Sample Mutations

```graphql
# Create a new user
mutation CreateUser($userInput: UserInput!) {
  createUser(userInput: $userInput) {
    id
    name
    email
    createdAt
    isActive
  }
}

# Variables for CreateUser:
{
  "userInput": {
    "name": "New User",
    "email": "newuser@example.com"
  }
}

# Create a new course
mutation CreateCourse($courseInput: CourseInput!) {
  createCourse(courseInput: $courseInput) {
    id
    title
    description
    instructor
    durationHours
    createdAt
  }
}

# Variables for CreateCourse:
{
  "courseInput": {
    "title": "New Course",
    "description": "Course description",
    "instructor": "Instructor Name",
    "durationHours": 10
  }
}
```

## 🧪 Testing

```bash
# Run tests
docker-compose exec web pytest

# Run tests with coverage
docker-compose exec web pytest --cov=app

# Run specific test file
docker-compose exec web pytest tests/test_graphql.py
```

## 🔒 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_URL` | Redis connection string | Required |
| `SECRET_KEY` | JWT secret key | Required |
| `DEBUG` | Enable debug mode | `False` |
| `GRAPHQL_PLAYGROUND` | Enable GraphQL playground | `False` |

## 📈 Monitoring

- **Health Check**: `GET /health`
- **Metrics**: Available through FastAPI metrics
- **Logs**: Structured logging with Docker

## 🔄 Data Persistence

Currently, the API uses in-memory data storage for rapid prototyping. Data will be reset when the application restarts. To add persistent storage:

1. Add a database service to `docker-compose.yml`
2. Update `requirements.txt` with database dependencies
3. Modify the GraphQL resolvers to use database operations
4. Add database models and migrations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please open an issue in the repository.