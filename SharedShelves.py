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

# sharedShelvesPath = "D:\Gizmos_Master"



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
	path = os.path.join(dropbox_sync_path, r'sharedNukeTools')
	if os.path.exists(path):
		return path
	return False

sharedShelvesName = "Shared Tools"
sharedShelvesPath = get_nuke_setup_path('personal')


def create_toolbar():
	sharedFolders = get_folders_in_directory(sharedShelvesPath)

	toolbar = nuke.toolbar("Nodes")
	sharedToolbar = toolbar.addMenu(sharedShelvesName, icon=os.path.join(sharedShelvesPath, "icons/sharedToolbar.png"))
	sharedToolbar.addCommand('update', 'SharedShelves.create_toolbar()')

	nuke.pluginAddPath(sharedShelvesPath, False)
	# if sharedDirectory in sys.path:
	# 	sys.path.remove(directory)
	populate_toolbar(sharedShelvesPath, sharedToolbar)


def get_folders_in_directory(path):
	folderList = [folder for folder in os.listdir(path)
		if os.path.isdir(os.path.join(path, folder))]

	return folderList

def get_plugins_in_directory(path):
	pluginList = [file for file in os.listdir(path)
		if os.path.isfile(os.path.join(path, file))]

	return pluginList

def get_gizmo_name(gizmo):
	if not '.gizmo' in gizmo or not '.nk' in gizmo: return False

	gizmoName = os.path.splitext(gizmo)[0]
	return gizmoName

def create_toolbar_shelf_name(path):
	# rString = "(?={}).*".format(path)
	shelfName = re.findall('(?=sharedNukeTools).*', path)
	print shelfName[0]
	return shelfName[0]

def populate_toolbar(sharedDirectory, sharedToolbar):
	print 'SEARCHING: ' + sharedDirectory

	plugIns = get_plugins_in_directory(sharedDirectory)
	if plugIns:
		# print 'PLUGINS:'
		for plugIn in plugIns:
			#gizmoName = get_gizmo_name(plugIn)
			#if not gizmoName: continue
			# createNode = "nuke.createNode('" + gizmoName + "')"
			create_toolbar_shelf_name(sharedDirectory)



	else:
		# print 'NO PLUGINS'
		pass

	folders = get_folders_in_directory(sharedDirectory)
	if not folders:
		# print 'NO FOLDERS'
		return
	# print 'FOLDERS:'
	for folder in folders:
		# print folder
		populate_toolbar(os.path.join(sharedDirectory, folder), sharedToolbar)