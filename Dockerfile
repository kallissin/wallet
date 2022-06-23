# Imagem do python
FROM python:3.8.11-slim-buster
# Copiando os arquivos do projeto para o diretorio app
COPY . /app
# Definindo o diretório onde o CMD será executado e copiando o arquivo de requerimentos
WORKDIR /app
COPY requirements.txt ./
# Instalando os requirements com o PIP
RUN pip install --no-cache-dir -r requirements.txt
# Comando para subir a aplicação
CMD ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:8000", "--workers", "3"]