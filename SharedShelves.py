'''
SharedShelves.py
version 0.3.1 - 17 August 2022
Isaac Spiegel
isaacspiegel.com
'''

import nuke
import os
import json
from pathlib import Path


class SharedShelves():
    def __init__(self, dropbox_tools_folder: str = 'sharedNukeTools', icon: str = None,
                 account_type: str = 'personal') -> None:
        '''
        __init__
        :param dropbox_tools_folder: str
            The name of the folder where the shared tools are stored
        :param icon: str
            The location of the icon for the toolbar menu
        :param account_type: str
            The type of Dropbox account the user is in possession of
        '''
        self.account_type = account_type
        self.dropbox_tools_folder = dropbox_tools_folder
        self.icon = icon
        self.dropbox_install_location = self.find_dropbox_install_directory()
        self.dropbox_tools_folder_location = self.find_folder_in_dropbox(self.dropbox_install_location, self.dropbox_tools_folder)
        self.VALID_ICON_FILE_TYPES = ['.png', '.jpg', '.jpeg']
        self.VALID_GIZMO_FILE_TYPES = ['.gizmo']
        self.VALID_TOOLSET_FILE_TYPES = ['.gizmo', '.nk']

    def find_dropbox_install_directory(self) -> str:
        '''
        Locates the filepath of the Dropbox install on the user's computer
        :return:
        '''
        dropbox_info_path = Path(Path(os.environ['LOCALAPPDATA']) / Path(r'Dropbox\info.json'))
        if not dropbox_info_path.exists():
            return None

        with open(dropbox_info_path, 'r') as info:
            content = info.read()
        dropbox_info_content = json.loads(content)

        return dropbox_info_content[self.account_type]['path']

    def find_folder_in_dropbox(self, install_directory: str, folder_name: str) -> Path:
        '''
        Locates a named folder inside a directory and returns the path to that folder.
        :param folder_name: str
            The name of the folder to find
        :param install_directory: str
            The directory to search for the folder_name
        :return:
            The path to the folder
        '''
        if not install_directory: return None

        install_directory = Path(install_directory)
        for folder in install_directory.glob('**/'):
            if folder.name == folder_name:
                return folder
        return None

    def _verify(self) -> bool:
        if self.dropbox_install_location is None:
            nuke.message(f"Unable to locate info.json in the Dropbox install directory."
                         f"\nDropbox tools will not be synced.")
            return False
        if self.dropbox_tools_folder_location is None:
            nuke.message(
                f"Unable to locate folder {self.dropbox_tools_folder} in directory {self.dropbox_install_location}."
                f"\nDropbox tools will not be synced.")
            return False
        return True


    def sync_gizmos(self, folder_name: str = 'gizmos') -> None:
        '''
        This is the primary method for syncing any gizmos found on Dropbox with a toolbar in Nuke. A new toolbar is
        created to house the loaded tools from Dropbox. This method expects a folder named 'gizmos' to exist
        somewhere inside the user-defined Dropbox folder.
        :return:
            None
        '''
        if not self._verify(): return

        toolbar = nuke.toolbar('Nodes').addMenu(self.dropbox_tools_folder, icon=self.icon)
        path_to_gizmos = Path(self.dropbox_tools_folder_location / Path(folder_name))
        nuke.pluginAddPath(str(path_to_gizmos), False)

        for folder in path_to_gizmos.glob('**/'):
            if str(folder) not in nuke.pluginPath():
                nuke.pluginAddPath(str(folder))
            icons = self.fetch_icons(folder)

            for file in folder.glob('*.*'):
                if file.suffix in self.VALID_GIZMO_FILE_TYPES:
                    shelf_name = self.retrieve_relative_path(file, relative_to=folder_name)
                    create_node = f"nuke.createNode('{file.stem}')"
                    if file.stem in icons:
                        icon_title = icons[file.stem]
                    else:
                        icon_title = ''
                    toolbar.addCommand(shelf_name, create_node, icon=icon_title)

    @staticmethod
    def retrieve_relative_path(file: Path, relative_to: str = '.nuke') -> str:
        '''
        Takes in a file path and a reference folder and outputs a filepath relative to the reference folder
        :param file: Path
            The larger filepath containing the 'relative_to' folder
        :param relative_to: str
            Where the truncated filepath will start
        :return: str
            A truncated filpath relative to the 'relative_to' folder
        '''
        relative_path_start = file.parts.index(relative_to) + 1
        relative_path_parts = file.parts[relative_path_start:]
        relative_path = ''
        for index, part in enumerate(relative_path_parts):
            if index == 0:
                relative_path = f'{part}'
            elif index == len(relative_path_parts) - 1:
                relative_path = f'{relative_path}/{file.stem}'
            else:
                relative_path = f'{relative_path}/{part}'

        return relative_path

    def fetch_icons(self, folder: Path) -> dict:
        '''
        Creates a dictionary of all files in the specified directory that contain an extension defined in
        VALID_ICON_FILE_TYPES
        :param folder: Path
            A full-length file path
        :return: icons: dict
            A dictionary containing the stem of the image file (no extension) for the keys and the name of the image
            file (with extension) for the values.
        '''
        icons = {}
        for file in folder.glob('*.*'):
            if file.suffix in self.VALID_ICON_FILE_TYPES:
                icons.update({file.stem: file.name})
        return icons

    def sync_toolsets(self, folder_name: str = 'ToolSets') -> None:
        '''
        This is the primary method for syncing any toolsets found on Dropbox with Nuke's "ToolSets" folder. This method
        expects a folder named "ToolSets" (case sensitive) to exist somewhere in the user-defined Dropbox folder
        structure.
        :param folder_name: str
            The name of the Dropbox folder this method should load toolsets from. "ToolSets" by default.
        :return:
        '''
        if not self._verify(): return

        toolsets_toolbar = nuke.toolbar('Nodes').menu('ToolSets')
        path_to_toolbar_items = Path(self.dropbox_tools_folder_location / Path(folder_name))
        nuke.pluginAddPath(str(path_to_toolbar_items), False)

        for folder in path_to_toolbar_items.glob('**/'):
            if str(folder) not in nuke.pluginPath():
                nuke.pluginAddPath(str(folder))
            icons = self.fetch_icons(folder)

            for file in folder.glob('*.*'):
                if file.suffix in self.VALID_TOOLSET_FILE_TYPES:
                    shelf_name = file.stem
                    create_command = f"nuke.createNode('{file.name}')"
                    if file.stem in icons:
                        icon_title = icons[file.stem]
                    else:
                        icon_title = ''
                    toolsets_toolbar.addCommand(shelf_name, create_command, icon=icon_title)
