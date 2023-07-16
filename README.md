# G-Code-Generator-in-Blender
Blender addon to produce G-Code for a given geometry

bl_info = {
    "name": "G-Code Generator",
    "author": "George Smith / Korberon",
    "version": (1, 0),
    "blender": (3, 5, 1),
    "location": "View3D > Sidebar > G-Code Generator",
    "description": "Generate G-Code from path",
    "category": "Object",
}


Thank you for using my Addon!
You don't need to extract the .zip to use this addon, but you do need to extract the .blend if you wish (explained in two lines)
I will give a simple set and a precise set of instructions, based on your blender experience.
Furthermore, a .blend file is supplied that walks through the process in detail using an example piece.

Please follow the simplified instructions below:
	- Create / import your path of vertices to cut (this can be a mesh or curve)
	- Rotate the curve so that it is in the y/z plane (looking from x positive / NumPad3)
	- Set the origin of the object to the start. This is the location that the G-Code will be zeroed at as well as the first vertex in the path
	- Press "Generate G-Code" and the G-Code and a csv of coordinates will be found in the same directory

If you are an inexperienced blender use, please follow the precise instructions below:
	- Import your CAD file using a .stl format
	- Select the object and go into edit mode [tab]
	- Go into vertex select mode [1] and select the vertices you wish the foam cutter to trace
		  - It may be helpful to know that if you select one vertex, then control+click another, it will draw the shortest path between them
		  - Repeat this for the full tool path
	- Separate these vertices [P > By Selection] and go out of edit mode [tab]
	- Select the new object, containing only these vertices, and hide all other objects [Shift+H]
		  - To unhide objects, press [Alt+H], or tick the eye in the top right
	- Go into edit mode [tab] and select the vertex you want the path to start at. This will be the origin of the curve and where the foam cutter will be zeroed
	- Place the 3D cursor on the vertex by pressing [Shift+S] and select "3D cursor to selected"
		  - There should be a dashed ring around the vertex
	- Exit out of edit mode [tab] and bring up the search menu [F3], and search for "Origin to 3D cursor", and select the entry
	- Within the 3D cursor, there should not be an orange point, denoting the origin of the object
	- Press N to bring up the properties menu, select the "Generate G-Code" addon panel, and click "Generate G-Code"
	- The code should be successfully generated, and a csv file in the same directory as the blend file used :)
		  - Any errors should be displayed over the mouse cursor when the generate button is activated

Thank you for using and please contact me if there are any issues
