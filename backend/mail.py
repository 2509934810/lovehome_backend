import smtplib
from os import path
import os
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import os


class SendMail(object):
    smtp_server = "smtp.qq.com"
    password = "fkgngrwblphqdjah"
    # from_addr = "qq2509934810@163.com"
    from_addr = "2509934810@qq.com"


    def __init__(self, text, sender, receiver, subject, address):
        self.text = text
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.address = address
        self.to_addr = address

        self.msg = MIMEText(self.text, "plain", "utf-8")
        self.msg["From"] = self._format_addr(self.sender + "<" + self.from_addr + ">")
        self.msg["To"] = self._format_addr(self.receiver + "<" + self.to_addr + ">")
        self.msg["Subject"] = Header(self.subject, "utf-8").encode()

    def _format_addr(self, addr):
        name, addr = parseaddr(addr)
        return formataddr((Header(name, "utf-8").encode(), addr))

    def send(self):
        server = smtplib.SMTP_SLL(self.smtp_server, 465)
        # server.set_debuglevel(1)
        server.login("2509934810@qq.com", "fkgngrwblphqdjah")
        server.sendmail("2509934810@qq.com", [self.to_addr], self.msg.as_string())
        server.close()


if __name__ == "__main__":
    client = SendMail(
        text="我是 小类 嘻嘻嘻",
        sender="qq2509934810@163.com",
        receiver="mr zhang",
        subject="authentical_email",
        address="2509934810@qq.com",
    )
    client.send()
