FROM python:3.12-slim

# Dépendances système
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Création du dossier pour le modèle avec les bonnes permissions
RUN mkdir -p /app/.u2net && chmod 777 /app/.u2net

# Téléchargement du modèle directement dans le dossier de travail
RUN curl -L https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx -o /app/.u2net/u2net.onnx

# Copie du projet
COPY . .

# Installation des libs
RUN pip install --no-cache-dir -r requirements.txt

# --- CRUCIAL : On dit à rembg où est le modèle ---
ENV U2NET_HOME=/app/.u2net
ENV PORT=7860
EXPOSE 7860

CMD ["python", "main.py"]