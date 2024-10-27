Python(Django) Project Task

This project is a Django-based web application that manages users, clients, and projects. It provides a REST API to perform operations like registering clients, managing client information, adding projects, and assigning users to projects. The system is designed to handle multiple clients, projects, and users.

Features

User Management: Uses Django's built-in user management for authentication.
Client Management: Create, view, update, and delete clients.
Project Management: Create projects for a client and assign users to these projects.
User-Project Assignment: Manage which users are assigned to various projects.
Authentication: Ensures only authenticated users can access certain endpoints.
Permissions: Implements role-based access control for different actions.

Entities

1. User: Represents the registered users in the system.
2. Client: Represents companies or organizations with projects.
3. Project: Represents projects that belong to a client and can be assigned to multiple users.

Relationships

- The system can have many users and many clients.
- A client can have multiple projects.
- A project can be assigned to multiple users.
