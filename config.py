"""Configuration settings for ZiCookie."""

from pathlib import Path

# Directories
COOKIE_INPUT_DIR = Path('json__spotify_cookies')
COOKIE_OUTPUT_DIR = Path('working_cookies')

# Spotify settings
SPOTIFY_ACCOUNT_URL = 'https://www.spotify.com/us/account'
REQUEST_TIMEOUT = 10  # seconds

# Plan types to check for
PLAN_TYPES = [
    'Premium Family',
    'Premium Duo',
    'Premium Student',
    'Premium'
]