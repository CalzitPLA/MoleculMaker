import FreeCAD as App
from FreeCAD import Vector as V3
import Part, math

# path and name of links file
atomfile = "/home/nemo/Dokumente/Privat/Fredo/aspirin.sphere.asc"
# path and name of links file
linkfile = "/home/nemo/Dokumente/Privat/Fredo/aspirin.verbindung.asc"

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


# Example: Link file

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



bondRadius = 0.05
useCurved = True
doc = App.ActiveDocument

zeroVec = V3(0,0,0)
atomlocs=[] # list of locations 1-based
atomradii = [] # list of corresponding radii 1-based
#0 index is dummy data
atomlocs.append(zeroVec)
atomradii.append(0.0)

file = open(atomfile, "r")  # open the file read
for line in file:
    X1, Y1, Z1, pe = line.split()
    atomlocs.append(V3(float(X1), float(Y1), float(Z1)))
    atomradii.append(float(pe))

file.close()


linkList = []
# open the file read
file = open(linkfile, "r")
for line in file:
    i1, i2, i3 = line.split()
    linkList.append((int(i1), int(i2), int(i3)))

file.close()

atomCompound = doc.addObject("Part::Compound","Atoms")
atomlinks = []
for i, loc in enumerate(atomlocs):
    if i == 0:
        pass
    else:
        sph = doc.addObject("Part::Sphere","Sphere")
        sph.Label = "Atom_" + str(i)
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


