# Sync your Gizmos and ToolSets from Dropbox to Nuke!

The SharedShelves Python script an out-of-the-box pipeline solution for small production studios (or individuals) that enables multiple 
remote artists to easily share their gizmos, templates, plug-ins, and toolsets with other team members.
The SharedShelves pipeline allows any artist to share their plug-ins to other team members by simply pasting .gizmo or .nk
files into a shared Dropbox folder. The SharedShelves script will reference the Dropbox folder and when Nuke launches, 
load any plug-ins from the folder into a new shelf in the toolbar with the same name as the Dropbox folder. Other artists
are then able to access the shared tools using Nuke's tab menu or toolbar window.

## Installation Instructions
1. Create a folder inside Dropbox and place your tools inside. 
2. Download the "SharedShelves.py" file and place it in your .nuke directory. 
3. Copy the contents from "menu.py" and paste them in your menu.py file located in your .nuke directory.
4. Edit the parameters in the SharedShelves() method with your unique Dropbox information (see below) 

>**dropbox_tools_folder**: --CASE SENSITIVE-- The name of the folder in your Dropbox containing the gizmos and 
toolsets you'd like to sync. Change this parameter to exactly match the name of your Dropbox folder. For example,
if your folder structure appears as below on Dropbox. Set the `dropbox_tools_folder` parameter to `sharedNukeTools`.

```commandline
    Dropbox/
        sharedNukeTools/
            gizmos/
                myCoolGizmo.gizmo
                anotherNeatGizmo.gizmo
                ...
            ToolSets/
                shotTemplate.nk
                keyerTemplate.nk
                ...
```

>**icon**: Change this to the filepath of icon you'd like to appear for the toolbar menu in Nuke. For example: 
`icon='G:/Dropbox/sharedNukeTools/icons/sharedToolbar.png'` Optional

>**account_type**: Change this to match the type of Dropbox account that you're using (personal, business, etc.)
> The default is `personal`

>Using the above examples, my SharedShelves class would look like this: 
`s = SharedShelves(dropbox_tools_folder='sharedNukeTools', icon='G:/Dropbox/sharedNukeTools/icons/sharedToolbar.png', account_type='personal')`
4. Edit the `folder_name` parameter for both `s.sync_gizmos()` and `s.sync_toolsets()` to EXACTLY match (case-sensitive) the name Dropbox folder where your gizmos and toolsets are stored. 
For example, if your gizmos are stored in `Dropbox/sharedNukeTools/myGizmos`, your sync_gizmos would be `s.sync_gizmos("myGizmos")`. 
By default, `sync_gizmos()` will look for a folder named "gizmos" and `sync_toolsets()` will look for a folder named "ToolSets".
5. Launch Nuke!