## A python demo script
## Author: Aldo Bergsma
## Date: Nov 2014

from osgeo import ogr
from osgeo import osr

# Create a point geometry
wkt = "POINT (173914.00 441864.00)"
pt = ogr.CreateGeometryFromWkt(wkt)

#Load the driver to create features in a shapefile
driver = ogr.GetDriverByName('ESRI Shapefile')
output = 'test.shp'

datasource = driver.CreateDataSource(output)

#Sefine the coordinate system used (28992 = RD)
proj = osr.SpatialReference()
proj.ImportFromEPSG(28992)

#Create a layer/features to work in
layer = datasource.CreateLayer('test', geom_type=ogr.wkbPolygon, srs = proj)
feature = ogr.Feature(layer.GetLayerDefn())

# Buffer the point in steps of 100m (start with the largest)
for bufferDistance in range (1100, 0, -100):
    poly = pt.Buffer(bufferDistance)
    # Wkt of the constructed buffer polygon
    polygon = ogr.CreateGeometryFromWkt(poly.ExportToWkt())
    feature.SetGeometry(polygon)
    # Add the features to the layer/shapefile
    layer.CreateFeature(feature)
    #Clean-up the added buffer polygon for next loop
    polygon.Destroy()

#Clean-up
feature.Destroy()
datasource.Destroy()
