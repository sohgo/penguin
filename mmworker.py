from pydantic import BaseModel
from modelMM import PenMMRESTRequestModel
from mmconf import PenMMConfigModel
from typing import Optional
import aiofile
# qrcode
import qrcode
from io import BytesIO
from base64 import b64encode
# mime
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.utils import make_msgid
from base64 import b64encode
# mail
import aiosmtplib
import ssl

async def read_file(file_path):
    async with aiofile.async_open(file_path, "r") as fd:
        content = await fd.read()
        return content

class SendMessage():
    def __init__(self, config):
        self.config = config

    async def request(self,
                      request: PenMMRESTRequestModel
                      ) -> bool:
        if self.config.queue.qsize == self.config.max_queue_size:
            return False
        await self.config.queue.put(request)
        return True

    async def worker(self):
        while True:
            # queue the request, and return True if successful.
            request = await self.config.queue.get()
            try:
                ret = await _sendmsg(self.config, request)
                self.config.logger.info(
                        f"message for Step2 sent to {request.emailAddr}")
            except Exception as e:
                self.config.logger.error(f"sendmsg: {e}")

async def _sendmsg(
        config: PenMMConfigModel,
        request: PenMMRESTRequestModel
        ) -> bool:
    #
    url = f"{config.public_fe_url}/2/x/{request.xpath}"
    #
    # QR code
    #
    img = qrcode.make(url)
    img = img.resize((192,192))
    #img.save("qrcode.png")
    buf = BytesIO()
    img.save(buf, format="PNG")
    qrcode_raw = buf.getvalue()
    buf.close()
    qrcode_b64 = b64encode(qrcode_raw).decode()
    config.logger.debug("sendmsg: generating qrcode done.")

    #
    # mail
    #
    mime_msg = MIMEMultipart("related")
    mime_msg["To"] = request.emailAddr
    mime_msg["From"] = config.mail_from
    if config.mail_bcc:
        mime_msg["Bcc"] = config.mail_bcc
    mime_msg["Subject"] = config.mail_subject

    msg_a = MIMEMultipart("alternative")

    guide_text_template = await read_file(config.mail_body_text_path)
    guide_text = guide_text_template.format(**vars())
    msg_t = MIMEText(guide_text, "plain")
    msg_a.attach(msg_t)

    guide_html_template = await read_file(config.mail_body_html_path)
    guide_html = guide_html_template.format(**vars())
    config.logger.debug(f"TEXT: {guide_text}")
    config.logger.debug(f"HTML: {guide_html}")
    msg_a.attach(MIMEText(guide_html, "html"))
    mime_msg.attach(msg_a)

    msg_img = MIMEImage(qrcode_raw)
    msg_img.add_header("Content-ID", "<qrcode.png>")
    mime_msg.attach(msg_img)
    config.logger.debug("sendmsg: generating message done.")

    # send mail.
    # NOTE: use_tls must be False if starttls is used.
    smtp = aiosmtplib.SMTP(hostname=config.smtp_server,
                           port=config.smtp_port,
                           use_tls=False)
    await smtp.connect()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    # XXX TBD
    context.verify_mode = ssl.CERT_NONE
    await smtp.starttls(tls_context=context)
    config.logger.debug("sendmsg: starttls done.")
    await smtp.login(config.mail_username, config.mail_password)
    await smtp.send_message(mime_msg)
    await smtp.quit()

    return True
