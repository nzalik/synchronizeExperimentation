import csv
import os
import sys

from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape
import random
from random import randint, choice
import base64
#from atomic_queries import _query_advanced_ticket, _login
import time
# from query_advanced_ticket import kk
import json
from typing import List
import random
from typing import List
import string
import logging
import random
import time


state_data = []
GLOBAL_MIN_USERS           = 10
GLOBAL_INTENSITY_FILE      = os.environ.get("INTENSITY_FILE")

HOST_URL = sys.argv[1]


class CustomLoadShape(LoadTestShape):
    host = HOST_URL
    row_offset = 0

    def tick(self):
        global cycle
        # if cycle == -1:
        #    return None

        user_count = GLOBAL_MIN_USERS
        csv_list = []
        try:
            with open(GLOBAL_INTENSITY_FILE) as intensity_csv:
                csv_reader = csv.reader(intensity_csv, delimiter=',')
                csv_list = list(csv_reader)

            if self.row_offset < len(csv_list):
                user_count = int(csv_list[self.row_offset][1])
                self.row_offset += 1
            else:
                return None

            spawn_rate = max(1, abs(user_count - self.get_current_user_count()))  # should not be 0
            return user_count, spawn_rate
        except FileNotFoundError:
            logging.error(f"Could not find intensity file: {GLOBAL_INTENSITY_FILE}")
            return None

class TrainTicketUserTasks(TaskSet):
    @task
    def home(self):
        start_time = time.time()
        response = self.client.get('/index.html')
        response_time = time.time() - start_time
        print({
            'url': '/index.html',
            'status_code': response.status_code,
            'response_time': response_time
        })


class WebsiteUser(HttpUser):
    host = HOST_URL
    wait_time = constant(1)  # Temps d'attente entre les tâches
    tasks = [TrainTicketUserTasks]