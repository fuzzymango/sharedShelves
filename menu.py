from SharedShelves import SharedShelves
s = SharedShelves(dropbox_tools_folder='sharedNukeTools', icon=None, account_type='personal')
s.sync_gizmos()
print(s.dropbox_install_location)
print(s.dropbox_tools_folder_location)


