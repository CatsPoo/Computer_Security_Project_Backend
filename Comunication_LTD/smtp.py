import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def send_email(sender_email,recipient_email,subject,body):
    # SMTP server configuration
    smtp_server = 'localhost'  # Change this to the address of your fake SMTP server
    smtp_port = 25  # Change this to the port of your fake SMTP server

    # Create a MIMEText object to represent the email body
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

    print('Email sent successfully.')
