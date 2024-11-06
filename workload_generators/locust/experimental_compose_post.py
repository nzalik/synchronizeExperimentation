import time
import os
import csv
from locust import LoadTestShape, HttpUser, task, between, events
import random
import resource
import json

resource.setrlimit(resource.RLIMIT_NOFILE, (250000, 250000))

# Simulation Configuration
GLOBAL_NGINX_FRONTEND_URL = os.environ.get("NGINX_ADDR")
GLOBAL_MEDIA_FRONTEND_URL = os.environ.get("MEDIA_ADDR")
GLOBAL_INTENSITY_FILE = os.environ.get("INTENSITY_FILE")
COMPOSITION_OPTION = os.environ.get("COMP_OPT")

GLOBAL_MIN_USERS = 100
GLOBAL_RANDOMNESS = 0.20
GLOBAL_WAIT_TIME = between(1, 3)

# Configuration des compositions
if COMPOSITION_OPTION == 'composePost':
    GLOBAL_COMPOSITIONS = [(100, 0, 0)]
elif COMPOSITION_OPTION == 'readHomeTimeline':
    GLOBAL_COMPOSITIONS = [(0, 100, 0)]
elif COMPOSITION_OPTION == 'readUserTimeline':
    GLOBAL_COMPOSITIONS = [(0, 0, 100)]
elif COMPOSITION_OPTION == 'mixed':
    GLOBAL_COMPOSITIONS = [(33, 33, 33)]
else:
    GLOBAL_COMPOSITIONS = [(5, 40, 55), (5, 45, 50), (5, 50, 45), (5, 55, 40),
                           (10, 35, 55), (10, 40, 50), (10, 45, 45), (10, 50, 40),
                           (10, 55, 35), (15, 35, 50), (15, 40, 45), (15, 45, 40),
                           (15, 50, 35)]

texts = [text.replace('@', '') for text in list(open('./datasets/fb-posts/news.txt'))]
media = [os.path.join('./datasets/inria-person', fname) for fname in os.listdir('./datasets/inria-person')]
users = list(range(1, 963))
active_users, inactive_users = [], list(range(1, 963))

# Chargement des amis
with open('./datasets/social-graph/socfb-Reed98.mtx', 'r') as f:
    friends = {}
    for edge in f.readlines():
        edge = list(map(int, edge.strip().split()))
        if len(edge) == 0:
            continue
        if edge[0] not in friends:
            friends[edge[0]] = set()
        if edge[1] not in friends:
            friends[edge[1]] = set()
        friends[edge[0]].add(edge[1])
        friends[edge[1]].add(edge[0])
    friends = {user: list(l) for user, l in friends.items()}

# Fonction pour initialiser le fichier custom_stats.csv
def initialize_csv(profile_id):
    filename = f"custom_stats.csv"
    filename2 = f"custom_stats_{profile_id}.csv"
    print("le file avec le profil peut etre comme ceci")
    print(filename2)
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "Target Time",
                "Load Intensity",
                "Successful Transactions",
                "Failed Transactions",
                "Dropped Transactions",
                "Avg Response Time",
                "Final Batch Dispatch Time"
            ])
    return filename

class LoadShape(LoadTestShape):
    row_offset = 0

    def tick(self):
        user_count = GLOBAL_MIN_USERS
        csv_list = []
        with open(GLOBAL_INTENSITY_FILE) as intensity_csv:
            csv_reader = csv.reader(intensity_csv, delimiter=',')
            csv_list = list(csv_reader)

        user_count = int(csv_list[self.row_offset][1])
        target_time = csv_list[self.row_offset][0]  # Récupérer le target_time

        # Stocker le target_time pour l'utiliser dans log_statistics
        self.current_target_time = target_time
        self.row_offset += 1

        if self.row_offset >= len(csv_list):
            return None

        spawn_rate = max(1, abs(user_count - self.get_current_user_count()))  # should not be 0
        return user_count, spawn_rate

class SocialNetworkUser(HttpUser):
    wait_time = GLOBAL_WAIT_TIME
    host = GLOBAL_NGINX_FRONTEND_URL

    total_successful_transactions = 0
    total_failed_transactions = 0

    def on_start(self):
        self.user_id = random.choice(inactive_users)
        active_users.append(self.user_id)
        inactive_users.remove(self.user_id)

        # Initialiser le fichier CSV pour ce profil
        self.profile_id = self.environment.runner.user_count  # Identifier le profil
        self.csv_file = initialize_csv(self.profile_id)

    # @task
    # def composePost(self):
    #     text = random.choice(texts)
    #
    #     # Mentions d'utilisateurs
    #     number_of_user_mentions = random.randint(0, min(5, len(friends[self.user_id])))
    #     if number_of_user_mentions > 0:
    #         for friend_id in random.choices(friends[self.user_id], k=number_of_user_mentions):
    #             text += " @username_" + str(friend_id)
    #
    #     # Média
    #     media_id = ''
    #     media_type = ''
    #     if random.random() < 0.20:
    #         with open(random.choice(media), "rb") as f:
    #             media_response = self.client.post(f'{GLOBAL_MEDIA_FRONTEND_URL}/upload-media', files={"media": f})
    #         if media_response.ok:
    #             media_json = json.loads(media_response.text)
    #             media_id = f'"{media_json["media_id"]}"'
    #             media_type = f'"{media_json["media_type"]}"'
    #
    #     headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #     data = {
    #         'username': 'username_' + str(self.user_id),
    #         'user_id': str(self.user_id),
    #         'text': text,
    #         'media_ids': f"[{media_id}]",
    #         'media_types': f"[{media_type}]",
    #         'post_type': '0'
    #     }
    #
    #     response = self.client.post("/wrk2-api/post/compose", data=data, headers=headers)
    #     self.log_statistics(response)

    @task
    def readHomeTimeline(self):
        start = random.randint(0, 100)
        stop = start + 10
        response = self.client.get(f"/wrk2-api/home-timeline/read?start={start}&stop={stop}&user_id={self.user_id}")
        self.log_statistics(response)

    # @task
    # def readUserTimeline(self):
    #     start = random.randint(0, 100)
    #     stop = start + 10
    #     user_id = random.choice(friends[self.user_id])
    #     response = self.client.get(f"/wrk2-api/user-timeline/read?start={start}&stop={stop}&user_id={user_id}")
    #     self.log_statistics(response)

    # def log_statistics(self, response):
    #     # Utiliser le target_time du LoadShape
    #     target_time = self.environment.shape.current_target_time
    #     load_intensity = self.get_current_user_count
    #     successful_transactions = 1 if response.ok else 0
    #     failed_transactions = 0 if response.ok else 1
    #     avg_response_time = response.elapsed.total_seconds() * 1000  # en ms
    #
    #     with open(self.csv_file, "a", newline="") as csvfile:
    #         writer = csv.writer(csvfile)
    #         writer.writerow([
    #             target_time,
    #             load_intensity,  # Load Intensity (à ajuster selon votre scénario)
    #             successful_transactions,
    #             failed_transactions,
    #             0,  # Dropped Transactions (pas supporté directement par Locust)
    #             avg_response_time,
    #             0  # Final Batch Dispatch Time (à ajuster si nécessaire)
    #         ])

    def log_statistics(self, response):
        # Vérifier si la réponse a réussi
        if response.ok:
            SocialNetworkUser.total_successful_transactions += 1
        else:
            SocialNetworkUser.total_failed_transactions += 1

    def on_stop(self):
        active_users.remove(self.user_id)
        inactive_users.append(self.user_id)

# Hook pour compter les requêtes
@events.request.add_listener
def count_requests(request_type, name, response_time, response_length, exception, **kwargs):
    if exception is None:
        SocialNetworkUser.total_successful_transactions += 1
    else:
        SocialNetworkUser.total_failed_transactions += 1

# Écrire les résultats dans le CSV après chaque intervalle
def write_results_to_csv():
    with open(f"custom_stats.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            LoadShape.current_target_time,
            LoadShape.get_current_user_count(),
            SocialNetworkUser.total_successful_transactions,
            SocialNetworkUser.total_failed_transactions,
            0,  # Dropped Transactions, à ajuster selon la logique
            0,  # Avg Response Time, à ajuster selon la logique
            0   # Final Batch Dispatch Time, à ajuster selon la logique
        ])

@events.test_stop.add_listener
def on_test_stop(**kwargs):
    write_results_to_csv()