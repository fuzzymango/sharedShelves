# LINK LUT
# version 0.0.1
# written by Isaac Spiegel
# isaacspiegel.com

import os
import sys
import json
import re

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



def link_lut():
  dropbox_sync_path = get_dropbox_location('personal')
  print dropbox_sync_path