# LINK LUT
# version 0.0.1
# written by Isaac Spiegel
# isaacspiegel.com

import os
import sys
import json
import re

LUT_NAME = 'blackf_REC_v2.cube'

def get_dropbox_location(account_type):
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


def find_folder(path, folderName):
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


def main():
  dropbox_sync_path = get_dropbox_location('personal')
  folderPath = find_folder(dropbox_sync_path, 'lut')
  file = find_file_in_directory(folderPath, LUT_NAME)

  filePath = os.path.join(folderPath, file[0])
  return filePath



lutFile = main().replace(os.sep, '/')
n = nuke.selectedNode()
n['file'].setValue(lutFile)
