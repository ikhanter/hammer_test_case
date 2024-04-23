# About
Referral system API.
API with authorization by phone-number, imitating confirmation code, possibility to set referrer for yourself only once.

### Routes
- /
  - GET - List of all numbers with codes
  - POST - {"phone_number": "+..."} - Login into service by a phone number. If it doesn't exist - create new user and login
- /confirm/
  - GET - Information about neccessarity to send POST
  - POST - {"conf_code": XXXX} - send confirmation code (any 4 digits are acceptable, generator is included)
- /me/
  - GET - User info
  - POST - {"code": XXXXXX} - Set your referrer. Only existing codes areexxeptable. Both users must be confirmed for referring
- /logout/
  - POST - Logout

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
