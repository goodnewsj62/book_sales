import requests
from dotenv import load_dotenv,find_dotenv
import os

load_dotenv(find_dotenv())

class Verify:
    PAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET")
    base_url = "https://api.paystack.co/transaction"

    def get_response(self,url:str) -> dict:
        headers = {
            "Authorization": "Bearer " + self.PAYSTACK_SECRET,
            "Content-Type": "application/json",
        }
        response = requests.get(url=url,headers=headers)
        if response.status_code == 200:
            return response.json()
        return response.json()
    
    def verify_payment(self,ref:str) -> dict:
        url = self.base_url + "/verify/" + ref
        return self.get_response(url)
        
    
    def list_transactions(self,page=1) -> dict:
        url = self.base_url +"?status=success"+ "&page=" + str(page)
        return self.get_response(url)

    def fetch_transaction(self,id:int) -> dict:
        url = self.base_url + "/" + id
        return self.get_response(url)
