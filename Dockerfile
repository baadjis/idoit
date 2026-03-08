FROM python:3.12-slim

# 1. Dépendances système (OpenCV + images)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. On pré-télécharge le modèle dans /tmp pour éviter tout problème de droits
RUN mkdir -p /tmp/.u2net && \
    curl -L https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx -o /tmp/.u2net/u2net.onnx && \
    chmod -R 777 /tmp/.u2net

# 3. Installation des bibliothèques
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. On copie le reste du code
COPY . .

# 5. Droits totaux sur le dossier app pour éviter les erreurs de logs
RUN chmod -R 777 /app

# 6. Variables d'environnement
ENV U2NET_HOME=/tmp
ENV PORT=7860
EXPOSE 7860

# Lancement via uvicorn direct (plus stable que python main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]