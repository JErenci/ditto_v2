import overpy
from shapely import geometry
import pandas as pd
import geopandas as gpd

def gen_pdf_osm(lat_min, lon_min, lat_max, lon_max, args,
                        l_keys_to_extract = [],
                        l_values_default = [],
                        d_key_replace = {},
                        d_parse_types = {},
                        l_drop_na = [],
                        is_gdf: bool = True) -> pd.DataFrame:
    
    api = overpy.Overpass()
    # fetch all  nodes
    result = api.query(f"""
        node[{args}]({lat_min},{lon_min},{lat_max},{lon_max});
        out meta;
        """)
    pdf = pd.DataFrame(result.nodes, columns=['nodes'])
    pdf['lat'] = pdf.nodes.apply(lambda x: x.lat)
    pdf['lon'] = pdf.nodes.apply(lambda x: x.lon)
    pdf['tags'] = pdf.nodes.apply(lambda x: x.tags)
    
    if l_keys_to_extract:
        for key,default_value in zip(l_keys_to_extract,l_values_default):
            pdf[key] = pdf.tags.apply(lambda x: x[key] if key in list(x.keys()) else default_value)

    if d_key_replace:
        for key,val in d_key_replace.items():
            for k2,v2 in val.items():
                pdf[key] = pdf[key].str.replace(k2,v2)

    if d_parse_types:
        for k,v in d_parse_types.items():
            pdf[k] = pdf[k].astype(v)

    if l_drop_na:
        pdf = pdf.dropna(subset=l_drop_na)

    if is_gdf:
        gdf = gpd.GeoDataFrame(pdf, 
                                geometry=[geometry.Point(xy) for xy in zip(pdf['lon'], pdf['lat'])],
                                crs=4326)
            
    return gdf