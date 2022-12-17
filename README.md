# Trips-API
Servicios de viaje para la aplicación.

**Installation**
1. curl -sSL https://install.python-poetry.org | python3 -
2. Agregar a env var PATH del OS

**Dependencies**
1. poetry config virtualenvs.in-project true
2. poetry install

## Scripts
**Run server**
- poetry run start

**Execute test**
- poetry run test

**Execute Linter**
- poetry run lint

**Formatting code**
- poetry run format

### Deploy

The pipeline deploys the server automatically on pushing to **master**

You should create the app on heroku first

You'll need to set the following actions secrets:

- `HEROKU_NAME`: App name
- `HEROKU_EMAIL`: Account email
- `HEROKU_API_KEY`: Account API key


# ---------------RUN WITH DOCKER---------------- #
**docker build . -t python-image**

**docker run -t python-image**


