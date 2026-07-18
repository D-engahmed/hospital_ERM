from django.core.mail import send_mail
from django.conf import settings


def send_email(email, token):
    subject = 'Password Reset - Hospital ERM'
    message = f'''
Hello,

You requested a password reset for your Hospital ERM account.

Click the link below to reset your password:
{settings.BASE_URL}/reset/{token}/

If you did not request this, please ignore this email.

Regards,
Hospital ERM Team
'''
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
