FROM python:3.9

LABEL maintainer="Aprila Hijriyan"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app /space/app
COPY ./Pipfile /space/app
COPY ./Pipfile.lock /space/app

WORKDIR /space/app

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
