package com.ltree;

import org.plyjy.factory.JythonObjectFactory;

public class Main {

    public static void main(String[] args) {

        try {

            // Obtain an instance of the object factory
            JythonObjectFactory factory = JythonObjectFactory.getInstance();

            // Call the createObject() method on the object factory by
            // passing the Java interface and the name of the Jython module
            // in String format. The returning object is casted to the the same
            // type as the Java interface and stored into a variable.
            BuildingType building = (BuildingType) factory.createObject(
                BuildingType.class, "Building");

            // Populate the object with values using the setter methods
            building.setBuildingName("BUILDING-A");
            building.setBuildingAddress("100 MAIN ST.");
            building.setBuildingId(1);

            System.out.println("Jython object from a Java application:");
            System.out.println(building.getBuildingId() + " " + building.getBuildingName() + " " +
                building.getBuildingAddress());
        }
        catch(Exception e) {
            e.printStackTrace();
        }

    }

}