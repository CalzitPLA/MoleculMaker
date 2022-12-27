from FreeCAD import Vector as V3
import Part, math
import FreeCADGui
import PySide
from PySide import QtCore, QtGui
from PySide.QtGui import QLineEdit, QRadioButton

periodic_table = {
"H" : ( 1, "120", (1.0, 1.0, 1.0) ),
"He" : ( 2, "140", (0.85, 1.0, 1.0) ),
"Li" : ( 3, "182", (0.8, 0.5, 1.0) ),
"Be" : ( 4, "153", (0.76, 1.0, 0.0) ),
"B" : ( 5, "192", (1.0, 0.71, 0.71) ),
"C" : ( 6, "170", (0.56, 0.56, 0.56) ),
"N" : ( 7, "155", (0.19, 0.31, 0.97) ),
"O" : ( 8, "152", (1.0, 0.05, 0.05) ),
"F" : ( 9, "147", (0.56, 0.88, 0.31) ),
"Ne" : ( 10, "154", (0.7, 0.89, 0.96) ),
"Na" : ( 11, "227", (0.67, 0.36, 0.95) ),
"Mg" : ( 12, "173", (0.54, 1.0, 0.0) ),
"Al" : ( 13, "184", (0.75, 0.65, 0.65) ),
"Si" : ( 14, "210", (0.94, 0.78, 0.63) ),
"P" : ( 15, "180", (1.0, 0.5, 0.0) ),
"S" : ( 16, "180", (1.0, 1.0, 0.19) ),
"Cl" : ( 17, "175", (0.12, 0.94, 0.12) ),
"Ar" : ( 18, "188", (0.5, 0.82, 0.89) ),
"K" : ( 19, "275", (0.56, 0.25, 0.83) ),
"Ca" : ( 20, "231", (0.24, 1.0, 0.0) ),
"Sc" : ( 21, "211", (0.9, 0.9, 0.9) ),
"Ti" : ( 22, "-", (0.75, 0.76, 0.78) ),
"V" : ( 23, "-", (0.65, 0.65, 0.67) ),
"Cr" : ( 24, "-", (0.54, 0.6, 0.78) ),
"Mn" : ( 25, "-", (0.61, 0.48, 0.78) ),
"Fe" : ( 26, "-", (0.88, 0.4, 0.2) ),
"Co" : ( 27, "-", (0.94, 0.56, 0.63) ),
"Ni" : ( 28, "163", (0.31, 0.82, 0.31) ),
"Cu" : ( 29, "140", (0.78, 0.5, 0.2) ),
"Zn" : ( 30, "139", (0.49, 0.5, 0.69) ),
"Ga" : ( 31, "187", (0.76, 0.56, 0.56) ),
"Ge" : ( 32, "211", (0.4, 0.56, 0.56) ),
"As" : ( 33, "185", (0.74, 0.5, 0.89) ),
"Se" : ( 34, "190", (1.0, 0.63, 0.0) ),
"Br" : ( 35, "185", (0.65, 0.16, 0.16) ),
"Kr" : ( 36, "202", (0.36, 0.72, 0.82) ),
"Rb" : ( 37, "303", (0.44, 0.18, 0.69) ),
"Sr" : ( 38, "249", (0.0, 1.0, 0.0) ),
"Y" : ( 39, "-", (0.58, 1.0, 1.0) ),
"Zr" : ( 40, "-", (0.58, 0.88, 0.88) ),
"Nb" : ( 41, "-", (0.45, 0.76, 0.79) ),
"Mo" : ( 42, "-", (0.33, 0.71, 0.71) ),
"Tc" : ( 43, "-", (0.23, 0.62, 0.62) ),
"Ru" : ( 44, "-", (0.14, 0.56, 0.56) ),
"Rh" : ( 45, "-", (0.04, 0.49, 0.55) ),
"Pd" : ( 46, "163", (0.0, 0.41, 0.52) ),
"Ag" : ( 47, "172", (0.75, 0.75, 0.75) ),
"Cd" : ( 48, "158", (1.0, 0.85, 0.56) ),
"In" : ( 49, "193", (0.65, 0.46, 0.45) ),
"Sn" : ( 50, "217", (0.4, 0.5, 0.5) ),
"Sb" : ( 51, "206", (0.62, 0.39, 0.71) ),
"Te" : ( 52, "206", (0.83, 0.48, 0.0) ),
"I" : ( 53, "198", (0.58, 0.0, 0.58) ),
"Xe" : ( 54, "216", (0.26, 0.62, 0.69) ),
"Cs" : ( 55, "343", (0.34, 0.09, 0.56) ),
"Ba" : ( 56, "268", (0.0, 0.79, 0.0) ),
"La" : ( 57, "-", (0.44, 0.83, 1.0) ),
"Ce" : ( 58, "-", (1.0, 1.0, 0.78) ),
"Pr" : ( 59, "-", (0.85, 1.0, 0.78) ),
"Nd" : ( 60, "-", (0.78, 1.0, 0.78) ),
"Pm" : ( 61, "-", (0.64, 1.0, 0.78) ),
"Sm" : ( 62, "-", (0.56, 1.0, 0.78) ),
"Eu" : ( 63, "-", (0.38, 1.0, 0.78) ),
"Gd" : ( 64, "-", (0.27, 1.0, 0.78) ),
"Tb" : ( 65, "-", (0.19, 1.0, 0.78) ),
"Dy" : ( 66, "-", (0.12, 1.0, 0.78) ),
"Ho" : ( 67, "-", (0.0, 1.0, 0.61) ),
"Er" : ( 68, "-", (0.0, 0.9, 0.46) ),
"Tm" : ( 69, "-", (0.0, 0.83, 0.32) ),
"Yb" : ( 70, "-", (0.0, 0.75, 0.22) ),
"Lu" : ( 71, "-", (0.0, 0.67, 0.14) ),
"Hf" : ( 72, "-", (0.3, 0.76, 1.0) ),
"Ta" : ( 73, "-", (0.3, 0.65, 1.0) ),
"W" : ( 74, "-", (0.13, 0.58, 0.84) ),
"Re" : ( 75, "-", (0.15, 0.49, 0.67) ),
"Os" : ( 76, "-", (0.15, 0.4, 0.59) ),
"Ir" : ( 77, "-", (0.09, 0.33, 0.53) ),
"Pt" : ( 78, "175", (0.82, 0.82, 0.88) ),
"Au" : ( 79, "166", (1.0, 0.82, 0.14) ),
"Hg" : ( 80, "155", (0.72, 0.72, 0.82) ),
"Tl" : ( 81, "196", (0.65, 0.33, 0.3) ),
"Pb" : ( 82, "202", (0.34, 0.35, 0.38) ),
"Bi" : ( 83, "207", (0.62, 0.31, 0.71) ),
"Po" : ( 84, "197", (0.67, 0.36, 0.0) ),
"At" : ( 85, "202", (0.46, 0.31, 0.27) ),
"Rn" : ( 86, "220", (0.26, 0.51, 0.59) ),
"Fr" : ( 87, "348", (0.26, 0.0, 0.4) ),
"Ra" : ( 88, "283", (0.0, 0.49, 0.0) ),
"Ac" : ( 89, "-", (0.44, 0.67, 0.98) ),
"Th" : ( 90, "-", (0.0, 0.73, 1.0) ),
"Pa" : ( 91, "-", (0.0, 0.63, 1.0) ),
"U" : ( 92, "186", (0.0, 0.56, 1.0) ),
"Np" : ( 93, "-", (0.0, 0.5, 1.0) ),
"Pu" : ( 94, "-", (0.0, 0.42, 1.0) ),
"Am" : ( 95, "-", (0.33, 0.36, 0.95) ),
"Cm" : ( 96, "-", (0.47, 0.36, 0.89) ),
"Bk" : ( 97, "-", (0.54, 0.31, 0.89) ),
"Cf" : ( 98, "-", (0.63, 0.21, 0.83) ),
"Es" : ( 99, "-", (0.7, 0.12, 0.83) ),
"Fm" : ( 100, "-", (0.7, 0.12, 0.73) ),
"Md" : ( 101, "-", (0.7, 0.05, 0.65) ),
"No" : ( 102, "-", (0.74, 0.05, 0.53) ),
"Lr" : ( 103, "-", (0.78, 0.0, 0.4) ),
"Rf" : ( 104, "-", (0.8, 0.0, 0.35) ),
"Db" : ( 105, "-", (0.82, 0.0, 0.31) ),
"Sg" : ( 106, "-", (0.85, 0.0, 0.27) ),
"Bh" : ( 107, "-", (0.88, 0.0, 0.22) ),
"Hs" : ( 108, "-", (0.9, 0.0, 0.18) ),
"Mt" : ( 109, "-", (0.92, 0.0, 0.15) ),
"Ds" : ( 110, "-", (0.0, 0.0, 0.0) ),
"Rg" : ( 111, "-", (0.0, 0.0, 0.0) ),
"Cn" : ( 112, "-", (0.0, 0.0, 0.0) ),
"Nh" : ( 113, "-", (0.0, 0.0, 0.0) ),
"Fl" : ( 114, "-", (0.0, 0.0, 0.0) ),
"Mc" : ( 115, "-", (0.0, 0.0, 0.0) ),
"Lv" : ( 116, "-", (0.0, 0.0, 0.0) ),
"Ts" : ( 117, "-", (0.0, 0.0, 0.0) ),
"Og" : ( 118, "-", (0.0, 0.0, 0.0) )
}


def curvedCylinder(radius, height, offset):
    circ = Part.makeCircle(radius)
    circtop = circ.copy()
    circtop.translate(V3(0, 0, height))
    sections = [Part.Wire(circ), Part.Wire(circtop)]
    pmid = V3(offset, 0, height/2)
    arc = Part.ArcOfCircle(zeroVec, pmid, V3(0, 0, height)) #Part.Arc deprecated
    spine = Part.Wire([arc.toShape()])
    curvedCyl = spine.makePipeShell(sections, True, True)
    return curvedCyl


def doubleBond(p1, p2, radius, offsetDist, planeNormal = V3(0, 0, 1)):
    #make a vertical cylinder at origin of length |p2 - p1|
    circ = Part.makeCircle(radius)
    cyl1 = Part.Face(Part.Wire(circ)).extrude(V3(0, 0, (p2 - p1).Length))
    cyl2 = cyl1.copy()
    pl = App.Placement()
    pl.Base = p1 
    pl.Rotation = App.Rotation(V3(0,0,1), p2 - p1)
    offsetVector = offsetDist*(planeNormal.cross(p2 - p1)).normalize()
    cyl1.Placement = pl
    cyl2.Placement = pl
    cyl1.Placement.Base += 0.5 * offsetVector
    cyl2.Placement.Base -= 0.5 * offsetVector
    dbond = cyl1.fuse(cyl2)
    return dbond

def tripleBond(p1, p2, radius, offsetDist, planeNormal = V3(0, 0, 1), planeQ = V3(0, 1, 0),):
    circ = Part.makeCircle(radius)
    cyl1 = Part.Face(Part.Wire(circ)).extrude(V3(0, 0, (p2 - p1).Length))
    cyl2 = cyl1.copy()
    cyl3 = cyl1.copy()
    pl = App.Placement()
    pl.Base = p1 
    pl.Rotation = App.Rotation(V3(0,0,1), p2 - p1)
    offsetVector = offsetDist*(planeNormal.cross(p2 - p1)).normalize()
    QVector = offsetDist*(planeQ.cross(p2 - p1)).normalize()
    cyl1.Placement = pl
    cyl2.Placement = pl
    cyl3.Placement = pl
    cyl2.Placement.Base += 0.5 * offsetVector
    cyl3.Placement.Base -= 0.5 * QVector
    tbond = cyl1.fuse([cyl2, cyl3])
    return tbond



def doubleBondCurved(p1, p2, radius, offsetDist, planeNormal = V3(0, 0, 1)):
    height = (p2 - p1).Length
    cc1 = curvedCylinder(radius, height, offsetDist/2)
    cc2 = curvedCylinder(radius, height, -offsetDist/2)
    pl = App.Placement()
    pl.Base = p1 
    pl.Rotation = App.Rotation(planeNormal.cross(p2-p1), zeroVec, p2 - p1, 'ZXY')
    cc1.Placement = pl
    cc2.Placement = pl
    return cc1.fuse(cc2)

def tripleBondCurved(p1, p2, radius, offsetDist, planeNormal = V3(0, 0, 1), planeQ = V3(0, 1, 0)):
    height = (p2 - p1).Length
    cc1 = curvedCylinder(radius, height, offsetDist/2)
    cc2 = curvedCylinder(radius, height, -offsetDist/2)
    cc3 = curvedCylinder(radius, height, -offsetDist/2)
    pl = App.Placement()
    pl.Base = p1
    QVector = offsetDist*(planeQ.cross(p2 - p1)).normalize() 
    pl.Rotation = App.Rotation(planeNormal.cross(p2-p1), zeroVec, p2 - p1, 'XYZ')
    cc1.Placement = pl
    cc2.Placement = pl
    planeNormal=planeQ
    pl.Rotation = App.Rotation(planeNormal.cross(p2-p1), zeroVec, p2 - p1, 'XYZ')
    pl.Base = p1    
    cc3.Placement = pl
    return cc1.fuse([cc2,cc3])

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

bondRadius = 0.05
useCurved = True
doc = App.ActiveDocument

global filename
global nameFile

try:
    filename, filefilter = QtGui.QFileDialog.getOpenFileName(QtGui.qApp.activeWindow(), 'Open a Pointcloud', '(*.dat *.sdf)')
except Exception:
    param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro")# macro path
    path = param.GetString("MacroPath","") + "/"                        # macro path
    filename, filefilter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Open a sdf-file", path, "(*.dat *.sdf)")

# path and name of links file
# path = "/home/nemo/Dokumente/Privat/Fredo/Conformer3D_CID_6658.sdf"

zeroVec = V3(0,0,0)
atomlocs=[] # list of locations 1-based
atomradii = [] # list of corresponding radii 1-based
atomcolor = []
#0 index is dummy data
atomlocs.append(zeroVec)
atomradii.append(0.0)
atomcolor.append((0.0, 0.0, 0.0)) # Float (R 0..1, G 0..1, B 0..1)
linkList = []

file = open(filename, "r")  # open the file read
i=1
for line in file:
    if i > 4:
      
#      print(len(line))
      #len(line) -25)
      if len(line) == 70:
       line=line[:-37]
       X1, Y1, Z1, pe = line.split()
       pei = periodic_table[pe][1]
       print(float(pei))
       atomradii.append(float(pei)/1000)
#       print(pe)
#       if pe is not str:
#        break
       atomlocs.append(V3(float(X1), float(Y1), float(Z1)))
       atomcolor.append(periodic_table[pe][2]) #(R 0..1, G 0..1, B 0..1)
      elif len(line) == 22:
       line=line[:-12]
       i1, i2, i3 = line.split()
       linkList.append((int(i1), int(i2), int(i3)))
#       print(i1)
#       if pe is not str:
#        break
#       atomlocs.append(V3(float(X1), float(Y1), float(Z1)))
#       print(pe)
#       print("a")
#       print(periodic_table[pe])

    i=i+1

file.close()
#print(atomlocs)
#print(linkList)

#added
i=1

atomCompound = doc.addObject("Part::Compound","Atoms")
atomlinks = []
for i, loc in enumerate(atomlocs):
    if i == 0:
        pass
    else:
        sph = doc.addObject("Part::Sphere","Sphere")
        sph.Label = "Atom_" + str(i)
        print(i)
#        print(atomradii[i])
#        print(periodic_table[atomradii[i]])
        sph.Radius= atomradii[i]
        sph.ViewObject.ShapeColor = atomcolor[i]
        pl = App.Placement()
        pl.Base = loc
        sph.Placement = pl
        atomlinks.append(sph)
        #junk = sph.adjustRelativeLinks(atomCompound) #suppress return value
        #junk = atomCompound.ViewObject.dropObject(sph, None,'',[])
    atomCompound.Links = atomlinks



bondCompound = doc.addObject("Part::Compound","Bonds")
bondlinks = []
for i, j, bondType in linkList:
    p1 = atomlocs[i]
    p2 = atomlocs[j]
    if bondType == 1:      
        bond = doc.addObject("Part::Cylinder", "Bond"+str(i)+ ' '+str(j))
        bond.Height = (p2 - p1).Length
        bond.Radius = bondRadius
        pl= App.Placement()
        pl.Base = p1 
        pl.Rotation = App.Rotation(V3(0,0,1), p2 - p1)
        bond.Placement = pl
        #junk = bond.adjustRelativeLinks(bondCompound)
        #junk = bondCompound.ViewObject.dropObject(bond, None,'',[])
        bondlinks.append(bond)
    elif bondType == 2:
        if useCurved:
            dbond = doubleBondCurved(p1, p2, bondRadius * 0.5, bondRadius * 2) # need more info to determine plane
        else:
            dbond = doubleBond(p1, p2, bondRadius * 0.5, bondRadius * 2)
        dbondobj = Part.show(dbond, 'DoubleBond' +str(i)+ ' '+str(j))
        #junk = dbondobj.adjustRelativeLinks(bondCompound)
        #junk = bondCompound.ViewObject.dropObject(dbondobj, None,'',[])
        bondlinks.append(dbondobj)
    elif bondType == 3:
        tbond = tripleBondCurved(p1, p2, bondRadius * 0.5, bondRadius * 3)
        tbondobj = Part.show(tbond, 'TripleBond' +str(i)+ ' '+str(j))
        #junk = tbondobj.adjustRelativeLinks(bondCompound)
        #junk = bondCompound.ViewObject.dropObject(tbondobj, None,'',[])
        bondlinks.append(tbondobj)
    bondCompound.Links = bondlinks


doc.recompute()

