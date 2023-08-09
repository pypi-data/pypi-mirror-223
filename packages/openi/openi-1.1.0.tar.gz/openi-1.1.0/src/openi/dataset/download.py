from openi.apis import OpeniAPI
from .dataset_file import *
from openi.utils import file_utils, logger
from openi.settings import *
from pathlib import Path
from tqdm import tqdm
import requests
import os
import logging

logger.setup_logger()


def download_with_tqdm(response: requests.Response, save_path: str, file: str):
    """
    Download file with tqdm progress bar
    """
    file_size = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 KB

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    outfile = os.path.join(save_path, file)
    if os.path.exists(outfile):
        outfile = file_utils.rename_existing_file(outfile)

    with tqdm(
        total=file_size,
        leave=True,
        unit="B",
        unit_scale=True,
        unit_divisor=1000,
        bar_format="{desc}{percentage:3.0f}%|{bar}{r_bar}",
        desc=f"{logger.get_time()} - Downloading: ",
        dynamic_ncols=True,
    ) as pbar:
        with open(outfile, "wb") as f:
            for data in response.iter_content(block_size):
                pbar.update(len(data))
                f.write(data)
    print(f"{logger.get_time()} - 🎉 Download complete! file was saved to `{outfile}`")


def download_file(
    file: str,
    repo_id: str,
    cluster: str = "NPU",
    save_path: str = PATH.SAVE_PATH,
    endpoint: str = None,
    token: str = None,
):
    """
    Download file from dataset
    """

    _, repo = get_owner_repo(repo_id)
    upload_type, cluster = get_upload_type(cluster.upper())

    print(f"{logger.get_time()} - `{file}`({cluster}) preprocessing...")
    outfile = os.path.join(save_path, file)

    api = OpeniAPI(endpoint=endpoint, token=token)

    _datasets = api.get_dataset_attachment(repo_id=repo_id, upload_type=upload_type)
    if _datasets["data"] is not None:
        _dataset_info = next(
            (d for d in _datasets["data"] if d["repo"]["name"] == repo), None
        )
    if _datasets["count"] == 0 or _dataset_info is None:
        raise ValueError(
            f"❌ `{repo_id}`: dataset not created OR no zipfile({cluster.upper()}) found."
        )
    if _dataset_info["attachments"] is not None:
        _attachment = next(
            (d for d in _dataset_info["attachments"] if d["name"] == file), None
        )
    if _attachment is None:
        raise ValueError(
            f"❌ `{file}`({cluster.upper()}): file not found in `{repo_id}`"
        )
    uuid = _attachment["uuid"]

    response = api.download_attachments(uuid, upload_type)
    download_with_tqdm(response, save_path, file)
