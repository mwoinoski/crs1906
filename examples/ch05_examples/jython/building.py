"""
building.py - Jython example from chapter 7
"""

from com.ltree import BuildingType


class Building(BuildingType):
    """Building object that subclasses a Java interface"""

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