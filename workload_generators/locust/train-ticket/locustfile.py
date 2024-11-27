import csv
import json
import logging
import os
import random
import string
import sys
import time
from datetime import datetime
from random import randint
import requests

import locust
import numpy as np
from locust import events
from locust import task, constant, HttpUser
from locust.env import Environment
from requests.adapters import HTTPAdapter
from test_data import USER_CREDETIALS, TRIP_DATA, TRAVEL_DATES

VERBOSE_LOGGING = 0  # ${LOCUST_VERBOSE_LOGGING}
# stat_file = open("output/requests_stats_u50_5.csv", "w")
state_data = []


def random_string_generator():
    len = randint(8, 16)
    prob = randint(0, 100)
    if prob < 25:
        random_string = ''.join([random.choice(string.ascii_letters) for n in range(len)])
    elif prob < 50:
        random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(len)])
    elif prob < 75:
        random_string = ''.join(
            [random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(len)])
    else:
        random_string = ''
    return random_string


def random_date_generator():
    temp = randint(0, 4)
    random_y = 2000 + temp * 10 + randint(0, 9)
    random_m = randint(1, 12)
    random_d = randint(1, 31)  # assumendo che la data possa essere non sensata (e.g. 30 Febbraio)
    return str(random_y) + '-' + str(random_m) + '-' + str(random_d)


def postfix(expected=True):
    if expected:
        return '_expected'
    return '_unexpected'


class Requests:

    def __init__(self, client):
        self.client = client
        dir_path = os.path.dirname(os.path.realpath(__file__))
        handler = logging.FileHandler(os.path.join(dir_path, "locustfile_debug.log"))
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        user = random.choice(USER_CREDETIALS)
        self.user_name = user
        self.password = user
        #self.trip_detail = random.choice(TRIP_DATA)
        self.trip_detail = {}
        self.contact = {}
        self.food_detail = {}
        self.assurance = {}
        self.contactid = ""
        self.departure_date = random.choice(TRAVEL_DATES)
        #self.user_name = "fdse_microservice"
        #self.password = "111111"

        if VERBOSE_LOGGING == 1:
            logger = logging.getLogger("Debugging logger")
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)
            self.debugging_logger = logger
        else:
            self.debugging_logger = None
        logging.basicConfig(level=logging.DEBUG)

    def log_verbose(self, to_log):
        if self.debugging_logger is not None:
            self.debugging_logger.debug(json.dumps(to_log))
        print("Logging:", to_log)

    def home(self, expected):
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        with self.client.get('/index.html', name=req_label) as response:
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time}
            self.log_verbose(to_log)

    def try_to_read_response_as_json(self, response):
        try:
            return response.json()
        except:
            try:
                return response.content.decode('utf-8')
            except:
                return response.content

    def search_ticket(self, expected):
        logging.debug("search ticket")
        # stations = ["Shang Hai", "Tai Yuan", "Nan Jing", "Wu Xi", "Su Zhou", "Shang Hai Hong Qiao", "Bei Jing",
        #             "Shi Jia Zhuang", "Xu Zhou", "Ji Nan", "Hang Zhou", "Jia Xing Nan", "Zhen Jiang"]
        stations = ["shanghai", "suzhou", "jinan"]
        #from_station, to_station = random.sample(stations, 2)
        from_station = "shanghai"
        to_station = "suzhou"
        # from_station = from_station.lower().replace(" ", "")
        # to_station = to_station.lower().replace(" ", "")
        departure_date = self.departure_date
        head = {"Accept": "application/json",
                "Content-Type": "application/json"}
        body_start = {
            "startingPlace": from_station,
            "endPlace": to_station,
           # "departureTime": departure_date
        }
        print(body_start)
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()

        response = self.client.post(
            url="/api/v1/travelservice/trips/left",
            headers=head,
            json=body_start,
            name=req_label)
        quickest_trip = self._query_quickest()

        if response.status_code is 200 :
            if response.json()["data"]:
                self.trip_detail = response.json()["data"][0]
                print("*********the output*********")
                print(response.json()["data"][0])
            if not response.json()["data"]:
                response = self.client.post(
                    url="/api/v1/travel2service/trips/left",
                    headers=head,
                    json=body_start,
                    name=req_label)
        else:
            response = quickest_trip
            self.trip_detail = quickest_trip
        to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                  'response_time': time.time() - start_time,
                  'response': self.try_to_read_response_as_json(response)}
        self.log_verbose(to_log)


    def _query_quickest(self, date="2021-12-31", headers: dict = {}, expected=True):
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        #url = f"{base_address}/api/v1/travelplanservice/travelPlan/quickest"
        print("On est dans la fontion quickest")

        payload = {
            "startingPlace": "Nan Jing",
            "endPlace": "Shang Hai",
            "departureTime": "2024-11-27"
        }

        r = self.client.post(
            url="/api/v1/travelplanservice/travelPlan/quickest",
            headers=headers,
            json=payload,
            name=req_label)

        #r = requests.post(url=url, json=payload, headers=headers)
        print(r.content)
        if r.status_code == 200:
            print("query quickest success")
        else:
            print("query quickest failed")

        return r.json()["data"][0]

    def _create_user(self, expected):

        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        document_num = random.randint(1, 5)  # added by me
        with self.client.post(url="/api/v1/adminuserservice/users",
                              headers={
                                  "Authorization": self.bearer, "Accept": "application/json",
                                  "Content-Type": "application/json"},
                              json={"documentNum": document_num, "documentType": 0, "email": "string", "gender": 0,
                                    "password": self.user_name, "userName": self.user_name},
                              name=req_label) as response2:
            to_log = {'name': req_label, 'expected': expected, 'status_code': response2.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response2)}
            self.log_verbose(to_log)

    def register(self, expected):
            req_label = sys._getframe().f_code.co_name + postfix(expected)
            start_time = time.time()
            document_num = random.randint(1, 5)  # added by me
            user = {
                #"userId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
                "userName": self.user_name,
                "password": self.user_name,
                "gender": 1,
                "documentType": 1,
                "documentNum": "2135488099312X",
                "email": "nzalikyannick01@gmail.com"
                }

            with self.client.post(url="/api/v1/userservice/users/register",
                                  headers={
                                      "Accept": "application/json",
                                      "Content-Type": "application/json"},
                                  json=user, name=req_label) as response2:
                print(response2.content)
                to_log = {'name': req_label, 'expected': expected, 'status_code': response2.status_code,
                          'response_time': time.time() - start_time,
                          'response': self.try_to_read_response_as_json(response2)}
                self.log_verbose(to_log)

    def _navigate_to_client_login(self, expected=True):
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        with self.client.get('/client_login.html', name=req_label) as response:
            to_log = {'name': req_label, 'expected': True, 'status_code': response.status_code,
                      'response_time': time.time() - start_time}
            self.log_verbose(to_log)

    def login(self, expected):
        # self._create_user(True)
        # self._navigate_to_client_login()
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        head = {"Accept": "application/json",
                "Content-Type": "application/json"}
        if expected:
            response = self.client.post(url="/api/v1/users/login",
                                        headers=head,
                                        json={
                                            "username": self.user_name,
                                            "password": self.password
                                        }, name=req_label)
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response)}
            self.log_verbose(to_log)
        else:
            response = self.client.post(url="/api/v1/users/login",
                                        headers=head,
                                        json={
                                            "username": self.user_name,
                                            # wrong password
                                            "password": random_string_generator()
                                        }, name=req_label)
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response)}
            self.log_verbose(to_log)

        print("####################################################################")
        print(json.dumps(response.json(), indent=4))
        print("####################################################################")
        response_as_json = response.json()["data"]
        if response_as_json is not None:
            token = response_as_json["token"]
            self.bearer = "Bearer " + token
            self.user_id = response_as_json["userId"]

    # purchase ticket

    #Go the the booking page with information about the trip
    def start_booking(self, expected):
        departure_date = self.departure_date
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        print("########tets################")
        print(self.trip_detail)
        with self.client.get(
                url="/client_ticket_book.html?tripId=" + self.trip_detail["tripId"]["type"] + self.trip_detail["tripId"]["number"] + "&from=" + self.trip_detail[
                    "startingStation"] +
                    "&to=" + self.trip_detail["terminalStation"] + "&seatType=" + "2" + "&seat_price=" +
                    self.trip_detail["priceForConfortClass"] +
                    "&date=" + departure_date,
                headers=head,
                name=req_label) as response:
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time}
            self.log_verbose(to_log)

    def get_assurance_types(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        with self.client.get(
                url="/api/v1/assuranceservice/assurances/types",
                headers=head,
                name=req_label) as response:
            self.assurance = response.json()["data"][0]
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response)}
            self.log_verbose(to_log)

    def get_foods(self, expected):
        departure_date = self.departure_date
        message = ""
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        with self.client.get(
                url="/api/v1/foodservice/foods/" + departure_date + "/" + self.trip_detail["startingStation"] + "/" +
                     self.trip_detail["priceForConfortClass"] + "/" + self.trip_detail["tripId"]["type"] + self.trip_detail["tripId"]["number"],
                headers=head,
                name=req_label) as response:
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print(response.json())
            if response.status_code is not 200 or response.json().get("data") is None:
                if response.json().get("data")["data"]["trainFoodList"] is None:
                    message = f"query food failed, response data is {response}"
                else:
                    resp_data = response.json()
                    if resp_data["data"]:
                        message = self.try_to_read_response_as_json(response)
                        if random.uniform(0, 1) <= 0.5:
                            self.food_detail = {"foodType": 2,
                                                "foodName": resp_data["data"]["trainFoodList"][0]["foodList"][0]["foodName"],
                                                "foodPrice": resp_data["data"]["trainFoodList"][0]["foodList"][0]["price"]}
                        else:
                            self.food_detail = {"foodType": 1,
                                                "foodName": resp_data["data"]["foodStoreListMap"][self.trip_detail["from"]][0][
                                                    "foodList"][0]["foodName"],
                                                "foodPrice": resp_data["data"]["foodStoreListMap"][self.trip_detail["from"]][0][
                                                    "foodList"][0]["price"]}
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time,
                      'response': message}
            self.log_verbose(to_log)

    def select_contact(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        response_contacts = self.client.get(
            url="/api/v1/contactservice/contacts/account/" + self.user_id,
            headers=head,
            name=req_label)
        to_log = {'name': req_label, 'expected': expected, 'status_code': response_contacts.status_code,
                  'response_time': time.time() - start_time,
                  'response': self.try_to_read_response_as_json(response_contacts)}
        self.log_verbose(to_log)

        response_as_json_contacts = response_contacts.json()["data"]

        if len(response_as_json_contacts) == 0:
            req_label = 'set_new_contact' + postfix(expected)
            response_contacts = self.client.post(
                url="/api/v1/contactservice/contacts",
                headers=head,
                json={
                    "name": self.user_id, "accountId": self.user_id, "documentType": "1",
                    "documentNumber": self.user_id, "phoneNumber": "123456"},
                name=req_label)

            response_as_json_contacts = response_contacts.json()["data"]
            self.contactid = response_as_json_contacts["id"]
        else:
            self.contactid = response_as_json_contacts[0]["id"]

    def finish_booking(self, expected):
        departure_date = self.departure_date
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        if (expected):
            body_for_reservation = {
                "accountId": self.user_id,
                "contactsId": self.contactid,
                "tripId": self.trip_detail["tripId"]["type"] + self.trip_detail["tripId"]["number"],
                "seatType": 2,
                "date": departure_date,
                "from": self.trip_detail["startingStation"],
                "to":  self.trip_detail["priceForConfortClass"],
                "assurance": "1",
                #"assurance": random.choice(["0", "1"]),
                "foodType": 1,
                "foodName": "Bone Soup",
                "foodPrice": 2.5,
                "stationName": "",
                "storeName": ""
            }
            if self.food_detail:
                body_for_reservation["foodType"] = self.food_detail["foodType"]
                body_for_reservation["foodName"] = self.food_detail["foodName"]
                body_for_reservation["foodPrice"] = self.food_detail["foodPrice"]
        else:
            body_for_reservation = {
                "accountId": self.user_id,
                "contactsId": self.contactid,
                "tripId": random_string_generator(),
                "seatType": "2",
                "date": departure_date,
                "from": "Shang Hai",
                "to": "Su Zhou",
                "assurance": "0",
                "foodType": 1,
                "foodName": "Bone Soup",
                "foodPrice": 2.5,
                "stationName": "",
                "storeName": ""
            }
        start_time = time.time()
        with self.client.post(
                url="/api/v1/preserveservice/preserve",
                headers=head,
                json=body_for_reservation,
                catch_response=True,
                name=req_label) as response:
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response)}
            self.log_verbose(to_log)

    def select_order(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        response_order_refresh = self.client.post(
            url="/api/v1/orderservice/order/refresh",
            name=req_label,
            headers=head,
            json={
                "loginId": self.user_id, "enableStateQuery": "false", "enableTravelDateQuery": "false",
                "enableBoughtDateQuery": "false", "travelDateStart": "null", "travelDateEnd": "null",
                "boughtDateStart": "null", "boughtDateEnd": "null"})

        to_log = {'name': req_label, 'expected': expected, 'status_code': response_order_refresh.status_code,
                  'response_time': time.time() - start_time,
                  'response': self.try_to_read_response_as_json(response_order_refresh)}
        self.log_verbose(to_log)

        response_as_json = response_order_refresh.json()["data"]
        if response_as_json:
            self.order_id = response_as_json[0]["id"]  # first order with paid or not paid
            self.paid_order_id = response_as_json[0]["id"]  # default first order with paid or unpaid.
        else:
            self.order_id = "sdasdasd"  # no orders, set a random number
            self.paid_order_id = "asdasdasn"
        # selecting order with payment status - not paid.
        for orders in response_as_json:
            if orders["status"] == 0:
                self.order_id = orders["id"]
                break
        for orders in response_as_json:
            if orders["status"] == 1:
                self.paid_order_id = orders["id"]
                break

    def pay(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        if not self.order_id:
            to_log = {'name': req_label, 'expected': expected, 'status_code': "N/A",
                      'response_time': time.time() - start_time,
                      'response': "Place an order first!"}
            self.log_verbose(to_log)
            return
        if (expected):
            with self.client.post(
                    url="/api/v1/inside_pay_service/inside_payment",
                    headers=head,
                    json={"orderId": self.order_id, "tripId": "D1345"},
                    name=req_label) as response:
                to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                          'response_time': time.time() - start_time,
                          'response': self.try_to_read_response_as_json(response)}
                self.log_verbose(to_log)
        else:
            with self.client.post(
                    url="/api/v1/inside_pay_service/inside_payment",
                    headers=head,
                    json={"orderId": random_string_generator(), "tripId": "D1345"},
                    name=req_label) as response:
                to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                          'response_time': time.time() - start_time,
                          'response': self.try_to_read_response_as_json(response)}
                self.log_verbose(to_log)

    # cancelNoRefund

    def cancel_with_no_refund(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        if (expected):
            with self.client.get(
                    url="/api/v1/cancelservice/cancel/" + self.order_id + "/" + self.user_id,
                    headers=head,
                    name=req_label) as response:
                to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                          'response_time': time.time() - start_time,
                          'response': self.try_to_read_response_as_json(response)}
                self.log_verbose(to_log)

        else:
            with self.client.get(
                    url="/api/v1/cancelservice/cancel/" + self.order_id + "/" + random_string_generator(),
                    headers=head,
                    name=req_label) as response:
                to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                          'response_time': time.time() - start_time,
                          'response': self.try_to_read_response_as_json(response)}
                self.log_verbose(to_log)

    # user refund with voucher

    def get_voucher(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        if (expected):
            with self.client.post(
                    url="/getVoucher",
                    headers=head,
                    json={"orderId": self.order_id, "type": 1},
                    name=req_label) as response:
                to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                          'response_time': time.time() - start_time,
                          'response': self.try_to_read_response_as_json(response)}
                self.log_verbose(to_log)

        else:
            with self.client.post(
                    url="/getVoucher",
                    headers=head,
                    json={"orderId": random_string_generator(), "type": 1},
                    name=req_label) as response:
                to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                          'response_time': time.time() - start_time}
                self.log_verbose(to_log)

    # consign ticket

    def get_consigns(self, expected):
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        with self.client.get(
                url="/api/v1/consignservice/consigns/order/" + self.order_id,
                headers=head,
                name=req_label) as response:
            to_log = {'name': req_label, 'expected': expected, 'status_code': response.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response)}
            self.log_verbose(to_log)

    def confirm_consign(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        if (expected):
            response_as_json_consign = self.client.put(
                url="/api/v1/consignservice/consigns",
                name=req_label,
                json={
                    "accountId": self.user_id,
                    "handleDate": self.departure_date,
                    "from": self.trip_detail["startingStation"],
                    "to":  self.trip_detail["priceForConfortClass"],
                    "orderId": self.order_id,
                    "consignee": self.order_id,
                    "phone": ''.join([random.choice(string.digits) for n in range(8)]),
                    "weight": "1",
                    "id": "",
                    "isWithin": "false"},
                headers=head)
            to_log = {'name': req_label, 'expected': expected, 'status_code': response_as_json_consign.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response_as_json_consign)}
            self.log_verbose(to_log)
        else:
            response_as_json_consign = self.client.put(
                url="/api/v1/consignservice/consigns",
                name=req_label,
                json={
                    "accountId": self.user_id,
                    "handleDate": self.departure_date,
                    "from": "Shang Hai",
                    "to": "Su Zhou",
                    "orderId": self.order_id,
                    "consignee": random_string_generator(),
                    "phone": random_string_generator(),
                    "weight": "1",
                    "id": "",
                    "isWithin": "false"}, headers=head)
            to_log = {'name': req_label, 'expected': expected, 'status_code': response_as_json_consign.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response_as_json_consign)}
            self.log_verbose(to_log)

    def collect_ticket(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        if expected:
            response_as_json_collect_ticket = self.client.get(
                url="/api/v1/executeservice/execute/collected/" + self.paid_order_id,
                name=req_label,
                headers=head)
            to_log = {'name': req_label, 'expected': expected,
                      'status_code': response_as_json_collect_ticket.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response_as_json_collect_ticket)}
            self.log_verbose(to_log)

    def enter_station(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name + postfix(expected)
        start_time = time.time()
        if expected:
            response_as_json_enter_station = self.client.get(
                url="/api/v1/executeservice/execute/execute/" + self.paid_order_id,
                name=req_label,
                headers=head)
            to_log = {'name': req_label, 'expected': expected,
                      'status_code': response_as_json_enter_station.status_code,
                      'response_time': time.time() - start_time,
                      'response': self.try_to_read_response_as_json(response_as_json_enter_station)}
            self.log_verbose(to_log)

    def perform_task(self, name):
        name_without_suffix = name.replace("_expected", "").replace("_unexpected", "")
        task = getattr(self, name_without_suffix)
        task(name.endswith('_expected'))



"""
Events for printing all requests into a file. 
"""

#
# class Print:  # pylint: disable=R0902
#     """
#     Record every response (useful when debugging a single locust)
#     """
#
#     def __init__(self, env: locust.env.Environment, include_length=False, include_time=False):
#         self.env = env
#         self.env.events.request_success.add_listener(self.request_success)
#
#     def request_success(self, request_type, name, response_time, response_length, **_kwargs):
#         users = self.env.runner.user_count
#         data = [datetime.now(), request_type, name, response_time, users]
#         state_data.append(data)
#
#
# @events.init.add_listener
# def locust_init_listener(environment, **kwargs):
#     Print(env=environment)
#
#
# @events.quitting.add_listener
# def write_statistics(environment, **kwargs):
#     with open("output1/requests_stats_u250_c.csv", "a+") as f:
#         csv_writer = csv.writer(f)
#         for row in state_data:
#             csv_writer.writerow(row)
