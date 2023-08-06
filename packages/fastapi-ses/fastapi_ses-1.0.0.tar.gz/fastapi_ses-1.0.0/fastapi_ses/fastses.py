"""FastAPI email library for Amazon SES."""

import boto3
import logging

from botocore.exceptions import BotoCoreError, ClientError

from fastapi_ses.message import EmailMessage

__license__ = "MIT"

logger = logging.getLogger(__name__)


class FastSES:
    """An email backend for use with Amazon SES."""

    def __init__(self,
                 region_name=None,
                 access_key_id=None,
                 secret_access_key=None,
                 **kwargs):
        """
        Creates a client for the Amazon SES API.

        Args:
            fail_silently: Flag that determines whether Amazon SES
                client errors should throw an exception.

        """

        self.ses_configuration_set = kwargs.get("ses_configuration_set", None)
        self.fail_silently = kwargs.get("fail_silently", False)
        self.ses_tags = kwargs.get("ses_tags", None)

        self.client = boto3.client(
            "ses",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name,
        )

    def send_messages(self, messages):
        """
        Sends one or more EmailMessage objects and returns the
        number of email messages sent.

        Args:
            messages: A list of EmailMessage objects.
        Returns:
            An integer count of the messages sent.
        Raises:
            ClientError: An interaction with the Amazon SES HTTP API failed.
        """

        if not messages:
            return 0

        sent_message_count = 0

        for message in messages:
            if self.send_email(message):
                sent_message_count += 1

        return sent_message_count

    def send_email(self, message):
        """
        Sends an individual message via the Amazon SES HTTP API.

        Args:
            message: A single EmailMessage object.
        Returns:
            True if the EmailMessage was sent successfully, otherwise False.
        Raises:
            ClientError: An interaction with the Amazon SES HTTP API failed.
        """

        try:
            kwargs = {
                "Source": message.sender,
                "Destinations": message.recipients,
                "RawMessage": {"Data": message.get_message()},
            }

            if self.ses_tags is not None:
                kwargs["Tags"] = self.ses_tags

            if self.ses_configuration_set is not None:
                kwargs["ConfigurationSetName"] = self.ses_configuration_set

            result = self.client.send_raw_email(**kwargs)
        except (ClientError, BotoCoreError) as e:
            if not self.fail_silently:
                raise

            return {"status": False,
                    "response": e.response,
                    "message_id": "undefined",
                    "message": e.response['Error']['Message']}
        else:
            return {"status": True,
                    "response": result,
                    "message_id": result['MessageId'],
                    "message": "Email Successfully Sent."}
