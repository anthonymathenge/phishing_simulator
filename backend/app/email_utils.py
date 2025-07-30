import smtplib
from email.mime.text import MIMEText
import json

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "zachmathenge@gmail.com"
SMTP_PASS = "mtiaydekjgvsqlww"  # Use an app password, NOT your main password

def send_phishing_email(to_email, user_id, name="User"):
    # Load template
    with open("email_template.json", "r") as f:
        template = json.load(f)

    subject = personalize_template(template["subject"], {"name": name})
    body = personalize_template(template["body"], {
        "name": name,
        "company": "ExampleCorp",
        "position": "Developer"
    })

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()
        print(f"[✓] Email sent to {to_email}")
    except Exception as e:
        print(f"[✗] Email failed to send: {e}")
        
def personalize_template(template: str, data: dict):
    for key, value in data.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template
