import asyncio
import os
from pathlib import Path

import PyPDF2
import pandas as pd
import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QProgressBar, QFileDialog, QMessageBox, QApplication
from loguru import logger
from utils import  ProgressBar
from config import path_posters
from created_pdf import one_pdf
from update_db import scan_files


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(439, 326)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_3.addWidget(self.lineEdit_2, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.checkBox = QtWidgets.QCheckBox(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox.setFont(font)
        self.checkBox.setCheckable(True)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_2.addWidget(self.checkBox)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_4.addWidget(self.pushButton_3, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_4)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_5.addWidget(self.lineEdit_3, 2, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_5.addWidget(self.pushButton_4, 2, 1, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_6.addWidget(self.label_4, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem2, 1, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_6.addWidget(self.pushButton_5, 3, 1, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox.setProperty("value", 1)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout_6.addWidget(self.spinBox, 2, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem3, 4, 0, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_6, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Создание PDF"))
        self.pushButton.setText(_translate("MainWindow", "Обновить"))
        self.label_2.setText(_translate("MainWindow", "Введите название"))
        self.pushButton_2.setText(_translate("MainWindow", "Выберите изображения"))
        self.label.setText(_translate("MainWindow", "Выберите изображения"))
        self.checkBox.setText(_translate("MainWindow", "Сжать"))
        self.pushButton_3.setText(_translate("MainWindow", "Создать файл"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Создать файл pdf"))
        self.label_3.setText(_translate("MainWindow", "Выберите заказ"))
        self.pushButton_4.setText(_translate("MainWindow", "Выбрать"))
        self.label_4.setText(_translate("MainWindow", "Введите сколько создать файлов"))
        self.pushButton_5.setText(_translate("MainWindow", "Создать"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  _translate("MainWindow", "Соединить несколько pdf"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.current_dir = Path.cwd()
        self.dialogs = []
        self.files = []

        self.move(550, 100)
        self.count_printer = 0
        self.column_counter_printer = 0

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(10, 10, 100, 25)
        self.progress_bar.setMaximum(100)
        self.statusbar.addWidget(self.progress_bar, 1)

        self.pushButton.clicked.connect(self.evt_btn_update)
        self.pushButton_2.clicked.connect(self.evt_btn_open_images)
        self.pushButton_3.clicked.connect(self.evt_btn_create_pdf)
        self.pushButton_4.clicked.connect(self.evt_btn_open_file_excel)
        self.pushButton_5.clicked.connect(self.evt_btn_created_order)

    def update_progress(self, current_value, total_value):
        progress = int(current_value / total_value * 100)
        self.progress_bar.setValue(progress)
        QApplication.processEvents()

    def evt_btn_update(self):
        try:
            asyncio.run(scan_files(self))
            QMessageBox.information(self, 'Загрузка', f'Загрузка завершена')
        except Exception as ex:
            logger.error(ex)

    def evt_btn_open_images(self):
        """Ивент на кнопку загрузить файлы изображений"""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        files, _ = QFileDialog.getOpenFileNames(self, "Загрузить изображения", str(self.current_dir),
                                                "Изображения (*.png *.jpg);;Все файлы (*)", options=options)

        if files:
            try:
                self.files = files
                self.lineEdit.setText(", ".join(files))
            except Exception as ex:
                logger.error(f'Ошибка при загрузке изображений: {ex}')
                QMessageBox.information(self, 'Инфо', f'Ошибка при загрузке изображений: {ex}')

    def evt_btn_create_pdf(self):
        if self.lineEdit_2.text():
            one_pdf(self)

    def evt_btn_open_file_excel(self):
        """Ивент на кнопку загрузить файл"""
        res, _ = QFileDialog.getOpenFileName(self, 'Загрузить файл', str(self.current_dir), 'Лист XLSX (*.xlsx)')
        if res:
            try:
                self.lineEdit_3.setText(res)
            except Exception as ex:
                logger.error(f'ошибка чтения xlsx {ex}')
                QMessageBox.information(self, 'Инфо', f'ошибка чтения xlsx {ex}')

    def evt_btn_created_order(self):
        if self.lineEdit_3.text():
            df = pd.read_excel(self.lineEdit_3.text())
            df['Артикул продавца'] = df['Артикул продавца'].apply(lambda x: x.lower() + '.pdf')
            art_list2 = df['Артикул продавца'].to_list()

            found_files_all, not_found_files = find_files_in_directory(path_posters, art_list2)
            if len(not_found_files) > 0:
                logger.error(f'Длина найденных артикулов {len(found_files_all)}')
                logger.error(f'Длина не найденных артикулов {len(not_found_files)}')
                logger.error("Файлы не найдены:")
                for file_name in not_found_files:
                    logger.error(file_name.replace('.pdf', ''))
                bad_arts_list = "\n".join(not_found_files)
                QMessageBox.warning(self, 'Ошибка', f'Найдены не все артикула:\n{bad_arts_list}')
            else:
                logger.success('Все артикула найденны')
                logger.success(f'Длина найденных артикулов {len(found_files_all)}')

                file_new_name = self.lineEdit_3.text().split("/")[-1]
                merge_pdfs(found_files_all, file_new_name, self.spinBox.value(), self)
                QMessageBox.Information(self, 'Инфо', f'Завершено!')


def split_list(lst, num_parts):
    avg = len(lst) // num_parts
    remainder = len(lst) % num_parts
    split_indices = [0] + [avg * i + min(i, remainder) for i in range(1, num_parts + 1)]
    return [lst[split_indices[i]:split_indices[i + 1]] for i in range(num_parts)]


def merge_pdfs(input_paths, output_path, count, self):
    pdf_writer = PyPDF2.PdfWriter()
    split_lists = split_list(input_paths, count)
    progress = ProgressBar(len(input_paths), self, 1)

    for group_index, current_group_paths in enumerate(split_lists, start=1):
        for index, input_path in enumerate(current_group_paths, start=1):
            try:
                print(index, input_path)
                with open(input_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    # Add all pages from PdfReader to PdfWriter
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
            except Exception as ex:
                os.remove(input_path)
                logger.error(input_path)
                with open('проблемные пдф.txt', "a") as file:
                    # Записываем строки в файл
                    file.writelines(f'{input_path}\n')
                QMessageBox.warning(self, 'Ошибка',
                                    f'В файле {input_path} обнаружена ошибка, он удален, нужно пересоздать файл')
            progress.update_progress()
        # Write the merged pages to the output file with an index
        current_output_path = f"{output_path}_{group_index}.pdf"
        with open(current_output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

        # Clear the PdfWriter for the next group
        pdf_writer = PyPDF2.PdfWriter()



def find_files_in_directory(directory_path, file_list):
    found_files = []
    not_found_files = []
    for file_name in file_list:
        file_path = os.path.join(directory_path, file_name)
        if os.path.exists(file_path):
            found_files.append(file_path)
        else:
            not_found_files.append(file_name)

    return found_files, not_found_files


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
