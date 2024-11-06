import csv
import os
import random
import time
import logging
from locust import HttpUser, task, between, events

# Configurer le logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables globales pour le suivi
total_requests = 0
total_successes = 0
total_failures = 0
user_count = 5  # Nombre d'utilisateurs à surveiller pour le test

# Liste d'utilisateurs inactifs (par exemple des IDs utilisateurs)
inactive_users = [1, 2, 3, 4, 5]

# Chemin vers le fichier CSV
csv_file = 'results.csv'
GLOBAL_NGINX_FRONTEND_URL = "http://172.16.20.25:30081"

# Configurer le fichier CSV avec les en-têtes si nécessaire
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Nombre d'utilisateurs", "Total Requêtes", "Succès", "Échecs"])

# Fonction pour enregistrer les résultats dans le CSV
def log_results():
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_count, total_requests, total_successes, total_failures])
    logger.info("Résultats enregistrés dans le CSV.")

# Événements pour suivre les requêtes
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception=None):
    global total_requests, total_successes, total_failures
    total_requests += 1
    if exception is None:
        total_successes += 1
        logger.info("Requête réussie")
    else:
        total_failures += 1
        logger.error("Requête échouée")

class MyUser(HttpUser):
    wait_time = between(1, 2)
    host = GLOBAL_NGINX_FRONTEND_URL
    running = True  # Variable d'état

    def on_start(self):
        self.user_id = random.choice(inactive_users)
        logger.info(f"User {self.user_id} is now active.")

    def task1(self):
        logger.info("bonjour")
        time.sleep(1)

    def tasks4(self):
        #start = random.randint(0, 100)
        start = 1
        stop = start + 10

        response = self.client.get(
            f"/wrk2-api/home-timeline/read?start=1&stop=4&user_id={self.user_id}",
            name="/wrk2-api/home-timeline/read?start=1&stop=4"
        )
        logger.info(f"Réponse : {response.status_code} - {response.text}")

    @task
    def sequential_tasks(self):
        if not self.running:
            return  # Ne rien faire si l'utilisateur ne doit pas continuer

        self.task1()
        #self.tasks4()

        # Vérifiez si le nombre d'utilisateurs atteint user_count
        #if self.environment.runner.user_count >= user_count:
        logger.info("Enregistrement des résultats dans le CSV...")
        log_results()
        reset_counters()

        # Condition pour arrêter après un certain nombre de requêtes
        if total_requests >= 1:
            logger.info("Limite de requêtes atteinte, arrêt de l'utilisateur.")
            self.running = False  # Mettre à jour la variable d'état

# Réinitialiser les compteurs après chaque enregistrement dans le CSV
def reset_counters():
    global total_requests, total_successes, total_failures
    total_requests = 0
    total_successes = 0
    total_failures = 0