FROM python:3.11.6

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

RUN ["mkdir", "-p", "database/ai_model"]

RUN ["pip", "install", "-e", "."]

# RUN ["alembic", "init", "alembic"]

# RUN ["mkdir", "-p", "alembic/versions"]

# RUN ["alembic", "revision", "-m", "initialization"]

# RUN ["alembic", "upgrade", "head"]

# RUN ["alembic", "revision", "--autogenerate"]

# RUN ["alembic", "upgrade", "head"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
