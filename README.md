# Share Gizmos and ToolSets from Dropbox to Nuke!
## Installation Instructions
1. Download the "SharedShelves.py" file and place it in your .nuke directory. 
2. Copy the contents from "menu.py" and paste them in your menu.py file located in your .nuke directory.
3. Edit the parameters in the SharedShelves() method with your unique Dropbox information (see below) 


**dropbox_tools_folder**: --CASE SENSITIVE-- The name of the folder in your Dropbox containing the gizmos and 
toolsets you'd like to sync. Change this parameter to exactly match the name of your Dropbox folder. For example,
if your folder sturcture appears as below on Dropbox. Set the `dropbox_tools_folder` parameter to `sharedNukeTools`.

```commandline
        sharedNukeTools
            gizmos
                myCoolGizmo
                anotherNeatGizmo
                etc.
            ToolSets
                shotTemplate
                keyerTemplate
                etc.
```

**icon**: Change this to the filepath of icon you'd like to appear for the toolbar menu in Nuke. For example: 
`icon='G:/Dropbox/sharedNukeToolsBETA/icons/sharedToolbar.png'`

**account_type**: Change this to match the type of Dropbox account that you're using (business, personal, etc.)

Using the above examples, my SharedShelves class would look like this: 
`s = SharedShelves(dropbox_tools_folder='sharedNukeToolsBETA', icon='G:/Dropbox/sharedNukeToolsBETA/icons/sharedToolbar.png', account_type='personal')`