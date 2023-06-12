import asyncio
import email
import imaplib
import smtplib
import sys
from traceback import print_exc

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem
from ui.login import Ui_dl_login
from ui.mail_content import Ui_dlg_mail_content
from ui.main_window import Ui_main_window


def show_popup(parent, tittle, message):
    window = QMessageBox(parent)
    window.setWindowTitle(tittle)
    window.setText(message)
    window.exec()


class MailContentWindow(QDialog, Ui_dlg_mail_content):
    def __init__(self, parent, content):
        super().__init__(parent)
        self.setupUi(self)
        self.te_content.setText(content)


class LoginWindow(QDialog, Ui_dl_login):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setupUi(self)

    @pyqtSlot()
    def on_btn_login_clicked(self):
        asyncio.run(self.login())

    @pyqtSlot()
    def on_btn_cancel_clicked(self):
        self.reject()

    @property
    def email(self):
        return self.le_email.text()

    async def login(self):
        email = self.le_email.text()
        passwd = self.le_password.text()
        self.btn_login.setDisabled(True)

        try:
            self.parent.smtp = smtplib.SMTP(self.le_smtp_server.text(), int(self.le_smtp_port.text()))
            self.parent.smtp.ehlo()
            self.parent.smtp.starttls()
            self.parent.smtp.login(email, passwd)

            try:
                self.parent.imap = imaplib.IMAP4(self.le_imap_server.text(), int(self.le_imap_port.text()))
                self.parent.imap.login(email, passwd)
            except Exception:
                try:
                    self.parent.imap = imaplib.IMAP4_SSL(self.le_imap_server.text(), int(self.le_imap_port.text()))
                    self.parent.imap.login(email, passwd)
                except Exception:
                    raise Exception

            self.btn_login.setDisabled(False)
        except Exception:
            print_exc()
            show_popup(self, "Login", "Failed to login! Please check your info!")
            self.btn_login.setDisabled(False)
            return

        show_popup(self, "Login", "Login successfully!")
        self.accept()


class MainWindow(QMainWindow, Ui_main_window):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.smtp: smtplib.SMTP
        self.imap: imaplib.IMAP4
        self.mail_content = []
        self.login()

    def login(self):
        self.hide()
        login_window = LoginWindow(self)
        if login_window.exec():
            self.email = login_window.email
            self.show()
        else:
            sys.exit()

    @pyqtSlot()
    def on_btn_reload_clicked(self):
        self.tb_mailbox.clearContents()
        self.tb_mailbox.setRowCount(0)

        self.lbl_total.setText("0")
        self.lbl_recent.setText("0")

        self.imap.select("INBOX")
        index = self.imap.search(None, "UNSEEN")[1]
        self.unseen = index[0].split()
        self.lbl_recent.setText(str(len(self.unseen)))

        index = self.imap.search(None, "ALL")[1]
        self.lbl_total.setText(str(len(index[0].split())))

        for email_id in index[0].split():
            msg = self.imap.fetch(email_id, "(BODY.PEEK[])")[1]
            msg = email.message_from_bytes(msg[0][1])

            pos = self.tb_mailbox.rowCount()
            self.tb_mailbox.insertRow(pos)

            for idx, header in enumerate(["Subject", "From", "Date"]):
                self.tb_mailbox.setItem(
                    pos, idx, QTableWidgetItem(str(email.header.make_header(email.header.decode_header(msg[header]))))
                )

            content = ""
            for part in msg.walk():
                charset = part.get_content_charset()
                if part.get_content_type() == "text/plain":
                    content += part.get_payload(decode=True).decode(charset)

            self.mail_content.append(content)

        self.tb_mailbox.resizeColumnsToContents()

    @pyqtSlot(int, int)
    def on_tb_mailbox_cellClicked(self, row, _):
        window = MailContentWindow(self, self.mail_content[row])
        window.exec()
        row = str(row + 1).encode()
        if row in self.unseen:
            asyncio.run(self.set_email_as_seen(row))

    @pyqtSlot()
    def on_btn_send_clicked(self):
        TO = self.le_to.text().replace(" ", "").split(",")
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (
            self.email,
            ", ".join(TO),
            self.le_subject.text(),
            self.pte_body.toPlainText(),
        )
        try:
            self.smtp.sendmail(self.email, TO, message)
            show_popup(self, "Send email", "Successfully sent the email!")
        except Exception:
            print_exc()
            show_popup(self, "Send email", "Failed to send email!")

    async def set_email_as_seen(self, index):
        self.imap.store(index.decode(), "+FLAGS", "\\Seen")
        self.lbl_recent.setText(str(int(self.lbl_recent.text()) - 1))
        self.unseen.remove(index)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
