# Imagen base
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instala dependencias de sistema necesarias para compilar mysqlclient
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Instala dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
