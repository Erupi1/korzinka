from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
from db import UserDB, init_db

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Вход в систему')
        self.setFixedSize(300, 320)
        self.user_db = UserDB()
        self.init_ui()
        self.check_first_user()
        self.user_info = None

    def init_ui(self):
        layout = QVBoxLayout()
        # --- Логотип ---
        logo_label = QLabel()
        logo_path = os.path.join('resources', 'logo.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap.scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo_label.setText('🛒')
            logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        # --- Название магазина ---
        title = QLabel('Корзинка')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 20px; font-weight: bold; color: #388e3c;')
        layout.addWidget(title)
        self.label = QLabel('Авторизация')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText('Логин')
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText('Пароль')
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.login_btn = QPushButton('Войти')
        self.login_btn.clicked.connect(self.try_login)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)

    def check_first_user(self):
        users = self.user_db.get_all_users()
        if not users:
            self.label.setText('Создайте первого администратора')
            self.login_btn.setText('Создать')
            self.login_btn.clicked.disconnect()
            self.login_btn.clicked.connect(self.create_admin)

    def create_admin(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        if not username or not password:
            QMessageBox.warning(self, 'Ошибка', 'Введите логин и пароль!')
            return
        try:
            self.user_db.add_user(username, password, 'admin')
            QMessageBox.information(self, 'Успех', 'Администратор создан! Теперь войдите.')
            self.label.setText('Авторизация')
            self.login_btn.setText('Войти')
            self.login_btn.clicked.disconnect()
            self.login_btn.clicked.connect(self.try_login)
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось создать пользователя: {e}')

    def try_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        if not username or not password:
            QMessageBox.warning(self, 'Ошибка', 'Введите логин и пароль!')
            return
        user = self.user_db.authenticate(username, password)
        if user:
            self.user_info = user
            self.accept()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль!') 