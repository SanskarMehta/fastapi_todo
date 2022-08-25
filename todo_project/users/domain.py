from fastapi_mail import MessageSchema
from typing import List, Dict


class Message:

    @staticmethod
    def generate_msg_schema(subject: str, recipients: List, body: Dict):
        """
        This method generate the message schema.
        :param subject: subject of the message schema.
        :param recipients: emails
        :param body: content of the message schema.
        :return:validate message schema.
        """
        return MessageSchema(subject=subject, recipients=recipients, template_body=body)
