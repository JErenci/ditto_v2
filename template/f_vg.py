import pandas as pd
import geopandas as gpd

def load_gdf(
    path:str          = None,
    date_YYYYMMDD:int = 20221231,
    product:str       = 'VG250',
    tablename:str     = 'VG250',
    crs_orig:str      = 'EPSG:25832', ## Used by BKG
    crs_dest:str      = 4326,         ## WGS84
    adm:float         = 1.0,
    is_duplicates:bool=False,
    col_duplicates:str=None,
    is_geo:bool       = True
) -> gpd.geodataframe:

    if product[0:2] == 'VG':
        if adm == 1.0:
            suffix = 'STA'
        elif adm == 2.0:
            suffix = 'LAN'
        elif adm == 3.0:
            suffix = 'RBZ'
        elif adm == 4.0:
            suffix = 'KRS'
        elif adm == 4.5:
            suffix = 'VWG'
        elif adm == 5.0:
            suffix = 'GEM'
        else:
            print(f'Error! Invalid suffix [{suffix}]')
            return None
    else:
        print(f'Error! Invalid product [{product}]')
        return None
    
    
    if is_geo:
        extension = 'shp'
    else:
        extension = 'dbf'
        
    filepath = f'{path}/{product}/{date_YYYYMMDD}/{tablename}_{suffix}.{extension}'
    print(f'Reading path [{filepath}]')
    gdf = gpd.read_file(filepath)

    # Remove duplicates
    if (is_duplicates):
        gdf = gdf[gdf[col_duplicates] != 0]
    
    # Shape and head
    print(f'shape={gdf.shape}')

    # Converting to WGS-84
    if 'geometry' in gdf.columns.values:
        gdf.crs = crs_orig
        print(f'Converting to WGS-84 [EPSG:4326]')
        gdf = gdf.to_crs(epsg=crs_dest)
        
    return gdf

def pimp_gdf(gdf, l_datetimes = ['BEGINN','WSK'], col_ewz = 'EWZ', col_fla = 'KFL'):
    for col in l_datetimes:
        gdf[col] = gdf[col].astype(str)
    gdf['BVD'] = gdf[col_ewz]/gdf[col_fla]
    gdf['BVD'] =gdf['BVD'].round(decimals=2)
    return gdf

# def check_sanity_gdf_geometry(gdf):
#     size1 = gdf.geometry.isna().count()
#     size2 = gdf.shape[0]

#     if (size1==size2):
#         print(f'  PASS --> Sanity check1 , size1={size1}, size2={size2}, [NaNs] --> [0]')
#     else:
#         print(f'  FAIL --> Sanity check1 , size1={size1}, size2={size2}, [NaNs] --> [0]')
#         raise Exception('NaNs in gdf')

#     try:
#         gj = folium.GeoJson(gdf)
#         print(f'  PASS --> Sanity check2 --> [GeoJson could be generated!]')
#     except:
        
#         print(f'  FAIL --> Sanity check2 --> [GeoJson could be generated!]')
#         raise Exception('Sanity check2 --> GeoJson can NOT be generated!')