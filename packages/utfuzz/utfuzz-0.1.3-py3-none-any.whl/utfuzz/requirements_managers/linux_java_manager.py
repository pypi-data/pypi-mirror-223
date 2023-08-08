import platform
import subprocess
import sys
import typing

from utfuzz.exceptions.exceptions import JavaIsNotInstalled
from utfuzz.requirements_managers.abc_requirements_manager import AbstractJavaRequirementsManger


class LinuxJavaManager(AbstractJavaRequirementsManger):
    def check_platform(self) -> bool:
        return platform.system() == 'Linux'

    def install_java(self):
        distributive: str
        if sys.version_info.major >= 3 and sys.version_info.major >= 10:
            distributive = platform.freedesktop_os_release()['ID']
        else:
            distributive = dict([
                p.split('=', maxsplit=1)
                for p in subprocess.check_output(['cat', '/etc/os-release']).decode().split('\n')
                if '=' in p
            ])['ID']

        install_command: typing.List[str]
        if distributive == 'arch':
            install_command = ['sudo', 'pacman', '-S', 'jdk17-openjdk']
        elif distributive in ['debian', 'ubuntu']:
            install_command = ['sudo', 'apt-get', 'install', 'openjdk-17-jdk']
        else:
            install_command = []

        try:
            if len(install_command) != 0:
                print('Try to install java...')
                install = input('Run this command? ' + ' '.join(install_command) + '? (Y/n) ')
                if install in {'Y', ''}:
                    subprocess.check_output(install_command)
                else:
                    return
        except Exception:
            print(f"Cannot install Java automatically, please install Java 17 or newer, see instruction here: "
                  f"https://docs.oracle.com/en/java/javase/17/install/installation-jdk-linux-platforms.html"
                  )
