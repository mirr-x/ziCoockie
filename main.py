from lib.spotify.spotify_cookie_checker import SpotifyCookieChecker
import os

def main():

    all_files = os.listdir('json__spotify_cookies')
    for file_name in all_files:
        if os.path.isfile(os.path.join('json__spotify_cookies', file_name)):
            cookie_checker = SpotifyCookieChecker(file_name)
            cookie_checker.check_if_cookies_are_working()

if __name__ == "__main__":
    main()

