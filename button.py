#Code permettant d'en plus de créer les boutons, faire disparaître des régions du viewport :

#AMELIORATION : 
#Fait disparaître juste les trucs nuls

import bpy

# ------------------------
# OPERATOR
# ------------------------

class SIMPLE_OT_toggle_header(bpy.types.Operator):
    bl_idname = "simple.toggle_header"
    bl_label = "Toggle Header"

    def execute(self, context):
        context.space_data.show_region_tool_header = not context.space_data.show_region_tool_header
        return {'FINISHED'}


# ------------------------
# PANEL
# ------------------------

class View_3D_Npanel_SimplePanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SIMPLE"
    bl_label = "SIMPLE"

    def draw(self, context):
        layout = self.layout

        layout.operator("simple.toggle_header", text="Toggle Header")

        layout.operator("mesh.primitive_ico_sphere_add", text="Add Ico Sphere")
        layout.operator("object.shade_smooth", text="Shade Smooth")


# ------------------------
# REGISTER
# ------------------------

classes = (
    SIMPLE_OT_toggle_header,
    View_3D_Npanel_SimplePanel,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register() 
