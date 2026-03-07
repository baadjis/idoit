FROM python:3.12-slim

# Dépendances système
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# On crée le dossier du modèle DANS /app pour qu'il soit visible
RUN mkdir -p /app/data/.u2net

# Téléchargement du modèle pendant le BUILD
RUN curl -L https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx -o /app/data/.u2net/u2net.onnx

# On donne les permissions totales sur ce dossier
RUN chmod -R 777 /app/data/.u2net

# Copie du projet
COPY . .

# Installation des libs
RUN pip install --no-cache-dir -r requirements.txt

# --- LES VARIABLES D'ENVIRONNEMENT CRUCIALES ---
# On force rembg à regarder UNIQUEMENT dans notre dossier local
ENV U2NET_HOME=/app/data/.u2net
ENV PORT=7860
EXPOSE 7860

CMD ["python", "main.py"]