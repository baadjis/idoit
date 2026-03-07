FROM python:3.12-slim

# 1. Dépendances système pour les images et curl pour le téléchargement
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Copie des fichiers
COPY . .

# 3. Installation des bibliothèques Python
RUN pip install --no-cache-dir -r requirements.txt

# 4. PRÉ-TÉLÉCHARGEMENT DU MODÈLE IA (Indispensable pour éviter le "Restarting")
# On crée le dossier caché et on télécharge le modèle u2net
RUN mkdir -p /root/.u2net && \
    curl -L https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx -o /root/.u2net/u2net.onnx

# Port Hugging Face
ENV PORT=7860
EXPOSE 7860

# Lancement
CMD ["python", "main.py"]