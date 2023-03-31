# This will be the source script of the SLR mapper
import arcpy
from arcpy import env
from arcpy.sa import *

env.workspace = r"C:\Users\wes\Documents\AAProffesional_paper"

#NOAA SLR Western Gulf Low is .49m/2050
#NOAA SLR Western Gulf intermediate is .59m/2050
#NOAA SLR Western Gulf high is .69m/2050
#Lui et al. Western Gulf is XX
# Detrended with no acceleration is 0.196

prjfile = r"C:\Users\wes\Documents\AAProffesional_paper\Python\NAD_1983_2011_UTM_Zone_15N.prj"

m = .59	# Inundation scenario setting, in meters
mID = "NOAA_Int.tif"
sd = (0.1**2 + 0.065**2)**0.5	# Std dev of inundation = (sd_dem^2 + sd_tidal^2)^0.5


prjfile = r"C:\Users\wes\Documents\AAProffesional_paper\Python\NAD_1983_2011_UTM_Zone_15N.prj"

# # # Unprojected DEM
# BayAreaDEM = r"C:\Users\wes\Documents\AAProffesional_paper\BayAreaDEM.tif"
# # # Projects to UTM 15m
# arcpy.ProjectRaster_management(BayAreaDEM, "BAproj.tif", prjfile, "BILINEAR", "2.85")

# Projected and CLipped DEM
BA_DEM = r"C:\Users\wes\Documents\AAProffesional_paper\BAproj.tif"
outputLocation = r"D:\AAProfessional_Paper\INTERMEDIATE\Altered"
# for the other flood scenarios replace str(m) with str(2*m) to fix the file extension problem

# # # Subtract DEM values from water surface to derive initial inundation depth grid
outCon = Con(Raster(BA_DEM) <= m, m - Raster(BA_DEM))
outCon.save(outputLocation + "\depth_" + mID)



# In preparation for evaluating connectivity, create single value DEM to show inundation extent
outCon2 = Con(Raster(BA_DEM) <= m, -99999)
outCon2.save(outputLocation + "\single_" + mID) # Save this one


# Evaluate connectivity of extent raster
outRgnGrp = RegionGroup(outCon2, "EIGHT", "WITHIN", "", "")
outRgnGrp.save(outputLocation + "\clumped_" + mID)

#low Count	267483256 267483000
#Int Count	281962805 281000000 
#High Count	294269525 29426900


# Extract connected inundation surface to be used as a mask for the original depth grid
attExtract = ExtractByAttributes(outRgnGrp, "COUNT > 267483000")
attExtract.save(outputLocation + "\connect_" + mID)


# Derive unconnected low-lying areas
attExtract2 = ExtractByAttributes(outRgnGrp, "COUNT < 267483000") * 0 + 999
attExtract2.save(outputLocation + "\lowlying_" + mID)



# Create depth grid for connected areas
outExtractByMask = ExtractByMask(outCon, attExtract)
outExtractByMask.save(outputLocation + "\con_depth_" + mID)

# # Create standard score (uncertainty) grid for entire elevation raster
# outSdScore = (m - Raster(BA_DEM)) / sd
# outSdScore.save(outputLocation + "\sd_score_" + mID)

# Mosaic unconnected (single value), connected (depth values), and present-day (2007) sea level (single_0) areas
arcpy.MosaicToNewRaster_management("lowlying_" + mID + ";" + "con_depth_" + mID + ";" + "single_0.tif", r"C:\Users\wes\Documents\AAProffesional_paper\Finals", "Mosaic_" + mID, prjfile, "32_BIT_FLOAT", "5", "1", "LAST", "FIRST")
  


# Mosaic standard score (uncertainty) and present-day (2007) sea level (single_0) areas
# arcpy.MosaicToNewRaster_management("sd_score_" + str(m) + ".tif" + ";" + "single_0", "C:\Users\wes\Documents\GEOG 665\Lab_6\Uncertainty", "sd_scr_msk_" + str(m) + ".tif", prjfile, "32_BIT_FLOAT", "5", "1", "LAST", "FIRST")
