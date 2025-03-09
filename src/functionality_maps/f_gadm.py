
import sys

sys.path.append('/Users/User/PycharmProjects/ditto_v2/')
# from functionality_maps.paths import d_stores_logo

# import f_maps
import os, requests
import folium, folium.plugins
import pandas as pd

d_stores_logo = {
    'sportscheck' : 'assets/SportScheck/1_Home/logo.png',
    'decathlon'   : 'assets/Decathlon/1_Home/Decathlon_Logo.jpg',
    'intersport'  : 'assets/Intersport/1_Home/logo.jpg'
}

def download_gpkg_country(country_ISO_3):
    url=f'https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/gadm41_{country_ISO_3}.gpkg'
    local_filename = f'assets/Geo/GADM/gadm41_{country_ISO_3}.gpkg'

    if os.path.exists(local_filename):
        print(f"File exists locally! [{local_filename}]")
    else:
        # Send a GET request to the URL
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Check if the request was successful

            # Open a local file with write-binary mode
            with open(local_filename, 'wb') as file:
                # Write the content to the local file in chunks
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"File downloaded! [{local_filename}]")
    return local_filename


import geopandas as gpd

def extract_gdf_gpkg(path:str, l_levels:list = [1,2,3,4], is_logging:bool=False) :
    l_gdf = []
    l_name_adm = []
    l_tooltip = []
    
    name_adm = 'COUNTRY'

    for level in l_levels:
        current_adm = int(level[-1])
        if is_logging:
            print(f' level={level}')
        
        print(f'path={path}')
        gdf_adm = gpd.read_file(path, layer=f'{level}')
        if is_logging:
            print(f'  Adding level={level} [{gdf_adm.shape[0]}]')
        l_gdf.append(gdf_adm)

        print(f'ADM={current_adm}')
        if (current_adm == 0):
            tooltip=folium.features.GeoJsonTooltip(fields=[name_adm])
        elif (current_adm in [1,2,3,4] ):
            print('yes')
            name_adm = extract_values(gdf_adm[f'TYPE_{current_adm}'].drop_duplicates().values)

            l_int = list(range(1, current_adm + 1))            
            l_columns = ['COUNTRY','GID_0'] + [f'NAME_{i}' for i in l_int] + [f'TYPE_{current_adm}']
            print(f'l_columns={l_columns}')
            tooltip=folium.features.GeoJsonTooltip(fields=l_columns)
        else:
            print('No')
        
        l_name_adm.append(name_adm)
        l_tooltip.append(tooltip)

    return [l_gdf, 
            l_name_adm, 
            l_tooltip,
           ]


def extract_values(col_values):
    name_adm = list(col_values)
    name_adm = [x for x in name_adm if x != 'NA']
    return name_adm


highlight_function = lambda x: {
    'fillColor': 'red',
    # 'color': 'black',
    # 'lineColor': 'red',
    'fillOpacity': 0.40,
    # 'weight': 0.1
}


def gen_map_gadm(
    l_adm, 
    l_gdf, 
    l_name_adm,
    l_tooltip, 
    is_logging:bool=False
) -> folium.Map():
    
    fm = folium.Map()
    
    
    for adm, gdf_adm, name_adm, tooltip_adm in zip(l_adm, l_gdf, l_name_adm, l_tooltip):
    # for adm, gdf_adm, tooltip_adm in zip(l_adm, l_gdf, l_tooltip):
    
        current_adm = int(adm[-1])
        if is_logging:
            print(f'Adding ADM={current_adm} [{gdf_adm.shape[0]}  {name_adm}]')
            # print(f'Adding ADM={adm} [{gdf_adm.shape[0]}]')
            
        gj = folium.GeoJson(
            gdf_adm,
            highlight_function=highlight_function,
            tooltip=tooltip_adm
        )            
        fg = folium.FeatureGroup(name=f'ADM={current_adm} [{gdf_adm.shape[0]} {name_adm}]')
        # fg = folium.FeatureGroup(name=f'ADM={adm} [{gdf_adm.shape[0]}]')
        fg.add_child(gj)
        fg.add_to(fm)
        
    folium.LayerControl(position='topright',
                        collapsed=False).add_to(fm)
    print('Adding layers')
    fullscreen = folium.plugins.Fullscreen(position='topleft',
                                           title='Expand me',
                                           title_cancel='Exit me',
                                           force_separate_button=True)
    fm.add_child(fullscreen)
    print('Full screen')
    
    fm.fit_bounds(fm.get_bounds())
    print('Fitting')
    
    
    return fm

from shapely.geometry import Polygon
from pyproj import Proj, Transformer


def get_store_markers(pdf:pd.DataFrame, l_popup_rows:list,
                      name:str, is_shown:bool=False) -> folium.FeatureGroup:
    fg = folium.FeatureGroup(name=name, 
                            show=is_shown)
    # Add markers to the map for each point in the DataFrame
    for idx, row in pdf.iterrows():
        if l_popup_rows:
            # Generate HTML content for the popup
            html_content = ''
            for item in l_popup_rows:
                html_row = f'<b>{item}:</b>{row[item]}<br>'
                html_content += html_row
            popup = folium.Popup(html_content, max_width=250)
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=popup,
                icon=folium.features.CustomIcon(icon_image=d_stores_logo[store],
                                                                icon_size=(50, 15)
                                                                ),
                tooltip=row['name']
            ).add_to(fg)
        else:
            
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=f'url=<a href={row['url']}>{row['url']}</a>',
                icon=folium.features.CustomIcon(icon_image=d_stores_logo[store],
                                                                icon_size=(50, 15)
                                                                ),
                tooltip=row['name']
            ).add_to(fg)
    return fg


def get_fg_store(pdf:pd.DataFrame, l_stores:list, 
                 l_popup_rows:list=[], 
                 is_shown:bool=False, is_logging:bool=False) -> list:
    l_fg = []
    for i,store in enumerate(l_stores):
        pdf_store = pdf[pdf['store'] == store]
        pdf_store = pdf_store.dropna(subset=['lat', 'lon'])
        if is_logging:
            print(f'[{i+1}/{len(l_stores)}] Store={store}')
            print(f'{pdf_store.shape}')
            print(pdf_store[['name','lon','lat']])


        fg = folium.FeatureGroup(name=f'[{len(pdf_store)}] STORES/{store}', 
                                 show=is_shown)
        if is_logging:
            print(f'logo path= {d_stores_logo[store]}')

        # Add markers to the map for each point in the DataFrame
        for idx, row in pdf_store.iterrows():
            if l_popup_rows:
                # Generate HTML content for the popup
                html_content = ''
                for item in l_popup_rows:
                    html_row = f'<b>{item}:</b>{row[item]}<br>'
                    html_content += html_row
                popup = folium.Popup(html_content, max_width=250)
                folium.Marker(
                    location=[row['lat'], row['lon']],
                    popup=popup,
                    icon=folium.features.CustomIcon(icon_image=d_stores_logo[store],
                                                                    icon_size=(50, 15)
                                                                    ),
                    tooltip=row['name']
                ).add_to(fg)
            else:
                
                folium.Marker(
                    location=[row['lat'], row['lon']],
                    popup=f'url=<a href={row['url']}>{row['url']}</a>',
                    icon=folium.features.CustomIcon(icon_image=d_stores_logo[store],
                                                                    icon_size=(50, 15)
                                                                    ),
                    tooltip=row['name']
                ).add_to(fg)


            loca = row['location']
            # print(f'loca={loca}')

            location_bbox = loca['raw']['boundingbox']
            points_rect = [[location_bbox[0],location_bbox[2]],[location_bbox[1],location_bbox[3]]]
            if is_logging:
                print(f'location_bbox={location_bbox}')
                print(f'points_rect={points_rect}')

            points_area = [
                    (location_bbox[0], location_bbox[2]),  # (min_lat, min_lon)
                    (location_bbox[1], location_bbox[2]),  # (max_lat, min_lon)
                    (location_bbox[1], location_bbox[3]),  # (max_lat, max_lon)
                    (location_bbox[0], location_bbox[3])   # (min_lat, max_lon)
                ]
            if is_logging:
                print(f'points_area={points_area}')
            polygon = Polygon(points_area)

            # Define the projection (WGS84 to UTM)
            transformer = Transformer.from_crs("EPSG:4326", "EPSG:32633")
            
            # Project the polygon to UTM
            projected_points = [transformer.transform(lon, lat) for lat, lon in points_area]
            projected_polygon = Polygon(projected_points)

            # Compute the area in square meters
            area_sq_meters = projected_polygon.area
            if is_logging:
                print(f'area_sq_meters={area_sq_meters}')
            
            folium.Rectangle(bounds=points_rect, color='#ff7800', fill=True, 
                        fill_color='#ffff00', fill_opacity=0.2, 
                        tooltip=f'<b>Area:</b> {area_sq_meters}  m2', 
                    ).add_to(fg)
        l_fg.append(fg)
    return l_fg