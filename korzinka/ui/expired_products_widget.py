from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel)
from PyQt5.QtCore import Qt, QDate
from db import ProductDB

class ExpiredProductsWidget(QWidget):
    def __init__(self, update_expired_count_callback=None):
        super().__init__()
        self.db = ProductDB()
        self.update_expired_count_callback = update_expired_count_callback
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()
        # Красный заголовок
        label = QLabel('Просроченные товары')
        label.setStyleSheet('font-size: 18px; font-weight: bold; color: red;')
        layout.addWidget(label)
        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Название', 'Штрихкод', 'Дата производства', 'Срок годности', 'Количество', 'Дата напоминания'
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.MultiSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        # Кнопки снятия
        self.btn_remove_selected = QPushButton('Снять выделенный с полки')
        self.btn_remove_selected.setStyleSheet('background-color: #ffb300; color: white; font-weight: bold; border-radius: 8px; padding: 8px;')
        self.btn_remove_selected.clicked.connect(self.remove_selected_expired)
        self.btn_remove = QPushButton('Снять все просроченные с полки')
        self.btn_remove.setStyleSheet('background-color: #e53935; color: white; font-weight: bold; border-radius: 8px; padding: 8px;')
        self.btn_remove.clicked.connect(self.remove_all_expired)
        layout.addWidget(self.btn_remove_selected)
        layout.addWidget(self.btn_remove)
        self.setLayout(layout)

    def load_data(self):
        today = QDate.currentDate().toString('yyyy-MM-dd')
        products = self.db.get_expired_products(today)
        self.table.setRowCount(len(products))
        for row, p in enumerate(products):
            for col in range(7):
                item = QTableWidgetItem(str(p[col]))
                self.table.setItem(row, col, item)

    def remove_all_expired(self):
        row_count = self.table.rowCount()
        if row_count == 0:
            QMessageBox.information(self, 'Нет просроченных', 'Нет просроченных товаров для снятия.')
            return
        ids = [int(self.table.item(row, 0).text()) for row in range(row_count)]
        self.db.remove_products(ids)
        QMessageBox.information(self, 'Готово', 'Все просроченные товары сняты с полки!')
        self.load_data()
        if self.update_expired_count_callback:
            self.update_expired_count_callback()

    def remove_selected_expired(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите товар для снятия!')
            return
        id_ = int(self.table.item(selected, 0).text())
        self.db.remove_products([id_])
        QMessageBox.information(self, 'Готово', 'Товар снят с полки!')
        self.load_data()
        if self.update_expired_count_callback:
            self.update_expired_count_callback() 