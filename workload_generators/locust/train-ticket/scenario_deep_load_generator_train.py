import csv
import os
import sys
import logging
import random
import time
import requests
import json
from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape

# Variables globales
GLOBAL_MIN_USERS = 10
GLOBAL_INTENSITY_FILE = os.environ.get("INTENSITY_FILE")
GLOBAL_TASK = os.environ.get("TASK")
HOST_URL = sys.argv[1]


# Classe utilitaire pour fonctions communes
class Utils:
    @staticmethod
    def home(client):
        print("--------------index------------")
        start_time = time.time()
        response = client.get('/index.html')
        response_time = time.time() - start_time
        print({
            'url': '/index.html',
            'status_code': response.status_code,
            'response_time': response_time
        })

    @staticmethod
    def login(client):
        username = "fdse_microservice"
        password = "111111"
        url = "/api/v1/users/login"
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Content-Type': 'application/json',
        }
        data = f'{{"username":"{username}","password":"{password}"}}'
        response = client.post(url, headers=headers, data=data, verify=False)
        print(response)
        if response.status_code == 200:
            data = response.json().get("data", {})
            return data.get("userId"), data.get("token")
        return None, None

    @staticmethod
    def query_advanced_ticket_use(client, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        place_pairs = [("Shang Hai", "Su Zhou"), ("Su Zhou", "Shang Hai"), ("Nan Jing", "Shang Hai")]
        url = "/api/v1/travelplanservice/travelPlan/quickest"
        place_pair = random.choice(place_pairs)

        payload = {
            "departureTime": time.strftime("%Y-%m-%d", time.localtime()),
            "startingPlace": place_pair[0],
            "endPlace": place_pair[1],
        }
        client.post(url, headers=headers, json=payload)

    @staticmethod
    def search_ticket(self, departure_date, from_station, to_station, expected=True):
        head = {"Accept": "application/json",
                "Content-Type": "application/json"}
        body_start = {
            "startingPlace": from_station,
            "endPlace": to_station,
            "departureTime": departure_date
        }

        response = requests.post(
            url=self.host + "/api/v1/travelservice/trips/left",
            headers=head,
            json=body_start)
        if not response.json()["data"]:
            print("travel 2 service")
            response = requests.post(
                url=self.host + "/api/v1/travel2service/trips/left",
                headers=head,
                json=body_start)
        print(json.dumps(response.json()))
        for res in response.json()["data"]:
            self.trip_id = res["tripId"]["type"] + res["tripId"]["number"]
            self.start_station = res["startingStation"]
            self.terminal_station = res["terminalStation"]

    @staticmethod
    def navigate_to_client_login(client):
        print("--------------index------------")
        start_time = time.time()
        response = client.get('/client_login.html')
        response_time = time.time() - start_time
        print({
            'url': '/client_login.html',
            'status_code': response.status_code,
            'response_time': response_time
        })

    @staticmethod
    def query_cheapest(self,date="2021-12-31", headers: dict = {}):
        url = f"/api/v1/travelplanservice/travelPlan/cheapest"

        payload = {
            "departureTime": date,
            "endPlace": "Shang Hai",
            "startingPlace": "Nan Jing"
        }

        r = self.client.post(url=url, json=payload, headers=headers)
        if r.status_code == 200:
            print("query cheapest success")
        else:
            print("query cheapest failed")

    @staticmethod
    def start_booking(self, from_station, expected=True):
        departure_date = "2021-04-21"
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response = requests.get(
            url=self.host + "/client_ticket_book.html?tripId=" + self.trip_id + "&from=" + self.start_station + "&to=" + self.terminal_station + "&seatType=2&seat_price=50.0"
                                                                                                                                                 "&date=" + departure_date,
            headers=head)
        print(response)

    @staticmethod
    def select_contact(self, expected=True):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        response_contacts = requests.get(
            url=self.host + "/api/v1/contactservice/contacts/account/" + self.user_id,
            headers=head)
        print(response_contacts.json())
        response_as_json_contacts = response_contacts.json()["data"]
        print(json.dumps(response_as_json_contacts))
        if len(response_as_json_contacts) == 0:
            response_contacts = requests.post(
                url=self.host + "/api/v1/contactservice/contacts",
                headers=head,
                json={
                    "name": self.user_id, "accountId": self.user_id, "documentType": "1",
                    "documentNumber": self.user_id, "phoneNumber": "123456"})

            response_as_json_contacts = response_contacts.json()["data"]
            # print(response_as_json_contacts)
            self.contactid = response_as_json_contacts["id"]
        else:
            self.contactid = response_as_json_contacts[0]["id"]

        print(self.contactid)

    @staticmethod
    def seat_service(self, departure):
        departure_date = departure
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        seat_select = {
            "date": departure_date,
            "from": self.start_station,
            "to": self.terminal_station
        }
        response = requests.post(
            url=self.host + "/api/v1/seatservice/seats",
            headers=head,
            json=seat_select)
        print(response.text)
        print(response.status_code)

    @staticmethod
    def finish_booking(self, dep):
        departure_date = dep
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        body_for_reservation = {
            "accountId": self.user_id,
            "contactsId": self.contactid,
            "tripId": self.trip_id,
            "seatType": "2",
            "date": departure_date,
            "from": self.start_station,
            "to": self.terminal_station,
            "assurance": "0",
            "foodType": 1,
            "foodName": "Bone Soup",
            "foodPrice": 2.5,
            "stationName": "",
            "storeName": ""
        }
        start_time = time.time()
        response = requests.post(
            url=self.host + "/api/v1/preserveservice/preserve",
            headers=head,
            json=body_for_reservation)
        print(response.text)
        print(response.status_code)

    @staticmethod
    def select_order(self):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response_order_refresh = requests.post(
            url=self.host + "/api/v1/orderservice/order/refresh",
            headers=head,
            json={
                "loginId": self.user_id, "enableStateQuery": "false", "enableTravelDateQuery": "false",
                "enableBoughtDateQuery": "false", "travelDateStart": "null", "travelDateEnd": "null",
                "boughtDateStart": "null", "boughtDateEnd": "null"})

        response_as_json = response_order_refresh.json()["data"]
        print(response_as_json)
        # print(json.dumps(response_order_refresh.json()))
        for orders in response_as_json:
            if orders["status"] == 1:
                self.paid_orderid = orders["id"]
                break
        for orders in response_as_json:
            if orders["status"] == 0:
                self.orderid = orders["id"]

    @staticmethod
    def pay(self):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response = requests.post(
            url=self.host + "/api/v1/inside_pay_service/inside_payment",
            headers=head,
            json={"orderId": self.orderid, "tripId": "D1345"})
        print(response.text)

    @staticmethod
    def collect_ticket(self):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        collect_ticket = requests.get(
            url=self.host + "/api/v1/executeservice/execute/collected/" + self.paid_orderid,
            headers=head)
        print(collect_ticket.text)

    @staticmethod
    def enter_station(self):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        enter_station = requests.get(
            url=self.host + "/api/v1/executeservice/execute/execute/" + self.paid_orderid,
            headers=head)
        print(enter_station.text)

# Classe pour personnaliser la charge
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


class HomePage(TaskSet):
    @task
    def load(self):
        Utils.home(self.client)
        Utils.navigate_to_client_login(self.client)
        _, token = Utils.login(self.client)
        print("the current token")
        print(token)
        if token:
            Utils.query_advanced_ticket_use(self.client, token)

# class BrowseTicketPay(TaskSet):
#     @task
#     def load(self):
#         Utils.home(self.client)
#         Utils.navigate_to_client_login(self.client)
#         _, token = Utils.login(self.client)
#         Utils.search_ticket()
#         Utils.query_cheapest()
#         Utils.start_booking()
#         Utils.select_contact()
#         Utils.seat_service()
#         Utils.pay()
#         Utils.finish_booking()
#         Utils.collect_ticket()
#         Utils.enter_station()
#
# class OrderAndCancel:
#     @task
#     def load(self):
#         Utils.home(self.client)
#         Utils.navigate_to_client_login(self.client)
#         _, token = Utils.login(self.client)
#
#
#
# class UserBooking(HttpUser):
#     host = HOST_URL
#     wait_time = constant(1)
#     highspeed_weights = {True: 60, False: 40}
#
#     # Associer les tâches dynamiques
#     def on_start(self):
#         task_mapping = {
#             "HomePage": HomePage,
#         }
#         self.tasks = [task_mapping.get(GLOBAL_TASK, HomePage)]  # Par défaut HomePage si non défini
