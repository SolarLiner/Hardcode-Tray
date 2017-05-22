#!/usr/bin/python3
"""
Fixes Hardcoded tray icons in Linux.

Author : Bilal Elmoussaoui (bil.elmoussaoui@gmail.com)
Contributors : Andreas Angerer, Joshua Fogg
Version : 3.8
Website : https://github.com/bil-elmoussaoui/Hardcode-Tray
Licence : The script is released under GPL, uses a modified script
     form Chromium project released under BSD license
This file is part of Hardcode-Tray.
Hardcode-Tray is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
Hardcode-Tray is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with Hardcode-Tray. If not, see <http://www.gnu.org/licenses/>.
"""
from os import path, remove, makedirs
from zipfile import ZipFile
from shutil import make_archive, rmtree
from src.decorators import install_wrapper
from src.utils import execute
from .binary import BinaryApplication


class ZipApplication(BinaryApplication):
    """Zip Application class."""

    def __init__(self, parser):
        """Init method."""
        BinaryApplication.__init__(self, parser)
        self.tmp_path = "/tmp/_{0!s}/".format(self.name)
        self.tmp_data = self.tmp_path + self.zip_path

    @property
    def zip_path(self):
        """Return the path of the icons in the zip file."""
        return self.parser.zip_path

    def extract(self, icon_path):
        """Extract the zip file in /tmp directory."""
        if path.exists(self.tmp_path):
            rmtree(self.tmp_path)
        makedirs(self.tmp_path, exist_ok=True)
        execute(["chmod", "0777", self.tmp_path])
        with ZipFile(icon_path + self.binary) as zf:
            zf.extractall(self.tmp_path)

    def pack(self, icon_path):
        """Recreate the zip file from the tmp directory."""
        zip_file = icon_path + self.binary
        if path.isfile(zip_file):
            remove(zip_file)
        make_archive(zip_file.replace(".zip", ""), 'zip', self.tmp_path)
        rmtree(self.tmp_path)

    @install_wrapper
    def install(self):
        """Install the application icons."""
        for icon_path in self.icons_path:
            self.backup_binary(icon_path)
            self.extract(icon_path)
            for icon in self.icons:
                self.install_icon(icon, self.tmp_data)
            self.pack(icon_path)