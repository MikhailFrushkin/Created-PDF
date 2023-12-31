import asyncio
import os
import time

import aiofiles
import aiohttp
import pandas as pd
from loguru import logger
from tqdm import tqdm
from config import token, path_base_y_disc, path_posters
from utils import df_in_xlsx


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


async def get_download_link(session, token, file_path):
    headers = {"Authorization": f"OAuth {token}"}
    url = "https://cloud-api.yandex.net/v1/disk/resources/download"
    params = {"path": file_path}

    try:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data["href"]
            else:
                print(f"Не удалось получить ссылку для скачивания файла '{file_path}'. Код ошибки:", response.status)
                return None
    except asyncio.TimeoutError:
        print(f"Время ожидания ответа от сервера истекло для файла '{file_path}'.")
        time.sleep(20)
        return None


async def get_yandex_disk_files(session, token, folder_path):
    headers = {"Authorization": f"OAuth {token}"}
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    files_on_yandex_disk = []

    stack = [(folder_path, folder_path)]
    while stack:
        current_folder_path, base_folder_path = stack.pop()
        params = {"path": current_folder_path, "limit": 1000}
        while True:
            async with session.get(url, headers=headers, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    files = data['_embedded']["items"]
                    if files:
                        for item in files:
                            if item["type"] == "dir":
                                stack.append((item["path"], current_folder_path))
                            elif item["type"] == "file":
                                file_name = item["name"]
                                file_path = item["path"]
                                if not os.path.exists(os.path.join(path_posters, file_name)):
                                    if file_name.split('.')[-1] in ['pdf']:
                                        files_on_yandex_disk.append((file_name, file_path))
                        print('Найденно новых файлов: ', len(files_on_yandex_disk))
                        # Проверяем, есть ли еще файлы для получения
                        if "offset" in data['_embedded']:
                            params["offset"] = data['_embedded']["offset"] + data['_embedded']["limit"]
                        else:
                            break
                    else:
                        break
    return files_on_yandex_disk


async def download_file(session, token, file_name, file_path, local_folder_path, progress=None):
    local_filepath = os.path.join(local_folder_path, file_name)
    if os.path.exists(local_filepath):
        # print(f"Файл '{file_name}' уже существует на компьютере. Пропускаем загрузку.")
        return
    download_link = await get_download_link(session, token, file_path)

    if download_link:
        async with session.get(download_link) as response:
            if response.status == 200:
                async with aiofiles.open(local_filepath, "wb") as f:
                    while True:
                        chunk = await response.content.read(8192)
                        if not chunk:
                            break
                        await f.write(chunk)
                print(f"загрузился файл '{file_name}'")
            else:
                print(f"Не удалось загрузить файл '{file_name}'. Код ошибки:", response.status)
    else:
        print(f"Не удалось получить ссылку для скачивания файла '{file_name}'.")


async def download_files_from_yandex_disk(token, files_to_download, local_folder_path=".", progress=None):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
        tasks = [download_file(session, token, file_name, file_path, local_folder_path, progress) for
                 file_name, file_path in
                 files_to_download]

        await asyncio.gather(*tasks)


async def scan_files(self=None):
    try:
        async with aiohttp.ClientSession() as session:
            logger.debug('Сканирование файлов')
            files_to_download = await get_yandex_disk_files(session, token, path_base_y_disc)
            try:
                logger.debug('Скачивание файлов')
                os.makedirs(path_posters, exist_ok=True)
                await download_files_from_yandex_disk(token, files_to_download, path_posters)
            except Exception as ex:
                logger.error(f'Ошибка  {ex}')

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(scan_files())
