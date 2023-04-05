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
        self.tools = [EvaluateConnectivity]
        
class EvaluateConnectivity(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Evaluate Connectivity"
        self.description = "This tool is used to find what bodies of water are tidally connected to open water."
        self.canRunInBackground = False
        self.category = "Evaluate Connectivity"

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
            displayName="Projected SLR Value",
            name="SLR_Scenario",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Output Save Folder",
            name="Save_Path",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Output Raster Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2, param3]
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
        m = float(parameters[1].value)
        #Define the progressor Variables
        readTime = 3    # The tiem for user to read the progress section
        start = 0       # The beginning position of the progressor
        max = 100       #The final position of the progressor
        step = 33       #How much each section of source code moves the progressor

        #Set up the Progressor
        arcpy.SetProgressor("Default", "Initiating conditional statement...", start, max, step)
        time.sleep(readTime)    #Pause the execution or 3 seconds to read progress
        #Add Message to the Results Pane
        arcpy.AddMessage("Initiating conditional statement...")
        outCon = Con(Raster(parameters[0].valueAsText) <= m, -99999)

        #Increment the Progressor
        arcpy.SetProgressor(start + step)   #Now 33% complete
        arcpy.SetProgressorLabel("Performing region group...")
        time.sleep(readTime)
        arcpy.AddMessage("Performing region group...")
        # Evaluate connectivity of extent raster
        outRgnGrp = RegionGroup(outCon, "EIGHT", "WITHIN", "", "")

        #Increment the Progressor
        arcpy.SetProgressor(start + step*2)   #Now 66% complete
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving...")
        outRgnGrp.save(parameters[2].valueAsText + "\\" + parameters[3].valueAsText)

         #Increment the Progressor
        arcpy.SetProgressor(start + step*3)   #Now 100% complete
        arcpy.SetProgressorLabel("Wrapping up...")
        time.sleep(readTime)
        arcpy.AddMessage("Wrapping up...")
        return

