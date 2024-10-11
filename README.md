# Nimap__Task
 

## Authentication

1. POST /api-token-auth/ - Obtain API token authentication

## Client Management

1. GET /clients/ - List all clients
2. POST /clients/ - Create a new client
3. GET /clients/<int:id>/ - Retrieve a specific client by ID
4. PUT /clients/<int:id>/- Edit a client 


## Project Management

1. POST /clients/<int:id>/projects/ - Create a new project for a specific client
2. GET /projects/ - List projects for the current user


## User Management

1. GET /users/ - List all users
2. POST /users/ - Create a new user
3. GET /users/<int:pk>/ - Retrieve a specific user by ID (primary key)
4. DELETE/users/<int:pk>/ - Deletes a specific user by ID
