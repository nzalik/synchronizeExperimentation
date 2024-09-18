from locust import LoadTestShape, HttpUser, task, between, events
import numpy as np
import resource
import pickle
import random
import math
import os
import csv
resource.setrlimit(resource.RLIMIT_NOFILE, (250000, 250000))


####################################################################################################################################
# Simulation Configuration
####################################################################################################################################
#GLOBAL_NGINX_FRONTEND_URL  = 'http://172.16.20.17:30080'
#GLOBAL_MEDIA_FRONTEND_URL  = 'http://172.16.20.19:30081'
GLOBAL_NGINX_FRONTEND_URL  = os.environ.get("NGINX_ADDR")
GLOBAL_MEDIA_FRONTEND_URL  = os.environ.get("MEDIA_ADDR")
GLOBAL_INTENSITY_FILE      = os.environ.get("INTENSITY_FILE")
COMPOSITION_OPTION         = os.environ.get("COMP_OPT")

#GLOBAL_EXPERIMENT_DURATION = 3600    # None = Run forever, 43200 = 12 hour
#GLOBAL_SECONDS_PER_DAY     = 3600    # 3600 = 1 hour
GLOBAL_MIN_USERS           = 100
#GLOBAL_PEAKS               = [140, 160, 180, 200]
GLOBAL_RANDOMNESS          = 0.20
GLOBAL_WAIT_TIME           = between(1, 3)
#GLOBAL_COMPOSITIONS = [(98, 1, 1)]

if COMPOSITION_OPTION == 'composePost':
    GLOBAL_COMPOSITIONS = [(100, 0, 0)]
elif COMPOSITION_OPTION == 'readUserTimeline':
    GLOBAL_COMPOSITIONS = [(0, 100, 0)]
elif COMPOSITION_OPTION == 'readHomeTimeline':
    GLOBAL_COMPOSITIONS = [(0, 0, 100)]
elif COMPOSITION_OPTION == 'mixed':
    GLOBAL_COMPOSITIONS = [(33, 33, 33)]
else:
    GLOBAL_COMPOSITIONS = [(5, 40, 55), (5, 45, 50), (5, 50, 45), (5, 55, 40), (10, 35, 55), (10, 40, 50), (10, 45, 45), (10, 50, 40), (10, 55, 35), (15, 35, 50), (15, 40, 45), (15, 45, 40), (15, 50, 35)]

####################################################################################################################################
texts = [text.replace('@', '') for text in list(open('./datasets/social-graph/fb-posts/news.txt'))]
media = [os.path.join('./datasets/inria-person', fname) for fname in os.listdir('./datasets/inria-person')]
users = list(range(1, 963))
cycle = 0
active_users, inactive_users = [], list(range(1, 963))
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

####################################################################################################################################

class LoadShape(LoadTestShape):
    row_offset = 0

    def tick(self):
        global cycle
        #if cycle == -1:
        #    return None

        user_count = GLOBAL_MIN_USERS
        csv_list = []
        with open(GLOBAL_INTENSITY_FILE) as intensity_csv:
            csv_reader = csv.reader(intensity_csv, delimiter=',')
            csv_list = list(csv_reader)

        user_count = int(csv_list[self.row_offset][1])
        self.row_offset += 1
        
        if self.row_offset % 60 == 0:
            cycle += 1 
        if self.row_offset >= len(csv_list):
            #cycle = -1
            return None
        
        spawn_rate = max(1, abs(user_count - self.get_current_user_count())) # should not be 0
        return user_count, spawn_rate


class SocialNetworkUser(HttpUser):
    wait_time = GLOBAL_WAIT_TIME
    host = GLOBAL_NGINX_FRONTEND_URL
    local_cycle = cycle
    
    def check_cycle(self):
        if cycle == 0:
            # Initialize start compostion
            self.tasks = [self.apis[0] for _ in range(GLOBAL_COMPOSITIONS[0][0])] + [self.apis[1] for _ in range(GLOBAL_COMPOSITIONS[0][1])] + [self.apis[2] for _ in range(GLOBAL_COMPOSITIONS[0][2])]
        
        if self.local_cycle != cycle:
            self.local_cycle = cycle
            composition = GLOBAL_COMPOSITIONS[self.local_cycle % len(GLOBAL_COMPOSITIONS)]
            self.tasks = [self.apis[0] for _ in range(composition[0])] + [self.apis[1] for _ in range(composition[1])] + [self.apis[2] for _ in range(composition[2])]

    @task
    def composePost(self):
        self.check_cycle()

        text = random.choice(texts)

        # User mentions
        number_of_user_mentions = random.randint(0, min(5, len(friends[self.user_id])))
        if number_of_user_mentions > 0:
            for friend_id in random.choices(friends[self.user_id], k=number_of_user_mentions):
                text += " @username_" + str(friend_id)
        # Media
        media_id = ''
        media_type = ''
        if random.random() < 0.20:
            with open(random.choice(media), "rb") as f:
                media_response = self.client.post('%s/upload-media' % GLOBAL_MEDIA_FRONTEND_URL,
                                                  files={"media": f})
            if media_response.ok:
                media_json = eval(media_response.text)
                media_id = '"%s"' % media_json['media_id']
                media_type = '"%s"' % media_json['media_type']
        # URLs - Note: no need to add it as the original post content has URLs already

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'username': 'username_' + str(self.user_id),
                'user_id': str(self.user_id),
                'text': text,
                'media_ids': "[" + str(media_id) + "]",
                'media_types': "[" + str(media_type) + "]",
                'post_type': '0'}

        self.client.post("/wrk2-api/post/compose", data=data, headers=headers)


    @task
    def readHomeTimeline(self):
        self.check_cycle()

        start = random.randint(0, 100)
        stop = start + 10

        response = self.client.get(
            "/wrk2-api/home-timeline/read?start=%s&stop=%s&user_id=%s" % (str(start), str(stop), str(self.user_id)),
            name="/wrk2-api/home-timeline/read?start=[start]&stop=[stop]")

    @task
    def readUserTimeline(self):
        self.check_cycle()

        start = random.randint(0, 100)
        stop = start + 10
        user_id = random.choice(friends[self.user_id])

        response = self.client.get(
            "/wrk2-api/user-timeline/read?start=%s&stop=%s&user_id=%s" % (str(start), str(stop), str(user_id)),
            name='/wrk2-api/user-timeline/read?start=[start]&stop=[stop]&user_id=[user_id]')

    apis = [composePost, readHomeTimeline, readUserTimeline]

    def on_stop(self):
        active_users.remove(self.user_id)
        inactive_users.append(self.user_id)

    def on_start(self):
        self.user_id = random.choice(inactive_users)
        active_users.append(self.user_id)
        inactive_users.remove(self.user_id)
