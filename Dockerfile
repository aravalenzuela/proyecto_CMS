# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# run collectstatic
RUN python manage.py collectstatic --noinput

# run migrations
RUN python manage.py migrate --settings=core.settings.production

EXPOSE 8000
ENTRYPOINT gunicorn core.wsgi --bind 0.0.0.0:8000 
