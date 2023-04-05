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
        self.tools = [SLR_Mapper]
        
#SLR Mapper
class SLR_Mapper(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Sea Level Rise Mapper"
        self.description = "This tool will map projected sea level rise based on a given projection value and connectivity value."
        self.canRunInBackground = False
        self.category = "Sea Level Rise Mapper"

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
            displayName="Connectivity Value",
            name="Conn_value",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Output Save Folder",
            name="Save_Path",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param4 = arcpy.Parameter(
            displayName="Output Low Lying Raster Name",
            name="Output_LL_Name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param5 = arcpy.Parameter(
            displayName="Output Tidally Connected Raster Name",
            name="Output_CD_Name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2, param3, param4, param5]
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
        input_DEM = parameters[0].valueAsText
        m = float(parameters[1].value)
        conn_value = parameters[2].value*.90

        #Define the progressor Variables
        readTime = 3    # The tiem for user to read the progress section
        start = 0       # The beginning position of the progressor
        max = 100       #The final position of the progressor
        step =11        #How much each section of source code moves the progressor

        #Set up the Progressor
        arcpy.SetProgressor("default", "Creating original depth grid...", start, max, step)
        time.sleep(readTime)    #Pause the execution or 3 seconds to read progress
        #Add Message to the Results Pane
        arcpy.AddMessage("Creating original depth grid...")
        #Create original depth grid
        outCon = Con(Raster(input_DEM) <= m, m - Raster(input_DEM))

        #Increment the Progressor
        arcpy.SetProgressor(start + step)   #Now 12% complete
        arcpy.SetProgressorLabel("Preparing to evaluate connectivity...")
        time.sleep(readTime)
        arcpy.AddMessage("Preparing to evaluate connectivity...")
        # In preparation for evaluating connectivity, create single value DEM to show inundation extent
        outCon2 = Con(Raster(input_DEM) <= m, -99999)

        #Increment the Progressor
        arcpy.SetProgressor(start + step*2)   #Now 24% complete
        arcpy.SetProgressorLabel("Evaluating connectivity...")
        time.sleep(readTime)
        arcpy.AddMessage("Evaluating connectivity...")
        # Evaluate connectivity of extent raster
        outRgnGrp = RegionGroup(outCon2, "EIGHT", "WITHIN", "", "")

        #Increment the Progressor
        arcpy.SetProgressor(start + step*3)   #Now 36% complete
        arcpy.SetProgressorLabel("Preparing tidal surface mask...")
        time.sleep(readTime)
        arcpy.AddMessage("Preparing tidal surface mask...")
        # Extract connected inundation surface to be used as a mask for the original depth grid
        attExtract = ExtractByAttributes(outRgnGrp, "COUNT > " + str(conn_value))

        #Increment the Progressor
        arcpy.SetProgressor(start + step*4)   #Now 48% complete
        arcpy.SetProgressorLabel("Deriving unconnected low-lying areas...")
        time.sleep(readTime)
        arcpy.AddMessage("Deriving unconnected low-lying areas...")
        # Derive unconnected low-lying areas
        attExtract2 = ExtractByAttributes(outRgnGrp, "COUNT < " + str(conn_value)) * 0 + 999

        #Increment the Progressor
        arcpy.SetProgressor(start + step*5)   #Now 60% complete
        arcpy.SetProgressorLabel("Saving unconnected low-lying raster...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving unconnected low-lying raster...")
        attExtract2.save(parameters[3].valueAsText + "\\" + parameters[4].valueAsText)

        #Increment the Progressor
        arcpy.SetProgressor(start + step*6)   #Now 72% complete
        arcpy.SetProgressorLabel("Deriving tidally connected areas areas...")
        time.sleep(readTime)
        arcpy.AddMessage("Deriving tidally connected areas...")
        # Create depth grid for connected areas
        outExtractByMask = ExtractByMask(outCon, attExtract)

        #Increment the Progressor
        arcpy.SetProgressor(start + step*7)   #Now 84% complete
        arcpy.SetProgressorLabel("Saving tidally connected raster...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving tidally connected raster...")
        outExtractByMask.save(parameters[3].valueAsText + "\\" + parameters[5].valueAsText)

        #Increment the Progressor
        arcpy.SetProgressor(start + step*8)   #Now 96% complete
        arcpy.SetProgressorLabel("Wrapping up...")
        time.sleep(readTime)
        arcpy.AddMessage("Wrapping up...")
        return

