##########################################
##       CONFIGURATION VARIABLES        ##
##########################################

import os

# Define .env variables to log into AGOL
PORTAL_URL = os.getenv("ARCGIS_URL")
USERNAME = os.getenv("ARCGIS_USERNAME")
PASSWORD = os.getenv("ARCGIS_PASSWORD")

# Target Hosted Layer URL
TARGET_SERVICE_ID = os.getenv("TARGET_ID")

# BOEM Wind Lease Outlines URL
WIND_LEASES_URL = "https://services7.arcgis.com/G5Ma95RzqJRPKsWL/ArcGIS/rest/services/Wind_Lease_Boundaries__BOEM_/FeatureServer/8"

# Columns to keep in the final output
KEEP_COLUMNS = ['LEASE_NUMBER_COMPANY', 'LEASE_NUMBER', 'PROJECT_NAME_1', 'PROJECT_STATUS', 'COP_STATUS', 'SURVEY_NAM', 'geometry']

# Survey URLs and names
SURVEY_CONFIG = {
    "bottom_trawl": {
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Bottom_Trawl_Survey/FeatureServer/0",
        "name": "Bottom Trawl Survey"
    },
    "scallop_historic": {
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Sea_Scallop_Survey/FeatureServer/1",
        "name": "Sea Scallop Survey - Historic"
    },
    "scallop":{
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Sea_Scallop_Survey/FeatureServer/0",
        "name": "Sea Scallop Survey"
    },
    "mmst": {
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Marine_Mammal_and_Sea_Turtle_Survey/FeatureServer/0",
        "name": "Marine Mammal and Sea Turtle Survey",
        "use_type_logic": True  # Flag to trigger specialized naming
    },
    "narw": {
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/North_Atlantic_Right_Whale_Aerial_Survey/FeatureServer/1",
        "name": "North Atlantic Right Whale Aeriel Survey"
    },
    "coastspan":{
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Cooperative_Atlantic_States_Shark_Pupping_and_Nursery_Survey/FeatureServer/0",
        "name": "Cooperative Atlantic States Shark Pupping and Nursery Survey"
    },
    "csbll":{
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Coastal_Shark_Bottom_Longline_Survey/FeatureServer/1",
        "name": "Coastal Shark Bottom Longline Survey"
    },
    "ecomon":{
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Ecosystem_Monitoring_Survey/FeatureServer/1",
        "name": "Ecosystem Monitoring Survey"
    },
    "edna":{
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/eDNA_Survey/FeatureServer/1",
        "name": "eDNA Survey"
    },
    "gombll":{
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Gulf_of_Maine_Bottom_Longline_Survey/FeatureServer/0",
        "name": "Gulf of Maine Bottom Longline Survey"
    },
    "hookandline":{
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Hook_and_Line_Survey/FeatureServer/0",
        "name": "Hook and Line Survey"
    },
    "sc":{
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Atlantic_Surfclam_and_Ocean_Quahog_Survey/FeatureServer/0",
        "name": "Atlantic Surfclam Survey"
    },
    "oq":{
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Atlantic_Surfclam_and_Ocean_Quahog_Survey/FeatureServer/1",
        "name": "Ocean Quahog Survey"
    },
    "seal":{
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Seal_Aerial_Survey/FeatureServer/0",
        "name": "Seal Aerial Survey"
    },
    "pam":{
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Passive_Acoustic_Monitoring_Survey/FeatureServer/0",
        "name": "Passive Acoustic Monitoring Survey"
    },
    "shrimp":{
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Northern_Shrimp_Survey/FeatureServer/0",
        "name": "Northern Shrimp Survey"
    },
    "turtle":{
        "url": "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Turtle_Ecology_Survey/FeatureServer/0",
        "name": "Turtle Ecology Survey"
    }
}