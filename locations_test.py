# #########################################################################
# Script Name: locations_test.py
# Description:
#   Tests the definitions within locations.py
# Parameters:
#   None
#
# Author: Dr Andrew Bell, Esri Ireland, 05/07/2023
# #########################################################################

# #########################################################################
# IMPORTS
# #########################################################################
import unittest
import locations
import pandas as pd
import config as cConfig
from pandas import (
    DataFrame,
)

# #########################################################################
# GLOBALS
# #########################################################################
global sub_divider_line
sub_divider_line = "------------------------------------------------------"

# #########################################################################
# DEFINITIONS
# #########################################################################
class Test(unittest.TestCase):

    def test_importCSV(self):
        con = cConfig.config()
        csv = con.csv
        result = locations.ClassProcess.createDataframe(self,csv)
        self.assertIsNotNone(result) # Test if the result is empty or not
        print(sub_divider_line)

    def test_csvToDataframe(self):
        con = cConfig.config()
        csv = con.csv
        result = locations.ClassProcess.createDataframe(self,csv)
        self.assertIsInstance(result, DataFrame)# Test if the result is a dataframe

    def test_columnsCSV(self):
        con = cConfig.config()
        csv = con.csv
        columns = ['Location', 'LocationCode', 'InService']
        result = locations.ClassProcess.createDataframe(self, csv)
        print("Printing the return object columns\n{0}".format(list(result)))
        expectedResult = columns
        returnedResult = list(result)
        self.assertEqual(returnedResult,expectedResult)

    def test_locations_update_object(self):
        data = {'Location': ['Bundoran'],
                'LocationCode': ['JK8002'],
                'InService': ['Yes']}
        df = pd.DataFrame(data, columns=['Location', 'LocationCode', 'InService'])
        result = [{'address': 'Donegal', 'location': {'x': -880073.0734253102, 'y': 7346830.974925843}, 'score': 100, 'attributes': {'Loc_name': 'World', 'Status': 'T', 'Score': 100, 'Match_addr': 'Donegal', 'LongLabel': 'Donegal, IRL', 'ShortLabel': 'Donegal', 'Addr_type': 'Locality', 'Type': 'State or Province', 'PlaceName': 'Donegal', 'Place_addr': 'Donegal', 'Phone': '', 'URL': '', 'Rank': 11, 'AddBldg': '', 'AddNum': '', 'AddNumFrom': '', 'AddNumTo': '', 'AddRange': '', 'Side': '', 'StPreDir': '', 'StPreType': '', 'StName': '', 'StType': '', 'StDir': '', 'BldgType': '', 'BldgName': '', 'LevelType': '', 'LevelName': '', 'UnitType': '', 'UnitName': '', 'SubAddr': '', 'StAddr': '', 'Block': '', 'Sector': '', 'Nbrhd': '', 'District': '', 'City': '', 'MetroArea': '', 'Subregion': '', 'Region': 'Donegal', 'RegionAbbr': 'DL', 'Territory': '', 'Zone': '', 'Postal': '', 'PostalExt': '', 'Country': 'IRL', 'CntryName': 'Ireland', 'LangCode': 'ENG', 'Distance': 0, 'X': -7.90583093, 'Y': 54.922456258, 'DisplayX': -7.90583093, 'DisplayY': 54.922456258, 'Xmin': -8.62483093, 'Xmax': -7.18683093, 'Ymin': 54.203456258, 'Ymax': 55.641456258, 'ExInfo': ''}, 'extent': {'xmin': -960111.7873056738, 'ymin': 7208783.026391074, 'xmax': -800034.3595449462, 'ymax': 7487368.339847798}}]
        locationResult = locations.ClassProcess.constructLocationsObject(self,df,result)
        print(locationResult)
        expectedResult = [{'attributes': {'Address': 'Donegal', 'Country': 'Ireland', 'LocationCode': 'JK8002', 'InService': 'Yes'},
                            'geometry': {'x': -880073.0734253102, 'y': 7346830.974925843}}] 
        self.assertEqual(locationResult,expectedResult)


# #########################################################################
# MAIN ENTRY POINT
# #########################################################################
if __name__ == '__main__':
    unittest.main()