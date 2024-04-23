# About
Task Manager is the web-service for organizing tasks between registered users. Each task must have status, executor, and optionally labels (m2m). All content (statuses, labels) creates by users themselves and can be updated by creators. If status, label or user are linked with tasks, they are unavailable for deleting.

# System requirements
#### PL, Virtual Environment, DBMS
- Python ^3.10;
- Poetry ^1.6.1;
- PostgreSQL ^15.
#### Modules
- python = "^3.10"
- django = "^5.0.4"
- djangorestframework = "^3.15.1"
- python-dotenv = "^1.0.1"
- psycopg2-binary = "^2.9.9"
- gunicorn = "^22.0.0"


# Installing
The command below will install all dependencies and database template for correct work of the web-service locally or on a deploy.

```make build```

After installing file ".env" should be created in the root directory of the project. This file must contain environment variables:
- SECRET_KEY;
- DEBUG;
- POSTGRESQL (Boolean);
- DB_HOST;
- DB_NAME;
- DB_USER;
- DB_PASSWORD;
- DB_PORT;


On a deployment these variables should be defined on your deploy service.

# Dev mode with debug
```make dev```

# Launch web-service
```make start```