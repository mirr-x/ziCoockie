# ZiCookie

## Overview

ZiCookie is a tool to check the validity of Spotify cookies stored in JSON files. It reads cookies from a specified directory, sends requests to Spotify, and determines if the cookies are valid based on the response.

![Rick and Morty Run the Jewels](https://media1.tenor.com/m/G_XMsjMfj5wAAAAd/rick-and-morty-samurai-shogun.gif)

## Features

- ✅ Validates Spotify cookies
- 🎵 Identifies Spotify plan types (Premium Family, Duo, Student, Premium, Free)
- 📁 Automatically saves working cookies
- 🎨 Colored console output
- 📊 Logging support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mirr-x/ziCoockie.git
cd ziCoockie
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your cookie JSON files in the `json__spotify_cookies/` directory
2. Run the checker:
```bash
python main.py
```

3. Working cookies will be saved in the `working_cookies/` directory

## Cookie Format

Cookies should be in JSON format as an array of objects:
```json
[
    {
        "name": "cookie_name",
        "value": "cookie_value",
        "domain": ".spotify.com"
    }
]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
