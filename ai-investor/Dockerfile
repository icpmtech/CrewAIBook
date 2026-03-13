FROM python:3.11-slim

WORKDIR /app

# Instalar dependências (aproveita cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY . .

# Criar directório de output
RUN mkdir -p output

CMD ["python", "main.py"]
