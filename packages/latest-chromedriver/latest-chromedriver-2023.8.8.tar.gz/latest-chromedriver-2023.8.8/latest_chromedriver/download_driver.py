"""The main module functionality, downloading the Google Chromedriver"""

import io
import os
import platform
import shutil
import stat
import subprocess
import sys
import zipfile
from functools import lru_cache

import requests
import ubelt as ub
from logzero import logger

from . import chrome_info, enviroment, version

CFT_JSON_ENDPOINT = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
HTTP_TIMEOUT = 120


def move_to_root_folder(root_path, cur_path):
    """Flatten a directory structure to root path"""
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
def _get_system_platform(chrome_bits):
    system_name = platform.system()
    if system_name == 'Windows':
        if '64' in chrome_bits:
            return "win64"
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


def get_chromedriver_version_cft(chrome_version, platform_system):
    """Find which is the latest chromedriver using 
    the Chrome for Testing availability JSON endpoints."""
    selected_version = None
    selected_url = None
    chrome_version_list = [int(x) for x in chrome_version.split('.')]
    max_version_size = max([len(x) for x in chrome_version.split('.')])
    order_of_score = 10**max_version_size
    #max_eligible_version = [-1 for _x in range(chrome_version_list)]
    max_score = float('-inf')

    r = requests.get(CFT_JSON_ENDPOINT, timeout=HTTP_TIMEOUT)
    data = r.json()
    for item in data["versions"]:
        item_version_list = [int(x) for x in item["version"].split('.')]

        compatibility_score = 0
        max_magnitude_size = len(chrome_version_list)
        for i in range(max_magnitude_size):
            magnitude_size = order_of_score**(max_magnitude_size - i)
            if item_version_list[i] == chrome_version_list[i]:
                compatibility_score += magnitude_size
            elif item_version_list[i] < chrome_version_list[i]:
                version_mismatch = int(
                    (1.0 - (item_version_list[i]/chrome_version_list[i]))*magnitude_size)
                compatibility_score += magnitude_size - version_mismatch
            else:
                compatibility_score -= magnitude_size

        if compatibility_score > max_score:
            if "chromedriver" in item["downloads"]:
                for download in item["downloads"]["chromedriver"]:
                    if download["platform"] == platform_system:
                        max_score = compatibility_score
                        selected_version = item["version"]
                        selected_url = download["url"]
    logger.info("ChromeDriver version needed: %s", selected_version)
    return (selected_version, selected_url)


def download_chromedriver_cft(url):
    """Download the latest chromedriver based on the url provided"""
    logger.debug("Downloading: %s", url)
    reponse = requests.get(url, timeout=HTTP_TIMEOUT)
    data = reponse.content
    logger.info("Downloaded: %d bytes", len(data))
    return data


def find_chromedriver_version_114(chrome_version):
    """Find which is the latest chromedriver using the old (pre 115) method"""
    # Method from https://chromedriver.chromium.org/downloads/version-selection
    # Take the Chrome version number, remove the last part, and append the
    # result to URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_"
    url_version = '.'.join(chrome_version.split('.')[:-1])
    url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{url_version}"
    response = requests.get(url, timeout=HTTP_TIMEOUT)
    data = response.text.strip()
    logger.info("ChromeDriver version needed: %s", data)
    return data


def download_chromedriver_zip_114(chromedriver_version):
    """Download the latest chromedriver using the old (pre 115) method"""
    # Method from https://chromedriver.chromium.org/downloads/version-selection
    zip_f = _get_driver_zipfile()
    url = f"https://chromedriver.storage.googleapis.com/{chromedriver_version}/{zip_f}"
    logger.debug("Downloading: %s/%s", chromedriver_version, zip_f)
    response = requests.get(url, timeout=HTTP_TIMEOUT)
    data = response.content
    logger.info("Downloaded: %d bytes", len(data))
    return data


def extract_zip(zip_data, folder="."):
    """Clean the target folder and rxtract all zip data to that folder"""
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
    logger.debug("Extracted executable into: %s", folder)


def get_version(folder):
    """Get the chromedriver version"""
    chromedriver_path = os.path.join(folder, _get_driver_filename())
    if not os.path.exists(chromedriver_path):
        return None
    output = subprocess.check_output(f'"{chromedriver_path}" -v', shell=True)
    output_str = output.decode(encoding='ascii')
    version_str = version.extract_version(output_str)
    logger.debug("Downloaded ChromeDriver Version: %s", version_str)
    return version_str


def download_only_if_needed(chrome_path=None, chromedriver_folder=None):
    """Check if there is a chromedriver in pathm and download new if needed"""
    if chromedriver_folder:
        dpath = chromedriver_folder
    else:
        dpath = ub.ensure_app_cache_dir('latest_chromedriver')

    cached_version = get_version(dpath)
    c_version = chrome_info.get_version(chrome_path=chrome_path)
    c_bits = chrome_info.get_architecture(chrome_path)

    if c_version:
        major_version = int(c_version.split('.')[0])
        if major_version < 114:
            online_version = find_chromedriver_version_114(c_version)
            if (not cached_version) or (online_version != cached_version):
                zip_data = download_chromedriver_zip_114(online_version)
                extract_zip(zip_data, dpath)
        else:
            (online_version, url) = get_chromedriver_version_cft(
                c_version, _get_system_platform(c_bits))
            if (not cached_version) or (online_version != cached_version):
                zip_data = download_chromedriver_cft(url)
                extract_zip(zip_data, dpath)

    return dpath
