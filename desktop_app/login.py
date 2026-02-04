from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter
import requests
from api import set_token

import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

TOKEN_URL = "http://127.0.0.1:8001/api/token/"
SIGNUP_URL = "http://127.0.0.1:8001/api/equipment/signup/"

class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        uic.loadUi(resource_path("ui/login.ui"), self)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))

        qt_rectangle = self.frameGeometry()
        center_point = QtWidgets.QApplication.desktop().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        self.txt_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup_confirm.setEchoMode(QtWidgets.QLineEdit.Password)

        self.setup_login_password_toggle()
        self.setup_signup_password_toggle()

        self.stackedWidget.setCurrentIndex(0)

        self.btn_login.clicked.connect(self.handle_login)
        self.btn_signup.clicked.connect(self.show_signup)
        self.btn_back_to_login.clicked.connect(self.show_login)
        self.btn_create_account.clicked.connect(self.handle_signup)

    def show_signup(self):
        self.stackedWidget.setCurrentIndex(1)

    def show_login(self):
        self.clear_signup_fields()
        self.stackedWidget.setCurrentIndex(0)

    def clear_signup_fields(self):
        self.signup_username.clear()
        self.signup_password.clear()
        self.signup_confirm.clear()
        self.chk_signup_show_password.setChecked(False)

    def setup_login_password_toggle(self):
        self.chk_show_password.setText("")
        self.chk_show_password.setStyleSheet("""
            QCheckBox {
                width: 24px;
                height: 24px;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
                border: none;
                background: transparent;
            }
        """)

        self.chk_show_password.stateChanged.connect(self.toggle_login_password)
        self.update_login_eye_icon()

    def update_login_eye_icon(self):
        icon = self.build_eye_icon(self.chk_show_password.isChecked())
        self.chk_show_password.setIcon(icon)
        self.chk_show_password.setIconSize(icon.actualSize(QtCore.QSize(24, 24)))

    def toggle_login_password(self):
        self.txt_password.setEchoMode(
            QtWidgets.QLineEdit.Normal
            if self.chk_show_password.isChecked()
            else QtWidgets.QLineEdit.Password
        )
        self.update_login_eye_icon()

    def setup_signup_password_toggle(self):
        self.chk_signup_show_password.setText("")
        self.chk_signup_show_password.setStyleSheet("""
            QCheckBox {
                width: 24px;
                height: 24px;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
                border: none;
                background: transparent;
            }
        """)

        self.chk_signup_show_password.stateChanged.connect(self.toggle_signup_password)
        self.update_signup_eye_icon()

    def update_signup_eye_icon(self):
        icon = self.build_eye_icon(self.chk_signup_show_password.isChecked())
        self.chk_signup_show_password.setIcon(icon)
        self.chk_signup_show_password.setIconSize(icon.actualSize(QtCore.QSize(24, 24)))

    def toggle_signup_password(self):
        mode = (
            QtWidgets.QLineEdit.Normal
            if self.chk_signup_show_password.isChecked()
            else QtWidgets.QLineEdit.Password
        )

        self.signup_password.setEchoMode(mode)
        self.signup_confirm.setEchoMode(mode)
        self.update_signup_eye_icon()

    def build_eye_icon(self, open_eye: bool) -> QIcon:
        size = 24
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)
        painter.drawEllipse(8, 8, 8, 8)

        painter.setBrush(Qt.darkGray)
        painter.drawEllipse(10, 10, 4, 4)

        if not open_eye:
            painter.setPen(Qt.white)
            painter.drawLine(4, 4, 20, 20)

        painter.end()
        return QIcon(pixmap)

    def handle_signup(self):
        username = self.signup_username.text().strip()
        password = self.signup_password.text().strip()
        confirm = self.signup_confirm.text().strip()

        if not username or not password or not confirm:
            QMessageBox.warning(self, "Error", "All fields are required")
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        self.set_loading(True)

        try:
            response = requests.post(
                SIGNUP_URL,
                data={"username": username, "password": password},
                timeout=5
            )
            response.raise_for_status()

            QMessageBox.information(
                self, "Success", "Account created successfully. Please login."
            )
            self.show_login()

        except requests.RequestException:
            QMessageBox.critical(
                self, "Signup Failed", "Username already exists or server error"
            )
        finally:
            self.set_loading(False)

    def handle_login(self):
        username = self.txt_username.text().strip()
        password = self.txt_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password required")
            return

        self.set_loading(True)

        try:
            response = requests.post(
                TOKEN_URL,
                data={"username": username, "password": password},
                timeout=5
            )
            response.raise_for_status()

            token = response.json()["token"]
            set_token(token)
            self.accept()

        except requests.RequestException:
            QMessageBox.critical(self, "Login Failed", "Invalid credentials")
        finally:
            self.set_loading(False)

    def set_loading(self, loading=True):
        self.btn_login.setEnabled(not loading)
        self.btn_signup.setEnabled(not loading)
        self.btn_create_account.setEnabled(not loading)
        self.btn_back_to_login.setEnabled(not loading)

        if loading:
            QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)
        else:
            QtWidgets.QApplication.restoreOverrideCursor()