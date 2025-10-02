FROM python:3.12.2-slim-bullseye
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

# Collect static files during build
RUN python manage.py collectstatic --noinput

ENTRYPOINT ["gunicorn", "core.wsgi", "--bind", "0.0.0.0:8000"]