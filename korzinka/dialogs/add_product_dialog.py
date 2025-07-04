from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QSpinBox, QMessageBox, QCompleter)
from PyQt5.QtCore import QDate, Qt
from db import ProductDB

class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить товар')
        self.setFixedSize(420, 420)
        self.db = ProductDB()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        # Название
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText('Название *')
        # --- автодополнение ---
        names = self.db.get_all_product_names()
        completer = QCompleter(names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.name_edit.setCompleter(completer)
        completer.activated.connect(self.on_name_selected)
        # Штрихкод
        self.barcode_edit = QLineEdit()
        self.barcode_edit.setPlaceholderText('Штрихкод')
        # Дата производства
        self.prod_date = QDateEdit()
        self.prod_date.setCalendarPopup(True)
        self.prod_date.setDisplayFormat('yyyy-MM-dd')
        self.prod_date.setDate(QDate.currentDate())
        # Срок годности
        self.expiry_date = QDateEdit()
        self.expiry_date.setCalendarPopup(True)
        self.expiry_date.setDisplayFormat('yyyy-MM-dd')
        self.expiry_date.setDate(QDate.currentDate())
        # Количество
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(100000)
        # Дата напоминания
        self.remind_date = QDateEdit()
        self.remind_date.setCalendarPopup(True)
        self.remind_date.setDisplayFormat('yyyy-MM-dd')
        self.remind_date.setDate(QDate.currentDate())
        # Кнопки
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton('Добавить')
        self.btn_cancel = QPushButton('Отмена')
        self.btn_add.clicked.connect(self.add_product)
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_cancel)
        # Компоновка
        layout.addWidget(QLabel('Название *'))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel('Штрихкод'))
        layout.addWidget(self.barcode_edit)
        layout.addWidget(QLabel('Дата производства *'))
        layout.addWidget(self.prod_date)
        layout.addWidget(QLabel('Срок годности *'))
        layout.addWidget(self.expiry_date)
        layout.addWidget(QLabel('Количество *'))
        layout.addWidget(self.quantity_spin)
        layout.addWidget(QLabel('Дата напоминания *'))
        layout.addWidget(self.remind_date)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def add_product(self):
        name = self.name_edit.text().strip()
        barcode = self.barcode_edit.text().strip() or None
        prod_date = self.prod_date.date().toString('yyyy-MM-dd')
        expiry_date = self.expiry_date.date().toString('yyyy-MM-dd')
        quantity = self.quantity_spin.value()
        remind_date = self.remind_date.date().toString('yyyy-MM-dd')
        # Валидация
        if not name or not prod_date or not expiry_date or not quantity or not remind_date:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните все обязательные поля!')
            return
        self.db.add_product(name, barcode, prod_date, expiry_date, quantity, remind_date)
        self.accept()

    def on_name_selected(self, text):
        barcode = self.db.get_barcode_by_name(text)
        if barcode:
            self.barcode_edit.setText(barcode)
        else:
            self.barcode_edit.clear() 