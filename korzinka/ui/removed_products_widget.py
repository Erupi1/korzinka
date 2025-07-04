from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel, QFileDialog)
from PyQt5.QtCore import Qt
from db import ProductDB
import openpyxl

class RemovedProductsWidget(QWidget):
    def __init__(self, is_admin=False):
        super().__init__()
        self.db = ProductDB()
        self.is_admin = is_admin
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel('История снятых товаров')
        label.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout.addWidget(label)
        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Название', 'Штрихкод', 'Дата производства', 'Срок годности', 'Количество', 'Дата напоминания'
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        # Кнопка экспорта
        self.btn_export = QPushButton('Экспорт в Excel')
        self.btn_export.setStyleSheet('background-color: #388e3c; color: white; font-weight: bold; border-radius: 8px; padding: 8px;')
        self.btn_export.clicked.connect(self.export_to_excel)
        if self.is_admin:
            layout.addWidget(self.btn_export)
        self.setLayout(layout)

    def load_data(self):
        products = self.db.get_removed_products()
        self.table.setRowCount(len(products))
        for row, p in enumerate(products):
            for col in range(7):
                self.table.setItem(row, col, QTableWidgetItem(str(p[col])))

    def export_to_excel(self):
        products = self.db.get_removed_products()
        if not products:
            QMessageBox.information(self, 'Нет данных', 'Нет снятых товаров для экспорта.')
            return
        path, _ = QFileDialog.getSaveFileName(self, 'Сохранить как', 'removed_products.xlsx', 'Excel Files (*.xlsx)')
        if not path:
            return
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['ID', 'Название', 'Штрихкод', 'Дата производства', 'Срок годности', 'Количество', 'Дата напоминания'])
        for p in products:
            ws.append(list(p[:7]))
        wb.save(path)
        QMessageBox.information(self, 'Успех', f'Экспортировано в {path}') 