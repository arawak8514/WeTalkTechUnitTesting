# #########################################################################
# Script Name: Locations.py
# Description:
#   gets a csv and geocdes this then adds to feature layer
# Parameters:
#   None
#
# Author: Dr Andrew Bell, Esri Ireland, 05/07/2023
# #########################################################################

import arcpy
from arcgis.gis import GIS
import sys
from copy import deepcopy
import json
import config as cConfig
import pandas as pd
from arcgis.geocoding import geocode

###Globalss###
sub_divider_line = '----------------------------------------------------------------------'

###Functions###
def Log(s_msg):
    arcpy.AddMessage(s_msg)

class ClassProcess:
    gis=None

    def __init__(self):
        ## Initializing variables that will be used conistently in below methods, connects to both portals
        try:
            Log(sub_divider_line)
            Log("Initializing process")
            Log("Connecting to portals")
            self.gis = GIS(portal,username=user, password=passw, verify_cert=True)
            Log("Connected to {0}".format(self.gis))
            Log("Initialization complete")
            Log(sub_divider_line)
        except Exception as ex:
            Log("Failed to initialize, Reason: {0}".format(ex))
            sys.exit(1)


    def createDataframe(self,_inputCsv):
        df = pd.read_csv(_inputCsv, header=0)
        Log(df)
        # Go into the main description
        arcpy.AddMessage(sub_divider_line)
        return df

    def searchLocationsFeatureLayer(self,_featureLayerID):
        try:
            featureItem = self.gis.content.get(_featureLayerID)
            featureLayer = featureItem.layers[0]
            Log(featureLayer)
        except Exception as ex:
            Log(ex)
            raise AssertionError("Feature layer not found")
        return featureLayer

    def run_locations(self, _df: pd.DataFrame):
        Log(sub_divider_line)
        Log("Running the Location process")

        #Get the dataframe into a list of locations
        locList = _df.values.tolist()
        print(locList)
        locationOutput = []

        try:
            for i in locList:
                print("Location to geocode:{0}".format(i[0]))
                location = geocode(i[0], out_sr=102100)
                if location.__len__() != 0:
                    locationOutput.append(location[0])
                else:
                    arcpy.AddMessage("No location found for: {0}".format(i[1]))
        except Exception as e:
            #arcpy.AddMessage("Error with the geocoding: {0}".format(e))
            raise ValueError("Error in the geocoding")

        #return the locations
        return locationOutput

    def constructLocationsObject(self,_df,_result):
        locationsObject = []
        for i in range(len(_df)):
            #build the object
            loc = {"attributes": {
                        "Address": _result[i]['address'],
                        "Country": _result[i]['attributes']['CntryName'],
                        "PremisesID": _df.loc[i, "PremisesID"],
                        "InService": _df.loc[i,"InService"]
                        },
                "geometry": {"x": _result[i]['location']['x'],
                             "y": _result[i]['location']['y']
                             }}
            locationsObject.append(loc)
        return locationsObject

    #TODO - Future development in Sprint 15 will update existing features
    def addLocations(self,_fSet,_fLayer):
        try:
            updatedFeature = _fLayer.edit_features(adds=_fSet, rollback_on_failure=True)
            return updatedFeature
        except Exception as x:
            Log(x)
            pass

# Run the above methods
def processLocations(_csv,_FeatureLayer):
    process = ClassProcess()

    arcpy.AddMessage("Processing the locationc for {0}".format(_csv))

    df = process.createDataframe(_csv)


    featureLayer = process.searchLocationsFeatureLayer(_FeatureLayer)

    #Geocode the dataframe
    result = process.run_locations(df)
    
    print("Printing the output result")
    print(result)

    featureSet = process.constructLocationsObject(df, result)
    print(featureSet)

    #Add to ArcGIS Online
    updateResult = process.addLocations(featureSet,featureLayer)
    Log(updateResult)

    arcpy.AddMessage("Script End")

#Run Class & Functions
if __name__ == '__main__':
    ##Getting the credentials
    con = cConfig.config()
    user = con.gisUsername
    passw = con.gisPassword
    portal = con.gisUrl
    csv = con.csv
    client = con.clientID
    secret = con.client_secret
    featureLayerID = con.fl

    arcpy.AddMessage("Got credentials now going into script.")

    #processTheLocations
    processLocations(csv,featureLayerID)
