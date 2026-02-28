Assignment Description
 
You are tasked with building a multi-tenant Django web application with a focus on scalability, performance, and real-time communication. The application will include a Django admin panel for managing tenants and users, a public and private schema for each tenant, ElasticSearch integration for fast and efficient search functionality, and WebSockets for real-time notifications.
 
Requirements
 
Multi-Tenant Architecture
Implement a multi-tenant architecture where each tenant has its own isolated database schema.
Use Django's routing capabilities or a library like django-tenant-schemas to achieve multi-tenancy.

Django Admin Panel
Customize the Django admin panel to support multi-tenancy.
Ensure that superusers can manage tenants and their users through the admin panel.
Public & Private Schema
Create a public schema that contains shared data accessible to all tenants.
Implement a private schema for each tenant to store tenant-specific data.
For CRUD operation implement REDIS cache mechanism wherever possible.
ElasticSearch Implementation
Integrate ElasticSearch into your Django project using the official Elasticsearch Python client.
Use ElasticSearch to index and search data across tenants, ensuring that each tenant's data is isolated.
WebSockets for Notifications
Implement WebSockets using Django Channels for real-time notifications.

Develop a simple React app that connects to the WebSocket server and displays notifications to users.
Additional Considerations
Ensure that the application is secure and follows best practices for Django development.
Implement proper error handling and logging.
Write unit tests to ensure the correctness of your code.
Document the architecture, design decisions, and setup instructions for the application.
Submission
Submit the source code of your Django project along with any necessary configuration files.
Evaluation Criteria
Adherence to requirements
Code quality and organization
Scalability and performance
Documentation and clarity of explanation