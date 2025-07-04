from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QLabel, QMessageBox
from db import UserDB

class UserManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Управление пользователями')
        self.setFixedSize(500, 400)
        self.user_db = UserDB()
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Логин', 'Роль'])
        layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton('Добавить')
        self.btn_delete = QPushButton('Удалить')
        self.btn_change_pw = QPushButton('Сменить пароль')
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_change_pw)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.refresh_table()
        self.btn_add.clicked.connect(self.add_user)
        self.btn_delete.clicked.connect(self.delete_user)
        self.btn_change_pw.clicked.connect(self.change_password)

    def refresh_table(self):
        data = self.user_db.get_users()
        self.table.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_user(self):
        login, ok = QLineEdit.getText(self, 'Добавить пользователя', 'Логин:')
        if not ok or not login:
            return
        password, ok = QLineEdit.getText(self, 'Добавить пользователя', 'Пароль:')
        if not ok or not password:
            return
        role, ok = QLineEdit.getText(self, 'Добавить пользователя', 'Роль (admin/seller):')
        if not ok or role not in ('admin', 'seller'):
            QMessageBox.warning(self, 'Ошибка', 'Роль должна быть admin или seller')
            return
        if self.user_db.add_user(login, password, role):
            self.refresh_table()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пользователь уже существует')

    def delete_user(self):
        row = self.table.currentRow()
        if row == -1:
            return
        username = self.table.item(row, 1).text()
        if username == 'admin':
            QMessageBox.warning(self, 'Ошибка', 'Нельзя удалить администратора')
            return
        if self.user_db.delete_user(username):
            self.refresh_table()

    def change_password(self):
        row = self.table.currentRow()
        if row == -1:
            return
        username = self.table.item(row, 1).text()
        new_pw, ok = QLineEdit.getText(self, 'Сменить пароль', f'Новый пароль для {username}:')
        if not ok or not new_pw:
            return
        if self.user_db.change_password(username, new_pw):
            QMessageBox.information(self, 'Успех', 'Пароль изменён')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Ошибка смены пароля') 