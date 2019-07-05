from smtplib import SMTPResponseException
from socket import error as socket_error

from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend

from conf.utils import get_site_setting


class EmailBackend(DjangoEmailBackend):
    """
    Handles emails using Site-based settings from Conf.
    """

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(
            host=get_site_setting("smtp_host"),
            port=get_site_setting("smtp_port"),
            username=get_site_setting("smtp_user"),
            password=get_site_setting("smtp_password"),
            use_tls=get_site_setting("use_tls"),
            fail_silently=fail_silently,
            **kwargs
        )

    def send_messages(self, email_messages):
        """
        Override the from_email property all email messages.
        """
        if not email_messages:
            return
        with self._lock:
            for message in email_messages:
                message.from_email = get_site_setting("smtp_from_address")
        try:
            super().send_messages(email_messages)
        except (SMTPResponseException, socket_error) as e:
            # TODO: Determine how to handle failures gracefully.
            raise e
