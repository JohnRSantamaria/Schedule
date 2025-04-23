FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code/backend

# Copiamos requirements y los instalamos
COPY requirements.txt /code/
RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-dev python3-dev \
    && pip install --upgrade pip \
    && pip install -r /code/requirements.txt \
    && apk del gcc musl-dev python3-dev

# Copiamos el resto del código al contenedor
COPY . /code/

RUN python manage.py collectstatic --noinput

# Ejecutamos gunicorn apuntando correctamente al módulo wsgi
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
