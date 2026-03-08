FROM python:3.12-slim

# 1. Dépendances système
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Création du dossier et téléchargement du modèle
# On crée /app/data/.u2net
RUN mkdir -p /app/data/.u2net
RUN curl -L https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx -o /app/data/.u2net/u2net.onnx

# 3. DROITS 777 SUR LE DOSSIER DATA (Crucial pour éviter le plantage)
RUN chmod -R 777 /app/data

# 4. Installation du projet
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Variables d'environnement
# rembg cherchera le dossier .u2net à l'intérieur de U2NET_HOME
ENV U2NET_HOME=/app/data
ENV PORT=7860
EXPOSE 7860

CMD ["python", "main.py"]