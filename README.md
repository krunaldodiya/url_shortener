# URL Shortener CLI

A Python-based URL shortener system that shortens URLs, tracks usage analytics, and allows for link expiration.

## Features

- Create shortened URLs with optional expiration and password protection.
- Redirect to the original URL using the short URL.
- View analytics for a shortened URL, including access logs and counts.

---

## Prerequisites

1. **Python Version**: Python 3.8 or later.
2. **SQLite**: Included with Python (no additional setup required).
3. Clone Repository:

   ```bash
   git clone git@github.com:krunaldodiya/url_shortener.git
   ```

4. **Dependencies**: Ensure required libraries are installed using:
   ```bash
   pip install -r requirements.txt
   ```
   or if you want to use Poetry, you can run:
   ```bash
   poetry install
   ```

## How to use

### 1. Shorten a URL:

python cli.py shorten "https://example.com" --expiry 48 --password "<YOUR_PASSWORD>"

### 2. Redirect using the shortened URL:

python cli.py redirect https://short.ly/100680 --password "<YOUR_PASSWORD>"

### 3. View analytics for the shortened URL:

python cli.py analytics https://short.ly/100680
