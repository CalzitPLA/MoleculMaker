from FreeCAD import Vector as V3
import Part, math
import FreeCADGui
import PySide
from PySide import QtCore, QtGui
from PySide.QtGui import QLineEdit, QRadioButton

periodic_table = {
"H":"120",
"He":"140",
"Li":"182",
"Be":"153",
"B":"192",
"C":"170",
"N":"155",
"O":"152",
"F":"147",
"Ne":"154",
"Na":"227",
"Mg":"173",
"Al":"184",
"Si":"210",
"P":"180",
"S":"180",
"Cl":"175",
"Ar":"188",
"K":"275",
"Ca":"231",
"Sc":"211",
"Ti":"-",
"V":"-",
"Cr":"-",
"Mn":"-",
"Fe":"-",
"Co":"-",
"Ni":"163",
"Cu":"140",
"Zn":"139",
"Ga":"187",
"Ge":"211",
"As":"185",
"Se":"190",
"Br":"185",
"Kr":"202",
"Rb":"303",
"Sr":"249",
"Y":"-",
"Zr":"-",
"Nb":"-",
"Mo":"-",
"Tc":"-",
"Ru":"-",
"Rh":"-",
"Pd":"163",
"Ag":"172",
"Cd":"158",
"In":"193",
"Sn":"217",
"Sb":"206",
"Te":"206",
"I":"198",
"Xe":"216",
"Cs":"343",
"Ba":"268",
"La":"-",
"Ce":"-",
"Pr":"-",
"Nd":"-",
"Pm":"-",
"Sm":"-",
"Eu":"-",
"Gd":"-",
"Tb":"-",
"Dy":"-",
"Ho":"-",
"Er":"-",
"Tm":"-",
"Yb":"-",
"Lu":"-",
"Hf":"-",
"Ta":"-",
"W":"-",
"Re":"-",
"Os":"-",
"Ir":"-",
"Pt":"175",
"Au":"166",
"Hg":"155",
"Tl":"196",
"Pb":"202",
"Bi":"207",
"Po":"197",
"At":"202",
"Rn":"220",
"Fr":"348",
"Ra":"283",
"Ac":"-",
"Th":"-",
"Pa":"-",
"U":"186",
"Np":"-",
"Pu":"-",
"Am":"-",
"Cm":"-",
"Bk":"-",
"Cf":"-",
"Es":"-",
"Fm":"-",
"Md":"-",
"No":"-",
"Lr":"-",
"Rf":"-",
"Db":"-",
"Sg":"-",
"Bh":"-",
"Hs":"-",
"Mt":"-",
"Ds":"-",
"Rg":"-",
"Cn":"-",
"Nh":"-",
"Fl":"-",
"Mc":"-",
"Lv":"-",
"Ts":"-",
"Og":"-"
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
    filename, filefilter = QtGui.QFileDialog.getOpenFileName(QtGui.qApp.activeWindow(), 'Open a Pointcloud', '*.dat')
except Exception:
    param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro")# macro path
    path = param.GetString("MacroPath","") + "/"                        # macro path
    filename, filefilter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Open a sdf-file", path, "*.dat")

# path and name of links file
# path = "/home/nemo/Dokumente/Privat/Fredo/Conformer3D_CID_6658.sdf"

zeroVec = V3(0,0,0)
atomlocs=[] # list of locations 1-based
atomradii = [] # list of corresponding radii 1-based
#0 index is dummy data
atomlocs.append(zeroVec)
atomradii.append(0.0)
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
       pei = periodic_table[pe]
       print(float(pei))
       atomradii.append(float(pei)/1000)
#       print(pe)
#       if pe is not str:
#        break
       atomlocs.append(V3(float(X1), float(Y1), float(Z1)))
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

