
FROM python:3.12-slim

# Dépendances système pour OpenCV et Pillow
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie des fichiers
COPY . .

# Installation des bibliothèques Python
RUN pip install --no-cache-dir -r requirements.txt

# --- ASTUCE ANTI-LENTEUR : Pré-téléchargement du modèle IA ---
# On crée le dossier où rembg cherche ses modèles et on le télécharge maintenant
RUN mkdir -p /root/.u2net && \
    curl -L https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx -o /root/.u2net/u2net.onnx

# Port Hugging Face
ENV PORT=7860
EXPOSE 7860

# Lancement
CMD ["python", "main.py"]