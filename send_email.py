import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    def __init__(self):
        self.smtp_server = 'vrsksmtp4.veriskdom.com'
        self.smtp_port = 25

    @staticmethod
    def get_otp_email_content(otp):
        subject = "OTP for verification"
        body = "Your otp for verification is : " + str(otp)
        return subject, body

    def send_email(self, subject, body, receiver):
        sender_email = "aayush.niraula@verisk.com"
        recipient_email = receiver
        smtp_server = self.smtp_server
        smtp_port = self.smtp_port

        # instance of MIMEMultipart
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email
        body_part = MIMEText(body)
        msg.attach(body_part)

        success = True
        try:
            # creates SMTP session
            s = smtplib.SMTP(smtp_server, smtp_port)
            # start TLS for security
            s.starttls()
            s.sendmail(sender_email, recipient_email, msg.as_string())
        except Exception as e:
            success = False
            print("Error while sending email: ", e)

        return success
