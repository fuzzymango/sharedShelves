"""
SharedShelves.py
26 August 2022
Isaac Spiegel
isaacspiegel.com
TODO: create a script to add the user's currently selected nodes to the shared Dropbox folder
"""

import nuke
import os
import json
from pathlib import Path
import platform


class SharedShelves:
    def __init__(self, dropbox_tools_folder: str = 'sharedNukeTools', icon: str = None,
                 account_type: str = 'personal') -> None:
        """
        __init__
        :param dropbox_tools_folder: str
            The name of the folder where the shared tools are stored
        :param icon: str
            The location of the icon for the toolbar menu
        :param account_type: str
            The type of Dropbox account the user is in possession of
        """
        self.VALID_ICON_FILE_TYPES = ['.png', '.jpg', '.jpeg']
        self.VALID_GIZMO_FILE_TYPES = ['.gizmo', '.nk']
        self.VALID_TOOLSET_FILE_TYPES = ['.gizmo', '.nk']
        self.USER_OS = platform.system()

        self.account_type = account_type
        self.dropbox_tools_folder = dropbox_tools_folder
        self.icon = icon
        self.dropbox_install_location = self.find_dropbox_install_directory()
        self.dropbox_tools_folder_location = self.find_folder_in_dropbox(self.dropbox_install_location,
                                                                         self.dropbox_tools_folder)
        menu = nuke.menu('Nuke').addMenu('SharedShelves')
        menu.addCommand('Publish Selection to Dropbox',
                        f"SharedShelves._publish_selection(\"{self.dropbox_tools_folder_location}\")")

    def find_dropbox_install_directory(self) -> str or None:
        """
        Locates the filepath of the Dropbox install on the user's computer
        :return: str
            The filepath to the Dropbox install directory as a string
        """
        dropbox_info_path = None
        if self.USER_OS == 'Windows':
            try:
                dropbox_info_path = Path(Path(os.environ['LOCALAPPDATA']) / Path(r'Dropbox\info.json'))
            except FileNotFoundError:
                dropbox_info_path = Path(Path(os.environ['APPDATA']) / Path(r'Dropbox\info.json'))
        elif self.USER_OS == 'Darwin':
            dropbox_info_path = Path(Path(os.path.expanduser('~')) / Path(r'.dropbox/info.json'))
        if not dropbox_info_path.exists():
            return None

        with open(dropbox_info_path, 'r') as info:
            content = info.read()
        dropbox_info_content = json.loads(content)

        return dropbox_info_content[self.account_type]['path']

    @staticmethod
    def find_folder_in_dropbox(install_directory: str, folder_name: str) -> Path or None:
        """
        Locates a named folder inside a directory and returns the path to that folder.
        :param folder_name: str
            The name of the folder to find
        :param install_directory: str
            The directory to search for the folder_name
        :return:
            The path to the folder
        """
        if not install_directory: return None

        install_directory = Path(install_directory)
        for folder in install_directory.glob('**/'):
            if folder.name == folder_name:
                return folder
        return None

    def _verify(self, sync_folder='folder_name') -> bool:
        """
        A check to see if the Dropbox install and folder have been correctly located. Opens a Nuke message window
        notifiying the user as to what's missing.
        :return: bool
            True if if it's all good and False if errors.
        """
        if self.dropbox_install_location is None:
            nuke.message(f"Unable to locate info.json in the Dropbox install directory."
                         f"\nDropbox folder \"{sync_folder}\" will not be synced.")
            return False
        if self.dropbox_tools_folder_location is None:
            nuke.message(
                f"Unable to locate folder \"{self.dropbox_tools_folder}\" in directory \"{self.dropbox_install_location}\"."
                f"\nDropbox folder \"{sync_folder}\" will not be synced.")
            return False
        return True

    def sync_gizmos(self, folder_name: str = 'gizmos') -> None:
        """
        This is the primary method for syncing any gizmos found on Dropbox with a toolbar in Nuke. A new toolbar is
        created to house the loaded tools from Dropbox. This method expects a folder named 'gizmos' to exist
        somewhere inside the user-defined Dropbox folder.
        :return:
            None
        """
        if not self._verify(folder_name):
            return

        toolbar = nuke.toolbar('Nodes').addMenu(self.dropbox_tools_folder, icon=self.icon)
        path_to_gizmos = Path(self.dropbox_tools_folder_location / Path(folder_name))
        if not path_to_gizmos.exists():
            self._folder_not_found_error(path_to_gizmos, folder_name)

        nuke.pluginAddPath(str(path_to_gizmos), False)

        for folder in path_to_gizmos.glob('**/'):
            if str(folder) not in nuke.pluginPath():
                nuke.pluginAddPath(str(folder))
            icons = self.fetch_icons(folder)

            for file in folder.glob('*.*'):
                if file.suffix in self.VALID_GIZMO_FILE_TYPES:
                    shelf_name = self.retrieve_relative_path(file, relative_to=folder_name)
                    if file.suffix == '.gizmo':
                        create_node = f"nuke.createNode('{file.stem}')"
                    elif file.suffix == '.nk':
                        create_node = f"nuke.createNode('{file.stem + file.suffix}')"
                    else:
                        nuke.tprint(f"SharedShelves failed to load: {file}")
                        continue
                    if file.stem in icons:
                        icon_title = icons[file.stem]
                    else:
                        icon_title = ''
                    toolbar.addCommand(shelf_name, create_node, icon=icon_title)

    @staticmethod
    def retrieve_relative_path(file: Path, relative_to: str = '.nuke') -> str:
        """
        Takes in a file path and a reference folder and outputs a filepath relative to the reference folder
        :param file: Path
            The larger filepath containing the 'relative_to' folder
        :param relative_to: str
            Where the truncated filepath will start
        :return: str
            A truncated filpath relative to the 'relative_to' folder
        """
        relative_path_start = file.parts.index(relative_to) + 1
        relative_path_parts = file.parts[relative_path_start:]
        relative_path = ''

        if len(relative_path_parts) == 1:
            return file.stem
        for index, part in enumerate(relative_path_parts):
            if index == 0:
                relative_path = f'{part}'
            elif index == len(relative_path_parts) - 1:
                relative_path = f'{relative_path}/{file.stem}'
            else:
                relative_path = f'{relative_path}/{part}'

        return relative_path

    def fetch_icons(self, folder: Path) -> dict:
        """
        Creates a dictionary of all files in the specified directory that contain an extension defined in
        VALID_ICON_FILE_TYPES
        :param folder: Path
            A full-length file path
        :return: icons: dict
            A dictionary containing the stem of the image file (no extension) for the keys and the name of the image
            file (with extension) for the values.
        """
        icons = {}
        for file in folder.glob('*.*'):
            if file.suffix in self.VALID_ICON_FILE_TYPES:
                icons.update({file.stem: file.name})
        return icons

    def sync_toolsets(self, folder_name: str = 'ToolSets') -> None:
        """
        This is the primary method for syncing any toolsets found on Dropbox with Nuke's "ToolSets" folder. This method
        expects a folder named "ToolSets" (case sensitive) to exist somewhere in the user-defined Dropbox folder
        structure.
        :param folder_name: str
            The name of the Dropbox folder this method should load toolsets from. "ToolSets" by default.
        :return:
        """
        if not self._verify(folder_name):
            return

        toolsets_toolbar = nuke.toolbar('Nodes').menu('ToolSets')
        path_to_toolbar_items = Path(self.dropbox_tools_folder_location / Path(folder_name))
        if not path_to_toolbar_items.exists():
            self._folder_not_found_error(path_to_toolbar_items, folder_name)

        nuke.pluginAddPath(str(path_to_toolbar_items), False)

        for folder in path_to_toolbar_items.glob('**/'):
            if str(folder) not in nuke.pluginPath():
                nuke.pluginAddPath(str(folder))
            icons = self.fetch_icons(folder)

            for file in folder.glob('*.*'):
                if file.suffix in self.VALID_TOOLSET_FILE_TYPES:
                    shelf_name = self.retrieve_relative_path(file, relative_to=folder_name)
                    create_command = f"nuke.createNode('{file.name}')"
                    if file.stem in icons:
                        icon_title = icons[file.stem]
                    else:
                        icon_title = ''
                    toolsets_toolbar.addCommand(shelf_name, create_command, icon=icon_title)

    @staticmethod
    def _folder_not_found_error(folder_path: Path, folder_name: str) -> None:
        """
        Prompts the user with a message window informing them which folder can't be found.
        :param folder_path: Path
            The filepath where the method was looking
        :param folder_name: str
            The name of the folder the method was hoping to find
        :return: None
        """
        nuke.message(f"Unable to locate the folder \"{folder_name}\" in location: \"{folder_path}\"\n"
                     f"Check that the folder name provided EXACTLY matches the name of the folder found on Dropbox"
                     f"(case-sensitive)")

    @staticmethod
    def _publish_selection(folder_path: Path) -> None:
        """
        Saves and uploads the user-selected nodes to the shared Dropbox folder. Because Nuke Indie and Non-Commercial
        encrypt their save files, this feature is not available when using those versions.

        :return:
        """
        envs = ['indie', 'nc']
        for i in envs:
            if nuke.env[i]:
                nuke.message('This feature is not available in the Non-Commercial and Indie versions of Nuke.')
                return

        nuke_ext = '.nk'
        publish_name = 'TOOLSET_NAME'
        user_selection = nuke.selectedNodes()
        if not user_selection:
            nuke.message('No nodes selected.')
            return
        if len(user_selection) == 1 and type(user_selection[0]) in [nuke.Group, nuke.Gizmo]:
            nuke_ext = '.gizmo'
            publish_name = user_selection[0].knob('name').getValue()

        try:
            save_path = nuke.getFilename('Publish Selection to Dropbox', '*.nk; *.gizmo',
                                         folder_path + '/' + publish_name + nuke_ext, 'save')

            if not save_path:
                return

            (root, ext) = os.path.splitext(save_path)
            if not ext:
                save_path += '.nk'
            elif ext not in ['.nk', '.gizmo']:
                save_path = save_path[0:-3] + 'nk'

            if os.path.exists(save_path):
                if not nuke.ask(f'Overwrite existing {save_path}?'):
                    return
            nuke.nodeCopy(save_path)
        except Exception as e:
            nuke.tprint(e)
