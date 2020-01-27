from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
import os


class smtp:

    def smtp(self, emailid, message):
        """
        Here message of reset link is sent to user
        email:param emailid:
        link message:param message:
        no :return:
        """
        s = smtplib.SMTP(os.getenv("SMTP_EXCHANGE_SERVER"), os.getenv("SMTP_EXCHANGE_PORT"))
        s.starttls()
        s.login(os.getenv("SMTP_EXCHANGE_USER_LOGIN"), os.getenv("SMTP_EXCHANGE_USER_PASSWORD"))
        msg = MIMEText(message)
        s.sendmail(os.getenv("SMTP_EXCHANGE_USER_LOGIN"), emailid, msg.as_string())
        s.quit()
