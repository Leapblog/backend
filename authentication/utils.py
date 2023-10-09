import random
import string

from django.conf import settings
from django.core.mail import send_mail


def generate_otp(length: int = 6) -> int:
    """
    Generates a random OTP (One-Time Password) of the specified length.

    Args:
        length (int): The length of the OTP to generate. Defaults to 6.

    Returns:
        int: The generated OTP as an integer.
    """
    characters = string.digits
    otp = "".join(random.choice(characters) for _ in range(length))
    return int(otp)


def send_otp_email(email: str, otp: int):
    """
    Sends an email containing the OTP for verification to the specified email address.

    Args:
        email (str): The email address to send the OTP to.
        otp (int): The OTP to include in the email message.
    """
    subject = "Verify your account!"
    message = f"Your OTP for verification is: {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
