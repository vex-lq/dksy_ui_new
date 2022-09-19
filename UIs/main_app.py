import Ui_main
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from codex import *


class UiWindow(Ui_main.Ui_MainWindow, QtWidgets.QMainWindow):  # 继承pyqt控件和ui装饰设置
    root_last_choose_memory = "F:\_____科创作业汇总"
    root_folder_valid = False
    errrrrrrrrrr:有歧义，区分作品根目录和系统根目录
    root_path = ""
    excel_file_path = ""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_func_set()

    def button_func_set(self):
        self.pushButton_set_root.clicked.connect(self.set_root_folder)
        self.pushButton_add_type_name.clicked.connect(
            self.work_folder_add_type)

    def set_root_folder(self):  # 选择根目录
        choosen_root = QtWidgets.QFileDialog.getExistingDirectory(
            None, "选取作品根目录", UiWindow.root_last_choose_memory)  # 起始路径
        if choosen_root != "":
            excel_file_path_x = excel_read.look_for_scoring_excel(choosen_root)
            if excel_file_path_x:  # 选择了根目录，并找到了excel
                self.labe_root.setText(choosen_root)
                self.labe_root.repaint()
                self.label_excel.setText(excel_file_path_x)
                self.label_excel.repaint()
                UiWindow.root_last_choose_memory = choosen_root  # 记录上次选择的文件夹
                UiWindow.root_folder_valid = True
                UiWindow.root_path = choosen_root
                UiWindow.excel_file_path = excel_file_path_x

    def work_folder_add_type(self):
        if UiWindow.root_folder_valid:
            work_folder_rename.add_or_remove_work_type_into_all_student_folders_at_all_classified_folders(
                UiWindow.root_path, add_or_delete_type=True,
                path_excel=UiWindow.excel_file_path,
                ask_before_delete_illegal_naming_folder=True
            )


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = UiWindow()
    window.show()
    sys.exit(app.exec_())
