from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QInputDialog)
from db import UserDB

class UserManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Управление пользователями')
        self.setMinimumSize(500, 400)
        self.db = UserDB()
        self.init_ui()
        self.load_users()

    def init_ui(self):
        layout = QVBoxLayout()
        # Таблица пользователей
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Логин', 'Роль'])
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        layout.addWidget(self.table)
        # Форма добавления
        form_layout = QHBoxLayout()
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText('Логин')
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText('Пароль')
        self.role_combo = QComboBox()
        self.role_combo.addItems(['admin', 'seller'])
        self.btn_add = QPushButton('Добавить')
        self.btn_add.clicked.connect(self.add_user)
        form_layout.addWidget(self.username_edit)
        form_layout.addWidget(self.password_edit)
        form_layout.addWidget(self.role_combo)
        form_layout.addWidget(self.btn_add)
        layout.addLayout(form_layout)
        # Кнопки удаления и смены пароля
        btns_layout = QHBoxLayout()
        self.btn_delete = QPushButton('Удалить')
        self.btn_delete.clicked.connect(self.delete_user)
        self.btn_change_pw = QPushButton('Сменить пароль')
        self.btn_change_pw.clicked.connect(self.change_password)
        btns_layout.addWidget(self.btn_delete)
        btns_layout.addWidget(self.btn_change_pw)
        layout.addLayout(btns_layout)
        self.setLayout(layout)

    def load_users(self):
        users = self.db.get_all_users()
        self.table.setRowCount(len(users))
        for row, u in enumerate(users):
            for col in range(3):
                self.table.setItem(row, col, QTableWidgetItem(str(u[col])))

    def add_user(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        role = self.role_combo.currentText()
        if not username or not password:
            QMessageBox.warning(self, 'Ошибка', 'Введите логин и пароль!')
            return
        try:
            self.db.add_user(username, password, role)
            self.load_users()
            self.username_edit.clear()
            self.password_edit.clear()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))

    def delete_user(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите пользователя для удаления!')
            return
        user_id = int(self.table.item(selected, 0).text())
        self.db.delete_user(user_id)
        self.load_users()

    def change_password(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите пользователя!')
            return
        user_id = int(self.table.item(selected, 0).text())
        new_pw, ok = QInputDialog.getText(self, 'Новый пароль', 'Введите новый пароль:')
        if ok and new_pw:
            self.db.change_password(user_id, new_pw)
            QMessageBox.information(self, 'Успех', 'Пароль изменён!') 