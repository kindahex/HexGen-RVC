import argparse
import os
import re
import six
import sys
import wget
import shutil
import zipfile
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlencode, parse_qs, urlparse

now_dir = os.getcwd()
sys.path.append(now_dir)

# Import your existing methods and dependencies
from programs.rvc.lib.utils import format_title
from programs.rvc.lib.tools import gdown
from programs.rvc.lib.tools.model_download import model_download_pipeline

# Define your functions here (copy all your existing functions like find_folder_parent, download_from_url, etc.)


def cli():
    parser = argparse.ArgumentParser(description="Model Download Pipeline CLI")
    parser.add_argument(
        "url",
        type=str,
        help="The URL of the file to download. Supports Google Drive, MediaFire, etc.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Specify the output folder for the downloaded files. Defaults to the logs directory.",
    )
    args = parser.parse_args()

    url = args.url
    output_folder = args.output

    if output_folder:
        global file_path, zips_path
        file_path = output_folder
        zips_path = os.path.join(file_path, "zips")

    print("Starting the model download pipeline...")
    result = model_download_pipeline(url)
    if result == "Error":
        print("An error occurred during the process.")
    else:
        print("Process completed successfully.")


if __name__ == "__main__":
    cli()
