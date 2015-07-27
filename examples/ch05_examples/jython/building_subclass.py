"""
building_subclass.py - Jython example from chapter 7

If you want a Java application to use a Python class that doesn't follow
Jython's rules, define a subclass that extends the original class and
implements a Java interface.

To test this:
1. Add a method to the interface BuildingType.java:
   void schedule_maintenance();
2. Add a method in Main.java:
   building.schedule_maintenance();
"""

from com.ltree import BuildingType

class RealBuilding:
    """Python class that doesn't follow Jython rules"""
    def __init__(self, name, address, id):
        self.name = name
        self.address = address
        self.id = id

    def schedule_maintenance(self):
        print "subclass: scheduling maintenance for " + str(self)

    def __str__(self):
        return "Building %d, %s %s" % (self.id, self.name, self.address)


class Building(RealBuilding, BuildingType):
    """Building object that extends a Python class and
       implements a Java interface"""

    def __init__(self):
        """Constructor can't take parameters. All values must be set by calling
           setter methods"""
        self.name = None
        self.address = None
        self.id = -1

    def getBuildingName(self):
        return self.name

    def setBuildingName(self, name):
        self.name = name

    def getBuildingAddress(self):
        return self.address

    def setBuildingAddress(self, address):
        self.address = address

    def getBuildingId(self):
        return self.id

    def setBuildingId(self, id):
        self.id = id
