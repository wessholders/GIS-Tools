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
        self.tools = [CurrentLevel, EvaluateConnectivity, SLR_Mapper, LowLying, TidallyConnected]


class CurrentLevel(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Current Sea Level"
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
        #Define the progressor Variables
        readTime = 3    # The tiem for user to read the progress section
        start = 0       # The beginning position of the progressor
        max = 100       #The final position of the progressor
        step = 50       #How much each section of source code moves the progressor

        #Set up the Progressor
        arcpy.SetProgressor("Default", "Initiating conditional statement...", start, max, step)
        time.sleep(readTime)    #Pause the execution or 3 seconds to read progress
        #Add Message to the Results Pane
        arcpy.AddMessage("Initiating conditional statement...")
        outCon = Con(Raster(parameters[0].valueAsText) <= 0, -99999)

          #Increment the Progressor
        arcpy.SetProgressor(start + step)   #Now 50% complete
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving...")
        outCon.save(parameters[1].valueAsText + "\\" + parameters[2].valueAsText)

          #Increment the Progressor
        arcpy.SetProgressor(start + step*2)   #Now 100% complete
        arcpy.SetProgressorLabel("Wrapping up...")
        time.sleep(readTime)
        arcpy.AddMessage("Wrapping up...")
        return
    
    #Connectivity Mapper
    
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
        m = int(parameters[1].value)
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
        m = int(parameters[1].value)
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

#Lowlying only    
class LowLying(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Low Lying"
        self.description = "This toll should be used to derive ~just~ low-lying areas."
        self.canRunInBackground = False
        self.category = "Low Lying"

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
        params = [param0, param1, param2, param3, param4]
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
        m = int(parameters[1].value)
        conn_value = parameters[2].value*.90

        #Define the progressor Variables
        readTime = 3    # The tiem for user to read the progress section
        start = 0       # The beginning position of the progressor
        max = 100       #The final position of the progressor
        step =20        #How much each section of source code moves the progressor

        #Set up the Progressor
        arcpy.SetProgressor("default", "Creating original depth grid...", start, max, step)
        time.sleep(readTime)    #Pause the execution or 3 seconds to read progress
        #Add Message to the Results Pane
        arcpy.AddMessage("Creating original depth grid...")
        #Create original depth grid
        outCon = Con(Raster(input_DEM) <= m, m - Raster(input_DEM))

        #Increment the Progressor
        arcpy.SetProgressor(start + step)   #Now 20% complete
        arcpy.SetProgressorLabel("Preparing to evaluate connectivity...")
        time.sleep(readTime)
        arcpy.AddMessage("Preparing to evaluate connectivity...")
        # In preparation for evaluating connectivity, create single value DEM to show inundation extent
        outCon2 = Con(Raster(input_DEM) <= m, -99999)

        #Increment the Progressor
        arcpy.SetProgressor(start + step*2)   #Now 40% complete
        arcpy.SetProgressorLabel("Evaluating connectivity...")
        time.sleep(readTime)
        arcpy.AddMessage("Evaluating connectivity...")
        # Evaluate connectivity of extent raster
        outRgnGrp = RegionGroup(outCon2, "EIGHT", "WITHIN", "", "")


        #Increment the Progressor
        arcpy.SetProgressor(start + step*3)   #Now 60% complete
        arcpy.SetProgressorLabel("Deriving unconnected low-lying areas...")
        time.sleep(readTime)
        arcpy.AddMessage("Deriving unconnected low-lying areas...")
        # Derive unconnected low-lying areas
        attExtract2 = ExtractByAttributes(outRgnGrp, "COUNT < " + str(conn_value)) * 0 + 999

        #Increment the Progressor
        arcpy.SetProgressor(start + step*4)   #Now 80% complete
        arcpy.SetProgressorLabel("Saving unconnected low-lying raster...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving unconnected low-lying raster...")
        attExtract2.save(parameters[3].valueAsText + "\\" + parameters[4].valueAsText)

        #Increment the Progressor
        arcpy.SetProgressor(start + step*5)   #Now 99% complete
        arcpy.SetProgressorLabel("Wrapping up...")
        time.sleep(readTime)
        arcpy.AddMessage("Wrapping up...")
        return

 #Tidally Connected   
class TidallyConnected(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tidally Connected"
        self.description = "This tool should be used to produce ~just~ tidally connected areas."
        self.canRunInBackground = False
        self.category = "Tidally Connected"

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
            displayName="Output Tidally Connected Raster Name",
            name="Output_CD_Name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2, param3, param4]
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
        m = int(parameters[1].value)
        conn_value = parameters[2].value*.90

        #Define the progressor Variables
        readTime = 3    # The tiem for user to read the progress section
        start = 0       # The beginning position of the progressor
        max = 100       #The final position of the progressor
        step =16        #How much each section of source code moves the progressor

        #Set up the Progressor
        arcpy.SetProgressor("default", "Creating original depth grid...", start, max, step)
        time.sleep(readTime)    #Pause the execution or 3 seconds to read progress
        #Add Message to the Results Pane
        arcpy.AddMessage("Creating original depth grid...")

        #Create original depth grid
        outCon = Con(Raster(input_DEM) <= m, m - Raster(input_DEM))

        #Increment the Progressor
        arcpy.SetProgressor(start + step)   #Now 16% complete
        arcpy.SetProgressorLabel("Preparing to evaluate connectivity...")
        time.sleep(readTime)
        arcpy.AddMessage("Preparing to evaluate connectivity...")



        # In preparation for evaluating connectivity, create single value DEM to show inundation extent
        outCon2 = Con(Raster(input_DEM) <= m, -99999)

        #Increment the Progressor
        arcpy.SetProgressor(start + step*2)   #Now 32% complete
        arcpy.SetProgressorLabel("Evaluating connectivity...")
        time.sleep(readTime)
        arcpy.AddMessage("Evaluating connectivity...")
        # Evaluate connectivity of extent raster
        outRgnGrp = RegionGroup(outCon2, "EIGHT", "WITHIN", "", "")

        #Increment the Progressor
        arcpy.SetProgressor(start + step*3)   #Now 48% complete
        arcpy.SetProgressorLabel("Preparing tidal surface mask...")
        time.sleep(readTime)
        arcpy.AddMessage("Preparing tidal surface mask...")
        # Extract connected inundation surface to be used as a mask for the original depth grid
        attExtract = ExtractByAttributes(outRgnGrp, "COUNT > " + str(conn_value))

        #Increment the Progressor
        arcpy.SetProgressor(start + step*4)   #Now 60% complete
        arcpy.SetProgressorLabel("Deriving tidally connected areas areas...")
        time.sleep(readTime)
        arcpy.AddMessage("Deriving tidally connected areas...")
        # Create depth grid for connected areas
        outExtractByMask = ExtractByMask(outCon, attExtract)

        #Increment the Progressor
        arcpy.SetProgressor(start + step*5)   #Now 72% complete
        arcpy.SetProgressorLabel("Saving tidally connected raster...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving tidally connected raster...")
        outExtractByMask.save(parameters[3].valueAsText + "\\" + parameters[4].valueAsText)

        #Increment the Progressor
        arcpy.SetProgressor(start + step*6)   #Now 88% complete
        arcpy.SetProgressorLabel("Wrapping up...")
        time.sleep(readTime)
        arcpy.AddMessage("Wrapping up...")
        return