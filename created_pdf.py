import io
import os
import tempfile

import fitz
from PIL import Image
from PyQt5.QtWidgets import QMessageBox
from loguru import logger
from reportlab.lib.pagesizes import A3
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from tqdm import tqdm
from utils import ProgressBar
from config import path_posters


def compression_pdf(pdf_file_path, output_pdf_path, progress):
    logger.debug(f'Сжатие файла {pdf_file_path}')
    pdf_document = fitz.open(pdf_file_path)
    # Параметры сжатия изображений
    image_compression_quality = 100  # Уровень качества JPEG
    # Создаем новый PDF-документ
    output_pdf = canvas.Canvas(output_pdf_path, pagesize=A3)
    # Размеры страницы A3
    a3_width, a3_height = A3
    # Обходим страницы PDF
    for page_num in tqdm(range(pdf_document.page_count), desc="Обработка страниц", unit="стр"):
        page = pdf_document[page_num]
        img_list = page.get_images(full=True)

        # Создаем новую страницу (кроме первой)
        if page_num != 0:
            output_pdf.showPage()

        # Обходим изображения на странице
        for img_index, img in enumerate(img_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            img_data = base_image["image"]

            # Сжимаем и сохраняем изображение
            img_pil = Image.open(io.BytesIO(img_data))
            img_pil.save('temp_img.jpg', format='JPEG', quality=image_compression_quality)

            # Загружаем изображение с помощью ReportLab
            img_width, img_height = img_pil.size

            # Рассчитываем размеры и координаты для вставки изображения на странице A3
            if img_width > a3_width or img_height > a3_height:
                img_width, img_height = a3_width, a3_height
            x_pos = (a3_width - img_width) / 2
            y_pos = (a3_height - img_height) / 2

            pdf_image = ImageReader('temp_img.jpg')

            # Вставляем изображение на текущую страницу
            output_pdf.drawImage(pdf_image, x_pos, y_pos, width=img_width, height=img_height)

            # Удаляем временное изображение
            img_pil.close()
        progress.update_progress()

    # Закрываем PDF-документ
    output_pdf.save()

    # Закрываем исходный PDF
    pdf_document.close()

    print("Готово!")


def one_pdf(self):
    filename = self.lineEdit_2.text()
    pdf_filename = f'{path_posters}\\{filename}.pdf'
    pdf_filename_out = f'{path_posters}\\{filename}.pdf'
    progress = ProgressBar(len(self.files) * 2, self)
    if os.path.exists(pdf_filename):
        logger.debug(f'Файл существует: {pdf_filename}')
        QMessageBox.information(self, 'Инфо', f'Файл существует: {pdf_filename}')
    else:
        good_files = []
        for file in self.files:
            good_files.append(file)
        c = canvas.Canvas(pdf_filename, pagesize=A3)
        for i, poster_file in enumerate(good_files):
            logger.debug(poster_file)
            image = Image.open(poster_file)
            width, height = image.size
            if width > height:
                rotated_image = image.rotate(90, expand=True)
                try:
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                        rotated_image.save(temp_file.name, format='JPEG')
                        c.drawImage(temp_file.name, 0, 0, width=A3[0], height=A3[1])
                except Exception as ex:
                    logger.error(ex)
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                        rotated_image.save(temp_file.name, format='PNG')
                        c.drawImage(temp_file.name, 0, 0, width=A3[0], height=A3[1])
            else:
                c.drawImage(poster_file, 0, 0, width=A3[0], height=A3[1])
            if i != len(self.files) - 1:
                c.showPage()
            progress.update_progress()
        c.save()
        logger.success(f'Создан файл: {pdf_filename}')

        if self.checkBox.isChecked():
            try:
                compression_pdf(pdf_filename, pdf_filename_out, progress)
            except Exception as ex:
                logger.error(ex)
                logger.error(pdf_filename)
        QMessageBox.information(self, 'Инфо', f'Создан файл: {pdf_filename}')


if __name__ == '__main__':
    one_pdf()
