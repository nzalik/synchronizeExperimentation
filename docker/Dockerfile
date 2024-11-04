# Utiliser l'image officielle de Locust
FROM locustio/locust

# Copier le fichier de test Locust dans l'image
COPY locustfile.py /locustfile.py

# Spécifier le fichier Locust comme fichier principal pour les tâches
ENV LOCUSTFILE /locustfile.py