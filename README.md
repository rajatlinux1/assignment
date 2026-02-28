# Django Multi-Tenant Application

This project is a high-performance multi-tenant web application built with Django. It utilizes PostgreSQL schema-based isolation for tenant data, Redis for caching, Elasticsearch for robust search capabilities, and WebSockets (via Django Channels & Daphne) for real-time features.

## Setup Instructions

### 1. System Requirements
Before proceeding, ensure your local development environment meets the following requirements:
- **Python:** 3.10 or higher
- **Database:** PostgreSQL
- **Cache & Message Broker:** Redis
- **Search Engine:** Elasticsearch (running locally or via a Docker container)

### 2. Installation
This project leverages `uv` for fast and reliable dependency management. Install the dependencies by running:
```bash
uv sync
```

### 3. Environment Configuration
Create a `.env` file in the root directory of the project to correctly configure your local stack variables. Include the following necessary keys:

```properties
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/1
ELASTICSEARCH_URL=http://localhost:9200
CORS_ALLOWED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
CORS_ALLOW_CREDENTIALS=True
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
```

### 4. Database Setup & Migrations
Initialize the system by generating any pending migrations, applying them across all tenant schemas, and creating an admin superuser:
```bash
uv run python manage.py makemigrations
uv run python manage.py migrate_schemas
uv run python manage.py createsuperuser
```

### 5. Seed Dummy Data (Optional)
Generate random dummy data for a target tenant schema to populate the catalog:
```bash
uv run python script/load_dummy_items.py <schema_name> <number_of_records>
```
*Example: `uv run python script/load_dummy_items.py tenant1 100`*

### 6. Configure Elasticsearch Indices
You must rebuild the search indices for the application to interact with Elasticsearch properly.

- **To rebuild indices for all available schemas:**
  ```bash
  uv run python manage.py rebuild
  ```

- **To rebuild indices for a specific schema:**
  ```bash
  uv run python manage.py rebuild <schema_name>
  ```

### 7. Testing
```bash
uv run pytest tenant_app/tests.py -v
```

### 8. Running the Application
The `daphne` ASGI server handles the standard Django runserver flow seamlessly while inherently providing support for long-polling asynchronous WebSockets channels. Start the development server using:
```bash
uv run python manage.py runserver 8000
```

Navigate your browser to [http://localhost:8000/admin](http://localhost:8000/admin) to log in and begin exploring the dashboard!
