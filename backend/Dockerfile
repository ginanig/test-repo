# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar poetry (opcional, se for usar) ou copiar requirements.txt
# RUN pip install poetry
# COPY poetry.lock pyproject.toml /app/
# RUN poetry install --no-dev

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Comando para rodar a aplicação será definido no docker-compose.yml
# Exemplo: CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
