import io
import os
import sys
from contextlib import redirect_stdout
from traceback import print_exc
from urllib.parse import urljoin

from charm.adapters.abenc_adapt_hybrid import HybridABEnc
from charm.core.engine.util import bytesToObject, objectToBytes
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import (QApplication, QDialog, QFileDialog, QMainWindow,
                             QMessageBox)
from requests import Session

from ui.login import Ui_dlg_login
from ui.main import Ui_main_window

AUTHORITY_SERVER_URL = "http://localhost:2808/"

ENCRYPTED_FILES_FOLDER = "encrypted_files"
DECRYPTED_FILES_FOLDER = "decrypted_files"
DOWNLOADED_FILES_FOLDER = "downloaded_files"


class LoginWindow(QDialog, Ui_dlg_login):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent

    @pyqtSlot()
    def on_btn_login_clicked(self):
        try:
            r = self.parent.session.post(
                urljoin(AUTHORITY_SERVER_URL, "/api/login"),
                json={"username": self.le_username.text(), "password": self.le_password.text()},
            )
        except Exception:
            print_exc()
            self.popup("Please check your internet connection!", "Failed to conenct to server")
            return

        if r.status_code == 200:
            self.accept()
        else:
            self.popup(r.text, "Failed to login")

    @pyqtSlot()
    def on_btn_cancel_clicked(self):
        self.reject()

    def popup(self, message, title="Error"):
        window = QMessageBox(self)
        window.setWindowTitle(title)
        window.setText(message)
        window.exec()


class MainWindow(QMainWindow, Ui_main_window):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.pairing_group = PairingGroup("SS512")
        self.hyb_abe = HybridABEnc(CPabe_BSW07(self.pairing_group), self.pairing_group)

        self.session = Session()
        self.login()

    @pyqtSlot()
    def on_act_logout_triggered(self):
        self.token = self.public_key = self.secret_key = None
        self.hide()
        self.login()

    @pyqtSlot()
    def on_act_quit_triggered(self):
        sys.exit()

    @pyqtSlot()
    def on_btn_browse_encrypt_file_clicked(self):
        self.browse_file(self.le_encrypt_file)

    @pyqtSlot()
    def on_btn_browse_decrypt_file_clicked(self):
        self.browse_file(self.le_decrypt_file)

    @pyqtSlot()
    def on_btn_encrypt_clicked(self):
        if not self.public_key or not self.secret_key:
            self.popup("No key found!")
            return

        policy = self.pte_policy.toPlainText()
        if not policy:
            self.popup("Policy can not be empty!")
            return

        file_name = self.le_encrypt_file.text()
        content = self.open_file(file_name)
        if not content:
            return

        os.makedirs(ENCRYPTED_FILES_FOLDER, exist_ok=True)

        try:
            f = io.StringIO()
            with redirect_stdout(f):
                enc = self.hyb_abe.encrypt(self.public_key, content, policy)

            if f.getvalue():
                raise Exception
        except Exception:
            print_exc()
            self.popup("Please double check your access policy", "Encryption Failed")
            return

        with open(os.path.join(ENCRYPTED_FILES_FOLDER, os.path.basename(file_name)) + ".enc", "wb") as f:
            f.write(objectToBytes(enc, self.pairing_group))

        self.popup("Encrypted successfully!", "Encryption Successful")

    @pyqtSlot()
    def on_btn_decrypt_clicked(self):
        if not self.public_key or not self.secret_key:
            self.popup("No key found!")
            return

        file_name = self.le_decrypt_file.text()
        content = self.open_file(file_name)
        if not content:
            return

        path, ext = os.path.splitext(file_name)
        if ext == ".enc":
            file_name = path

        os.makedirs(DECRYPTED_FILES_FOLDER, exist_ok=True)

        try:
            with open(os.path.join(DECRYPTED_FILES_FOLDER, os.path.basename(file_name)), "wb") as f:
                f.write(
                    self.hyb_abe.decrypt(self.public_key, self.secret_key, bytesToObject(content, self.pairing_group))
                )

            self.popup("Decrypted successfully!", "Decryption Successful")
        except Exception:
            print_exc()
            self.popup(
                "You may not have the necessary permissions to decrypt this file",
                "Decryption Failed",
            )

    def login(self):
        if LoginWindow(self).exec():
            self.show()
            self.get_keys_from_server()
        else:
            sys.exit()

    def browse_file(self, line_edit):
        path, _ = QFileDialog.getOpenFileName(self, filter="All files (*.*)")
        if path:
            line_edit.setText(path)

    def open_file(self, file_name):
        try:
            with open(file_name, "rb") as f:
                return f.read()
        except Exception:
            print_exc()
            self.popup(f"Cannot access {file_name}: No such file or directory")
            return None

    def get_keys_from_server(self):
        data = self.session.get(urljoin(AUTHORITY_SERVER_URL, "api/parameters")).json()

        self.token = data["token"]
        self.public_key = bytesToObject(data["public_key"], self.pairing_group)
        self.secret_key = bytesToObject(data["secret_key"], self.pairing_group)

    def popup(self, message, title="Error"):
        window = QMessageBox(self)
        window.setWindowTitle(title)
        window.setText(message)
        window.exec()


app = QApplication(sys.argv)
main = MainWindow()
sys.exit(app.exec())
