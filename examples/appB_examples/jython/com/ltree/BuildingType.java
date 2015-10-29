package com.ltree;

/**
 * Java interface that will be implemented/subclassed by the Jython Building
 * class.
 *
 * Note that the interface must define setters and getters for all attributes
 * of the Python class.
 */
public interface BuildingType {

    public String getBuildingName();
    public String getBuildingAddress();

    public int getBuildingId();
    public void setBuildingName(String name);

    public void setBuildingAddress(String address);
    public void setBuildingId(int id);
}