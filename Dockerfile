# -------- STAGE 1: Builder --------
FROM python:3.11-slim AS builder

WORKDIR /app

# Instala librerías necesarias para compilar mysqlclient
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements primero
COPY requirements.txt .

# Instala dependencias del proyecto
RUN pip install --user --no-cache-dir -r requirements.txt

# -------- STAGE 2: Final --------
FROM python:3.11-slim AS final

WORKDIR /app

# Copia dependencias instaladas en builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copia código fuente
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]