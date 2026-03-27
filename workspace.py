import bpy

workSpaceList = []

for workspace in bpy.data.workspaces :
    workSpaceList.append(workspace)

bpy.ops.workspace.append_activate(idname = 'Layout', filepath = '<startup.blend>')
    
for workspace in bpy.data.workspaces :
    if not workspace in workSpaceList : 
        bpy.context.window.workspace = workspace
        workspace.name = "SimpleWorkspace"