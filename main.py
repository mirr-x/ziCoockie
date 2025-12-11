from lib.spotify.spotify_cookie_checker import SpotifyCookieChecker
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Main function to check all cookie files."""
    cookie_dir = Path('json__spotify_cookies')
    
    if not cookie_dir.exists():
        logging.error(f"Directory not found: {cookie_dir}")
        return
    
    cookie_files = [f for f in cookie_dir.iterdir() if f.is_file() and f.suffix == '.json']
    
    if not cookie_files:
        logging.warning(f"No JSON files found in {cookie_dir}")
        return
    
    logging.info(f"Found {len(cookie_files)} cookie files to check")
    
    working_count = 0
    for file_path in cookie_files:
        try:
            cookie_checker = SpotifyCookieChecker(file_path.name)
            if cookie_checker.check_if_cookies_are_working():
                working_count += 1
        except Exception as e:
            logging.error(f"Error processing {file_path.name}: {e}")
    
    logging.info(f"Completed: {working_count}/{len(cookie_files)} cookies are working")

if __name__ == "__main__":
    main()

