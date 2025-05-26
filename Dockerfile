# Usar uma imagem base do Python
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos de requirements primeiro (para otimizar o cache do Docker)
COPY requirements.txt .

# Instalar as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código da aplicação
COPY . .

# Criar diretórios necessários (se houver)
RUN mkdir -p static templates

# Expor a porta que a aplicação Flask vai usar
EXPOSE 5000

# Definir variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Comando para executar a aplicação
CMD ["python", "app.py"]