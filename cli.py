import click

from datetime import datetime
from database import setup_database, get_url, log_access, get_analytics
from url_shortener import (
    generate_short_url,
    get_public_ip,
    validate_url,
    verify_password,
)


@click.group()
def cli():
    setup_database()


@click.command()
@click.argument("original_url")
@click.option("--expiry", default=24, help="Expiry time in hours. Default is 24.")
@click.option(
    "--password", default=None, help="Optional password for the shortened URL."
)
def shorten(original_url, expiry, password):
    if not validate_url(original_url):
        message = "Invalid URL. Please provide a valid URL."
        click.echo(click.style(message, fg="red", bold=True))
        return

    short_url = generate_short_url(original_url, expiry, password)

    message = f"Shortened URL: {short_url}"
    click.echo(click.style(message, fg="green", bold=True))


@click.command()
@click.argument("short_url")
@click.option("--password", default=None, help="Password for the analytics, if set.")
def redirect(short_url, password):
    url_data = get_url(short_url)

    if not url_data:
        message = f"Short URL not found."
        click.echo(click.style(message, fg="red", bold=True))
        exit()

    if datetime.now() > datetime.fromisoformat(url_data["expires_at"]):
        message = f"This URL has expired."
        click.echo(click.style(message, fg="red", bold=True))
        exit()

    if url_data["password"] and not password:
        message = f"Password is required to access this URL."
        click.echo(click.style(message, fg="red", bold=True))
        exit()

    if not verify_password(url_data["password"], password):
        message = f"Incorrect password. Access denied."
        click.echo(click.style(message, fg="red", bold=True))
        exit()

    ip_address = get_public_ip()

    log_access(short_url, ip_address)

    message = f"Redirecting to: {url_data['original_url']}"
    click.echo(click.style(message, fg="green", bold=True))


@click.command()
@click.argument("short_url")
def analytics(short_url):
    url_data = get_url(short_url)

    if not url_data:
        message = f"Short URL not found."
        click.echo(click.style(message, fg="red", bold=True))
        return

    analytics_data = get_analytics(short_url)

    click.echo("----------------------")

    message = f"Analytics for {short_url}:"
    click.echo(click.style(message, fg="green", bold=True))

    click.echo("----------------------")

    message = f"Access count: {len(analytics_data)}"
    click.echo(click.style(message, fg="green", bold=True))

    click.echo("----------------------")

    message = f"Access Logs:"
    click.echo(click.style(message, fg="green", bold=True))

    click.echo("----------------------")

    for log in analytics_data:
        click.echo(f"- {log['accessed_at']} from {log['ip_address']}")

    click.echo("----------------------")


cli.add_command(shorten)
cli.add_command(redirect)
cli.add_command(analytics)

if __name__ == "__main__":
    cli()
