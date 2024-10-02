import requests
import json
import base64
from io import BytesIO
import threading

class ScoreServer():

    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.last_request_status = None

    def post_score(self, score):
        data = {
            'userID': self.name,
            'score': score
        }
        post_thread = threading.Thread(target=self._post_score_thread, args=(data,))
        post_thread.start()
        
    def _post_score_thread(self, data):
        response = requests.post(self.url + '/leaderboard', json=data)
        if response.status_code == 200:
            print("Score posted successfully")
            print(f'Response: {response.text}')
            self.last_request_status = True
            return True
        else:
            print("Error posting score")
            print(f'Error: {response.text}')
            self.last_request_status = False
            return False

    def get_background(self,name):
        response = requests.get(self.url + '/asset/background?name=' + name)
        image_data = response.text
        image = BytesIO(base64.b64decode(image_data))
        if response.status_code == 200:
            self.last_request_status = True
        else:
            self.last_request_status = False
        return image
    
    def get_backgrounds(self):
        print('Getting backgrounds from server')
        response = requests.get(self.url + '/asset/background/all')
        backgrounds = json.loads(response.json()['body'])
        backgrounds = {entry['Key'] for entry in backgrounds if entry['Size'] > 0}
        if response.status_code == 200:
            self.last_request_status = True
        else:
            self.last_request_status = False
        return backgrounds
    
    def get_leaderboard(self):
        print('Getting leaderboard from server')
        response = requests.get(self.url + '/leaderboard')
        leaderboard = json.loads(response.json()['body'])
        leaderboard = {entry['userID']: entry['score'] for entry in leaderboard}
        if response.status_code == 200:
            self.last_request_status = True
        else:
            self.last_request_status = False
        return leaderboard