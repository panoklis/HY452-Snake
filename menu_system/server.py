import requests
from requests.exceptions import RequestException
import json
import base64
from io import BytesIO
import threading
import hashlib

class ScoreServer():

    def __init__(self, url):
        self.url = url
        self.last_request_status = None

    def post_score(self, score, name):
        data = {
            'userID': name,
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
        try:
            response = requests.get(self.url + '/asset/background?name=' + name)
            response.raise_for_status()
        except RequestException as e:
            print(f'Error: {e}')
            self.last_request_status = False
            return None
        image_data = response.text
        image = BytesIO(base64.b64decode(image_data))
        self.last_request_status = True
        return image
    
    def get_backgrounds(self):
        print('Getting backgrounds from server')
        try:
            response = requests.get(self.url + '/asset/background/all', timeout=5)
            response.raise_for_status()
        except RequestException as e:
            print(f'Error: {e}')
            self.last_request_status = False
            return None
        backgrounds = json.loads(response.json()['body'])
        backgrounds = {entry['Key'] for entry in backgrounds if entry['Size'] > 0}
        self.last_request_status = True
        return backgrounds
    
    def get_leaderboard(self):
        print('Getting leaderboard from server')
        try:
            response = requests.get(self.url + '/leaderboard')
            response.raise_for_status()
        except RequestException as e:
            print(f'Error: {e}')
            self.last_request_status = False
            return None
        leaderboard = json.loads(response.json()['body'])
        leaderboard = {entry['userID']: entry['score'] for entry in leaderboard}
        self.last_request_status = True
        return leaderboard

    def register_user(self, name, password, email):
        data = {
            'Action': 'Register',
            'Username': name,
            'Email': email,
            'PasswordHash': hashlib.sha1(password.encode()).hexdigest()
        }
        try:
            response = requests.post(self.url + '/register', json=data)
            response.raise_for_status()
        except RequestException as e:
            print("Error registering user")
            print(f'Error: {e}')
            print(f'Error: {response.text}')
            self.last_request_status = False
            return False

        print("User registered successfully")
        print(f'Response: {response.text}')
        self.last_request_status = True
        return True

    def login_user(self, name, password):
        data = {
            'Action': 'Login',
            'Username': name,
            'PasswordHash': hashlib.sha1(password.encode()).hexdigest()
        }
        try:
            response = requests.post(self.url + '/login', json=data)
            response.raise_for_status()
        except RequestException as e:
            print("Error logging in")
            print(f'Error: {e}')
            print(f'Error: {response.text}')
            self.last_request_status = False
            return False

        print("User logged in successfully")
        print(f'Response: {response.text}')
        self.last_request_status = True
        return True