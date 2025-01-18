import click
import hashlib
import bcrypt
import requests

from urllib.parse import urlparse
from datetime import datetime, timedelta
from database import get_url, insert_url
from vars import BASE_URL, IP_ADDRESS_API


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hashed_password.decode("utf-8")


def verify_password(stored_hash: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))


def generate_short_url(
    original_url: str, expiry: int = 24, password: str | None = None
) -> str:
    """
    Generate a unique short URL identifier for a given original URL.
    :param original_url: The original URL to be shortened.
    :return: The short URL identifier.
    """
    existing_url = get_url(original_url, "original")

    if existing_url:
        short_url = existing_url["short_url"]

        warning_message = f"Short URL: {short_url} already exists for {original_url}"
        click.echo(click.style(warning_message, fg="red", bold=True))
        exit()

    password_hash = hash_password(password) if password else None

    url_hash = hashlib.sha256(original_url.encode()).hexdigest()

    short_identifier = url_hash[:6]

    short_url = f"{BASE_URL}/{short_identifier}"

    expiry_time = datetime.now() + timedelta(hours=expiry)

    insert_url(original_url, short_url, expiry_time, password_hash)

    return short_url


def get_public_ip():
    try:
        response = requests.get(IP_ADDRESS_API)
        ip_data = response.json()
        return ip_data["ip"]
    except requests.RequestException:
        return "127.0.0.1"


def validate_url(url):
    """
    Validate if a given URL is well-formed.
    :param url: The URL to validate.
    :return: True if the URL is valid, False otherwise.
    """
    try:
        parsed = urlparse(url)

        return bool(parsed.scheme) and bool(parsed.netloc)
    except Exception:
        return False


def is_url_expired(expires_at):
    """
    Check if a URL is expired based on its expiration timestamp.
    :param expires_at: The expiration timestamp of the URL.
    :return: True if expired, False otherwise.
    """
    return datetime.now() > datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S")
