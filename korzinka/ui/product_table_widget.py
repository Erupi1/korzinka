from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QPushButton, QComboBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from db import ProductDB

class ProductTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = ProductDB()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()
        # --- Фильтры и поиск ---
        filter_layout = QHBoxLayout()
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText('Название')
        self.search_barcode = QLineEdit()
        self.search_barcode.setPlaceholderText('Штрихкод')
        self.status_filter = QComboBox()
        self.status_filter.addItems(['Все', 'on_shelf', 'removed'])
        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDisplayFormat('yyyy-MM-dd')
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.setToolTip('Фильтр по дате производства')
        self.btn_search = QPushButton('Поиск')
        self.btn_search.clicked.connect(self.load_data)
        filter_layout.addWidget(QLabel('Фильтры:'))
        filter_layout.addWidget(self.search_name)
        filter_layout.addWidget(self.search_barcode)
        filter_layout.addWidget(QLabel('Статус:'))
        filter_layout.addWidget(self.status_filter)
        filter_layout.addWidget(QLabel('Дата:'))
        filter_layout.addWidget(self.date_filter)
        filter_layout.addWidget(self.btn_search)
        # --- Таблица ---
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Название', 'Штрихкод', 'Дата производства', 'Срок годности', 'Количество', 'Дата напоминания'
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        # --- Компоновка ---
        layout.addLayout(filter_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_data(self):
        name = self.search_name.text().strip().lower()
        barcode = self.search_barcode.text().strip()
        status = self.status_filter.currentText()
        date = self.date_filter.date().toString('yyyy-MM-dd')
        # Получаем все товары
        products = self.db.get_all_products()
        # Фильтрация
        filtered = []
        for p in products:
            if name and name not in p[1].lower():
                continue
            if barcode and barcode not in (p[2] or ''):
                continue
            if status != 'Все' and p[7] != status:
                continue
            if date and p[3] != date:
                continue
            filtered.append(p)
        self.table.setRowCount(len(filtered))
        for row, p in enumerate(filtered):
            for col in range(7):
                self.table.setItem(row, col, QTableWidgetItem(str(p[col]))) 