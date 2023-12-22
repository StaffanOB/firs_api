
import os
import requests
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")


def send_simple_message(to_user, subject, body):
    """ Simple message function to send emails to users """
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": f"LibAPI <mailgun@{DOMAIN}>",
        "to": [to_user],
        "subject": subject,
        "text": body},
        timeout=3
    )


def send_user_registration_email(email, username):
    """ Pre defined registration message to new users."""
    return send_simple_message(
        email,
        "Successfully signed up",
        f"Hi {username}. You have successfully signed up to the Book Library API",
    )
