from queries import Query
from utilities import *
import logging
import csv
import os
import sys

from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape
import random
import time

state_data = []
GLOBAL_MIN_USERS = 10
GLOBAL_INTENSITY_FILE = os.environ.get("INTENSITY_FILE")
GLOBAL_TASK = os.environ.get("TASK")

print("la tache courante")
print(GLOBAL_TASK)

HOST_URL = sys.argv[1]


class CustomLoadShape(LoadTestShape):
    host = HOST_URL
    row_offset = 0

    def tick(self):
        user_count = GLOBAL_MIN_USERS
        try:
            with open(GLOBAL_INTENSITY_FILE) as intensity_csv:
                csv_reader = csv.reader(intensity_csv, delimiter=',')
                csv_list = list(csv_reader)

            if self.row_offset < len(csv_list):
                user_count = int(csv_list[self.row_offset][1])
                self.row_offset += 1
            else:
                return None

            spawn_rate = max(1, abs(user_count - self.get_current_user_count()))
            return user_count, spawn_rate
        except FileNotFoundError:
            logging.error(f"Could not find intensity file: {GLOBAL_INTENSITY_FILE}")
            return None


class UserBehavior(TaskSet):
    @task
    def query_and_cancel(self):
        print("################home########################")
        q = Query()
        if random_from_weighted(self.user.highspeed_weights):
            pairs = q.query_orders(types=tuple([0, 1]))
        else:
            pairs = q.query_orders(types=tuple([0, 1]), query_other=True)

        if not pairs:
            return

        pair = random_from_list(pairs)
        q.cancel_order(order_id=pair[0])


class QueryCollect(TaskSet):
    @task
    def query_and_collect(self):
        print("***************collect***************")
        q = Query()
        if random_from_weighted(self.user.highspeed_weights):
            pairs = q.query_orders(types=tuple([1]))
        else:
            pairs = q.query_orders(types=tuple([1]), query_other=True)

        if not pairs:
            return

        pair = random_from_list(pairs)
        q.collect_order(order_id=pair[0])


class TrainTicketUserTasks(TaskSet):
    @task
    def home(self):
        print("--------------index------------")
        start_time = time.time()
        response = self.client.get('/index.html')
        response_time = time.time() - start_time
        print({
            'url': '/index.html',
            'status_code': response.status_code,
            'response_time': response_time
        })


class UserBooking(HttpUser):
    tasks = [GLOBAL_TASK]
    host = HOST_URL
    wait_time = constant(1)
    highspeed_weights = {True: 60, False: 40}
