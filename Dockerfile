# On garde ta version 3.12
FROM python:3.12-slim

# CORRECTION ICI : on remplace libgl1-mesa-glx par libgl1
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# On copie tout le projet
COPY . .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Port pour Hugging Face
ENV PORT=7860
EXPOSE 7860

# Lancement de l'app
CMD ["python", "main.py"]