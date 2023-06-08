import bpy
import random

# put this addon in the 'sidebar'

bl_info = {
    "name": "Randomize Color",
    "blender": (2, 80, 0),
    "category": "Object",
    "location": "3D View > UI > Randomize Object(s) Color",
}

class ROCLayout(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Randomize Object(s) Color"
    bl_idname = "ROC_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Randomize Color"

    def draw(self, context):
        layout = self.layout
        column = layout.column(align=True)
        
        
        # Big render button
        layout.label(text="Randomize Object(s) Color:")
        row = layout.row()
        row.scale_y = 1.0
        row.operator("object.randomize_color")

class RandomizeColor(bpy.types.Operator):
    bl_idname = "object.randomize_color"
    bl_label = "Randomize Object(s) Color"
    #bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        # get selected object(s)
        rgb = random_color_gen()
        r = float(rgb[0])
        g = float(rgb[1])
        b = float(rgb[2])

        # iterate over selected objects
        random_color = bpy.data.materials.new("Random Color")
       
        random_color.use_nodes = True
        tree = random_color.node_tree
        nodes = tree.nodes
        bsdf = nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (r,g,b,1)
        random.diffuse_color = (r,g,b,1)
            
        for o in bpy.context.selected_objects:
             o.active_material = random_color # assign them the random rgb values

        return {'FINISHED'}

# set idname in there
def menu_func(self, context):
    self.layout.operator(RandomizeColor.bl_idname)

def random_color_gen():
    rgb = [] # array for r,g, and b
    # randomly assign each value
    rgb.append(format(random.uniform(0,1),'.7f'))
    rgb.append(format(random.uniform(0,1),'.7f'))
    rgb.append(format(random.uniform(0,1),'.7f'))
    return rgb

#print(type(random_color_gen()[0]))
#print(random_color_gen()[1])
#print(random_color_gen()[2])
#print(selection_names)

def register():
    bpy.utils.register_class(RandomizeColor)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    bpy.utils.register_class(ROCLayout)
def unregister():
    bpy.utils.unregister_class(RandomizeColor)
    bpy.utils.unregister_class(ROCLayout)

if __name__ == "__main__":
    register()

"""
SOURCES:

https://www.bing.com/videos/search?q=how+to+make+a+blender+plugin&view=detail&mid=8AEC4337ABD2CE5EF1278AEC4337ABD2CE5EF127&FORM=VIRE

https://blender.stackexchange.com/questions/36281/bpy-context-selected-objects-context-object-has-no-attribute-selected-objects#:~:text=The%20context%20is%20dependent%20on%20quite%20a%20number,o%20for%20o%20in%20bpy.context.scene.objects%20if%20o.select%20%5D

https://stackoverflow.com/questions/27265915/get-list-of-selected-objects-as-string-blender-python

https://blender.stackexchange.com/questions/153094/blender-2-8-python-how-to-set-material-color-using-hex-value-instead-of-rgb#:~:text=import%20bpy%20def%20hex_to_rgb%20%28hex_value%29%3A%20b%20%3D%20%28hex_value,0xE7E7FF%20obj%20%3D%20bpy.context.object%20add_material%20%28obj%2C%20%22test%22%2C%20h%29

https://blender.stackexchange.com/questions/201874/how-to-add-a-color-to-a-generated-cube-within-a-python-script#:~:text=What%20you%20can%20do%20using%20ops%20is%3A%20import,in%20solid%20view%20when%20object%20is%20selected%20here%3A

https://blender.stackexchange.com/questions/80735/change-diffuse-color-for-all-selected-objects-in-scene-with-python#:~:text=import%20bpy%20r%2Cg%2Cb%20%3D%20%280.1%2C%200.5%2C%200.7%29%20%23,color%20to%20the%20specified%20RGB%20o.active_material.diffuse_color%20%3D%20%28r%2Cg%2Cb%29

https://www.w3docs.com/snippets/python/limiting-floats-to-two-decimal-points.html

https://blender.stackexchange.com/questions/251254/how-to-set-color-object-using-python-and-blender-3-0-individually-using-a-templa

"""