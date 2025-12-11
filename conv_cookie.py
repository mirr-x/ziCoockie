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




def get_cookie_folder_path() -> Optional[str]:
    """
    Get the path to the cookies folder.
    On Linux, uses 'cookies' directory. On other systems, prompts user to select folder.
    
    Returns:
        Path to the cookies folder or None if cancelled
    """
    if os.name == "posix":
        folder_path = "cookies"
        if not os.path.isdir(folder_path):
            logging.error(f"Default folder '{folder_path}' not found")
            return None
        return folder_path
    else:
        import tkinter
        from tkinter import filedialog

        print(Fore.YELLOW + "\n<<< Select Netscape cookies folder >>>\n" + Fore.RESET)
        tkinter.Tk().withdraw()
        folder_path = filedialog.askdirectory()
        
        if folder_path == "":
            if os.path.isdir("cookies"):
                folder_path = "cookies"
                print(Fore.YELLOW + "Using default folder 'cookies'\n" + Fore.RESET)
                return folder_path
            else:
                logging.error("No folder selected or default 'cookies' folder not found")
                return None
        
        return folder_path


def setup_output_directory(output_path: str) -> bool:
    """
    Create or clean the output directory for JSON cookies.
    
    Args:
        output_path: Path to the output directory
        
    Returns:
        True if setup successful, False otherwise
    """
    try:
        if os.path.exists(output_path):
            response = input(
                Fore.YELLOW
                + f"Do you want to remove old '{output_path}' folder? (y/n)\n"
                + " [y] Recommended - Clean start\n"
                + " [n] New cookies will be appended\n"
                + " > : "
                + Fore.RESET
            ).strip().lower()
            
            if response == "y":
                shutil.rmtree(output_path)
                os.makedirs(output_path)
                print(Fore.GREEN + f"Folder '{output_path}' cleaned and recreated!\n" + Fore.RESET)
            else:
                print(Fore.YELLOW + f"Appending to existing '{output_path}' folder\n" + Fore.RESET)
        else:
            os.makedirs(output_path)
            print(Fore.GREEN + f"Folder '{output_path}' created!\n" + Fore.RESET)
        
        return True
    except Exception as e:
        logging.error(f"Error setting up output directory: {str(e)}")
        return False


def process_cookie_file(filepath: str, filename: str, output_path: str) -> bool:
    """
    Process a single cookie file and convert it to JSON format if needed.
    
    Args:
        filepath: Full path to the cookie file
        filename: Name of the cookie file
        output_path: Path to output directory
        
    Returns:
        True if file was processed successfully, False otherwise
    """
    file_type = identify_file(filepath)
    destination_path = os.path.join(output_path, filename)
    
    try:
        if file_type == "json":
            if os.path.exists(destination_path):
                with open(filepath, "r", encoding="utf-8") as f:
                    new_data = json.load(f)
                append_json_files(destination_path, new_data)
                print(Fore.GREEN + f"[✔️] {filename} - Appended to output folder!" + Fore.RESET)
            else:
                shutil.copy(filepath, destination_path)
                print(Fore.GREEN + f"[✔️] {filename} - Copied to output folder!" + Fore.RESET)
            return True
            
        elif file_type == "netscape":
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            
            json_data = convert_netscape_cookie_to_json(content)
            
            if os.path.exists(destination_path):
                append_json_files(destination_path, json_data)
                print(Fore.GREEN + f"[✔️] {filename} - Converted and appended!" + Fore.RESET)
            else:
                with open(destination_path, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, indent=4)
                print(Fore.GREEN + f"[✔️] {filename} - Converted to JSON!" + Fore.RESET)
            return True
            
        else:
            print(Fore.RED + f"[⚠️] {filename} - Error: Could not identify file type!" + Fore.RESET)
            return False
            
    except Exception as e:
        logging.error(f"Error processing {filename}: {str(e)}")
        print(Fore.RED + f"[⚠️] {filename} - Error: {str(e)}" + Fore.RESET)
        return False


def main():
    """Main function to convert cookie files to JSON format."""
    output_path = "json__spotify_cookies"
    converted_count = 0
    
    try:
        # Get input folder path
        folder_path = get_cookie_folder_path()
        if not folder_path:
            print(Fore.RED + "[⚠️] No folder selected, exiting..." + Fore.RESET)
            sys.exit(1)
        
        # Setup output directory
        if not setup_output_directory(output_path):
            print(Fore.RED + "[⚠️] Failed to setup output directory, exiting..." + Fore.RESET)
            sys.exit(1)
        
        # Process all files in the input folder
        cookie_files = [f for f in os.listdir(folder_path) 
                       if os.path.isfile(os.path.join(folder_path, f))]
        
        if not cookie_files:
            print(Fore.YELLOW + f"[⚠️] No files found in '{folder_path}'" + Fore.RESET)
            sys.exit(0)
        
        print(Fore.CYAN + f"\nProcessing {len(cookie_files)} files...\n" + Fore.RESET)
        
        for filename in cookie_files:
            filepath = os.path.join(folder_path, filename)
            if process_cookie_file(filepath, filename, output_path):
                converted_count += 1
        
        # Summary
        print(Fore.CYAN + "\n" + "=" * 50 + Fore.RESET)
        print(Fore.GREEN + f"✔ Successfully processed: {converted_count}/{len(cookie_files)} files" + Fore.RESET)
        print(Fore.CYAN + "=" * 50 + "\n" + Fore.RESET)
        
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[⚠️] Program interrupted by user" + Fore.RESET)
        sys.exit(130)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        print(Fore.RED + f"\n[⚠️] Unexpected error: {str(e)}" + Fore.RESET)
        sys.exit(1)


if __name__ == "__main__":
    main()

