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
                             QMessageBox, QTableWidgetItem)
from requests import Session

from ui.login import Ui_dlg_login
from ui.main import Ui_main_window

AUTHORITY_SERVER_URL = "http://localhost:2808/"
CLOUD_SERVER_URL = "http://localhost:2809/"
DOWNLOAD_LOCATION = "downloads"


class LoginWindow(QDialog, Ui_dlg_login):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.le_username.setText("admin")
        self.le_password.setText("password")

    @pyqtSlot()
    def on_btn_login_clicked(self):
        resp = self.parent.make_request(
            urljoin(AUTHORITY_SERVER_URL, "/api/login"),
            {"username": self.le_username.text(), "password": self.le_password.text()},
        )
        if resp is None:
            return

        if resp.status_code == 200:
            self.accept()
        else:
            self.popup(resp.text, "Failed to login")

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
        self.cb_table.currentIndexChanged.emit(self.cb_table.currentIndex())

        self.pairing_group = PairingGroup("SS512")
        self.hyb_abe = HybridABEnc(CPabe_BSW07(self.pairing_group), self.pairing_group)

        self.session = Session()
        self.login()

    @pyqtSlot()
    def on_act_change_password_triggered(self):
        # TODO: change password
        pass

    @pyqtSlot()
    def on_act_logout_triggered(self):
        self.token = self.public_key = self.secret_key = None
        self.hide()
        self.login()

    @pyqtSlot()
    def on_act_quit_triggered(self):
        sys.exit()

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, _):
        self.cb_table.currentIndexChanged.emit(self.cb_table.currentIndex())

    @pyqtSlot(int)
    def on_cb_table_currentIndexChanged(self, index):
        if self.tabWidget.currentIndex():
            self.lbl_description.show()
            self.le_description.show()
            if index:
                self.lbl_date_of_birth.hide()
                self.le_date_of_birth.hide()
                self.lbl_address.hide()
                self.le_address.hide()
            else:
                self.lbl_date_of_birth.show()
                self.le_date_of_birth.show()
                self.lbl_address.show()
                self.le_address.show()
        else:
            self.lbl_description.hide()
            self.le_description.hide()
            if index:
                self.lbl_date_of_birth.hide()
                self.le_date_of_birth.hide()
                self.lbl_address.hide()
                self.le_address.hide()
            else:
                self.lbl_date_of_birth.show()
                self.le_date_of_birth.show()
                self.lbl_address.show()
                self.le_address.show()

    @pyqtSlot()
    def on_btn_browse_clicked(self):
        path, _ = QFileDialog.getOpenFileName(self, filter="All files (*.*)")
        if path:
            self.le_file_name.setText(path)

    @pyqtSlot()
    def on_btn_download_clicked(self):
        item_id = self.tb_found_items.item(self.tb_found_items.currentRow(), 0).text()
        resp = self.make_request(
            urljoin(CLOUD_SERVER_URL, "pull"), {"table": self.cb_table.currentText(), "id": int(item_id)}
        )
        if resp is None or resp == []:
            return

        resp = resp.json()[0]
        try:
            decrypted_data = self.hyb_abe.decrypt(
                self.public_key, self.secret_key, bytesToObject(resp["data"], self.pairing_group)
            )
        except Exception:
            print_exc()
            self.popup("You may not have the necessary permissions to decrypt this file", "Decryption Failed")
            return

        os.makedirs(DOWNLOAD_LOCATION, exist_ok=True)
        with open(os.path.join(DOWNLOAD_LOCATION, resp["file_name"]), "wb") as f:
            f.write(decrypted_data)

        self.popup("Downloaded and decrypted successfully!", "Successful")

    @pyqtSlot()
    def on_btn_search_clicked(self):
        data = {
            "table": self.cb_table.currentText(),
            "uid": self.le_uid.text(),
            "name": self.le_name.text(),
            "address": self.le_address.text(),
            "date_of_birth": self.le_date_of_birth.text(),
        }

        resp = self.make_request(urljoin(CLOUD_SERVER_URL, "search"), data)
        if resp is None:
            return

        self.tb_found_items.clearContents()
        self.tb_found_items.setRowCount(0)

        for item in resp.json():
            pos = self.tb_found_items.rowCount()
            self.tb_found_items.insertRow(pos)
            self.tb_found_items.setItem(pos, 0, QTableWidgetItem(str(item["id"])))
            self.tb_found_items.setItem(pos, 1, QTableWidgetItem(item["name"]))
            self.tb_found_items.setItem(pos, 2, QTableWidgetItem(item["file_name"]))
            self.tb_found_items.setItem(pos, 3, QTableWidgetItem(item["description"]))
            self.tb_found_items.setItem(pos, 4, QTableWidgetItem(item["last_modified"]))

    @pyqtSlot()
    def on_btn_upload_clicked(self):
        policy = self.pte_policy.toPlainText()
        if not policy:
            self.popup("Policy can not be empty!")
            return

        if not self.le_file_name.text():
            self.popup("Please select a file to upload")
            return

        try:
            with open(self.le_file_name.text(), "rb") as f:
                content = f.read()
        except Exception:
            print_exc()
            self.popup(f"Cannot access {self.le_file_name.text()}: No such file or directory")
            return

        try:
            f = io.StringIO()
            with redirect_stdout(f):
                encrypted_data = self.hyb_abe.encrypt(self.public_key, content, policy)

            if f.getvalue():
                raise Exception
        except Exception:
            print_exc()
            self.popup("Please double check your access policy", "Encryption Failed")
            return

        data = {
            "table": self.cb_table.currentText(),
            "uid": int(self.le_uid.text()),
            "name": self.le_name.text(),
            "address": self.le_address.text(),
            "date_of_birth": self.le_date_of_birth.text(),
            "description": self.le_description.text(),
            "file_name": os.path.basename(self.le_file_name.text()),
            "data": objectToBytes(encrypted_data, self.pairing_group).decode(),
        }

        resp = self.make_request(urljoin(CLOUD_SERVER_URL, "push"), data)
        if resp is None:
            return

        if resp.status_code == 200:
            self.popup(resp.text, "Uploaded Successfully")
        else:
            self.popup(resp.text, "Failed to upload")

    def login(self):
        if LoginWindow(self).exec():
            self.show()
            self.get_keys_from_server()
        else:
            sys.exit()

    def make_request(self, url, data={}):
        try:
            if data:
                return self.session.post(url, json=data)
            return self.session.get(url)
        except Exception:
            print_exc()
            self.popup("Please check your internet connection!", "Failed to conenct to server")
            return None

    def get_keys_from_server(self):
        resp = self.make_request(urljoin(AUTHORITY_SERVER_URL, "api/parameters"))
        if resp is None:
            return

        resp = resp.json()

        self.session.headers["Authorization"] = "Bearer " + resp["token"]
        self.public_key = bytesToObject(resp["public_key"], self.pairing_group)
        self.secret_key = bytesToObject(resp["secret_key"], self.pairing_group)

    def popup(self, message, title="Error"):
        window = QMessageBox(self)
        window.setWindowTitle(title)
        window.setText(message)
        window.exec()


app = QApplication(sys.argv)
main = MainWindow()
sys.exit(app.exec())
