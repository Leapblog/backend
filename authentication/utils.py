import random
import string
from django.core.mail import send_mail
from django.conf import settings


def generate_otp(length: int = 6) -> int:
    characters = string.digits
    otp = "".join(random.choice(characters) for _ in range(length))
    return int(otp)


def send_otp_email(email: str, otp: int):
    subject = "Verify your account!"
    message = f"Your OTP for verification is: {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
