
FROM python:3.12-slim

# 1. Dépendances système pour OpenCV et ONNX
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Pré-téléchargement du modèle dans /tmp (seul dossier 100% accessible)
RUN mkdir -p /tmp/.u2net && \
    curl -L https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx -o /tmp/.u2net/u2net.onnx && \
    chmod -R 777 /tmp/.u2net

# 3. Installation des libs (avec rembg[cpu] défini dans requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copie du code
COPY . .
RUN chmod -R 777 /app

# 5. Configuration de l'environnement
ENV U2NET_HOME=/tmp
ENV PORT=7860
EXPOSE 7860

# Lancement stable
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]