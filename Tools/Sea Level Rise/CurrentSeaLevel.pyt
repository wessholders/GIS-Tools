import arcpy
from arcpy import env
from arcpy.sa import*

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [CurrentLevel]


class CurrentLevel(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "CurrentSeaLevel"
        self.description = "This tool will output a raster surface of the current sea level."
        self.canRunInBackground = False
        self.category = "Current Sea Level"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Input DEM",
            name="in_DEM",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="Output Save Folder",
            name="Save_Path",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Output Raster Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # outputLocation = parameters[0]
        # input_raster = parameters[1]
     
        m = 0
        mID ="\current_level.tif"
        outCon = Con((parameters[0]) <= m, int(-99999))
        # outCon.save((parameters[0]) + mID)
        outCon.save(parameters[1].valueAsText + "\\" + parameters[2].valueAsText + ".tif")
        return
