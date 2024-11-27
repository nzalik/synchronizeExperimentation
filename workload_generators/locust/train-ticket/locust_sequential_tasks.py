import logging
import os
import sys
import csv
from locust import task, HttpUser, SequentialTaskSet, LoadTestShape, constant
from locust.exception import StopUser
import numpy as np
from requests.adapters import HTTPAdapter

from locustfile import Requests

GLOBAL_MIN_USERS = 10
GLOBAL_INTENSITY_FILE = os.environ.get("INTENSITY_FILE")
GLOBAL_TASK = os.environ.get("TASK")
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

class SearchTicket(SequentialTaskSet):

    @task
    def only_search(self):
        #logging.info("Running task 'only search'...")
        #task_sequence = ["register_expected"]
        task_sequence = ["home_expected", "search_ticket_expected"]
        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)

    @task
    def stop(self):
        #logging.info("Stopping task 'only search'...")
        raise StopUser()

class HomeLoginSearchStartBooking(SequentialTaskSet):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.client.mount('https://', HTTPAdapter(pool_maxsize=50))
    #     self.client.mount('http://', HTTPAdapter(pool_maxsize=50))

    @task
    def homeLoginSearchStartBooking(self):
        #logging.info("Running Tasks for booking...")
        task_sequence = ["home_expected",
                         "login_expected",
                         "register_expected",
                         "search_ticket_expected",
                         "start_booking_expected"
                         ]

        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)

    @task
    def stop(self):
        #logging.info("Stopping booking tasks")
        raise StopUser()

class HomeLoginSearchStartBookingAssuranceFood(SequentialTaskSet):

    @task
    def homeLoginSearchStartBookingAssuranceFood(self):
        #logging.info("Running Tasks for booking...")
        task_sequence = ["home_expected",
                         "register_expected",
                         "login_expected",
                         "search_ticket_expected",
                         "start_booking_expected",
                         "get_assurance_types_expected",
                         "get_foods_expected",
                         "select_contact_expected",
                         #"finish_booking_expected"
                         ]

        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)

class BookTicket(SequentialTaskSet):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.client.mount('https://', HTTPAdapter(pool_maxsize=50))
    #     self.client.mount('http://', HTTPAdapter(pool_maxsize=50))

    @task
    def book_ticket(self):
        # logging.info("Running Tasks for booking...")
        task_sequence = [  #
            "home_expected",
            "register_expected",
            "login_expected",
            "search_ticket_expected",
            "start_booking_expected",
            "get_assurance_types_expected",
            "get_foods_expected",
            "select_contact_expected",
            "finish_booking_expected"
        ]

        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)
    @task
    def stop(self):
        #logging.info("Stopping booking tasks")
        raise StopUser()

class ConsignTicket(SequentialTaskSet):

    @task
    def perform_task(self):
       #logging.debug("Running tasks for 'consign ticket'...")
        task_sequence = [
            "home_expected",
            "register_expected",
            "login_expected",
            "select_contact_expected",
            "finish_booking_expected",
            "select_order_expected",
            "get_consigns_expected",
            "confirm_consign_expected",
        ]

        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)

    @task
    def stop(self):
        #logging.info("Stopping consign tasks")
        raise StopUser()

class PayForTickets(SequentialTaskSet):
    @task
    def perform_task(self):
        # logging.debug("Running tasks for 'pay'...")

        task_sequence = ["home_expected",
                         "register_expected",
                         "login_expected",
                         "select_contact_expected",
                         "finish_booking_expected",
                         "select_order_expected",
                         "pay_expected"]

        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)

    @task
    def stop(self):
        #logging.info("Stopping pay tasks")
        raise StopUser()

class CollectTicketTasks(SequentialTaskSet):

    @task
    def perform_task(self):
        #logging.debug("Running user 'collect ticket'...")

        task_sequence = [
            "home_expected",
            "register_expected",
            "login_expected",
            "select_order_expected",
            "pay_expected",
            "collect_ticket_expected",
        ]

        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)

    @task
    def stop(self):
        #logging.info("Stopping collect ticket tasks")
        raise StopUser()


class UserCancelNoRefund(SequentialTaskSet):
    weight = 0
   # wait_time = constant(0)

    @task
    def perform_task(self):
        logging.debug("Running user 'cancel no refund'...")

        task_sequence = [
            "home_expected",
            "register_expected",
            "login_expected",
            "select_order_expected",
            "cancel_with_no_refund_expected",
        ]

        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)

class UserOnlyLogin(SequentialTaskSet):
    weight = 1
    # wait_function = random.expovariate(1) * 1000
    wait_time = constant(0)

    @task()
    def perform_task(self):
        logging.debug("User home -> login")
        request = Requests(self.client)
        number = np.random.uniform()
        if number < 0.98:
            tasks_sequence = ["login_expected"]
        else:
            tasks_sequence = ["login_unexpected"]
        for tasks in tasks_sequence:
            request.perform_task(tasks)


class UserNoLogin(SequentialTaskSet):
    weight = 1
    wait_time = constant(0)

    def perfom_task(self):
        logging.debug("Running user 'only search'...")

        task_sequence = ["home_expected", "search_ticket_expected"]

        requests = Requests(self.client)
        for task in task_sequence:
            requests.perform_task(task)

class UserGlobal(HttpUser):
    task_mapping = {
        "SearchTicket": SearchTicket,
        "BookTicket": BookTicket,
        "ConsignTicket": ConsignTicket,
        "HomeLoginSearchStartBookingAssuranceFood":HomeLoginSearchStartBookingAssuranceFood,
        "HomeLoginSearchStartBooking": HomeLoginSearchStartBooking,
        "PayForTickets": PayForTickets,
        "CollectTicketTasks": CollectTicketTasks,
    }

    tasks = [task_mapping.get(GLOBAL_TASK, SearchTicket)]  # Par défaut HomePage si non défini

