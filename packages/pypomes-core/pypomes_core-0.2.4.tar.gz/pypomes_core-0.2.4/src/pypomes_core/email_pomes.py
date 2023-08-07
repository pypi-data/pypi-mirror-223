import sys
from email.message import EmailMessage
from smtplib import SMTP
from typing import Final
from .env_pomes import APP_PREFIX, env_get_str, env_get_int

EMAIL_ACCOUNT: Final[str] = env_get_str(f"{APP_PREFIX}_EMAIL_ACCOUNT")
EMAIL_PWD: Final[str] = env_get_str(f"{APP_PREFIX}_EMAIL_PWD")
EMAIL_PORT: Final[int] = env_get_int(f"{APP_PREFIX}_EMAIL_PORT")
EMAIL_SERVER: Final[str] = env_get_str(f"{APP_PREFIX}_EMAIL_SERVER")


def email_send(errors: list[str], user_email: str, subject: str, content: str) -> None:
    """
    Send email, to *user_email", with *subject* as the email subject, and *content* as the email message.

    :param errors: incidental error messages
    :param user_email: the address to send the email to
    :param subject: the email subject
    :param content: the email message
    """
    # import needed function
    from .exception_pomes import exc_format

    # build the email object
    email_msg = EmailMessage()
    email_msg.set_content(content)
    email_msg["Subject"] = subject
    email_msg["From"] = EMAIL_ACCOUNT
    email_msg["To"] = user_email

    # instanciate the email server
    server = SMTP(host=EMAIL_SERVER, port=EMAIL_PORT)
    server.starttls()
    server.login(user=EMAIL_ACCOUNT, password=EMAIL_PWD)

    # send the message
    try:
        server.send_message(email_msg)
        server.quit()
    except Exception as e:
        # the operatin raised an exception
        errors.append(f"Error sending the email: {exc_format(e, sys.exc_info())}")
