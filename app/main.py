"""
FastAPI TodoList application with GraphQL endpoints using Strawberry.

This module contains the main FastAPI application with GraphQL
functionality for TodoList operations.
"""

from typing import Any, Dict

from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from strawberry.fastapi import GraphQLRouter

from app.graphql.schema import schema

# Initialize FastAPI app
app = FastAPI(
    title="Crehana TodoList GraphQL API",
    description="A TodoList API with GraphQL endpoints using Strawberry",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create GraphQL router with GraphQL IDE enabled
graphql_app = GraphQLRouter(
    schema, graphql_ide="graphiql", path="/graphql"  # Enable GraphiQL interface
)

# Include GraphQL router
app.include_router(graphql_app, prefix="")


# Add a custom GraphQL endpoint for better Swagger documentation
@app.post(
    "/graphql-query",
    summary="Execute GraphQL Query",
    description="""
    Execute GraphQL queries and mutations for TodoList operations.

    **Example Queries:**

    Get all tasks:
    ```json
    {
      "query": "{ tasks { id title description completed } }"
    }
    ```

    Get task by ID:
    ```json
    {
      "query": "{ task(taskId: 1) { id title description completed } }"
    }
    ```

    **Example Mutations:**

    Create task:
    ```json
    {
      "query": "mutation { createTask(taskInput: { title: \\"New Task\\", description: \\"Task description\\", completed: false }) { id title description completed } }"
    }
    ```

    Update task:
    ```json
    {
      "query": "mutation { updateTask(taskId: 1, taskInput: { title: \\"Updated Task\\", completed: true }) { id title description completed } }"
    }
    ```

    Delete task:
    ```json
    {
      "query": "mutation { deleteTask(taskId: 1) }"
    }
    ```
    """,
    tags=["GraphQL Operations"],
)
async def graphql_query(
    query_data: Dict[str, Any] = Body(
        ...,
        examples={"default": {"value": {"query": "{ tasks { id title description completed } }"}}},
        description="GraphQL query or mutation",
    )
):
    """
    Execute GraphQL queries and mutations.

    Args:
        query_data: Dictionary containing the GraphQL query

    Returns:
        GraphQL response with data or errors
    """
    # This endpoint delegates to the main GraphQL router
    # Create a mock request for the GraphQL router
    import json

    from fastapi import Request
    from fastapi.responses import JSONResponse
    from starlette.datastructures import Headers
    from starlette.requests import Request as StarletteRequest
    from strawberry.fastapi import GraphQLRouter

    # Execute the GraphQL query using Strawberry
    result = await schema.execute(
        query_data.get("query", ""),
        variable_values=query_data.get("variables", {}),
        context_value=None,
        operation_name=query_data.get("operationName"),
    )

    response_data = {"data": result.data}
    if result.errors:
        response_data["errors"] = [{"message": str(error)} for error in result.errors]

    return response_data


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Health status
    """
    return {"status": "healthy", "service": "TodoList GraphQL API"}


# GraphQL Schema endpoint for introspection
@app.get("/graphql-schema", response_class=HTMLResponse)
async def get_graphql_schema():
    """
    Get GraphQL schema documentation.

    Returns:
        HTML: GraphQL schema documentation
    """
    schema_str = str(schema)
    return f"""
    <html>
        <head>
            <title>GraphQL Schema</title>
            <style>
                body {{ font-family: monospace; margin: 20px; }}
                pre {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>GraphQL Schema</h1>
            <pre>{schema_str}</pre>
        </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
