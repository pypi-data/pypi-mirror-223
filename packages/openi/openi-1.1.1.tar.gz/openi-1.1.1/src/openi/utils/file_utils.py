import hashlib
import math
import json
from datetime import datetime
from pathlib import Path
from openi.settings import *


def calculateMD5(filepath: str = None) -> str:
    """
    计算文件的完整md5
    :param self.filepath:
    :return:
    """
    m = hashlib.md5()  # 创建md5对象
    with open(filepath, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            m.update(data)  # 更新md5对象
    return m.hexdigest()  # 返回md5对象


def read_file_chunk(
    filepath: str = None, start_position: int = 0, chunk_size: int = None
):
    with open(filepath, "rb") as file:
        file.seek(start_position)
        chunk = file.read(chunk_size)
        return chunk


def get_file_chunk(chunk_size: int, filesize: int = 0) -> dict:
    total_chunks_count = math.ceil(filesize / chunk_size)
    return total_chunks_count


def get_token() -> str:
    return json.loads(Path(PATH.TOKEN_PATH).read_text())


def rename_existing_file(filepath):
    if "tar.gz" in filepath:
        path = filepath.replace(".tar.gz", "")
        suffix = ".tar.gz"
    else:
        path, suffix = os.path.splitext(filepath)

    counter = 1
    while os.path.exists(filepath):
        filepath = "{}({}){}".format(path, counter, suffix)
        counter += 1
    return filepath
