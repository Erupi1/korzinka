from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from db import UserDB

class ChangePasswordDialog(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Смена пароля')
        self.setFixedSize(300, 180)
        self.db = UserDB()
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.old_pw = QLineEdit()
        self.old_pw.setPlaceholderText('Старый пароль')
        self.old_pw.setEchoMode(QLineEdit.Password)
        self.new_pw = QLineEdit()
        self.new_pw.setPlaceholderText('Новый пароль')
        self.new_pw.setEchoMode(QLineEdit.Password)
        self.btn_change = QPushButton('Сменить')
        self.btn_change.clicked.connect(self.change_pw)
        layout.addWidget(QLabel('Старый пароль'))
        layout.addWidget(self.old_pw)
        layout.addWidget(QLabel('Новый пароль'))
        layout.addWidget(self.new_pw)
        layout.addWidget(self.btn_change)
        self.setLayout(layout)

    def change_pw(self):
        old = self.old_pw.text().strip()
        new = self.new_pw.text().strip()
        if not old or not new:
            QMessageBox.warning(self, 'Ошибка', 'Заполните оба поля!')
            return
        # Проверка старого пароля
        from db import UserDB
        user_db = UserDB()
        user = user_db.authenticate_by_id(self.user_id, old)
        if not user:
            QMessageBox.warning(self, 'Ошибка', 'Старый пароль неверен!')
            return
        user_db.change_password(self.user_id, new)
        QMessageBox.information(self, 'Успех', 'Пароль изменён!')
        self.accept() 