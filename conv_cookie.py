import json
import os
import shutil
import sys
import logging
from pathlib import Path
from typing import List, Dict, Optional
from colorama import init, Fore

init()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def identify_file(file_path: str) -> str:
    """
    Identify whether a file contains JSON or Netscape format cookies.
    
    Args:
        file_path: Path to the cookie file
        
    Returns:
        'json', 'netscape', or 'error'
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file_content:
            json.load(file_content)
            return "json"
    except json.JSONDecodeError:
        return "netscape"
    except Exception as e:
        logging.error(f"Error processing {file_path}: {str(e)}")
        return "error"


def convert_netscape_cookie_to_json(cookie_file_content: str) -> List[Dict]:
    """
    Convert Netscape format cookies to JSON format.
    
    Args:
        cookie_file_content: Content of the Netscape cookie file
        
    Returns:
        List of cookie dictionaries
    """
    cookies = []
    for line in cookie_file_content.splitlines():
        # Skip comments and empty lines
        if line.startswith("#") or not line.strip():
            continue
            
        fields = line.strip().split("\t")
        if len(fields) >= 7:
            cookie = {
                "domain": fields[0].replace("www", ""),
                "flag": fields[1],
                "path": fields[2],
                "secure": fields[3] == "TRUE",
                "expiration": fields[4],
                "name": fields[5],
                "value": fields[6],
            }
            cookies.append(cookie)
    
    return cookies


def append_json_files(existing_file: str, data: List[Dict]) -> None:
    """
    Append cookie data to an existing JSON file.
    
    Args:
        existing_file: Path to the existing JSON file
        data: List of cookie dictionaries to append
    """
    try:
        with open(existing_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
        
        if not isinstance(existing_data, list):
            existing_data = [existing_data]
        
        existing_data.extend(data)
        
        with open(existing_file, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4)
    except Exception as e:
        logging.error(f"Error appending to {existing_file}: {str(e)}")


no_of_cookies = 0

try:
    if os.name  == "posix":
        folder_path = "cookies"
    else:
        while True:
            import tkinter
            from tkinter import filedialog

            print(
                Fore.YELLOW
                + "\n<<< Select Netscape cookies folder >>>\n\n"
                + Fore.RESET
            )
            tkinter.Tk().withdraw()
            folder_path = filedialog.askdirectory()
            if folder_path == "":
                if os.path.isdir("cookies"):
                    folder_path = "cookies"
                    print(
                        Fore.YELLOW
                        + "Trying to use default folder 'cookies'\n"
                        + Fore.RESET
                    )
                    break
                else:
                    print(
                        Fore.RED
                        + "[⚠️] No folder selected or default 'cookies' folder not found, Exiting..."
                        + Fore.RESET
                    )
                    sys.exit()

            else:
                break

    path = "json__spotify_cookies"
    try:
        os.mkdir(path)
        print(Fore.RED + f"Folder {path} created!\n" + Fore.RESET)
    except FileExistsError:
        if (
            input(
                Fore.YELLOW
                + "Do you want to remove old cookies folder? (y/n)\n [y] Recommended \n [n] New cookies will be appended > : "
                + Fore.RESET
            )
            == "y"
        ):
            shutil.rmtree(path)
            os.mkdir(path)
        else:
            print(
                Fore.YELLOW
                + "Appending to existing 'json_cookies' folder\n"
                + Fore.RESET
            )

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            file_type = identify_file(filepath)
            if file_type == "json":
                destination_path = os.path.join(path, filename)
                if os.path.exists(destination_path):
                    with open(filepath, "r", encoding="utf-8") as f:
                        new_data = json.load(f)
                    append_json_files(destination_path, new_data)
                    print(
                        Fore.GREEN
                        + f"[✔️] {filename} - Appended to 'json_cookies' folder!"
                        + Fore.RESET
                    )
                else:
                    shutil.copy(filepath, destination_path)
                    print(
                        Fore.GREEN
                        + f"[✔️] {filename} - Copied to 'json_cookies' folder!"
                        + Fore.RESET
                    )
            elif file_type == "netscape":
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()

                json_data = json.loads(convert_netscape_cookie_to_json(content))

                destination_path = os.path.join(path, filename)
                if os.path.exists(destination_path):
                    append_json_files(destination_path, json_data)
                    print(
                        Fore.GREEN
                        + f"[✔️] {filename} - Appended to 'json_cookies' folder!"
                        + Fore.RESET
                    )
                else:
                    with open(destination_path, "w", encoding="utf-8") as f:
                        f.write(json.dumps(json_data, indent=4))
                    print(Fore.GREEN + f"[✔️] {filename} - DONE!" + Fore.RESET)
                    no_of_cookies += 1
            else:
                print(
                    Fore.RED
                    + f"[⚠️] {filename} - Error: File type could not be identified!"
                    + Fore.RESET
                )

    print(
        Fore.YELLOW
        + f"\nConverted {no_of_cookies} cookies to JSON format\n"
        + Fore.RESET
    )
except KeyboardInterrupt:
    print(Fore.RED + "\n\nProgram Interrupted by user" + Fore.RESET)
    sys.exit()
