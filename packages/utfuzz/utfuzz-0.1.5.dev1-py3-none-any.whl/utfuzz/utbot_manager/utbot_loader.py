import pathlib
import zipfile

import requests


def download_utbot(project_dir: pathlib.Path):
    utbot_url = 'https://github.com/UnitTestBot/UTBotJava/suites/14873916912/artifacts/847168659'
    data = requests.get(utbot_url)
    jar_file_name = project_dir / 'utbot-cli-python.jar'
    zip_file_name = project_dir / 'utbot-cli-python.zip'
    zip_dir = project_dir / 'utbot-cli-python'
    if not jar_file_name.exists():
        with open(str(zip_file_name), 'wb') as fout:
            fout.write(data.content)
        zip_file = zipfile.ZipFile(zip_file_name, 'r')
        zip_file.extractall(zip_dir)
        jar_file = list(zip_dir.iterdir())[0]
        return jar_file_name
