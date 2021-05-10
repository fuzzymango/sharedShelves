# SHARED SHELVES
# version 0.1.1
# developed by Adam Thompson 2018
# updated by Isaac Spiegel 2021
# isaacspiegel.com

# place this in menu.py
# import SharedShelves
# SharedShelves.main()

import nuke
import os
import sys
import json
import re

SHARED_TOOLS_FOLDER_NAME = r'sharedNukeToolsBETA'
LUT_FILE_NAME = 'blackf_REC_v2.cube'



VALID_ICON_FILE_TYPES = ['.png', '.jpg']
VALID_GIZMO_FILE_TYPES = ['.gizmo', '.nk', '.hroxind']
TERMINAL_WINDOW_LEN = 110
ACCOUNT_TYPE = 'personal'

def get_dropbox_location(account_type):
	ACCOUNT_TYPE = account_type
	info_path = create_dropbox_info_path('LOCALAPPDATA')
	info_dict = get_dictionary_from_path_to_json(info_path)
	return info_dict[account_type]['path']

def create_dropbox_info_path(appdata_str):
	path = os.path.join(os.environ[appdata_str], r'Dropbox\info.json')
	if os.path.exists(path):
		return path
	return None

def get_dictionary_from_path_to_json(info_path):
	with open(info_path, 'r') as f:
		text = f.read()

	return json.loads(text)	

# FIND SHARED TOOLS FOLDER
# walks through the synced dropbox filepath looking for the shared nuke tools folder
# path: the filepath pointing to the synced dropbox folder
def find_shared_tools_folder(path):
	for roots, dirs, files in os.walk(path, topdown=True):
		if SHARED_TOOLS_FOLDER_NAME in dirs:
			return os.path.join(roots, SHARED_TOOLS_FOLDER_NAME)


# GET NUKE SETUP PATH
# returns the filepath where dropbox syncs
# account_type: the type of dropbox account the user has. 'personal' or 'buisiness'
def get_nuke_setup_path(account_type):
	dropbox_sync_path = get_dropbox_location(account_type)
	path = find_shared_tools_folder(dropbox_sync_path)
	if os.path.exists(path):
		return path
	return None

sharedShelvesName = "Shared Tools"
SHARED_UTILITIES_MENU_NAME = 'Shared Utilities'
SHARED_SHELVES_PATH = get_nuke_setup_path('personal')
SHARED_SHELVES_PATH_GIZMOS = os.path.join(SHARED_SHELVES_PATH, 'gizmos')
SHARED_SHELVES_PATH_TOOLSETS = os.path.join(SHARED_SHELVES_PATH, 'ToolSets')
SHARED_SHELVES_PATH_KNOB_DEFAULTS = os.path.join(SHARED_SHELVES_PATH, 'knob_defaults.py')
SHARED_SHELVES_PATH_PYTHON_SCRIPTS = os.path.join(SHARED_SHELVES_PATH, 'scripts')

# MAIN
# execute this function to start the program
def main():
	print 'BETA BETA BETA'
	create_toolbar()
	print 'SETTING KNOB DEFAULTS...'
	set_knob_defaults(SHARED_SHELVES_PATH_KNOB_DEFAULTS)
	print 'LOADING PYTHON SCRIPTS...\n'
	populate_scripts_menu(SHARED_SHELVES_PATH_PYTHON_SCRIPTS)


# CREATE TOOLBAR
# creates a Nuke menu toolbar to store tools synced from Dropbox
def create_toolbar():
	sharedFolders = get_folders_in_directory(SHARED_SHELVES_PATH)

	toolbar = nuke.toolbar("Nodes")
	sharedToolbar = toolbar.addMenu(sharedShelvesName, icon=os.path.join(SHARED_SHELVES_PATH, "icons/sharedToolbar.png"))

	print 'LOADING PLUGINS.....\n'
	populate_toolbar(SHARED_SHELVES_PATH_GIZMOS, sharedToolbar)
	print 'LOADING PLUGINS COMPLETE\n'

	print 'LOADING UTILITIES.....\n'
	populate_toolsets_menu(SHARED_SHELVES_PATH_TOOLSETS, sharedToolbar)
	print 'LOADING UTILITIES COMPLETE\n'


def get_folders_in_directory(path):
	folderList = [folder for folder in os.listdir(path)
		if os.path.isdir(os.path.join(path, folder))]

	return folderList

def get_plugins_in_directory(path):
	pluginList = [file for file in os.listdir(path)
		if os.path.isfile(os.path.join(path, file))]

	return pluginList

def find_folder_in_directory(path, folderName):
  for roots, dirs, files in os.walk(path, topdown=True):
    if folderName in dirs:
      folderPath = os.path.join(roots, folderName)
  if os.path.exists(folderPath):
    return folderPath
  return None	

def find_file_in_directory(path, fileName):
  fileList = [file for file in os.listdir(path)
    if os.path.isfile(os.path.join(path, file))]

  return fileList

def get_gizmo_name(gizmo):
	if [ext for ext in VALID_GIZMO_FILE_TYPES if(ext in gizmo)]:
		gizmoName = os.path.splitext(gizmo)[0]
		return gizmoName

	return None

def create_toolbar_shelf_name(path, name, folder):
	rString = "(?={}).*".format(folder)
	shelfNameBkSlash = re.findall(rString, path)
	shelfNameFwdSlash = shelfNameBkSlash[0].replace(os.sep, '/')
	return '{}/{}'.format(shelfNameFwdSlash, name)
	

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
# directory: the filepath to look for plugins
# sharedToolbar: the nuke toolbar where the plugins will be added
def populate_toolbar(directory, sharedToolbar):
	print 'SEARCHING: ' + directory
	nuke.pluginAddPath(directory, False)
	plugIns = get_plugins_in_directory(directory)
	if plugIns:
		for plugIn in plugIns:
			textOutput = plugIn + "."*(TERMINAL_WINDOW_LEN-len(plugIn)-7)
			gizmoName = get_gizmo_name(plugIn)
			if not gizmoName: continue
			try:
				shelfPath = create_toolbar_shelf_name(directory, gizmoName, 'gizmos')
				createNode = "nuke.createNode('{}')".format(gizmoName)
				icon = get_gizmo_icon(directory, gizmoName)
				sharedToolbar.addCommand(shelfPath, createNode, icon=icon)
				print textOutput + 'SUCCESS'
			except:
				print textOutput + 'FAILED '

	else:
		print 'NO PLUGINS FOUND'
		pass

	folders = get_folders_in_directory(directory)
	if not folders:
		return
	for folder in folders:
		populate_toolbar(os.path.join(directory, folder), sharedToolbar)


# POPULATE TOOLSETS MENU
# recursively loops through a folder structure adding any .nk files to the shared toolbar
# directory: the filepath to look for plugins
# sharedToolbar: the nuke toolbar where the plugins will be added
def populate_toolsets_menu(directory, sharedToolbar):
	print 'SEARCHING: ' + directory
	nuke.pluginAddPath(directory, False)
	toolsets = get_plugins_in_directory(directory)
	if toolsets:
		try:
			for tool in toolsets:
				textOutput = tool + "."*(TERMINAL_WINDOW_LEN-len(tool)-7)
				toolName = get_gizmo_name(tool)
				if not toolName: continue
				shelfPath = create_toolbar_shelf_name(directory, toolName, 'ToolSets')
				toolsetPath = os.path.join(directory, tool)
				createToolset = "nuke.loadToolset('{}')".format(toolsetPath.replace(os.sep, '/'))
				sharedToolbar.addCommand(shelfPath, createToolset)
				print textOutput + 'SUCCESS'
		except:
			print textOutput + 'FAILED'

	else:
		print 'NO TOOLSETS FOUND'
		pass

	folders = get_folders_in_directory(directory)
	if not folders:
		return
	for folder in folders:
		populate_toolsets_menu(os.path.join(directory, folder), sharedToolbar)

# SET KNOB DEFAULTS
# reads executes the knob_defaults.py file in the shared dropbox folder
# scriptPath: the filepath leading to the knob_defaults.py file
def set_knob_defaults(scriptPath):
	if not os.path.exists(scriptPath):
		print 'UNABLE TO LOCATE knob_defaults.py'
		return
	
	try: 
		path = scriptPath
		execfile(path)
		print 'KNOB DEFAULTS LOADED\n'
	except Exception as e:
		errorMessage = 'ERROR: {}\nFailed to set knob defaults. Check the knob_defaults.py file.'.format(str(e))
		nuke.message(errorMessage)



def shot_starter():
	toolsetPath = os.path.join(SHARED_SHELVES_PATH_PYTHON_SCRIPTS, 'BF_shotstarter', 'BF_ShotStarter.nkind')
	nuke.loadToolset(toolsetPath)

	dropbox_sync_path = get_dropbox_location(ACCOUNT_TYPE)
	lutFolderPath = find_folder_in_directory(dropbox_sync_path, 'lut')
	lutFile = find_file_in_directory(lutFolderPath, LUT_FILE_NAME)
	lutFilePath = os.path.join(lutFolderPath, lutFile[0]).replace(os.sep, '/')
	if not os.path.exists(lutFilePath):
		errorMessage = 'ERROR: LUT file not found\\n{}'.format(lutFilePath)
		nuke.message(errorMessage)
		return

	viewerInput = nuke.toNode('VIEWER_INPUT')
	viewerInput.begin()
	viewerInputOCIOtransform = nuke.toNode('OCIOFileTransform_LUT_FILE')
	viewerInputOCIOtransform['file'].setValue(lutFilePath)
	viewerInput.end()

	bakeLUT = nuke.toNode('OCIOFileTransform_BAKE_LUT')
	bakeLUT['file'].setValue(lutFilePath)

	projectFormat = "{} {} {}".format(2880, 2160, 2, 'black_firday')
	
	nuke.root()['format'].setValue(nuke.addFormat(projectFormat))



# POPULATE SCRIPT MENU
# loads and adds python scripts to a Nuke menu 
# scrips must be hardcoded here in order to be loaded and added
# scriptsFolderDirectory: the filepath pointing to where the scripts are stored
def populate_scripts_menu(scriptsFolderDirectory):
	print 'SEARCHING: ' + scriptsFolderDirectory
	if not os.path.exists(scriptsFolderDirectory):
		print 'UNABLE TO LOCATE SCRIPTS DIRECTORY'
		return

	nuke.pluginAddPath(scriptsFolderDirectory)
	nuke.pluginAddPath(os.path.join(scriptsFolderDirectory, 'BF_shotstarter'))

	scriptsMenu = nuke.menu('Nuke').addMenu('Shared Scripts')
	# scripts menu syntax for adding other scripts
	# scriptsMenu.addCommand('script menu name', 'import scriptName; scriptName.startFunc()')
	scriptsMenu.addCommand('BF Shot Starter', lambda:shot_starter())
	scriptsMenu.addCommand('Read from Write', 'import read_from_write; read_from_write.read_from_write()', 'alt+r', shortcutContext = 2)

	print 'SCRIPTS LOADED'