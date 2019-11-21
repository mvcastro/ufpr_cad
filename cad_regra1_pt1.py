from osgeo import ogr
import os

# Get the input Layer
path = "C:/Temp/ufpr_cad_shapefiles/original/"
shapefile = "solos_AWC_hybras+ibge_s86+sr_VF.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource = driver.Open(path + shapefile, 1)

dataSource.CopyLayer(dataSource.GetLayer(), 'solos_com_cad')
dataSource.CopyLayer(dataSource.GetLayer(), 'solos_sem_cad')

layer_com_cad = dataSource.GetLayerByName('solos_com_cad')
layer_sem_cad = dataSource.GetLayerByName('solos_sem_cad')

print(layer_com_cad.GetFeatureCount())
print(layer_sem_cad.GetFeatureCount())

layer_com_cad.SetAttributeFilter("\"tipo_ordem\" = 'OUTROS'  OR \"AWC_%_coun\" <0")
for feat in layer_com_cad:
    layer_com_cad.DeleteFeature(feat.GetFID())


layer_sem_cad.SetAttributeFilter("\"tipo_ordem\" = 'OUTROS' OR \"AWC_%_coun\" >0")
for feat in layer_sem_cad:
    layer_sem_cad.DeleteFeature(feat.GetFID())

layer_com_cad = None
layer_sem_cad = None
dataSource = None