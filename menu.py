from SharedShelves import SharedShelves
s = SharedShelves(dropbox_tools_folder='DROPBOX_FOLDER_NAME', icon=None, account_type='personal')
s.sync_gizmos('gizmos')
s.sync_toolsets('ToolSets')


