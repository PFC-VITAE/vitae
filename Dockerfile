# Escolha a imagem base de Python, por exemplo, Python 3.9
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instale as dependências do sistema necessárias (ghostscript e python3-tk)
RUN apt-get update && apt-get install -y \
    ghostscript \
    python3-tk

# Copia os arquivos do seu projeto para o container
COPY . /app

# Se o projeto tiver dependências, copie o arquivo requirements.txt e instale-as
RUN pip install --no-cache-dir -r requirements.txt

# Especifica o comando que será executado ao iniciar o container
CMD ["python", "app/main.py"]