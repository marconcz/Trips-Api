FROM python:3.8

RUN mkdir /trips-api 
COPY . /trips-api/
COPY pyproject.toml /trips-api 
COPY README.md /trips-api 
WORKDIR /trips-api

ENV HOST=
ENV PORT=
EXPOSE 7777
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi