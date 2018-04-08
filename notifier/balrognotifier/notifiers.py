import os
import boto3
import smtplib
from email.message import EmailMessage


class Notifier(object):
    def notify(self, payload, **kwargs):
        raise NotImplementedError()


class EmailNotifier(Notifier):
    def __init__(self, host=None, port=None, user_name=None,
                 password=None, to_addr=None, from_addr=None,
                 use_tls=False):
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.host = host or os.getenv('SMTP_HOST', '')
        self.port = port or os.getenv('SMTP_PORT', '')
        self.user_name = user_name or os.getenv('SMTP_USERNAME', '')
        self.password = password or os.getenv('SMTP_PASSWORD', '')
        self.use_tls = os.getenv('SMTP_TLS', use_tls)    

    def build_mail_message(self, payload, to_addr, from_addr, subject):
        message = EmailMessage()
        message.set_content(payload)
        message['Subject'] = subject
        message['To'] = to_addr
        message['From'] = from_addr
        return message

    def notify(self, payload, **kwargs):
        subject = kwargs.get('subject', 'Untitled')
        to_addr = self.to_addr or kwargs.get('to_addr')
        from_addr = self.from_addr or kwargs.get('from_addr')
        message = self.build_mail_message(
            payload, to_addr, from_addr, subject)
        try:
            with smtplib.SMTP(host=self.host, port=self.port) as smtp:
                smtp.ehlo()
                if self.use_tls:
                    smtp.starttls()
                    conn.ehlo()
                if self.user_name and self.password:
                    smtp.login(self.user_name, self.password)
                smtp.send_message(message)
                # TODO: log exception messages
        except smtplib.SMTPServerDisconnected:
            pass
        except smtplib.SMTPResponseException:
            pass
        except smtplib.SMTPSenderRefused:
            pass
        except smtplib.SMTPRecipientsRefused:
            pass
        except smtplib.SMTPDataError:
            pass
        except smtplib.SMTPConnectError:
            pass
        except smtplib.SMTPHeloError:
            pass
        except smtplib.SMTPAuthenticationError:
            pass
        except Exception:
            pass


class AmazonSNSNotifier(Notifier):
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region=None):
        self.client = boto3.client(
            aws_access_key_id=(aws_access_key_id or os.getenv('AWS_KEY_ID', '')),
            aws_secret_access_key=(aws_secret_access_key or os.getenv('AWS_KEY_SECRET', '')),
            region=(region or os.getenv('AWS_REGION', '')))

    def notify(self, payload, **kwargs):
        # Only for dev, remove later: 
        # https://github.com/boto/boto3/blob/develop/boto3/session.py#L48
        # https://boto3.readthedocs.io/en/latest/reference/services/sns.html
        # https://github.com/boto/botocore/blob/30c96a24796e423b25108e9c72d2c541d4bdf617/botocore/session.py#L734
        raise NotImplementedError()
