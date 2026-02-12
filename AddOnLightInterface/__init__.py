import bpy
import os
import bpy.utils.previews

# icônes personnalisées(1 pour l'instant)

preview_collections = {}

def load_icons():
    global preview_collections

    pcoll = bpy.utils.previews.new()
    preview_collections["main"] = pcoll

    # chemin du dossier addon (portable)
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    icon_path = os.path.join(addon_dir, "logo1.png")

    if os.path.isfile(icon_path):
        pcoll.load("simple_icon", icon_path, 'IMAGE')


def unload_icons():
    global preview_collections

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)

    preview_collections.clear()



# quand on crée le workspace on force le mode object
# sinon Blender peut rester en Edit mode 
def force_object_mode():
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    return None


# interface UI simplifiée avec toggle (cache / affiche les icones)

class SIMPLE_OT_toggle_ui(bpy.types.Operator):
    bl_idname = "simple.toggle_ui"
    bl_label = "Toggle Simple UI"

    def execute(self, context):

        # cache / affiche le header de la View3D
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.show_region_tool_header = not space.show_region_tool_header

        # cache / affiche les onglets du panneau Properties(icons)
        for area in context.screen.areas:
            if area.type == 'PROPERTIES':
                for space in area.spaces:
                    if space.type == 'PROPERTIES':

                        state = not getattr(space, "show_properties_tool", True)

                        attrs = [
                            "show_properties_tool",
                            "show_properties_view_layer",
                            "show_properties_collection",
                            "show_properties_object",
                            "show_properties_data",
                            "show_properties_scene",
                        ]

                        for attr in attrs:
                            if hasattr(space, attr):
                                setattr(space, attr, state)
                        space.context = 'MODIFIER'
                        
        for area in context.screen.areas:
            if area.type == 'OUTLINER':
                for space in area.spaces:
                    if space.type == 'OUTLINER':
                        space.show_region_header = not space.show_region_header

        return {'FINISHED'}

#appliquer font
class SIMPLE_OT_apply_readable_font(bpy.types.Operator):
    bl_idname = "simple.apply_readable_font"
    bl_label = "Dyslexic Mode ON"

    def execute(self, context):

        prefs = bpy.context.preferences
        addon_dir = os.path.dirname(os.path.realpath(__file__))
        font_path = os.path.join(addon_dir, "OpenDyslexic-Regular.otf")

        if os.path.isfile(font_path):
            prefs.view.font_path_ui = font_path

        prefs.view.ui_scale = 1.3

        self.report({'INFO'}, "Dyslexic font enabled ✨")

        return {'FINISHED'}

class SIMPLE_OT_reset_font(bpy.types.Operator):
    bl_idname = "simple.reset_font"
    bl_label = "Dyslexic Mode OFF"

    def execute(self, context):

        prefs = bpy.context.preferences

        #  chemin officiel police Blender
        default_font = os.path.join(
            bpy.utils.resource_path('LOCAL'),
            "datafiles", "fonts", "bfont.ttf"
        )

        prefs.view.font_path_ui = default_font

        self.report({'INFO'}, "Font reset clean")

        return {'FINISHED'}



# applique un thème  

class SIMPLE_OT_apply_theme(bpy.types.Operator):
    bl_idname = "simple.apply_theme"
    bl_label = "Apply Simple Theme"

    def execute(self, context):

        # chemin dossier addon 
        addon_dir = os.path.dirname(os.path.realpath(__file__))

        theme_path = os.path.join(addon_dir, "Blue_Theme_Blender.xml")

        if not os.path.isfile(theme_path):
            self.report({'ERROR'}, f"Theme not found:\n{theme_path}")
            return {'CANCELLED'}

        bpy.ops.script.execute_preset(
            filepath=theme_path,
            menu_idname="USERPREF_MT_interface_theme_presets"
        )

        return {'FINISHED'}


# remet thème Blender comme avant

class SIMPLE_OT_reset_theme(bpy.types.Operator):
    bl_idname = "simple.reset_theme"
    bl_label = "Reset Theme"

    def execute(self, context):
        bpy.ops.preferences.reset_default_theme()
        return {'FINISHED'}


# crée un nouveau workspace basé sur Modeling

class SIMPLE_OT_create(bpy.types.Operator):
    bl_idname = "simple.create"
    bl_label = "Create Simple Workspace"

    def execute(self, context):

        # on garde la liste actuelle pour détecter le nouveau workspace
        old = list(bpy.data.workspaces)

        # charge Modeling depuis le startup.blend
        bpy.ops.workspace.append_activate(
            idname='Modeling',
            filepath='<startup.blend>'
        )

        # on récupère le workspace nouvellement créé
        for ws in bpy.data.workspaces:
            if ws not in old:
                context.window.workspace = ws
                ws.name = "SimpleWorkspace"
                break

        # forcer object mode après le switch
        bpy.app.timers.register(force_object_mode, first_interval=0.05)

        return {'FINISHED'}


# supprime tous les autres workspaces pour garder seulement simple
# ça nettoie interface et évite d'etre perdu

class SIMPLE_OT_delete_others(bpy.types.Operator):
    bl_idname = "simple.delete_others"
    bl_label = "Delete Other Workspaces"

    def execute(self, context):

        current = context.workspace
        others = [w for w in bpy.data.workspaces if w != current]

        bpy.data.batch_remove(others)

        return {'FINISHED'}


# bouton all for one
# crée le workspace + supprime les autres + active l’UI simplifiée
# pratique pour tout faire en un seul clic

class SIMPLE_OT_all_in_one(bpy.types.Operator):
    bl_idname = "simple.all_in_one"
    bl_label = "✨ Simple Mode ✨"

    def execute(self, context):

        # créer le workspace
        bpy.ops.simple.create()

        # attendre que append_activate ait fini
        bpy.app.timers.register(self.finish, first_interval=0.15)

        return {'FINISHED'}

    def finish(self):
        bpy.ops.simple.delete_others()
        bpy.ops.simple.toggle_ui()
        return None


# panel dans le N-panel
# affiche les boutons sur le côté droit de Blender

class VIEW3D_PT_simple_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Light Interface"
    bl_label = "Light Interface"

    def draw(self, context):
        layout = self.layout

        col = layout.column()

        # big bouton principal
        col.scale_y = 3.0
        col.scale_x = 1.3
        pcoll = preview_collections["main"]

        col.operator(
            "simple.all_in_one",
            text=" SIMPLE MODE ",
            icon_value=pcoll["simple_icon"].icon_id
        )

        col.separator()

        # autres boutons un peu plus gros aussi
        col.scale_y = 1.4
        col.operator("simple.toggle_ui", icon="HIDE_OFF")
        col.operator("simple.apply_readable_font", icon="FONT_DATA")
        col.operator("simple.reset_font", icon="LOOP_BACK")

        col.separator()

        col.operator("simple.apply_theme", icon="COLOR")
        col.operator("simple.reset_theme", icon="LOOP_BACK")


# register permet d’enregistrer les classes pour que Blender affiche le panel sur l'ui

classes = (
    SIMPLE_OT_toggle_ui,
    SIMPLE_OT_create,
    SIMPLE_OT_apply_theme,
    SIMPLE_OT_reset_theme,
    SIMPLE_OT_delete_others,
    SIMPLE_OT_all_in_one,
    SIMPLE_OT_apply_readable_font,
    SIMPLE_OT_reset_font, 
    VIEW3D_PT_simple_panel,
)


def register():
    load_icons()  # charge icône

    for c in classes:
        bpy.utils.register_class(c)


def unregister():

    for c in reversed(classes):
        bpy.utils.unregister_class(c)

    unload_icons()  # nettoie  icône


if __name__ == "__main__":
    register()