# ---
# title: Create ESRI Shape file from CSV
# 
# Arvind Kumar Gupta 
#
#
#---------------------------------------------

import pandas as pd

from mpl_toolkits.basemap import Basemap
toronto_raw = pd.read_csv('.\\data\\ToronotoCrime.csv');

# Select relavent columns
data = toronto_raw[['premisetype', 'offence', 'occurrenceyear', 'occurrencemonth', 
                'occurrenceday', 'occurrencedayofweek', 'occurrencehour', 'MCI', 
                'Division', 'Hood_ID', 'Neighbourhood', 'Lat', 'Long']]

data.info()

# Change Column Name
data.columns = ['premType', 'offence', 'oyear', 'ocmonth', 
                'oday', 'odayweek', 'ohour', 'MCI', 
                'Division', 'Hood_ID', 'NbrHood', 'Lat', 'Long']

data.info()
#---------------------------------------------
#data.to_csv('output\ToronotoCrime1_noIndex.csv', index=0)
#data.to_csv('output\ToronotoCrime1.csv', index=0)
#---------------------------------------------
import osgeo
import osgeo.ogr, osgeo.osr
from osgeo import ogr 

# Create SHAPE file rom dataframe
def Create_ESRI_ShapeFile(mydata, EPSG_code='4326', export_shp='output.shp'): 
    #will create a spatial reference locally to tell the system what the reference will be
    spatialReference = osgeo.osr.SpatialReference() 
    
    #Define above reference to be the EPSG code
    spatialReference.ImportFromEPSG(int(EPSG_code))
    
    # Select the driver for shp-file creation.
    driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
    
    #store our data
    shapeData = driver.CreateDataSource(export_shp) 
    
    #create a corresponding layer for data with given spatial information.
    layer = shapeData.CreateLayer('layer', spatialReference, osgeo.ogr.wkbPoint) 
    
    # gets parameters of the current shapefile
    layer_defn = layer.GetLayerDefn()
    
    index = 0
     
    for field in mydata.columns:
        new_field = ogr.FieldDefn(field, ogr.OFTString) #we will create a new field with the content of our header
        #new_field.SetWidth(24)
        layer.CreateField(new_field)

    for row in mydata.iterrows():
        row = row[1]
        #print(row['Lat'], row['Long'])
        point = osgeo.ogr.Geometry(osgeo.ogr.wkbPoint)
        point.AddPoint(float(row['Long']), float(row['Lat'])) 
        #Here LATs and LONs as Strings, so convert them
        feature = osgeo.ogr.Feature(layer_defn)
        feature.SetGeometry(point) #set the coordinates
        feature.SetFID(index)
        for field in mydata.columns:
            i = feature.GetFieldIndex(field)
            feature.SetField(i, row[field])
        layer.CreateFeature(feature)
        index += 1
        if index%500 == 0:
            print(index)
    shapeData.Destroy() #lets close the shapefile
#------------------------------------------------------

mydata = data #.head(3)
EPSG_code='4326'
export_shp1='output\ToronotoCrime.shp'

Create_ESRI_ShapeFile(mydata, export_shp=export_shp1)

#---------------------------------------------


