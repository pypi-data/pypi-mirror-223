import io
import os
import platform
import re
import stat
import subprocess
import zipfile
from functools import lru_cache
import shutil
import sys

import requests
import ubelt as ub
from logzero import logger

from . import chrome_info, enviroment, version

CFT_JSON_ENDPOINT = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"


def move_to_root_folder(root_path, cur_path):
    for filename in os.listdir(cur_path):
        if os.path.isfile(os.path.join(cur_path, filename)):
            shutil.move(os.path.join(cur_path, filename),
                        os.path.join(root_path, filename))
        elif os.path.isdir(os.path.join(cur_path, filename)):
            move_to_root_folder(root_path, os.path.join(cur_path, filename))
        else:
            sys.exit("Should never reach here.")
    # remove empty folders
    if cur_path != root_path:
        os.rmdir(cur_path)


@lru_cache(maxsize=1)
def _get_system_platform():
    system_name = platform.system()
    if system_name == 'Windows':
        return "win32"
    if system_name == 'Linux':
        return "linux64"
    if system_name == 'Darwin':
        if enviroment.get_cpu_arch() == 'arm':
            return "mac-arm64"
        else:
            return "mac-x64"
    return None


@lru_cache(maxsize=1)
def _get_driver_zipfile():
    system_name = platform.system()
    if system_name == 'Windows':
        return "chromedriver_win32.zip"
    if system_name == 'Linux':
        return "chromedriver_linux64.zip"
    if system_name == 'Darwin':
        if enviroment.get_cpu_arch() == 'arm':
            return "chromedriver_mac64_m1.zip"
        else:
            return "chromedriver_mac64.zip"
    return None


@lru_cache(maxsize=1)
def _get_driver_filename():
    system_name = platform.system()
    if system_name == 'Windows':
        return "chromedriver.exe"
    if system_name == 'Linux':
        return "chromedriver"
    if system_name == 'Darwin':
        return "chromedriver"
    return None


def get_chromedriver_version_CfT(chrome_version, platform_system):
    selected_version = None
    selected_url = None
    max_minor_version = -1
    base_chrome_version = '.'.join(chrome_version.split('.')[:-1])
    r = requests.get(CFT_JSON_ENDPOINT)
    data = r.json()
    for item in data["versions"]:
        base_item_version = '.'.join(item["version"].split('.')[:-1])
        if base_item_version == base_chrome_version:
            if "chromedriver" in item["downloads"]:
                minor_version = int(item["version"].split('.')[-1])
                if minor_version > max_minor_version:
                    for download in item["downloads"]["chromedriver"]:
                        if download["platform"] == platform_system:
                            selected_version = item["version"]
                            selected_url = download["url"]
    return (selected_version, selected_url)


def download_chromedriver_CfT(url):
    # Method from https://chromedriver.chromium.org/downloads/version-selection
    logger.debug(
        f"Downloading: {url}")
    r = requests.get(url)
    data = r.content
    logger.info(f"Downloaded: {len(data)} bytes")
    return data


def find_chromedriver_version_114(chrome_version):
    # Method from https://chromedriver.chromium.org/downloads/version-selection
    # Take the Chrome version number, remove the last part, and append the result to URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_"
    url_version = '.'.join(chrome_version.split('.')[:-1])
    url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{url_version}"
    r = requests.get(url)
    data = r.text.strip()
    logger.info(f"ChromeDriver version needed: {data}")
    return data


def download_chromedriver_zip_114(chromedriver_version):
    # Method from https://chromedriver.chromium.org/downloads/version-selection
    url = f"https://chromedriver.storage.googleapis.com/{chromedriver_version}/{_get_driver_zipfile()}"
    logger.debug(
        f"Downloading: {chromedriver_version}/{_get_driver_zipfile()}")
    r = requests.get(url)
    data = r.content
    logger.info(f"Downloaded: {len(data)} bytes")
    return data


def extract_zip(zip_data, folder="."):
    chromedriver_path = os.path.join(folder, _get_driver_filename())
    if os.path.exists(chromedriver_path):
        os.remove(chromedriver_path)

    with io.BytesIO(zip_data) as f:
        with zipfile.ZipFile(file=f, mode='r') as zip_ref:
            zip_ref.extractall(folder)

    for filename in os.listdir(folder):
        cur_path = os.path.join(folder, filename)
        if os.path.isdir(cur_path):
            move_to_root_folder(folder, cur_path)
            
    os.chmod(chromedriver_path, mode=stat.S_IRWXU |
             stat.S_IXGRP | stat.S_IXOTH)
    logger.debug(f"Extracted executable into: {folder}")


def get_version(folder):
    chromedriver_path = os.path.join(folder, _get_driver_filename())
    if not os.path.exists(chromedriver_path):
        return None
    output = subprocess.check_output(
        '"%s" -v' % (chromedriver_path), shell=True)
    output_str = output.decode(encoding='ascii')
    version_str = version.extract_version(output_str)
    logger.debug(f"Downloaded ChromeDriver Version: {version_str}")
    return version_str


def download_only_if_needed(chrome_path=None, chromedriver_folder=None):
    if chromedriver_folder:
        dpath = chromedriver_folder
    else:
        dpath = ub.ensure_app_cache_dir('latest_chromedriver')

    cached_version = get_version(dpath)
    c_version = chrome_info.get_version(chrome_path=chrome_path)

    if c_version:
        major_version = int(c_version.split('.')[0])
        if major_version < 114:
            online_version = find_chromedriver_version_114(c_version)
            if (not cached_version) or (online_version != cached_version):
                zip_data = download_chromedriver_zip_114(online_version)
                extract_zip(zip_data, dpath)
        else:
            (online_version, url) = get_chromedriver_version_CfT(
                c_version, _get_system_platform())
            if (not cached_version) or (online_version != cached_version):
                zip_data = download_chromedriver_CfT(url)
                extract_zip(zip_data, dpath)

    return dpath
