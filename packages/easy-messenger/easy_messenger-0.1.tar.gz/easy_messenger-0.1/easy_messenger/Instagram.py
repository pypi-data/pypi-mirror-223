import requests
import json



class Instagram:
    def __init__(self, access_token, version="v17.0"):
        self.access_token = access_token
        self.version = version
        self.base_url = "https://graph.facebook.com/" + self.version + "/"

    def send_message(self, message_text, recipient_igsid):
        url = f'https://graph.facebook.com/v17.0/me/messages?access_token={self.access_token}&recipient={{"id":"{recipient_igsid}"}}&message={{"text":"{message_text}"}}'
        response = requests.post(url)

        return response.json()
    
    def get_message_text(self, response: dict):
        return response["entry"][0]["messaging"][0]["message"]["text"]
    
    def get_user_igsid(self, response):
        return response["entry"][0]["messaging"][0]["sender"]["id"]

    def get_username(self, esponse):
        pass


    