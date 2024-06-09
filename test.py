from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QMainWindow, QPushButton
from PySide6.QtCore import Qt

class IndexedButtonWidget(QPushButton):
    def __init__(self, text, parent=None):
        super(IndexedButtonWidget, self).__init__(text, parent)
        self.button_row = 0
        self.button_column = 0

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.setCentralWidget(self.table)
        data1 = ['row1', 'row2', 'row3', 'row4']
        data2 = ['1', '2.0', '3.00000001', '3.9999999']

        self.table.setRowCount(4)

        for index in range(4):
            item1 = QTableWidgetItem(data1[index])
            self.table.setItem(index, 0, item1)
            item2 = QTableWidgetItem(data2[index])
            self.table.setItem(index, 1, item2)
            self.btn_sell = IndexedButtonWidget('Edit')
            self.btn_sell.button_row = index
            self.btn_sell.button_column = 2
            self.btn_sell.clicked.connect(self.handleButtonClicked)
            self.table.setCellWidget(index, 2, self.btn_sell)

    def handleButtonClicked(self):
        button = self.sender()
        print(f'Button clicked at row {button.button_row} column {button.button_column}')

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.resize(400, 300)
    window.show()
    app.exec()
