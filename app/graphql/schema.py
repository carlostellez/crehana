"""
GraphQL schema for the TodoList application.

This module creates the main GraphQL schema using Strawberry
by combining queries and mutations.
"""

import strawberry

from app.graphql.resolvers import Mutation, Query

# Create the GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
