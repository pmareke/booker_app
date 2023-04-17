import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from domain.client_notifier import ClientNotifier
from domain.subscriptions.subscription import Subscriptions


class EmailClientNotifier(ClientNotifier):
    def notify(self, subscriptions: Subscriptions) -> None:
        message_lines = []
        for subscription, books in subscriptions.items():
            titles = [
                f"<li><a href='{book.url}'>{book.title}</a></li>" for book in books
            ]
            message_lines.append(
                "<br>".join(
                    [
                        f"<b>Query: {subscription.upper()}</b>",
                        "<ul>",
                        "<br>".join(titles),
                        "</ul>",
                        "<br>",
                    ]
                )
            )
        if message_lines:
            self._send_email("\n".join(message_lines))

    def _send_email(self, content: str) -> None:
        message = self._create_message(content)
        self._create_session(message)

    @staticmethod
    def _create_message(content: str) -> MIMEMultipart:
        message = MIMEMultipart()
        message["From"] = os.getenv("GMAIL_SENDER")
        message["To"] = os.getenv("GMAIL_RECEIVER")
        message["Subject"] = "Booker updates, there are new books available!"
        message.attach(MIMEText(content, "html"))
        return message

    @staticmethod
    def _create_session(message: MIMEMultipart) -> None:
        address = os.getenv("GMAIL_SENDER")
        assert address
        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()
        password = os.getenv("GMAIL_PASS")
        assert password
        session.login(address, password)
        session.sendmail(address, address, message.as_string())
        session.quit()
