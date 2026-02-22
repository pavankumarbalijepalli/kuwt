import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from markdown import markdown
from datetime import datetime as dt
import os

email_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>KUWT – Daily Digest</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&display=swap');

    body {{
    margin: 0;
    padding: 0;
    background-color: #faf7ff; /* soft lavender background */
    font-family: 'Merriweather', 'Segoe UI', Arial, sans-serif;
    }}

    .container {{
    max-width: 700px;
    margin: 20px auto;
    background-color: #ffffff;
    border-radius: 16px;
    box-shadow: 0 6px 25px rgba(155, 123, 255, 0.15); /* subtle purple glow */
    overflow: hidden;
    border: 1px solid #f2e6ff;
    }}

    /* Header */
    .header {{
    background: linear-gradient(135deg, #dba7ff, #9b7bff);
    color: #fff;
    text-align: center;
    padding: 35px 15px;
    border-bottom: 4px solid #f9b9e1;
    }}

    .header img {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 3px solid #fff;
    margin-bottom: 12px;
    box-shadow: 0 0 12px rgba(255, 255, 255, 0.4);
    }}

    .header h1 {{
    font-size: 26px;
    margin: 10px 0 4px;
    font-weight: 700;
    color: #ffffff;
    }}

    .header p {{
    font-size: 14px;
    margin: 0;
    color: #f9eaff;
    }}

    /* Section */
    .section {{
    padding: 28px;
    }}

    .section h2 {{
    font-size: 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    }}

    .section p {{
    font-size: 15px;
    line-height: 1.6;
    color: #444;
    margin-bottom: 15px;
    }}

    /* Buttons */
    .btn {{
    display: inline-block;
    padding: 10px 22px;
    color: #fff;
    text-decoration: none;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
    }}

    .linkedin {{
    background: linear-gradient(135deg, #8cdbff, #0077b5);
    }}

    .medium {{
    background: linear-gradient(135deg, #8affc1, #02b875);
    }}

    .youtube {{
    background: linear-gradient(135deg, #ff7b7b, #ff0000);
    }}

    .btn:hover {{
    opacity: 0.9;
    transform: translateY(-1px);
    }}

    /* Divider */
    .divider {{
    border-top: 1px solid #eee;
    }}

    /* Footer */
    .footer {{
    background-color: #1d093c;
    text-align: center;
    padding: 25px;
    color: #c7b6ff;
    font-size: 12px;
    }}

    .footer a {{
    color: #f9b9e1;
    text-decoration: none;
    font-weight: 600;
    }}

    .footer a:hover {{
    text-decoration: underline;
    }}

  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="{kundelu_ai}" alt="HappyDev Logo"/>
      <h1>Kundelu AI Digest</h1>
      <p>Curated by K.U.W.T Multi Agent Orchestrator</p>
    </div>

    <div class="section">
      <h2 style="color:#02b875;">Your Daily {post_type} Content</h2>
      <p>
        {full_post}
      </p>
    </div>

    <div class="divider"></div>

    <div class="footer">
      <p>© 2025 Kundelu AI | Created by Pavan Kumar Balijepalli</p>
      <p>
        <a href="https://www.linkedin.com/in/pavan-kumar-balijepalli/">LinkedIn</a> •
        <a href="https://medium.com/@pavanbalijepalli.bits">Medium</a> •
        <a href="https://youtube.com/@kundelu-ai">YouTube</a>
      </p>
    </div>
  </div>
</body>
</html>

"""

def send_email(post_type, full_post):
    # Email credentials
    sender_email = os.getenv("EMAIL_FROM")
    app_password = os.getenv("EMAIL_PASSWORD")
    receiver_email = os.getenv("EMAIL_TO")

    # Create the email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Your Daily AI Content on {dt.now().strftime('%d-%b-%Y')}: {post_type.upper()}"
    msg["From"] = f"K.U.W.T Multi Agent Orchestrator <{sender_email}>"
    msg["To"] = receiver_email

    # Email content (plain + HTML)
    # text = "Hi there!\nThis is a test email sent from Python."
    html = email_template.format(
        post_type=post_type,
        full_post=full_post,
        kundelu_ai="https://raw.githubusercontent.com/pavankumarbalijepalli/pavankumarbalijepalli/refs/heads/main/kundelu_ai.png"
    )

    # msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    # Send the email via Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())