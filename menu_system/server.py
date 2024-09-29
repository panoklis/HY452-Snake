import requests
import json
import base64
from io import BytesIO
import threading

class ScoreServer():

    def __init__(self, url, name):
        self.url = url
        self.name = name

    def post_score(self, score):
        data = {
            'userID': self.name,
            'score': score
        }
        post_thread = threading.Thread(target=self._post_score_thread, args=(data,))
        post_thread.start()
        
    def _post_score_thread(self, data):
        response = requests.post(self.url + '/update-leaderboard', json=data)
        if response.status_code == 200:
            print("Score posted successfully")
            print(f'Response: {response.text}')
            return True
        else:
            print("Error posting score")
            print(f'Error: {response.text}')
            return False

    def get_background(self):
        response = requests.get(self.url + '/theme')
        image_data = response.json()['body']
        image = BytesIO(base64.b64decode(image_data))
        return image
    
    def get_leaderboard(self):
        print('Getting leaderboard from server')
        response = requests.get(self.url + '/update-leaderboard')
        leaderboard = json.loads(response.json()['body'])
        leaderboard = {entry['userID']: entry['score'] for entry in leaderboard}
        return leaderboard