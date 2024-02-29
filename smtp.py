import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP server configuration
smtp_server = 'smtp.mail.com'
smtp_port = 587  # Default SMTP port for TLS
smtp_username = 'communication_ltd@mail.com'
smtp_password =  'DALUJQHEPFEXV5ZWXS6R' # 'CZYLGYGMVK2C7DRI3FOG'

def send_email(sender_email, receiver_email, subject, message):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS
        # Login to the SMTP server
        server.login(smtp_username, smtp_password)
        # Send email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
    finally:
        # Close the SMTP server session
        if(server):
            server.quit()

# Example usage:
sender_email = 'communication_ltd@mail.com'
receiver_email = 'stevi.awa@marsoak.com'
subject = 'Test Email'
message = 'This is a test email from Python SMTP server.'

send_email(sender_email, receiver_email, subject, message)
