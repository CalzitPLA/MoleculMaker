"""
Name: MoleculeMaker.py
Author: nemo
"""

import math
import FreeCAD
from FreeCAD import Placement, Rotation, Vector
import FreeCADGui
import Part

DOC_NAME = "test_molecule"

if FreeCAD.ActiveDocument is None:
    FreeCAD.newDocument(DOC_NAME)
    print(f"Document: {DOC_NAME}")

# test if there is an active document with a "proper" name
if FreeCAD.ActiveDocument.Name == DOC_NAME:
    print("DOC_NAME exist")
else:
    print("DOC_NAME is not active")
    # test if there is a document with a "proper" name
    try:
        FreeCAD.getDocument(DOC_NAME)
    except NameError:
        print(f"No Document: {DOC_NAME}")
        FreeCAD.newDocument(DOC_NAME)
        print(f"Document Created: {DOC_NAME}")

DOC = FreeCAD.getDocument(DOC_NAME)
GUI = FreeCADGui.getDocument(DOC_NAME)
VIEW = GUI.ActiveView


# path and name of sphere file

pfad = "/home/nemo/Dokumente/Privat/Fredo/aspirin.sphere.asc"
# path and name of links file
pfad1 = "/home/nemo/Dokumente/Privat/Fredo/aspirin.verbindung.asc"

# Example: sphere file  - It is more easy to copy and paste this way.

"""

1.2333    0.5540    0.7792 0.152
-0.6952   -2.7148   -0.7502 0.152
0.7958   -2.1843    0.8685 0.152
1.7813    0.8105   -1.4821 0.152
-0.0857    0.6088    0.4403 0.17
-0.7927   -0.5515    0.1244 0.17
-0.7288    1.8464    0.4133 0.17
-2.1426   -0.4741   -0.2184 0.17
-2.0787    1.9238    0.0706 0.17
-2.7855    0.7636   -0.2453 0.17
-0.1409   -1.8536    0.1477 0.17
2.1094    0.6715   -0.3113 0.17
3.5305    0.5996    0.1635 0.17
-0.1851    2.7545    0.6593 0.12
-2.7247   -1.3605   -0.4564 0.12
-2.5797    2.8872    0.0506 0.12
-3.8374    0.8238   -0.5090 0.12
3.7290    1.4184    0.8593 0.12
4.2045    0.6969   -0.6924 0.12
3.7105   -0.3659    0.6426 0.12
-0.2555   -3.5916   -0.7337 0.12
"""

# Example: Link file
"""
1  5  1
1 12  1
2 11  1
2 21  1
3 11  2
4 12  2
5  6  1
5  7  2
6  8  2
6 11  1
7  9  1
7 14  1
8 10  1
8 15  1
9 10  2
9 16  1
10 17  1
12 13  1
13 18  1
13 19  1
13 20  1
"""

file = open(pfad, "r")  # open the file read
matrix1 = []
i = 1
X1 = 0.0
Y1 = 0.0
Z1 = 0.0
pe = 0.0

for ligne in file:
    coordinates = ligne.split()
    # print(coordinates)
    X1, Y1, Z1, pe = coordinates  # separate the coordinates
    # append the coordinates
    matrix1.append((float(X1), float(Y1), float(Z1), float(pe)))
    # print(X1," ",Y1," ",Z1,"",pe)
    pe = float(pe) * 2.0
    sphere = DOC.addObject("Part::Sphere", "Sphere")
    sphere.Label = "Kugel"
    sphere.Radius = pe
    sphere.Placement = Placement(
        Vector(float(X1), float(Y1), float(Z1)),
        Rotation(Vector(0.0, 0.0, 1.0), 0.0))


file.close()

# open the file read
file = open(pfad1, "r")
i = 1
A1 = 0.0
A2 = 0.0
No = 0.0
for ligne in file:
	coordinates = ligne.split()
	A1, A2, No = coordinates  # separate the coordinates
	A1 = int(A1) - 1
	A2 = int(A2) - 1

# Up to 5 Bonds possible
# This Macro will work until 3 Bonds
# The rest you must do by hand :D
	if float(No) < 2:
		X1 = matrix1[int(A1)][0]
		Y1 = matrix1[int(A1)][1]
		Z1 = matrix1[int(A1)][2]
		X2 = matrix1[int(A2)][0]
		Y2 = matrix1[int(A2)][1]
		Z2 = matrix1[int(A2)][2]
        # append the coordinates
		pt1 = Vector(float(X1), float(Y1), float(Z1))
		pt2 = Vector(float(X2), float(Y2), float(Z2))	
		c_length = pt1.distanceToPoint(pt2)
		c_axis = pt2.sub(pt1)
        # tube 0.3 diam
		t1 = Part.makeCylinder(0.15, c_length, pt1, c_axis)
		Part.show(t1, "tube_A")
	elif float(No) < 3:
        # print("2")
		X1 = matrix1[int(A1)][0] - matrix1[int(A1)][3]
		print(X1, matrix1[int(A1)][0], matrix1[int(A1)][3])
		Y1 = matrix1[int(A1)][1]
		Z1 = matrix1[int(A1)][2]
		X2 = matrix1[int(A2)][0] - matrix1[int(A2)][3]
		Y2 = matrix1[int(A2)][1]
		Z2 = matrix1[int(A2)][2]
		print(X1, Y1, Z1, X2, Y2, Z2)
		dx = X1 - X2
		dy = Y1 - Y2
		dz = Z1 - Z2
		x = (float(dx) * 2 + float(dy) * 1) / (float(dz) * -1)
		norm = math.sqrt((x * x) + 4 + 1)
		print(f"x: {x} >> {norm}")
		#Calculate Start and Endpoint of the shifted bond
		X1 = matrix1[int(A1)][0] - 2 / norm * ((matrix1[int(A1)][3] * 2) -0.1)  # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		Y1 = matrix1[int(A1)][1] - 1 / norm * ((matrix1[int(A1)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		Z1 = matrix1[int(A1)][2] - x / norm * ((matrix1[int(A1)][3] * 2) - 0.1)# (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		X2 = matrix1[int(A2)][0] - 2 / norm * ((matrix1[int(A2)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		Y2 = matrix1[int(A2)][1] - 1 / norm * ((matrix1[int(A2)][3] * 2) - 0.1)# (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		Z2 = matrix1[int(A2)][2] - x / norm * ((matrix1[int(A2)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)

        # append the coordinates
		pt1 = Vector(float(X1), float(Y1), float(Z1))
		pt2 = Vector(float(X2), float(Y2), float(Z2))
		c_length = pt1.distanceToPoint(pt2)
		c_axis = pt2.sub(pt1)
        # tube 0.2 diam
		t1 = Part.makeCylinder(0.1, c_length, pt1, c_axis)
		Part.show(t1, "tube_2")
		#Calculate Start and Endpoint of the shifted bond
		X1 = matrix1[int(A1)][0] + 2 / norm * ((matrix1[int(A1)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (((Value of Vector) * (Van der Waals Radius))-(bond diameter)) 
		Y1 = matrix1[int(A1)][1] + 1 / norm * ((matrix1[int(A1)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		Z1 = matrix1[int(A1)][2] + x / norm * ((matrix1[int(A1)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		X2 = matrix1[int(A2)][0] + 2 / norm * ((matrix1[int(A2)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		Y2 = matrix1[int(A2)][1] + 1 / norm * ((matrix1[int(A2)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		Z2 = matrix1[int(A2)][2] + x / norm * ((matrix1[int(A2)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		# append the coordinates
		pt1 = Vector(float(X1), float(Y1), float(Z1))
		pt2 = Vector(float(X2), float(Y2), float(Z2))
		c_length = pt1.distanceToPoint(pt2)
		c_axis = pt2.sub(pt1)
		# tube 0.2 diam
		t1 = Part.makeCylinder(0.1, c_length, pt1, c_axis)
		Part.show(t1, "tube_2")

		DOC.recompute()

	else:

#https://www.chemie.de/lexikon/Dreifachbindung.html
#Aus quantenchemischer Sicht kommen Bindungen durch Überlappung von Atomorbitalen zu einem Molekülorbital zustande.
#Die geläufigste Beschreibung der Dreifachbindung in Alkinen ist über eine Sigma-Bindung aus sp-Hybridorbitalen, die zwischen der Kernverbindungsachse liegt 
#und zwei Pi-Bindungen, die untereinander einen Winkel von 90° bilden
#und beide außerhalb der Kernverbindungsachse liegen. Eine alternative, vollkommen äquivalente Beschreibung benutzt drei gleichwertige "Bananen"-Bindungen,
#die durch Überlappung von sp3-Hybridorbitalen gebildet werden
#https://de.wikipedia.org/wiki/Drehmatrix

#The Rotation around ndach is the next step of implementation
        # print("A")
		X1 = matrix1[int(A1)][0]
		Y1 = matrix1[int(A1)][1]
		Z1 = matrix1[int(A1)][2]
		X2 = matrix1[int(A2)][0]
		Y2 = matrix1[int(A2)][1]
		Z2 = matrix1[int(A2)][2]
        # append the coordinates
		pt1 = Vector(float(X1), float(Y1), float(Z1))
		pt2 = Vector(float(X2), float(Y2), float(Z2))
		c_length = pt1.distanceToPoint(pt2)
		c_axis = pt2.sub(pt1)
        # tube 0.3 diam
		t1 = Part.makeCylinder(0.15, c_length, pt1, c_axis)
		Part.show(t1, "tube_A")
		X1 = matrix1[int(A1)][0] - matrix1[int(A1)][3]
		print(X1, matrix1[int(A1)][0], matrix1[int(A1)][3])
		Y1 = matrix1[int(A1)][1]
		Z1 = matrix1[int(A1)][2]
		X2 = matrix1[int(A2)][0] - matrix1[int(A2)][3]
		Y2 = matrix1[int(A2)][1]
		Z2 = matrix1[int(A2)][2]
		print(X1, Y1, Z1, X2, Y2, Z2)
		dx = X1 - X2
		dy = Y1 - Y2
		dz = Z1 - Z2
		x = (float(dx) * 2 + float(dy) * 1) / (float(dz) * -1)
		norm = math.sqrt((x * x) + 4 + 1)
		print(f"x: {x} >> {norm}")
		#Calculate Start and Endpoint of the shifted bond
		X1 = matrix1[int(A1)][0] - 2 / norm * ((matrix1[int(A1)][3] * 2) -0.1)  # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		Y1 = matrix1[int(A1)][1] - 1 / norm * ((matrix1[int(A1)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		Z1 = matrix1[int(A1)][2] - x / norm * ((matrix1[int(A1)][3] * 2) - 0.1)# (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		X2 = matrix1[int(A2)][0] - 2 / norm * ((matrix1[int(A2)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		Y2 = matrix1[int(A2)][1] - 1 / norm * ((matrix1[int(A2)][3] * 2) - 0.1)# (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		Z2 = matrix1[int(A2)][2] - x / norm * ((matrix1[int(A2)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)

        # append the coordinates
		pt1 = Vector(float(X1), float(Y1), float(Z1))
		pt2 = Vector(float(X2), float(Y2), float(Z2))
		c_length = pt1.distanceToPoint(pt2)
		c_axis = pt2.sub(pt1)
        # tube 0.2 diam
		t1 = Part.makeCylinder(0.1, c_length, pt1, c_axis)
		Part.show(t1, "tube_2")
		#Calculate Start and Endpoint of the shifted bond
		X1 = matrix1[int(A1)][0] + 2 / norm * ((matrix1[int(A1)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (((Value of Vector) * (Van der Waals Radius))-(bond diameter)) 
		Y1 = matrix1[int(A1)][1] + 1 / norm * ((matrix1[int(A1)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		Z1 = matrix1[int(A1)][2] + x / norm * ((matrix1[int(A1)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		X2 = matrix1[int(A2)][0] + 2 / norm * ((matrix1[int(A2)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		Y2 = matrix1[int(A2)][1] + 1 / norm * ((matrix1[int(A2)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		Z2 = matrix1[int(A2)][2] + x / norm * ((matrix1[int(A2)][3] * 2) - 0.1) # (Center Coordinate) - (guessed X-Vector)/ (Value of Vector) * (Van der Waals Radius)
		# append the coordinates
		pt1 = Vector(float(X1), float(Y1), float(Z1))
		pt2 = Vector(float(X2), float(Y2), float(Z2))
		c_length = pt1.distanceToPoint(pt2)
		c_axis = pt2.sub(pt1)
		# tube 0.2 diam
		t1 = Part.makeCylinder(0.1, c_length, pt1, c_axis)
		Part.show(t1, "tube_3")

file.close()

DOC.recompute()

