# Sea Level Rise Mapper

### This tool will take an input coastal Digital Elevation Model (DEM) and create projected inundation surfaces based upon specified sea level rise (SLR) scenarios.

<br>

#### What kind of DEM works best?
Tidally referenced Coastal DEM's of all coastal counties and territories in the United States have been produced by NOAA. They can be downloaded [here](https://coast.noaa.gov/slrdata/). To download you will want to select the state/territory, find the counties/region of interest (not all are 100% accurate), and click the DEM icon to initiate a download.
#### Why are the NOAA DEM's the best?
- They are extremely high resolution (<3m)
- The original water surface in the DEM extends out to sea.
- - This helps to capture beachfront impacts.
- They are already tidally referenced.
- - Any DEM can be tidally referenced using NOAA's [VDATUM](https://vdatum.noaa.gov/), however it can be quite a pain.
- All water crossings such as bridges and pipelines have been removed.
- - This has the benefit of connecting all bodies of water.
- - Without the removal of these water crossings, the script would view every water corssing as a dam.

#### There are six .pyt files included in this repo:
There is [Sea Level Rise.pyt]() which includes each and every step of the SLR mapping process, and there the five tools that go into the Sea Level Rise Mapper toolbox.

Five Tools:
- [CurrentSeaLevel.pyt]() creates a raster of modern day sea level, i.e., an SLR projection value of 0.
- [EvaluateConnectivity.pyt]() creates a raster used for determining a connectivity value, which is needed for differentiating between open bodies of water and land locked low-lying bodies of water.
- [SLRMapper.pyt]() takes a SLR Projection value and the connectivity value to create two inundation rasters:
- - A tidally connected inundation raster
- - A low-lying inundation raster
- [LowLying.pyt]() is the same process as SLRMapper.pyt, but only creates a low-lying inundation surface.
- [TidallyConnected.pyt]() is the same process as SLRMapper.pyt, but only creates a tidally connected inundation surface.
