from sys import argv, exit

from PyQt5.QtWidgets import QApplication, QMainWindow
from qt_test import Ui_MainWindow  # 导入uitestPyQt5.ui转换为uitestPyQt5.py中的类


class Mywindow(QMainWindow, Ui_MainWindow):
    # 建立的是Main Window项目，故此处导入的是QMainWindow
    # 参考博客中建立的是Widget项目，因此哪里导入的是QWidget
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def click_test(self):  # 定义槽函数btn_click(),也可以理解为重载类Ui_MainWindow中的槽函数btn_click()
        self.textEdit.setText("hi,PyQt5~")


app = QApplication(argv)
window = Mywindow()
window.show()
exit(app.exec_())
