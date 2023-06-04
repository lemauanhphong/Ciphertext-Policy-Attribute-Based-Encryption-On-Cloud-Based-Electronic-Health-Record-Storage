import os
import sys
from traceback import print_exc

from charm.adapters.abenc_adapt_hybrid import HybridABEnc
from charm.core.engine.util import bytesToObject, objectToBytes
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow, QMessageBox
from ui.login import Ui_dlg_login
from ui.main import Ui_main_window

AUTHORITY_SERVER_URL = "http://localhost"

KEYS_FILE_NAME = ".keys"
DOWNLOAD_FOLDER = "downloaded_files"
ENCRYPT_FOLDER = "encrypted_files"
DECRYPT_FOLDER = "decrypted_files"


class LoginWindow(QDialog, Ui_dlg_login):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_btn_login_clicked(self):
        pass

    @pyqtSlot()
    def on_btn_cancel_clicked(self):
        self.reject()


class MainWindow(QMainWindow, Ui_main_window):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_abe()

    @pyqtSlot()
    def on_act_login_triggered(self):
        print("login")
        window = LoginWindow(self)
        if window.exec():
            self.get_keys_from_server()
            self.load_keys_from_file()

    @pyqtSlot()
    def on_act_logout_triggered(self):
        if os.path.isfile(KEYS_FILE_NAME):
            os.remove(KEYS_FILE_NAME)

    @pyqtSlot()
    def on_btn_browse_encrypt_file_clicked(self):
        self.browse_file(self.le_encrypt_file)

    @pyqtSlot()
    def on_btn_browse_decrypt_file_clicked(self):
        self.browse_file(self.le_decrypt_file)

    @pyqtSlot()
    def on_btn_encrypt_clicked(self):
        if not self.public_key or not self.private_key:
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

        os.makedirs(ENCRYPT_FOLDER, exist_ok=True)
        with open(os.path.join(ENCRYPT_FOLDER, os.path.basename(file_name)) + ".enc", "wb") as f:
            f.write(objectToBytes(self.hyb_abe.encrypt(self.public_key, content, policy), self.pairing_group))

        self.popup("Encrypted successfully!", "Encryption")

    @pyqtSlot()
    def on_btn_decrypt_clicked(self):
        if not self.public_key or not self.private_key:
            self.popup("No key found!")
            return

        file_name = self.le_decrypt_file.text()
        content = self.open_file(file_name)
        if not content:
            return

        path, ext = os.path.splitext(file_name)
        if ext == ".enc":
            file_name = path

        os.makedirs(DECRYPT_FOLDER, exist_ok=True)
        with open(os.path.join(DECRYPT_FOLDER, os.path.basename(file_name)), "wb") as f:
            f.write(self.hyb_abe.decrypt(self.public_key, self.private_key, bytesToObject(content, self.pairing_group)))

        self.popup("Decrypted successfully!", "Decryption")

    def browse_file(self, line_edit):
        path = QFileDialog.getOpenFileName(self, filter="All files (*.*)")[0]
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

    def init_abe(self):
        self.pairing_group = PairingGroup("SS512")
        self.hyb_abe = HybridABEnc(CPabe_BSW07(self.pairing_group), self.pairing_group)
        self.public_key = self.private_key = None
        self.load_keys_from_file()

    def get_keys_from_server(self):
        pass

    def load_keys_from_file(self, file_name=KEYS_FILE_NAME):
        try:
            with open(file_name, "rb") as f:
                content = f.read().splitlines()
                self.public_key = bytesToObject(content[0], self.pairing_group)
                self.private_key = bytesToObject(content[1], self.pairing_group)
        except Exception:
            pass

    def popup(self, message, title="Error"):
        window = QMessageBox(self)
        window.setWindowTitle(title)
        window.setText(message)
        window.exec()


app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec())
