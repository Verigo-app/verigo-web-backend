import smtplib
from email.message import EmailMessage
from app.core.config import settings

def send_verification_email(email: str, code: str):
    msg = EmailMessage()
    msg['Subject'] = "Your Verigo Verification Code"
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = email
    msg.set_content(f"""
Hello,

Thank you for registering with Verigo!
Your verification code is: {code}

Enter this code in the app to verify your account.

Best regards,
Verigo Team
    """)

    print(f"[DEBUG] Sending email to {email} with code {code}")  # For testing

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        print(f"[INFO] Verification email sent to {email}")
    except Exception as e:
        print(f"[ERROR] Could not send email to {email}: {e}")
