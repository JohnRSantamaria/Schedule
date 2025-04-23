# Entra a cada app que tú creaste y borra migraciones

Remove-Item -Recurse -Force .\backend\users\migrations\ -Exclude **init**.py

# Borrar cachés de Python

Remove-Item -Recurse -Force .\backend\*\*\_\_pycache\_\_\

# 💥 Eliminar completamente el esquema de Django en PostgreSQL

# Conéctate de a la DB en Docker:

```bash
docker exec -it postgres_db psql -U admin -d schedule_db
```

# Crear el superusuario de nuevo

Desde tu terminal con el entorno virtual activado y dentro del directorio backend/, ejecuta:

```bash
python manage.py createsuperuser
```

# Ejecutar el projecto

```bash
python manage.py runserver
```

# Vuelve a reconstruir todo desde cero

Corre esto desde la raíz del proyecto:

```bash
docker-compose down --volumes --remove-orphans
docker-compose build --no-cache
docker-compose up
```

🔁 Esto forzará a Docker a reinstalar todo incluyendo gunicorn.

# Reconstruye el contenedor

Desde la raíz del proyecto (schedule/):

```bash
docker-compose down --volumes
docker-compose up --build
```

# Crear un superusuario

```bash
docker-compose exec web python manage.py createsuperuser
```

# Mostrar migraciones

```bash
docker-compose exec web python manage.py showmigrations
```

# Realizar migraciones 

```bash
docker-compose exec web python manage.py makemigrations {app_name}

```

