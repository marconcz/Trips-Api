FROM python:3.8

#RUN mkdir -p api/ 
#WORKDIR /api/
#RUN printf "HOST=\nPORT=" >.env
RUN mkdir -p /trips-api 
COPY . /trips-api/
COPY .env .
WORKDIR /trips-api

ENV HOST=
ENV PORT=
EXPOSE 7777
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

RUN pip3 install poetry
RUN poetry config virtualenvs.create true
RUN poetry install --no-interaction --no-ansi
