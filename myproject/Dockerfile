# Use uma imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos necessários para o contêiner
COPY requirements.txt /app/

# Instala as dependências do Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do código para o contêiner
COPY . /app/

# Expõe a porta padrão do Django
EXPOSE 8000

# Comando padrão para rodar o servidor de desenvolvimento
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]