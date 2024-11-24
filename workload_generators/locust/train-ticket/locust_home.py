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
    def __init__(self, parent):
        super().__init__(parent)


    def query_min_station(self,date="2021-12-31", headers: dict = {}):
        url = f"/api/v1/travelplanservice/travelPlan/minStation"

        payload = {
            "departureTime": date,
            "endPlace": "Shang Hai",
            "startingPlace": "Nan Jing"
        }

        r = self.client.post(url=url, json=payload, headers=headers)
        if r.status_code == 200:
            print("query min station success")
        else:
            print("query min station failed")


    def query_quickest(self,date="2021-12-31", headers: dict = {}):
        url = f"/api/v1/travelplanservice/travelPlan/quickest"

        payload = {
            "departureTime": date,
            "endPlace": "Shang Hai",
            "startingPlace": "Nan Jing"
        }

        r = self.client.post(url=url, json=payload, headers=headers)
        if r.status_code == 200:
            print("query quickest success")
        else:
            print("query quickest failed")


    def query_admin_basic_price(self,headers: dict = {}):
        url = f"/api/v1/adminbasicservice/adminbasic/prices"
        response = self.client.get(url=url,
                                headers=headers)
        if response.status_code == 200:
            print(f"price success")
            return response
        else:
            print(f"price failed")
            return None


    def rebook_ticket(self,old_order_id, old_trip_id, new_trip_id, new_date, new_seat_type, headers):
        url = f"/api/v1/rebookservice/rebook"

        payload = {
            "oldTripId": old_trip_id,
            "orderId": old_order_id,
            "tripId": new_trip_id,
            "date": new_date,
            "seatType": new_seat_type
        }
        print(payload)
        r = self.client.post(url=url, json=payload, headers=headers)
        if r.status_code == 200:
            print(r.text)
        else:
            print(f"Request Failed: status code: {r.status_code}")
            print(r.text)


    def query_admin_travel(self,headers):
        url = f"/api/v1/admintravelservice/admintravel"

        r = self.client.get(url=url, headers=headers)
        if r.status_code == 200 and r.json()["status"] == 1:
            print("success to query admin travel")
        else:
            print(f"faild to query admin travel with status_code: {r.status_code}")

    def query_one_and_cancel(self,headers, uuid="4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"):
        """
        查询order并取消order
        :param uuid:
        :param headers:
        :return:
        """
        pairs = self.query_orders(headers=headers, types=tuple([0]))
        pairs2 = self.query_orders(headers=headers, types=tuple([0]), query_other=True)

        if not pairs and not pairs2:
            return

        pairs = pairs + pairs2

        # (orderId, tripId) pair
        pair = self.random_from_list(pairs)
        print(pair[0])
        print("...............................")
        order_id =self.cancel_one_order(order_id=pair[0], uuid=self.uuid, headers=headers)
        if not order_id:
            return

        print(f"{order_id} queried and canceled")

    def query_and_collect_ticket(self,headers):

        pairs = self.query_orders(headers=headers, types=tuple([0]))
        pairs2 = self.query_orders(headers=headers, types=tuple([0]), query_other=True)

        if not pairs and not pairs2:
            return

        pairs = pairs + pairs2

        # (orderId, tripId)
        pair = self.random_from_list(pairs)

        order_id = self.collect_one_order(order_id=pair[0], headers=headers)
        if not order_id:
            return

        print(f"{order_id} queried and collected")

    def query_and_enter_station(self,headers):
        pairs = self.query_orders(headers=headers, types=tuple([0]))
        pairs2 = self.query_orders(headers=headers, types=tuple([0]), query_other=True)

        if not pairs and not pairs2:
            return

        pairs = pairs + pairs2

        # (orderId, tripId)
        pair = self.random_from_list(pairs)

        order_id = self.enter_station(order_id=pair[0], headers=headers)
        if not order_id:
            return

        print(f"{order_id} queried and entered station")

    def query_one_and_put_consign(self,headers, pairs):
        """
        查询order并put consign
        :param uuid:
        :param headers:
        :return:
        """

        pair = self.random_from_list(pairs)

        order_id = self.put_consign(result=pair, headers=headers)
        if not order_id:
            return

        print(f"{order_id} queried and put consign")

    def query_and_rebook(self,headers):

        pairs = self.query_orders(headers=headers, types=tuple([0]))
        print(pairs)
        pairs2 = self.query_orders(headers=headers, types=tuple([1]), query_other=True)

        if not pairs and not pairs2:
            return

        pairs = pairs + pairs2

        # (orderId, tripId)
        pair = self.random_from_list(pairs)
        new_trip_id = "D1345"
        new_date = time.strftime("%Y-%m-%d", time.localtime())
        new_seat_type = "3"

        for pair in pairs:
            #print(pair)
            self.rebook_ticket(old_order_id=pair[0], old_trip_id=pair[1], new_trip_id=new_trip_id, new_date=new_date, new_seat_type=new_seat_type, headers=headers)

    def query_order_and_pay(self,headers, pairs):
        """
        查询Order并付款未付款Order
        :return:
        """

        # (orderId, tripId) pair
        pair = self.random_from_list(pairs)

        order_id = self.pay_one_order(pair[0], pair[1], headers=headers)
        if not order_id:
            return

        print(f"{order_id} queried and paid")

    def query_travel_left_parallel(self,headers):
        """
        1. 查票（随机高铁或普通）
        2. 查保险、Food、Contacts
        3. 随机选择Contacts、保险、是否买食物、是否托运
        4. 买票
        :return:
        """
        start = ""
        end = ""
        trip_ids = []
        PRESERVE_URL = ""

        start = "Su Zhou"
        end = "Shang Hai"
        high_speed_place_pair = (start, end)
        trip_ids = self.query_high_speed_ticket_parallel(place_pair=high_speed_place_pair, headers=headers, time=time.strftime("%Y-%m-%d", time.localtime()))

    def query_travel_left(self,headers):
        """
        1. 查票（随机高铁或普通）
        2. 查保险、Food、Contacts
        3. 随机选择Contacts、保险、是否买食物、是否托运
        4. 买票
        :return:
        """
        start = ""
        end = ""
        trip_ids = []
        PRESERVE_URL = ""

        high_speed = False
        if high_speed:
            start = "Shang Hai"
            end = "Su Zhou"
            high_speed_place_pair = (start, end)
            trip_ids = self.query_high_speed_ticket(place_pair=high_speed_place_pair, headers=headers, time=time.strftime("%Y-%m-%d", time.localtime()))
        else:
            start = "Shang Hai"
            end = "Nan Jing"
            other_place_pair = (start, end)
            trip_ids = self.query_normal_ticket(place_pair=other_place_pair, headers=headers, time=time.strftime("%Y-%m-%d", time.localtime()))

class WebsiteUser(HttpUser):
    def on_start(self):
        return super().on_start()

    def on_stop(self):
        return super().on_stop()

    host = HOST_URL
    wait_time = constant(1)
    tasks = [TrainTicketUserTasks]
    #tasks = [BoutiqueUserTasks]
    # tasks = [SockShopUserTasks]