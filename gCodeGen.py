bl_info = {
    "name": "G-Code Generator",
    "author": "George Smith / Korberon",
    "version": (1, 0),
    "blender": (3, 5, 1),
    "location": "View3D > Sidebar > G-Code Generator",
    "description": "Generate G-Code from path",
    "category": "Object",
}

import bpy
import os
from bpy.props import StringProperty
import numpy as npy

# UI panel
class gCodePanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_my_gCodeGen"
    bl_label = "G-Code Generator Add-on"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'G-Code Generation'

    def draw(self, context):
        layout = self.layout

        # Explanation
        layout.label(text="Please locate the origin at the start of the") ;
        layout.label(text="line you wish to cut and press generate") ;
        # Add the generate G-Code button
        layout.operator("object.generate_gcode")
        # Add text input box
        layout.label(text="Optional:") ;
        layout.prop(context.scene,"feedrate_prop") ;
        layout.prop(context.scene,"y1_prop") ;
        layout.prop(context.scene,"z1_prop") ;
        layout.prop(context.scene,"y2_prop") ;
        layout.prop(context.scene,"z2_prop") ;
    
# Operator
class GenerateGCode(bpy.types.Operator):
    bl_idname = "object.generate_gcode"
    bl_label = "Generate G-Code"

    def execute(self, context):

        # Get the current location of the blend file
        current_file_path = bpy.data.filepath
        current_directory = os.path.dirname(current_file_path)
        csvFile = current_directory+"/outputCoords.csv" ;
        txtFile = current_directory+"/outputGCode.txt" ;

        # Get the selected object and its data
        selected_object = bpy.context.active_object ;
        # Detect if there is no selected object
        if selected_object is None or not selected_object.select_get():
            raise Exception("ERROR: You have no currently selected object!") ;
        
        ## Make a curved copy of the object
        # Duplicate the selected object
        duplicated_object = selected_object.copy()
        duplicated_object.data = selected_object.data.copy()

        # Link the duplicated object to the scene
        bpy.context.collection.objects.link(duplicated_object)

        # Set the duplicated object as the active object
        bpy.context.view_layer.objects.active = duplicated_object
        duplicated_object.select_set(True)

        # Clear the selection of the original object
        selected_object.select_set(False)

        # Now the duplicated object is selected and can be accessed using 'duplicated_object' or 'work_object'
        work_object = duplicated_object
        work_object.name = "Working Piece" ;
        bpy.ops.object.mode_set(mode='OBJECT')

        # Select the object and make it the active object
        work_object.select_set(True)
        bpy.context.view_layer.objects.active = work_object

        # Convert the selected object to a curve
        bpy.ops.object.convert(target='CURVE')
        
        # Detect if selected object has multiple splines
        if len(work_object.data.splines) > 1:
            raise Exception("ERROR: Only one curve is allowed, please limit the object to a single cut") ;

        ## Is the origin on a starting point?
        if npy.linalg.norm(work_object.data.splines[0].points[0].co) <= 0.000001 :
            print("Origin at start of curve") ;
        elif npy.linalg.norm(work_object.data.splines[0].points[-1].co) <= 0.000001 :
            print("Origin at end of curve, adjusting curve direction...") ;

            # Reverse direction
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.curve.select_all(action='SELECT')
            bpy.ops.curve.switch_direction()
            bpy.ops.object.mode_set(mode='OBJECT')
            
            if npy.linalg.norm(work_object.data.splines[0].points[0].co) <= 0.000001 :
                print("Adjusted successfully") ;
        else:
            raise Exception("ERROR: The origin of the object is not located at the start of the curve!") ;
            

        # Export the GCode !
        # Get the coordinates in the y/z plane (numpad 3)
        coords = npy.array([[v.co[1], v.co[2]] for spline in work_object.data.splines for v in spline.points])

        # Convert coordinates from meters to millimeters
        coords *= 1000

        # Export the raw coordinates to CSV file
        npy.savetxt(csvFile, coords, delimiter=',')

        # Generate G-Code
        # check if Feedrate is int
        try:
            float(context.scene.feedrate_prop) ;
        except:
            print("Invalid feedrate detected, resorting to default") ;
            feedrate = float(150) ;
        else:
            feedrate = float(context.scene.feedrate_prop)

        # Get XYZA
        y1 = str(context.scene.y1_prop) ; z1 = str(context.scene.z1_prop) ;
        y2 = str(context.scene.y2_prop) ; z2 = str(context.scene.z2_prop) ;
        gCode = ["G01F"+str(feedrate)] + [f"{y1}{format(row[0], 'f')}{z1}{format(row[1], 'f')}{y2}{format(row[0], 'f')}{z2}{format(row[1], 'f')}" for row in coords]

        # Write G-Code to text file
        with open(txtFile, 'w') as file:
            file.write('\n'.join(gCode))
        
        # Print the success
        self.report({"INFO"},"G-Code and CSV files generated successfully.") ;
        bpy.data.objects.remove(work_object, do_unlink=True)
        return{'FINISHED'} ;

# Register and unregister
def register():
    bpy.utils.register_class(gCodePanel)
    bpy.utils.register_class(GenerateGCode)
    bpy.types.Scene.feedrate_prop = bpy.props.StringProperty \
                                     (
                                         name = "  Feedrate",
                                         description = "Enter feedrate for cutting (mm/min)",
                                         default = "150"
                                         )
    bpy.types.Scene.y1_prop = bpy.props.StringProperty \
                                     (
                                         name = "  y1",
                                         description = "Enter the notation for the first horizontal direction syntax on your wire cutter",
                                         default = "X"
                                         )
    bpy.types.Scene.z1_prop = bpy.props.StringProperty \
                                     (
                                         name = "  z1",
                                         description = "Enter the notation for the first vertical direction syntax on your wire cutter",
                                         default = "Y"
                                         )
    bpy.types.Scene.y2_prop = bpy.props.StringProperty \
                                     (
                                         name = "  y2",
                                         description = "Enter the notation for the second horizontal direction syntax on your wire cutter",
                                         default = "Z"
                                         )
    bpy.types.Scene.z2_prop = bpy.props.StringProperty \
                                     (
                                         name = "  z2",
                                         description = "Enter the notation for the second vertical direction syntax on your wire cutter",
                                         default = "A"
                                         )

def unregister():
    bpy.utils.unregister_class(gCodePanel)
    bpy.utils.unregister_class(GenerateGCode)
    del bpy.types.Scene.feedrate_prop
    del bpy.types.Scene.y1_prop
    del bpy.types.Scene.z1_prop
    del bpy.types.Scene.y2_prop
    del bpy.types.Scene.z2_prop

if __name__ == "__main__":
    register()
