from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import openpyxl

class RemovedProductsDialog(QDialog):
    def __init__(self, product_db, parent=None):
        super().__init__(parent)
        self.setWindowTitle('История снятых товаров')
        self.setFixedSize(800, 500)
        self.product_db = product_db
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Название', 'Штрихкод', 'Дата производства', 'Годен до', 'Количество', 'Дата напоминания'
        ])
        layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        self.btn_export = QPushButton('Экспорт в Excel')
        self.btn_export.clicked.connect(self.export_excel)
        btn_layout.addWidget(self.btn_export)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.refresh_table()

    def refresh_table(self):
        data = self.product_db.get_removed_history()
        self.table.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def export_excel(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Сохранить как', '', 'Excel Files (*.xlsx)')
        if not path:
            return
        data = self.product_db.get_removed_history()
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['ID', 'Название', 'Штрихкод', 'Дата производства', 'Годен до', 'Количество', 'Дата напоминания'])
        for row in data:
            ws.append(row)
        try:
            wb.save(path)
            QMessageBox.information(self, 'Успех', 'Экспорт завершён!')
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не удалось сохранить файл: {e}') 