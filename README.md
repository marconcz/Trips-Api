# Trips-API
Servicios de viaje para la aplicación.

**Instalar poetry**
1. curl -sSL https://install.python-poetry.org | python3 -
2. Agregar a env var PATH del OS

**Instalar dependencias**
1. poetry config virtualenvs.in-project true
2. poetry install

## Scripts
**Levantar servidor**
- poetry run start

**Ejecutar pruebas**
- poetry run test

**Ejecutar linter**
- poetry run lint

**Revisar formateo del codigo codigo**
- poetry run format

**Refactorizar el codigo**
- poetry run reformat
