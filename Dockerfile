FROM python:3.12-slim

# 1. Installation des dépendances système
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Création d'un utilisateur non-root (obligatoire pour la stabilité sur HF)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    U2NET_HOME=/home/user/app/data

WORKDIR $HOME/app

# 3. Création du dossier et téléchargement du modèle PENDANT LE BUILD
# Note le chemin : data/.u2net
RUN mkdir -p $HOME/app/data/.u2net && \
    curl -L https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx -o $HOME/app/data/.u2net/u2net.onnx

# 4. Installation des dépendances Python
COPY --chown=user . .
RUN pip install --no-cache-dir --user -r requirements.txt

# 5. Variables d'environnement
ENV PORT=7860
EXPOSE 7860

CMD ["python", "main.py"]