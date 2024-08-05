import requests
from sympy import false, true
import os
import json
from colorama import init, Fore
init()

class SpotifyCookieChecker():

    def __init__(self, file_name):
        self.url = 'https://www.spotify.com/us/account'
        self.directory_path = 'json__spotify_cookies'
        self.file_name = file_name
        self.cookie_json = self.get_cookies()

    def get_cookies(self):
        file_path = os.path.join(self.directory_path, self.file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                cookies = json.load(file)
                return cookies
    
    def convert_cookies_to_dict(self, cookies):
        cookies_dict = {}
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
        return cookies_dict
    
    def get_response_html(self, cookies):
        response = requests.get(self.url, cookies=cookies)
        return response.text
    
    def check_cookies(self, response_text):
        if "Manage your subscription" in response_text:

            if "Premium Family" in response_text:
                return "Premium Family"
            elif "Premium Duo" in response_text:
                return "Premium Duo"
            elif "Premium Student" in response_text:
                return "Premium Student"
            elif "Premium" in response_text:
                return "Premium"
            else:
                return "Free"
        else:
            return false
    
    def save_working_cookies(self, plan):
        if not os.path.exists('working_cookies'):
            os.mkdir('working_cookies')
        file_path = os.path.join("working_cookies", self.file_name)
        edit_file_name = "{:s}_{:s}".format(file_path, plan)
        with open(edit_file_name, 'w', encoding='utf-8') as file:
            json.dump(self.cookie_json, file, indent=4)

    def print_cookies_status_and_save(self, response_text):
        plan = self.check_cookies(response_text)
        if plan != false:
            self.save_working_cookies(plan)
            print(Fore.GREEN + f"[✔️] Cookie Working - {self.file_name} | Plan {plan}" + Fore.RESET)
        else:
            print(Fore.RED + f"[❌] Cookie Not Working - {self.file_name}" + Fore.RESET)
    
    def check_if_cookies_are_working(self):
        cookies = self.cookie_json
        cookies_dict = self.convert_cookies_to_dict(cookies)
        response_text = self.get_response_html(cookies_dict)
        self.print_cookies_status_and_save(response_text)
