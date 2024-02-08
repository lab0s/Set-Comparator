from design import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    
        self.pushButton.clicked.connect(self.show_lines)

    def show_lines(self):
        print(self.lineEdit.text())
        print(self.lineEdit_2.text())
        print(self.checkBox.isChecked())


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())