# SHARED SHELVES
# version 0.0.2
# developed by Adam Thompson 2018
# updated by Isaac Spiegel 2021
# isaacspiegel.com

import nuke
import os
import sys
import json
import re

SHARED_TOOLS_FOLDER_NAME = r'sharedNukeTools'

VALID_ICON_FILE_TYPES = ['.png', '.jpg']
VALID_GIZMO_FILE_TYPES = ['.gizmo', '.nk']



def get_dropbox_location(account_type):
	info_path = create_dropbox_info_path('LOCALAPPDATA')
	info_dict = get_dictionary_from_path_to_json(info_path)
	return info_dict[account_type]['path']

def create_dropbox_info_path(appdata_str):
	path = os.path.join(os.environ[appdata_str], r'Dropbox\info.json')
	if os.path.exists(path):
		return path
	return False

def get_dictionary_from_path_to_json(info_path):
	with open(info_path, 'r') as f:
		text = f.read()

	return json.loads(text)	

def get_nuke_setup_path(account_type):
	dropbox_sync_path = get_dropbox_location(account_type)
	path = os.path.join(dropbox_sync_path, SHARED_TOOLS_FOLDER_NAME)
	if os.path.exists(path):
		return path
	return False

sharedShelvesName = "Shared Tools"
SHARED_SHELVES_PATH = get_nuke_setup_path('personal')


def create_toolbar():
	sharedFolders = get_folders_in_directory(SHARED_SHELVES_PATH)

	toolbar = nuke.toolbar("Nodes")
	sharedToolbar = toolbar.addMenu(sharedShelvesName, icon=os.path.join(SHARED_SHELVES_PATH, "icons/sharedToolbar.png"))
	sharedToolbar.addCommand('update', 'SharedShelves.create_toolbar()')

	print 'LOADING PLUGINS.....'
	populate_toolbar(SHARED_SHELVES_PATH, sharedToolbar)


def get_folders_in_directory(path):
	folderList = [folder for folder in os.listdir(path)
		if os.path.isdir(os.path.join(path, folder))]

	return folderList

def get_plugins_in_directory(path):
	pluginList = [file for file in os.listdir(path)
		if os.path.isfile(os.path.join(path, file))]

	return pluginList

def get_gizmo_name(gizmo):
	if [ext for ext in VALID_GIZMO_FILE_TYPES if(ext in gizmo)]:
		gizmoName = os.path.splitext(gizmo)[0]
		return gizmoName

	return False

def create_toolbar_shelf_name(path, gizmoName):
	rString = "(?={}).*".format(SHARED_TOOLS_FOLDER_NAME)
	shelfNameBkSlash = re.findall(rString, path)
	shelfNameFwdSlash = shelfNameBkSlash[0].replace(os.sep, '/')
	return '{}/{}'.format(shelfNameFwdSlash, gizmoName)

def get_gizmo_icon(path, gizmoName):
	files = get_plugins_in_directory(path)
	for file in files:
		if gizmoName not in file: continue
		fileExtension = os.path.splitext(file)[1]
		if fileExtension in VALID_GIZMO_FILE_TYPES: continue
		if fileExtension in VALID_ICON_FILE_TYPES:
			return file
		return None


# POPULATE TOOLBAR
# recursively loops through a folder structure adding any .nk or .gizmo files to the shared toolbar
# sharedDirectory: the filepath to look for plugins
# sharedToolbar: the nuke toolbar where the plugins will be added
def populate_toolbar(sharedDirectory, sharedToolbar):
	print 'SEARCHING: ' + sharedDirectory
	nuke.pluginAddPath(sharedDirectory, False)
	plugIns = get_plugins_in_directory(sharedDirectory)
	if plugIns:
		for plugIn in plugIns:
			textOutput = plugIn + "...................."
			gizmoName = get_gizmo_name(plugIn)
			if not gizmoName: continue
			try:
				shelfPath = create_toolbar_shelf_name(sharedDirectory, gizmoName)
				createNode = "nuke.createNode('{}')".format(gizmoName)
				icon = get_gizmo_icon(sharedDirectory, gizmoName)
				sharedToolbar.addCommand(shelfPath, createNode, icon=icon)
				print textOutput + 'SUCCESS'
			except:
				print textOutput + 'FAILED'

	else:
		print 'NO PLUGINS FOUND'
		pass

	folders = get_folders_in_directory(sharedDirectory)
	if not folders:
		return
	for folder in folders:
		populate_toolbar(os.path.join(sharedDirectory, folder), sharedToolbar)