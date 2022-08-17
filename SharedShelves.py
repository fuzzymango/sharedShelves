'''
SharedShelves.py
version 0.3.1 - 16 August 2022
Isaac Spiegel
isaacspiegel.com
'''

import nuke
import os
import sys
import json
import pathlib
from pathlib import Path


class SharedShelves():
    def __init__(self, dropbox_tools_folder: str = 'sharedNukeTools', icon: str = None, account_type: str = 'personal') -> None:
        '''
        TODO: proper naming for dropbox_tools_folder
        '''
        self.account_type = account_type
        self.dropbox_tools_folder = dropbox_tools_folder
        self.icon = icon
        self.dropbox_install_location = self.find_dropbox_install_directory()
        self.dropbox_tools_folder_location = self.find_folder_in_dropbox(self.dropbox_install_location)

    def find_dropbox_install_directory(self) -> str:
        '''
        TODO: error handling when the info path doesn't exist
        :return:
        '''
        dropbox_info_path = Path(Path(os.environ['LOCALAPPDATA']) / Path(r'Dropbox\info.json'))
        if not dropbox_info_path.exists():
            return None

        with open(dropbox_info_path, 'r') as info:
            content = info.read()
        dropbox_info_content = json.loads(content)

        return dropbox_info_content[self.account_type]['path']

    def find_folder_in_dropbox(self, install_directory: str):
        '''
        TODO: add error handling for if the shared tools folder name isn't found in dropbox
        :param install_directory:
        :return:
        '''
        install_directory = Path(install_directory)
        for folder in install_directory.glob('**/'):
            if folder.name == self.dropbox_tools_folder:
                return folder

    def sync_gizmos(self):
        '''
        TODO: write the populate toolbar functionality in this method
        :return:
        '''
        # toolbar = nuke.toolbar('Nodes').addMenu(self.dropbox_tools_folder, icon=self.icon)
        pass
