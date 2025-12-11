import requests
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from colorama import init, Fore

init()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SpotifyCookieChecker():
    
    def __init__(self, file_name: str, directory_path: str = 'json__spotify_cookies'):
        """Initialize the cookie checker with file name and directory path."""
        self.url = 'https://www.spotify.com/us/account'
        self.directory_path = Path(directory_path)
        self.file_name = file_name
        self.cookie_json = self.get_cookies()

    def get_cookies(self) -> Optional[List[Dict]]:
        """Load cookies from JSON file."""
        file_path = self.directory_path / self.file_name
        try:
            if file_path.is_file():
                with open(file_path, 'r', encoding='utf-8') as file:
                    cookies = json.load(file)
                    if not isinstance(cookies, list):
                        logging.error(f"Invalid cookie format in {self.file_name}")
                        return None
                    return cookies
            else:
                logging.warning(f"File not found: {file_path}")
                return None
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error in {self.file_name}: {e}")
            return None
        except Exception as e:
            logging.error(f"Error reading {self.file_name}: {e}")
            return None
    
    def convert_cookies_to_dict(self, cookies):
        cookies_dict = {}
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
        return cookies_dict
    
    def get_response_html(self, cookies: Dict[str, str]) -> Optional[str]:
        """Send request to Spotify with cookies and return response text."""
        try:
            response = requests.get(self.url, cookies=cookies, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Request error for {self.file_name}: {e}")
            return None
    
    def check_cookies(self, response_text: str) -> Optional[str]:
        """Check if cookies are valid and return the plan type."""
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
            return None  # Changed from false to None
    
    def save_working_cookies(self, plan: str) -> None:
        """Save working cookies to a file."""
        try:
            working_dir = Path('working_cookies')
            working_dir.mkdir(exist_ok=True)
            
            file_path = working_dir / f"{self.file_name}_{plan.replace(' ', '_')}"
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(self.cookie_json, file, indent=4)
            logging.info(f"Saved working cookie: {file_path}")
        except Exception as e:
            logging.error(f"Error saving cookies for {self.file_name}: {e}")
    
    def print_cookies_status_and_save(self, response_text: str) -> None:
        """Print cookie status and save if working."""
        plan = self.check_cookies(response_text)
        if plan is not None:  # Changed from != false
            self.save_working_cookies(plan)
            print(Fore.GREEN + f"[✔️] Cookie Working - {self.file_name} | Plan {plan}" + Fore.RESET)
        else:
            print(Fore.RED + f"[❌] Cookie Not Working - {self.file_name}" + Fore.RESET)
    
    def check_if_cookies_are_working(self) -> bool:
        """Check if the cookies are valid and working."""
        if not self.cookie_json:
            print(Fore.RED + f"[❌] Invalid cookie file - {self.file_name}" + Fore.RESET)
            return False
        
        cookies_dict = self.convert_cookies_to_dict(self.cookie_json)
        response_text = self.get_response_html(cookies_dict)
        
        if response_text is None:
            print(Fore.RED + f"[❌] Request failed - {self.file_name}" + Fore.RESET)
            return False
        
        self.print_cookies_status_and_save(response_text)
        return True
