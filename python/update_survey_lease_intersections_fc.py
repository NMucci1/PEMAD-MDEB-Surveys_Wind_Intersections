#################################################################
##     UPDATE HOSTED FEATURE SERVICE ON AGOL THAT DISPLAYS     ##
##   INTERSECTIONS OF OFFSHORE WIND LEASES WITH NEFSC SURVEYS  ##
#################################################################
   
# --- IMPORT LIBRARIES ---
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import geopandas as gpd
import pandas as pd
import numpy as np
from config import PORTAL_URL, USERNAME, PASSWORD, TARGET_SERVICE_ID, SURVEY_CONFIG, WIND_LEASES_URL, KEEP_COLUMNS

# Connect to ArcGIS Online
try:
    print("---  Connecting to ArcGIS Online...  ---")
    gis = GIS(url=PORTAL_URL, username=USERNAME, password=PASSWORD)
    print("---  Successfully connected  ---")
except Exception as e:
    print(f"Could not connect to ArcGIS Online. Error: {e}")

# Load Wind Leases (Exclude Easements)
print("Loading Wind Lease boundaries...")
wf_layer = FeatureLayer(WIND_LEASES_URL)
wf_sdf = wf_layer.query(where="LEASE_TYPE <> 'Easement'").sdf
wf_gdf = gpd.GeoDataFrame(wf_sdf, geometry=wf_sdf.spatial.name, crs=f"EPSG:{wf_sdf.spatial.sr['latestWkid']}")

all_results = []

# Loop through surveys in survey config dictionary
for key, info in SURVEY_CONFIG.items():
    try:
        print(f"--- Processing {info['name']} ---")
        s_layer = FeatureLayer(info['url'])
        s_sdf = s_layer.query().sdf
        
        if s_sdf is None or s_sdf.empty:
            print(f"Skipping {key}: No data found.")
            continue
        
        # Create GeoDataFrame
        s_gdf = gpd.GeoDataFrame(s_sdf, geometry=s_sdf.spatial.name, crs=f"EPSG:{s_sdf.spatial.sr['latestWkid']}")
        if s_gdf.crs != wf_gdf.crs:
            s_gdf = s_gdf.to_crs(wf_gdf.crs)

        # Determine geometry type safely
        # Use the first row to check if it's a Point or Polygon
        geom_type = s_gdf.geometry.iloc[0].geom_type.lower()

        if "point" in geom_type:
            print(f"Applying Spatial Join (Points -> Leases) for: {info['name']}")
            # SJOIN: Grab the Lease Polygons that contain the survey points
            # Keep 'wf_gdf' as the left side to preserve the Lease Geometry
            intersected_raw = gpd.sjoin(wf_gdf, s_gdf, how="inner", predicate="intersects")
            
            # Cast back to GeoDataFrame
            intersected = gpd.GeoDataFrame(intersected_raw, geometry='geometry', crs=wf_gdf.crs)
            
        else:
            print(f"Applying Intersection (Polygons -> Leases) for: {info['name']}")
            # OVERLAY: Cookie-cutter the survey to the lease shape
            intersected = gpd.overlay(s_gdf, wf_gdf, how='intersection')

        if not intersected.empty:
            # Apply the Standardized Name from config file
            # This overwrites any messy 'Name' columns from the original layers
            intersected['SURVEY_NAM'] = info['name']

            # Apply Marine Mammal naming logic (separate the aerial from shipboard survey)
            if info.get('use_type_logic') and 'TYPE' in intersected.columns:
                conditions = [
                    intersected['TYPE'].str.contains('Aerial', case=False, na=False),
                    intersected['TYPE'].str.contains('Shipboard', case=False, na=False)
                ]
                choices = ['Marine Mammal and Sea Turtle Survey - Aerial', 'Marine Mammal and Sea Turtle Survey - Shipboard']
                intersected['SURVEY_NAM'] = np.select(conditions, choices, default=info['name'])

            # Cleanup Columns
            # Ensure SURVEY_NAM is in the keep list
            current_keep = [c for c in KEEP_COLUMNS if c in intersected.columns]
            if 'SURVEY_NAM' not in current_keep:
                current_keep.append('SURVEY_NAM')
                
            intersected = intersected[current_keep]

            # DISSOLVE: One unique row per Lease/Survey Name pair
            dissolved = intersected.dissolve(by=['LEASE_NUMBER', 'SURVEY_NAM'], as_index=False)
            all_results.append(dissolved)

    except Exception as e:
        print(f"Error processing {key}: {e}")

# Combine results and upload to AGOL
if all_results:
    final_gdf = gpd.GeoDataFrame(pd.concat(all_results, ignore_index=True))
    final_gdf = final_gdf.to_crs(epsg=3857)
    
    print("Converting GeoPandas to SEDF...")
    final_sedf = pd.DataFrame.spatial.from_geodataframe(final_gdf, column_name='geometry')
    final_sedf.spatial.sr = {'wkid': 3857}
    
    print("Standardizing JSON geometry format...")
    fs = final_sedf.spatial.to_featureset()
    
    # Clean the features: ArcGIS REST API is picky about 'attributes' vs 'geometry'
    features_to_add = fs.features

    # Retrieve target AGOL feature service
    target_item = gis.content.get(TARGET_SERVICE_ID)
    target_layer = target_item.layers[0]
    
    print(f"Updating hosted feature service with {len(features_to_add)} records...")
    
    try:
        # Clear existing data
        target_layer.manager.truncate()
        
        # Upload in chunks (Standardizes the POST request)
        # Using a smaller chunk size (100) avoids the 'Invalid Parameters' 400 error on large JSON strings
        chunk_size = 100
        for i in range(0, len(features_to_add), chunk_size):
            chunk = features_to_add[i:i + chunk_size]
            result = target_layer.edit_features(adds=chunk)
            print(f"Uploaded chunk {i//chunk_size + 1}...")

        print("Success! Update complete.")

    except Exception as e:
        print(f"Failed at Upload step: {e}")