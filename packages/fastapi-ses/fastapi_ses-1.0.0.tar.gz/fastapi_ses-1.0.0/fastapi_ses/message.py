import sys

from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

PY3 = sys.version_info[0] == 3


class EmailMessage:
    """
    Mail message parameters

    :param: subject: Email subject header
    :param: recipients: List of email addresses
    :param: body: Plain text message or HTML message
    :param: alternative_body: Plain text message or HTML message
    :param: template_body: Data to pass into chosen Jinja2 template
    :param: subtype: either "plain" or "html"
    :param: sender: Email sender address
    :param: cc: CC list
    :param: bcc: BCC list
    :param: reply_to: Reply-To list
    :param: attachments: List of attachment instances
    :param: multipart_subtype: either "mixed" or "alternative"
    :param: headers: Dict of custom SMTP headers
    """

    def __init__(self, **kwargs):
        self.sender = kwargs.get("sender", [])
        self.recipients = kwargs.get("recipients", [])
        self.attachments = kwargs.get("attachments", None)
        self.subject = kwargs.get("subject", "")
        self.body = kwargs.get("body", "")
        self.alternative_body = kwargs.get("alternative_body", "")
        self.template_body = kwargs.get("template_body", "")
        self.cc = kwargs.get("cc", [])
        self.bcc = kwargs.get("bcc", [])
        self.reply_to = kwargs.get("reply_to", "")
        self.charset = kwargs.get("charset", "utf-8")
        self.subtype = kwargs.get("subtype", "html")
        self.multipart_subtype = kwargs.get("multipart_subtype", "mixed")
        self.headers = kwargs.get("headers", {})

    def _mimetext(self, text: str, subtype: str) -> MIMEText:
        """
        Creates a MIMEText object
        """
        return MIMEText(text, _subtype=subtype, _charset=self.charset)

    def attach_file(self, message, attachment):
        """
        Creates a MIMEBase object
        """
        for file, file_meta in attachment:
            if file_meta and "mime_type" in file_meta and "mime_subtype" in file_meta:
                part = MIMEBase(
                    _maintype=file_meta["mime_type"], _subtype=file_meta["mime_subtype"]
                )
            else:
                part = MIMEBase(_maintype="application", _subtype="octet-stream")

            part.set_payload(file.read())
            encode_base64(part)
            file.close()

            if file_meta and "headers" in file_meta:
                for header in file_meta["headers"].keys():
                    part.add_header(header, file_meta["headers"][header])

            # Add an implicit `Content-Disposition` attachment header,
            #   but only if it wasn't supplied explicitly.
            #   More info here: https://github.com/sabuhish/fastapi-mail/issues/128
            if not part.get("Content-Disposition"):
                filename = file.filename
                try:
                    filename and filename.encode("ascii")
                except UnicodeEncodeError:
                    if not PY3:
                        filename = filename.encode("utf8")

                filename = ("UTF8", "", filename)
                part.add_header("Content-Disposition", "attachment", filename=filename)

            self.message.attach(part)

    def attach_alternative(self, message: MIMEMultipart) -> MIMEMultipart:
        """
        Attaches an alternative body to a given message
        """

        tmpmsg = message

        tmpmsg.attach(self._mimetext(self.alternative_body, self.subtype))
        message = MIMEMultipart(self.multipart_subtype)
        message.set_charset(self.charset)
        message.attach(tmpmsg)

        return message

    def get_message(self):
        """
        Creates the email message
        """

        self.message = MIMEMultipart(self.multipart_subtype)
        self.message.set_charset(self.charset)

        if self.template_body:
            self.message.attach(self._mimetext(self.template_body, self.subtype))
        elif self.body:
            self.message.attach(self._mimetext(self.body, self.subtype))

        if (
            self.alternative_body is not None
            and self.multipart_subtype == "alternative"
        ):
            self.message = self.attach_alternative(self.message)

        self.message["From"] = self.sender
        self.message["To"] = ", ".join(self.recipients)

        if self.subject:
            self.message["Subject"] = self.subject

        if self.cc:
            self.message["Cc"] = ", ".join(self.cc)

        if self.bcc:
            self.message["Bcc"] = ", ".join(self.bcc)

        if self.reply_to:
            self.message["Reply-To"] = ", ".join(self.reply_to)

        if self.attachments:
            self.attach_file(self.message, self.attachments)

        if self.headers:
            for header_name, header_content in self.headers.items():
                self.message.add_header(header_name, header_content)

        return self.message.as_string()
