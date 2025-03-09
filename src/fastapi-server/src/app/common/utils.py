import os

import aiofiles

from app.config import UPLOAD_FOLDER


def file_exists_in_uploads_folder(file_name: str):
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    return os.path.exists(file_path)


async def async_file_read(file_path: str):
    async with aiofiles.open(file_path, "r") as f:
        content = await f.read()
    return content


async def async_file_write(file_path: str, content: str):
    async with aiofiles.open(file_path, "w") as f:
        await f.write(content)
