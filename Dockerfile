FROM alpine

WORKDIR /srv/timestrap

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache python3 python3-dev py3-pip nodejs nodejs-dev yarn \
    postgresql-dev gcc musl-dev libffi-dev

COPY Pipfile Pipfile.lock package.json yarn.lock /srv/timestrap/
RUN pip3 install --upgrade pip \
    && pip3 install pipenv \
    && pipenv install --dev --system \
    && yarn install

COPY . .

RUN yarn run build:prod
RUN python3 manage.py collectstatic --noinput
