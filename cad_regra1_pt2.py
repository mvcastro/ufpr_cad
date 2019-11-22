from osgeo import ogr, gdalconst
import rtree
import os
import csv

# Get the input Layer
path = "C:/Temp/ufpr_cad_shapefiles/original/"
shapefile1 = "solos_com_cad.shp"
shapefile2 = "solos_sem_cad.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")

dataSource1 = driver.Open(path + shapefile1, gdalconst.GA_ReadOnly)
dataSource2 = driver.Open(path + shapefile2, gdalconst.GA_ReadOnly)

layer_com_cad = dataSource1.GetLayerByName('solos_com_cad')
layer_sem_cad = dataSource2.GetLayerByName('solos_sem_cad')

num_dados_com_cad = layer_com_cad.GetFeatureCount()
num_dados_sem_cad = layer_sem_cad.GetFeatureCount()

print(num_dados_com_cad)
print(num_dados_sem_cad)

lista_resultados = []


# Criando índice espacial com rtree
index = rtree.index.Index(interleaved=False)
for fid1 in range(0, num_dados_com_cad):
    feature1 = layer_com_cad.GetFeature(fid1)
    geometry1 = feature1.GetGeometryRef()
    xmin, xmax, ymin, ymax = geometry1.GetEnvelope()
    index.insert(fid1, (xmin, xmax, ymin, ymax))



for i in range(0, num_dados_sem_cad):
    # Get the input Feature
    feat_sem_cad = layer_sem_cad.GetFeature(i)
    geom_sem_cad = feat_sem_cad.GetGeometryRef()
    xmin, xmax, ymin, ymax = geom_sem_cad.GetEnvelope()

    for i in list(index.intersection((xmin, xmax, ymin, ymax))):
        feat_com_cad = layer_com_cad.GetFeature(i)
        geom_com_cad = feat_com_cad.GetGeometryRef()
        isFound = False
        if geom_com_cad.Intersects(geom_sem_cad):

            if feat_sem_cad.GetField('ordem') == feat_com_cad.GetField('ordem') and feat_sem_cad.GetField('subordem') == feat_com_cad.GetField('subordem'):
                tuple_result = (int(feat_sem_cad.GetField('id')), \
                                int(feat_com_cad.GetField('id')), \
                                float(feat_com_cad.GetField("AWC_%_coun")), \
                                float(feat_com_cad.GetField("AWC_%_min")), \
                                float(feat_com_cad.GetField("AWC_%_max")), \
                                float(feat_com_cad.GetField("AWC_%_mean")), \
                                float(feat_com_cad.GetField("AWC_%_medi")), \
                                float(feat_com_cad.GetField("AWC_%_stdd")))

                print(tuple_result)
                lista_resultados.append(tuple_result)
                isFound = True
            
            if feat_sem_cad.GetField('ordem') == feat_com_cad.GetField('ordem') and not isFound:
                tuple_result = (int(feat_sem_cad.GetField('id')), \
                                int(feat_com_cad.GetField('id')), \
                                float(feat_com_cad.GetField("AWC_%_coun")), \
                                float(feat_com_cad.GetField("AWC_%_min")), \
                                float(feat_com_cad.GetField("AWC_%_max")), \
                                float(feat_com_cad.GetField("AWC_%_mean")), \
                                float(feat_com_cad.GetField("AWC_%_medi")), \
                                float(feat_com_cad.GetField("AWC_%_stdd")))
                print(tuple_result)
                lista_resultados.append(tuple_result)

# close DataSources
dataSource1.Destroy()
dataSource2.Destroy()

# Armazenando os resultados no shape original          
shapefile = "solos_AWC_hybras+ibge_s86+sr_VF.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource = driver.Open(path + shapefile, 1)

layer = dataSource.GetLayer('solos_AWC_hybras+ibge_s86+sr_VF')

lista_id = [int(i[0]) for i in lista_resultados]

for feat in layer:
#for i in range(0, layer.GetFeatureCount()):
    #feat = layer.GetFeature(i)
    feat_id = int(feat.GetField('id'))
    if feat_id in lista_id:
        for dados in lista_resultados:
            if dados[0] == feat_id:
                print(dados)
                feat.SetField("AWC_%_coun", dados[2]),\
                feat.SetField("AWC_%_min",  dados[3]),\
                feat.SetField("AWC_%_max",  dados[4]),\
                feat.SetField("AWC_%_mean", dados[5]),\
                feat.SetField("AWC_%_medi", dados[6]),\
                feat.SetField("AWC_%_stdd", dados[7])
                layer.SetFeature(feat)
                

dataSource.Destroy()