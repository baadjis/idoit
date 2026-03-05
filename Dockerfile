FROM python:3.12-slim

# Mise à jour pour Debian Trixie : on utilise libgl1 au lieu de libgl1-mesa-glx
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie de tous les fichiers du projet
COPY . .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Port obligatoire pour Hugging Face
ENV PORT=7860
EXPOSE 7860

# Lancement de l'application
CMD ["python", "main.py"]