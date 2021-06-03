from pydantic import BaseModel
from modelMM import PenMMRESTRequestModel
from mmconf import PenMMConfigModel
from typing import Optional
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
            ret = await _sendmsg(self.config, request)

async def _sendmsg(
        config: PenMMConfigModel,
        request: PenMMRESTRequestModel
        ) -> bool:
    #
    url = f"{config.public_api_url}/2/x/{request.xpath}"
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
    guide_text = f"""
このメールは患者XXXシステムのご利用を開始した方にお送りしております。
心当たりがない場合は、お手数ですが破棄して下さい。

{request.name} 様、

下記リンクは、行動履歴入力のためのアドレスです。

    {url}

クリックすると認証画面が表示されますので、
初期登録で入力した {request.name} 様の
誕生日の月日と色を入力して下さい。

その後、行動履歴を入力する画面に進みます。

添付のQRコードは上記アドレスと同じものです。
必要であれば利用して下さい。

下記3つの「ひらがなコード」は看護師に尋ねられた場合にお伝え下さい。

    {request.c3w_words}

お手数をおかけいたしますが、
ご協力の程、よろしくお願いいたします。

連絡先: xxx at xxx.xxx
"""

    msg_t = MIMEText(guide_text, "plain")
    msg_a.attach(msg_t)

    guide_html = f"""
<html>
  <head>
    <style>
      div {{ margin: 0 0 10px 2px }}
      .focus {{ margin: 5px 0 15px 15px; font-size: large; font-weight: bold; }}
      .preamble {{ margin: 0 auto 10px 5px; font-size: x-small; }}
      #qrcode {{ display: block; margin-left:auto; margin-right:auto }}
      hr {{ width: 80%; margin: 10px auto 10px 0 }}
    </style>
  </head>
  <body>

    <div class="preamble">
        このメールは患者XXXシステムの
        ご利用を開始した方にお送りしております。
    </div>

    <div class="preamble">
        心当たりがない場合は、お手数ですが破棄して頂けますと幸いです。
    </div>

    <hr>

    <h3>{request.name} 様、</h3>

    <div>
        行動履歴を入力するためには下記のリンクをクリックして下さい。
    </div>

    <div class="focus">
        <a href="{url}">行動履歴入力へのリンク</a>
    </div>

    <div>
        クリックすると認証画面が表示されます。
    <div>

    </div>
        初期登録で入力した {request.name} 様の
        誕生日の月日と色を入力して下さい。
    </div>

    <div>
        その後、行動履歴を入力する画面に進みます。
    </div>

    <div>
        添付のQRコードは上記アドレスと同じものです。
        必要であれば利用して下さい。
    </div>

    <div>
        下記3つの「ひらがなコード」は看護師に尋ねられた場合にお伝え下さい。
    </div>

    <div class="focus">
        {request.c3w_words}
    </div>

    <div>
        お手数をおかけいたしますが、
        ご協力の程、よろしくお願いいたします。
    </div>

    <div>
        {config.mail_reference}
    </div>

    <div>
        <img id="qrcode" src="data:image/png;base64,{qrcode_b64}" />
    </div>

  </body>
</html>
    """
    msg_a.attach(MIMEText(guide_html, "html"))
    mime_msg.attach(msg_a)

    msg_img = MIMEImage(qrcode_raw)
    msg_img.add_header("Content-ID", "<qrcode.png>")
    mime_msg.attach(msg_img)

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
    await smtp.login(config.mail_username, config.mail_password)
    await smtp.send_message(mime_msg)
    await smtp.quit()

    return True
