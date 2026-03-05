# On utilise bien la version 3.12-slim comme ton PC
FROM python:3.12-slim

# On installe libgl1 (le remplaçant de libgl1-mesa-glx) et libglib2.0-0
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie des fichiers
COPY . .

# Installation des bibliothèques Python
RUN pip install --no-cache-dir -r requirements.txt

# Port spécifique Hugging Face
ENV PORT=7860
EXPOSE 7860

# Lancement
CMD ["python", "main.py"]