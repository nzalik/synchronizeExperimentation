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
        q = Query()
        if random_from_weighted(self.user.highspeed_weights):
            pairs = q.query_orders(types=tuple([0, 1]))
        else:
            pairs = q.query_orders(types=tuple([0, 1]), query_other=True)

        if not pairs:
            return

        pair = random_from_list(pairs)
        q.cancel_order(order_id=pair[0])

    @task
    def query_and_collect(self):
        q = Query()
        if random_from_weighted(self.user.highspeed_weights):
            pairs = q.query_orders(types=tuple([1]))
        else:
            pairs = q.query_orders(types=tuple([1]), query_other=True)

        if not pairs:
            return

        pair = random_from_list(pairs)
        q.collect_order(order_id=pair[0])

    @task
    def query_and_execute(self):
        q = Query()
        if random_from_weighted(self.user.highspeed_weights):
            pairs = q.query_orders(types=tuple([1]))
        else:
            pairs = q.query_orders(types=tuple([1]), query_other=True)

        if not pairs:
            return

        pair = random_from_list(pairs)
        q.enter_station(order_id=pair[0])

    @task
    def query_and_preserve(self):
        q = Query()
        high_speed = random_from_weighted(self.user.highspeed_weights)
        if high_speed:
            start = "Shang Hai"
            end = "Su Zhou"
            high_speed_place_pair = (start, end)
            trip_ids = q.query_high_speed_ticket(place_pair=high_speed_place_pair)
        else:
            start = "Shang Hai"
            end = "Nan Jing"
            other_place_pair = (start, end)
            trip_ids = q.query_normal_ticket(place_pair=other_place_pair)

        q.query_assurances()
        q.preserve(start, end, trip_ids, high_speed)

    @task
    def query_and_consign(self):
        q = Query()
        if random_from_weighted(self.user.highspeed_weights):
            orders_info = q.query_orders_all_info()
        else:
            orders_info = q.query_orders_all_info(query_other=True)

        if not orders_info:
            return

        res = random_from_list(orders_info)
        q.put_consign(res)

    @task
    def query_and_pay(self):
        q = Query()
        if random_from_weighted(self.user.highspeed_weights):
            pairs = q.query_orders(types=tuple([0, 1]))
        else:
            pairs = q.query_orders(types=tuple([0, 1]), query_other=True)

        if not pairs:
            return

        pair = random_from_list(pairs)
        q.pay_order(pair[0], pair[1])

    @task
    def query_and_rebook(self):
        q = Query()
        if random_from_weighted(self.user.highspeed_weights):
            pairs = q.query_orders(types=tuple([0, 1]))
        else:
            pairs = q.query_orders(types=tuple([0, 1]), query_other=True)

        if not pairs:
            return

        pair = random_from_list(pairs)
        q.cancel_order(order_id=pair[0])
        q.rebook_ticket(pair[0], pair[1], pair[1])


class UserBooking(HttpUser):
    tasks = [UserBehavior]
    host = HOST_URL
    wait_time = constant(1)
    highspeed_weights = {True: 60, False: 40}
