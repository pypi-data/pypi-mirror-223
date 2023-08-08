import subprocess
import sys
import importlib.util
import logging
import os.path
import os

from .examon_config import DEFAULT_FOLDER


class PipInstaller:
    @staticmethod
    def install(packages):
        logging.info(f"installing {len(packages)} repos")
        for package in packages:
            with open(f'{os.path.expanduser(DEFAULT_FOLDER)}/pip_install.log', "w") as outfile:
                cmd = [sys.executable, "-m", "pip", "install", package['name'], '--upgrade']
                logging.debug(cmd)
                subprocess.run(cmd, stdout=outfile)

    @staticmethod
    def is_package_installed(package_name):
        if importlib.util.find_spec(package_name) is None:
            return False
        return True

    @staticmethod
    def import_packages(packages):
        logging.info(f'Importing Packages ({len(packages)})')
        for repo in packages:
            __import__(repo, fromlist=['*'])
