import os
import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
DEFAULT_FROM = os.getenv('DEFAULT_FROM_EMAIL', SMTP_USER)

def send_alert_email(to_email: str, subject: str, body_html: str, body_text: str = ""):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = DEFAULT_FROM
    msg['To'] = to_email

    part1 = MIMEText(body_text or ' ', 'plain')
    part2 = MIMEText(body_html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(DEFAULT_FROM, to_email, msg.as_string())
