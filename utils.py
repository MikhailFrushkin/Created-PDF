import os
import shutil
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from loguru import logger
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


class ProgressBar:
    def __init__(self, total, progress_bar, current=0):
        self.current = current
        self.total = total
        self.progress_bar = progress_bar

    def update_progress(self):
        self.current += 1
        self.progress_bar.update_progress(self.current, self.total)

    def __str__(self):
        return str(self.current)


def df_in_xlsx(df, filename, max_width=50):
    # Создание нового рабочего книги Excel
    workbook = Workbook()
    # Создание нового листа в рабочей книге
    sheet = workbook.active
    # Конвертация DataFrame в строки данных
    for row in dataframe_to_rows(df, index=False, header=True):
        sheet.append(row)
        # Ограничение ширины колонок
    for column in sheet.columns:
        column_letter = column[0].column_letter
        max_length = max(len(str(cell.value)) for cell in column)
        adjusted_width = min(max_length + 2, max_width)
        sheet.column_dimensions[column_letter].width = adjusted_width
    # Сохранение рабочей книги в файл
    workbook.save(f"{filename}.xlsx")


if __name__ == '__main__':
    pass
