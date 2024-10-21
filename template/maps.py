import pandas as pd

import geopandas as gpd
import folium
import folium.plugins

def gen_map(
    pdf:pd.DataFrame, 
    legend_str:str, 
    is_pdf_breakdown:bool=False,
    col_pdf_breakdown:str=None,
    dict_zones:dict=None,
    sel_col:str=None,
    highlight_function=None, 
    dict_tooltip:dict=None,
    logging:bool=False
) -> folium.Map:


    # Define the custom style function
    def style_fn(feature):
        value = feature['properties'][col_pdf_breakdown]
        return {'fillColor': value, 'fillOpacity': 0.2}
    
    # Create Folium map
    m = folium.Map(tiles='cartodbpositron')

    if dict_tooltip == None:
        tooltip = None
    else:
        tooltip = folium.GeoJsonTooltip(fields=list(dict_tooltip.keys()), 
                                aliases=list(dict_tooltip.values()))
        
    if is_pdf_breakdown == False:
        # Add GeoJSON object to the map
        fg = folium.FeatureGroup(name=legend_str)
        gj = folium.GeoJson(
                data=pdf,
                nan_fill_opacity=0.1,
                line_color=None,
                # highlight_function=highlight_function,
                tooltip=tooltip
            )
        
        fg.add_child(gj)
        m.add_child(fg)

    else:
        l_breakdown = list(pdf[col_pdf_breakdown].unique())
        l_featGroups = []
        for zone in l_breakdown:
                
            fg_name = f'{legend_str} [{zone}, {dict_zones[zone]}]'
            fg_name_styled = f'<span style="color: {zone};">{fg_name}</span>'
            
            if logging:
                print(f'fg_name={fg_name}')
            fg = folium.FeatureGroup(name=fg_name_styled)

            pdf_zone = pdf[pdf[col_pdf_breakdown] == zone]            
            gj = folium.GeoJson(
            data=pdf_zone,
            # nan_fill_opacity=0.1,
            style_function=style_fn,
            # line_color=zone,
            highlight_function=highlight_function,
            tooltip=folium.GeoJsonTooltip(fields=list(dict_tooltip.keys()), 
                              aliases=list(dict_tooltip.values()))
            )
        
            fg.add_child(gj)
            l_featGroups.append(fg)
            # m.add_child(fg)

        if logging:
            print(f'Adding Folium.FeatureGroups [{len(l_featGroups)}]')
        for fgr in l_featGroups:
            fgr.add_to(m)
            # m.add_child(fgr)

    if logging:
        print('Adding fullscreen')
    fullscreen = folium.plugins.Fullscreen(position='topleft',
                                           title='Expand me',
                                           title_cancel='Exit me',
                                           force_separate_button=True)
    m.add_child(fullscreen)
    
    
    # Display the map
    
    if logging:
        print('Adding minimap')
    m.add_child(folium.plugins.MiniMap())
    
    # Add layer control to toggle feature groups
    if logging:
        print('Adding LayerControl')
    folium.LayerControl(position='topright',
                        collapsed=False).add_to(m)
    
    m.fit_bounds(m.get_bounds())
    
    return m


highlight_function = lambda x: {
    # 'fillColor': 'red',
                                # 'color': 'black',
                                # 'lineColor': 'red',
                                'fillOpacity': 0.80,
                                # 'weight': 0.1
}


def map_range(x,dict_color):
    for key, value in dict_color.items():
        if key[0] <= x <= key[1]:
            return value
    return np.nan  # or any default value you prefer

def add_color_column_to_pdf_based_on_limits(pdf, col_ref:str, 
                                            first_lim:float, second_lim:float,
                                            first_color:str='green', second_color:str='yellow', third_color:str='red',
                                            col_color:str='color',
):
    dict_color = {
        (0, first_lim): first_color, 
        (first_lim, second_lim): second_color, 
        (second_lim, float('inf')): third_color
    }
    dict_color_inv = {v: k for k, v in dict_color.items()}
    # dict_color_inv

    def map_range(x,dict_color):
        for key, value in dict_color.items():
            if key[0] <= x <= key[1]:
                return value
        return np.nan  # or any default value you prefer
        
    pdf[col_color] = pdf[col_ref].apply(lambda x : map_range(x,dict_color))
    return [pdf,dict_color,dict_color_inv]
    
import json
import base64
from flask import request

import geopandas as gpd
import folium
import pandas as pd

from dash import html
import sys

import folium.plugins

# sys.path.append('/Users/User/PycharmProjects/ditto_v2/')
# from functionality_maps import Defs
# from functionality_maps import paths


def get_folium_map_countries(l_fg: list = None, d_company: dict = None):
    print()
    print('get_folium_map_countries()')

    fm = folium.Map(  # max_zoom=18,
        # zoom_start=5,
        tiles=None,
        no_wrap=True,
    )
    for tile in paths.l_tilelayer:
        tile.add_to(fm)

    for fg in l_fg:
        fg.add_to(fm)

    if d_company:
        print('Getting Icons')
        icon_company = folium.features.CustomIcon(d_company['icon'],
                                                  icon_size=(50, 50))

        pdf_marker_coords = pd.DataFrame.from_dict(d_company['locations'], orient='index')

        # print('Single marker')
        # feature_group2 = folium.FeatureGroup(name='Company2 with Single Marker')
        #
        # folium.Marker(location=[47.5618,9.7],
        #                               popup='popup',
        #                               icon=icon_company,
        #                               tooltip='tooltip').add_to(feature_group2)
        # fm.add_child(feature_group2)

        print('Adding markers to a feature group')
        fg_markers = folium.FeatureGroup(name=d_company['name'])

        for index, row in pdf_marker_coords.iterrows():
            folium.Marker(location=[row["lat"], row["lon"]],
                          popup=row["address"],
                          tooltip=index,
                          icon=folium.features.CustomIcon(icon_image=d_company['icon'],
                                                          icon_size=(50, 50))
                          ).add_to(fg_markers)
        fm.add_child(fg_markers)

    ## DID NOT WORK ##
    # pdf_marker_coords.apply(lambda row: folium.Marker(location=[row['lat'], row['lon']],
    #                                                   # tooltip=row['address'],
    #                                                   icon=icon,
    #                                                   # popup='Baumgartner'
    #                                                   ).add_to(fg_markers),
    #                         axis=1)

    print('Adding fullscreen')
    fullscreen = folium.plugins.Fullscreen(position='topleft',
                                           title='Expand me',
                                           title_cancel='Exit me',
                                           force_separate_button=True)
    fm.add_child(fullscreen)

    print('Adding minimap')
    fm.add_child(folium.plugins.MiniMap())

    print('Adding LayerControl')
    layercontrol = folium.LayerControl(position='topright',
                                       collapsed=False)
    fm = fm.add_child(layercontrol)

    print('Adding coordinates')
    fm.add_child(folium.LatLngPopup())

    print('Fitting bounds')
    fm.fit_bounds(fm.get_bounds())

    print('Finished')

    return fm


def get_folium_featuregroup(pdf: pd.DataFrame,
                            fg_name: str,
                            fields: list = None,
                            aliases: list = None,
                            is_tooltip: bool = True,  # does NOT add weight to map
                            is_highlighted: bool = True  # does NOT add weight to map
                            ) -> folium.FeatureGroup:
    # Avoid mutable elements
    if fields is None:  #
        fields = ['ISO_A3', 'ADMIN']
    if aliases is None:
        aliases = ['Country Code:', 'Country Name:']

    fg = folium.FeatureGroup(name=fg_name)

    # Add hover functionality_maps.
    style_function = lambda x: {'fillColor': 'blue',
                                'color': 'black',
                                'line_color': 'red',
                                'fillOpacity': 0.3,
                                'weight': 0.1}

    tooltip = None
    if is_tooltip:
        tooltip = folium.features.GeoJsonTooltip(
            fields=fields,
            aliases=aliases
        )

    highlight_function = None
    if is_highlighted:
        highlight_function = lambda x: {'fillColor': 'red',
                                        'color': 'black',
                                        'lineColor': 'red',
                                        'fillOpacity': 0.50,
                                        'weight': 0.1}

    gj = folium.GeoJson(
        data=pdf,
        # nan_fill_opacity=0.1,
        style_function=style_function,
        # line_color='black',
        highlight_function=highlight_function,
        tooltip=tooltip
    )

    fg.add_child(gj)

    # NO NEED TO USE THIS, HIGHLIGHT DOES NOT WORK!
    #     else:
    #         choropleth = folium.Choropleth(
    #             pdf,
    #             fill_opacity = 0.3,
    #             nan_fill_color='purple',
    #             nan_fill_opacity=0.1,
    #             style_function=style_function,
    #             # highlight_function=highlight_function,
    #             Highlight= True,
    #             )#.add_to(fg)

    #         cp = choropleth.geojson.add_child(
    #             tooltip)
    #         fg.add_child(cp)

    return fg


def load_gdf_from_csv(path: str, crs: str = None) -> gpd.GeoDataFrame:
    # Avoid default arg warning
    if crs is None:
        crs = "EPSG:4326"
    pdf_countries = pd.read_csv(path, index_col=[0])
    # Filter countries with null geometry
    pdf_countries = pdf_countries[pdf_countries['geometry'].notnull()]
    gs = gpd.GeoSeries.from_wkt(pdf_countries['geometry'])
    # print(f'gs.shape={gs.shape()}')
    pdf_countries = gpd.GeoDataFrame(pdf_countries, geometry=gs, crs=crs)
    return pdf_countries


def get_fg_from_locations(coords: pd.DataFrame) -> folium.FeatureGroup:
    print('Adding markers to a feature group')
    fg_markers = folium.FeatureGroup(name=Defs.company['name'])

    for index, row in coords.iterrows():
        folium.Marker(location=[row["lat"], row["lon"]],
                      popup=row["address1"] + '\n' + row["address2"],
                      tooltip=index,
                      icon=folium.features.CustomIcon(icon_image=Defs.company['icon'],
                                                      icon_size=(50, 50))
                      ).add_to(fg_markers)

    return fg_markers


def read_dict_temp(path: str):
    f = open(path)
    data = json.load(f)
    # Closing file
    f.close()
    return data


def get_image(path: str):
    image_encoded = base64.b64encode(open(path, 'rb').read())
    image = html.Img(src=f'data:image/png;base64,{image_encoded.decode()}',
                     style={'height': '50%', 'width': '50%'},
                     width='800', height='600'
                     )
    return image


def try_read_dict_temp():
    try:
        company = request.authorization['username']
        # print(f'company: {company}')

        path = f'data_loaded.json'
        # print(f'path={path}')
        d_company = read_dict_temp(path)
        print(f'd_company: {d_company}')
    except Exception as ex:
        print(ex)
    return [company, d_company]


def write_dict_temp(d: dict, path: str):
    with open(f'{path}.json', 'w') as json_file:
        json.dump(d, json_file)

    # f = open(f"{path}.txt", "w")
    # f.write(json.dumps(d))
    # f.close()
    print("Dictionary has been written!")


def write_map_temp(fm: folium.Map(), name_map: str):
    f = open(f"{name_map}.txt", "w")
    f.write(fm._repr_html_())
    f.close()
    print("Map has been written!")


def get_feature_group(pdf: pd.DataFrame,
                      category: str) -> folium.FeatureGroup:
    if not pdf.empty:
        print(f'Count: [{pdf.shape[0]}]')
        print(f'pdf [{pdf.head(1)}]')

        fg_districts = get_folium_featuregroup(pdf=pdf,
                                               fg_name=f'{category} [{pdf.shape[0]}]',
                                               fields=paths.fields[category],
                                               aliases=paths.aliases[category],
                                               )
        return fg_districts
    else:
        return None


def get_feature_group_countries(gdf_world: gpd.geodataframe.GeoDataFrame,
                                l_countries: list = None,
                                l_columns_invalid: list = None,
                                key_filter: str = None,
                                fields: list = None,
                                aliases: list = None
                                ):
    # Avoid unmutable default arg warning
    if l_countries is None:
        l_countries = []
    if l_columns_invalid is None:
        l_columns_invalid = ['geometry']
    if key_filter is None:
        key_filter = 'ISO_A3'
    if fields is None:
        fields = ['ISO_A3', 'ADMIN']
    if aliases is None:
        aliases = ['Country Code:', 'Country Name:']

    print('[1/4] Filtering countries...')
    print(f'   Total countries:{gdf_world.shape[0]}')
    if l_countries:
        gdf_world = gdf_world[gdf_world[key_filter].isin(l_countries)]
    else:
        gdf_world = gdf_world
    print(f'   Used countries:{gdf_world.shape[0]}')
    # pdf_countries

    # Removing rows with invalid geometries
    print('[2/4] Removing rows with invalid values...')
    for invalid_row in l_columns_invalid:
        print(f' Row: [{invalid_row}]')
        if invalid_row in gdf_world.columns:
            print(f' Removing [{invalid_row}]')
            total = gdf_world.shape[0]
            print(f'   Total:  {total}')
            invalid = gdf_world[gdf_world[invalid_row].isnull()].shape[0]
            print(f'   Invalid:{invalid}, {gdf_world[gdf_world[invalid_row].isnull()][key_filter].to_list()}')
            gdf_world = gdf_world[gdf_world[invalid_row].notnull()]
            total = gdf_world.shape[0]
            print(f'   Total after removal:  {total}')

    print('[3/4] Getting Feature Group...')
    fg_countries = get_folium_featuregroup(pdf=gdf_world,
                                           fg_name=f'Countries [{gdf_world.shape[0]}]',
                                           fields=fields,
                                           aliases=aliases,
                                           )
    return fg_countries