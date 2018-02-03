FROM node:8 as build
WORKDIR /app

COPY . /build/

RUN npm i -g gulp-cli
RUN npm i

RUN gulp build


FROM python:3 as app
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY . /app/

RUN pip install pipenv
RUN pipenv install --three --system

COPY --from=build /build/timestrap/static /app/timestrap/static
