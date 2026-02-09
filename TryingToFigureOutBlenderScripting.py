import bpy

# Print all objects
for obj in bpy.data.objects:
    print(obj.name + " " + obj.type)
#    bpy.data.objects.remove(obj, do_unlink=True)


# Print all scene names in a list.
print(bpy.data.scenes.keys())


## Reset scene
#for name in ["Cube", "Camera", "Light"]:
#    if name in bpy.data.objects:
#        obj = bpy.data.objects[name]
#        print("removing object", obj)
#        bpy.data.objects.remove()


# Write images into a file next to the blend.
import os
with open(os.path.splitext(bpy.data.filepath)[0] + ".txt", 'w') as fs:
    for image in bpy.data.images:
        fs.write("{:s} {:d} x {:d}\n".format(image.filepath, image.size[0], image.size[1]))