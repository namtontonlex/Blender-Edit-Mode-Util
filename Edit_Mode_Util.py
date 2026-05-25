# Edit_Mode_Util - Integrated tools for Surface Snapping and Vertex Locking
# Copyright (C) 2026 [Your Name/Organization]
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

bl_info = {
    "name": "Edit_Mode_Util",
    "author": "Gemini & ChatGPT",
    "version": (1, 1),
    "blender": (4, 0, 0),
    "description": "Integrated tools for Surface Snapping and Vertex Locking in Edit Mode",
    "category": "Mesh",
}

import bpy
import bmesh
import gpu
from gpu_extras.batch import batch_for_shader
from bpy_extras import view3d_utils
from mathutils.bvhtree import BVHTree
from mathutils import Vector
from math import sin, cos, pi

# ---------------------------------------------------------------------
# 📌 Global Variables & Constants
# ---------------------------------------------------------------------
GROUP_NAME = "Lock"
COLOR_LAYER_NAME = "LockColor"
LOCK_COLOR = (1.0, 0.0, 1.0, 0.5)    # Purple
NORMAL_COLOR = (1.0, 1.0, 1.0, 1.0)  # White

LOCKED_VERT_POSITIONS = {} 
LOCKED_VERT_INDICES = set()
ADDON_KEYMAPS = []

# ---------------------------------------------------------------------
# 🛠 Utility Functions
# ---------------------------------------------------------------------
def get_or_create_vertex_group(obj, name):
    return obj.vertex_groups.get(name) or obj.vertex_groups.new(name=name)

def ensure_color_layer(obj, name):
    if name not in obj.data.color_attributes:
        obj.data.color_attributes.new(name=name, domain='CORNER', type='BYTE_COLOR')
    return obj.data.color_attributes[name]

# ---------------------------------------------------------------------
# 🎯 Tool 1: Interactive Surface Snap
# ---------------------------------------------------------------------
class EDIT_OT_InteractiveSnap(bpy.types.Operator):
    bl_idname = "mesh.interactive_snap_tool"
    bl_label = "Interactive Surface Snap"
    bl_options = {'REGISTER', 'UNDO'}
    
    def __init__(self):
        self.target_obj = None
        self.target_bvh = None
        self.bm = None
        self.brush_size = 50.0
        self.is_drawing = False
        self.mouse_pos = Vector((0, 0))
        self._handle = None

    def modal(self, context, event):
        context.area.tag_redraw()
        self.mouse_pos = Vector((event.mouse_region_x, event.mouse_region_y))

        if event.type == 'LEFT_BRACKET' and event.value == 'PRESS':
            self.brush_size = max(5.0, self.brush_size - 10.0)
            return {'RUNNING_MODAL'}
        if event.type == 'RIGHT_BRACKET' and event.value == 'PRESS':
            self.brush_size += 10.0
            return {'RUNNING_MODAL'}

        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS': self.is_drawing = True
            elif event.value == 'RELEASE': self.is_drawing = False

        if event.type == 'MOUSEMOVE' and self.is_drawing:
            self.snap_vertices(context)
            return {'RUNNING_MODAL'}

        elif event.type in {'ESC', 'RIGHTMOUSE'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bmesh.update_edit_mesh(context.active_object.data)
            return {'FINISHED'}

        return {'PASS_THROUGH'}

    def snap_vertices(self, context):
        active_obj = context.active_object
        mw = active_obj.matrix_world
        mwi = mw.inverted()
        region = context.region
        rv3d = context.region_data
        target_mw = self.target_obj.matrix_world
        target_mwi = target_mw.inverted()

        changed = False
        for v in self.bm.verts:
            world_v_pos = mw @ v.co
            screen_pos = view3d_utils.location_3d_to_region_2d(region, rv3d, world_v_pos)
            
            if screen_pos:
                dist = (Vector(screen_pos) - self.mouse_pos).length
                if dist < self.brush_size:
                    local_target_pos = target_mwi @ world_v_pos
                    loc, norm, idx, d = self.target_bvh.find_nearest(local_target_pos)
                    if loc:
                        v.co = mwi @ (target_mw @ loc)
                        changed = True
        
        if changed:
            bmesh.update_edit_mesh(active_obj.data)

    def draw_brush_callback(self, context):
        try: shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        except: shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
            
        gpu.state.blend_set('ALPHA')
        segments, radius = 64, self.brush_size
        vertices = [(self.mouse_pos[0] + cos(i*2*pi/segments)*radius, 
                     self.mouse_pos[1] + sin(i*2*pi/segments)*radius) for i in range(segments)]
            
        batch = batch_for_shader(shader, 'LINE_LOOP', {"pos": vertices})
        shader.bind()
        shader.uniform_float("color", (1.0, 0.5, 0.0, 0.8)) 
        batch.draw(shader)
        gpu.state.blend_set('NONE')

    def invoke(self, context, event):
        if not context.active_object or context.mode != 'EDIT_MESH':
            self.report({'ERROR'}, "Please enter Edit Mode first")
            return {'CANCELLED'}

        targets = [obj for obj in context.scene.objects if obj != context.active_object and obj.type == 'MESH']
        if not targets:
            self.report({'ERROR'}, "No target mesh found in scene")
            return {'CANCELLED'}
        
        self.target_obj = targets[0]
        self.bm = bmesh.from_edit_mesh(context.active_object.data)
        
        target_bm = bmesh.new()
        target_bm.from_mesh(self.target_obj.data)
        self.target_bvh = BVHTree.FromBMesh(target_bm)
        target_bm.free()

        self._handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_brush_callback, (context,), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

# ---------------------------------------------------------------------
# 🔒 Tool 2: Vertex Lock Logic
# ---------------------------------------------------------------------
class MESH_OT_LockSelected(bpy.types.Operator):
    bl_idname = "mesh.lock_selected_verts"
    bl_label = "Lock Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH': return {'CANCELLED'}

        vg = get_or_create_vertex_group(obj, GROUP_NAME)
        bpy.ops.object.mode_set(mode='OBJECT')
        selected = [v.index for v in obj.data.vertices if v.select]

        if not selected:
            bpy.ops.object.mode_set(mode='EDIT')
            return {'CANCELLED'}

        vg.add(selected, 1.0, 'ADD')
        obj_name = obj.name
        if obj_name not in LOCKED_VERT_POSITIONS:
            LOCKED_VERT_POSITIONS[obj_name] = {}
        
        for idx in selected:
            LOCKED_VERT_POSITIONS[obj_name][idx] = obj.data.vertices[idx].co.copy()
            LOCKED_VERT_INDICES.add(idx)

        ensure_color_layer(obj, COLOR_LAYER_NAME)
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)
        color_layer = bm.loops.layers.color.get(COLOR_LAYER_NAME) or bm.loops.layers.color.new(COLOR_LAYER_NAME)

        for v in bm.verts:
            if v.index in LOCKED_VERT_INDICES:
                for loop in v.link_loops: loop[color_layer] = LOCK_COLOR
                v.select = False

        bmesh.update_edit_mesh(obj.data)
        context.area.tag_redraw()
        return {'FINISHED'}

class MESH_OT_UnlockAll(bpy.types.Operator):
    bl_idname = "mesh.unlock_all_verts"
    bl_label = "Unlock All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH': return {'CANCELLED'}

        if obj.name in LOCKED_VERT_POSITIONS: del LOCKED_VERT_POSITIONS[obj.name]
        LOCKED_VERT_INDICES.clear()

        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)
        if COLOR_LAYER_NAME in bm.loops.layers.color:
            col = bm.loops.layers.color[COLOR_LAYER_NAME]
            for v in bm.verts:
                for lp in v.link_loops: lp[col] = NORMAL_COLOR

        bpy.ops.object.mode_set(mode='OBJECT')
        if GROUP_NAME in obj.vertex_groups:
            obj.vertex_groups.remove(obj.vertex_groups[GROUP_NAME])
        
        bpy.ops.object.mode_set(mode='EDIT')
        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}

# ---------------------------------------------------------------------
# 🧠 Handlers
# ---------------------------------------------------------------------
def lock_handler(scene):
    obj = bpy.context.active_object
    if not obj or obj.mode != 'EDIT' or obj.name not in LOCKED_VERT_POSITIONS: return
    
    locked_data = LOCKED_VERT_POSITIONS[obj.name]
    bm = bmesh.from_edit_mesh(obj.data)
    changed = False
    
    for v in bm.verts:
        if v.index in locked_data:
            orig = locked_data[v.index]
            if (v.co - orig).length_squared > 0.000001:
                v.co = orig
                changed = True
        # Auto-deselect logic
        if v.index in LOCKED_VERT_INDICES and v.select:
            v.select = False
            changed = True

    if changed:
        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)

# ---------------------------------------------------------------------
# 🪟 UI Panel
# ---------------------------------------------------------------------
class VIEW3D_PT_EditUtilPanel(bpy.types.Panel):
    bl_label = "Edit Mode Utils"
    bl_idname = "VIEW3D_PT_edit_util"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Edit Util'

    def draw(self, context):
        layout = self.layout
        
        # Section 1: Surface Snap
        box = layout.box()
        box.label(text="Surface Snap", icon='SNAP_ON')
        if context.mode == 'EDIT_MESH':
            box.operator("mesh.interactive_snap_tool", text="Start Snap Brush")
            box.label(text="Use [ , ] to resize brush", icon='INFO')
            box.label(text="ESC or Right click to Exit")
        else:
            box.label(text="Switch to Edit Mode", icon='ERROR')

        # Section 2: Lock Tools
        box = layout.box()
        box.label(text="Vertex Lock", icon='LOCKED')
        row = box.row(align=True)
        row.operator("mesh.lock_selected_verts", text="Lock", icon='RESTRICT_SELECT_ON')
        row.operator("mesh.unlock_all_verts", text="Unlock All", icon='RESTRICT_SELECT_OFF')

# ---------------------------------------------------------------------
# 🔄 Registration
# ---------------------------------------------------------------------
classes = (
    EDIT_OT_InteractiveSnap,
    MESH_OT_LockSelected,
    MESH_OT_UnlockAll,
    VIEW3D_PT_EditUtilPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Handlers
    if lock_handler not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(lock_handler)
    
    # Hotkeys
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        # Alt + Space to Lock
        kmi_lock = km.keymap_items.new(MESH_OT_LockSelected.bl_idname, 'SPACE', 'PRESS', alt=True)
        # Ctrl + Alt + Space to Unlock
        kmi_unlock = km.keymap_items.new(MESH_OT_UnlockAll.bl_idname, 'SPACE', 'PRESS', ctrl=True, alt=True)
        ADDON_KEYMAPS.append((km, kmi_lock))
        ADDON_KEYMAPS.append((km, kmi_unlock))

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    if lock_handler in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(lock_handler)
        
    for km, kmi in ADDON_KEYMAPS:
        km.keymap_items.remove(kmi)
    ADDON_KEYMAPS.clear()

if __name__ == "__main__":
    register()
