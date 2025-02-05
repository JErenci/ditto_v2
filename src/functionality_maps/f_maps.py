import json
import base64
from flask import request

import geopandas as gpd
import folium
import pandas as pd

from dash import html
import sys

import folium.plugins

import folium
from folium.plugins import MarkerCluster

sys.path.append('/Users/User/PycharmProjects/ditto_v2/')
from functionality_maps import Defs
from functionality_maps import paths

highlight_function = lambda x: {'fillColor': 'red',
                                'color': 'black',
                                'lineColor': 'red',
                                'fillOpacity': 0.50,
                                'weight': 0.1}

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
        print(f'{d_company["icon"]}')
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
        print(f'path={path}')
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


def get_feature_group(pdf: pd.DataFrame, category: str) -> folium.FeatureGroup:
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


def extract_gdf_json(path:str = 'GADM/gadm41_', country_3:str = 'AUT', l_levels:list = [1,2,3,4], is_logging:bool=False) :
    l_gdf = []
    l_name_adm = []
    l_tooltip = []
    
    l_field = []
    l_alias = []
    
    l_field_ini = []
    l_alias_ini = []
    
    for level in l_levels:
        if is_logging:
            print(f' level={level}')
        path_adm = f'{path}{country_3}_{level}.json'
        gdf_adm = gpd.read_file(path_adm)
        if is_logging:
            print(f'  Adding level={level} [{gdf_adm.shape[0]}]')
        l_gdf.append(gdf_adm)

        col_name = f'TYPE_{level}'
        if is_logging:
            print(f'col_name={col_name}')
        name_adm = extract_values(gdf_adm[col_name].drop_duplicates().values)
        if is_logging:
            print(f'  Extracting name for ADM={level} [{name_adm}]')
        l_name_adm.append(name_adm)

        if not l_field_ini:
            l_field_ini = [f'NAME_{level}']
        else:
            l_field_ini.append(f'NAME_{level}')
        l_field.append(l_field_ini)
        if is_logging:
            print(f'l_field_ini = {l_field_ini} in tooltip{level}')
            
        if not l_alias_ini:
            l_alias_ini = [name_adm]
        else:
            l_alias_ini.append(name_adm)
        l_alias.append(l_alias_ini)
        if is_logging:
            print(f'l_alias_ini= {l_alias_ini} to tooltip{level}')
            
        tooltip = folium.GeoJsonTooltip(
            fields=l_field_ini.copy(),
            aliases=l_alias_ini.copy(),
        )
        l_tooltip.append(tooltip)


    return [l_gdf, l_name_adm, 
            l_tooltip,
            l_field, l_alias
           ]


def extract_gdf_gpkg(path:str, l_levels:list = [1,2,3,4], is_logging:bool=False) :
    l_gdf = []
    l_name_adm = []
    l_tooltip = []
    
    l_field = []
    l_alias = []
    
    l_field_ini = []
    l_alias_ini = []
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
            # l_field, 
            # l_alias
           ]


def extract_values(col_values):
    name_adm = list(col_values)
    name_adm = [x for x in name_adm if x != 'NA']
    return name_adm


def gen_maps(l_adm:list, l_gdf:list, l_name_adm:list, l_tooltip:list, is_logging:bool=False) -> folium.Map():
    
    fm = folium.Map()
    
    for adm, gdf_adm, name_adm, tooltip_adm in zip(l_adm, l_gdf, l_name_adm, l_tooltip):
    # for adm, gdf_adm, tooltip_adm in zip(l_adm, l_gdf, l_tooltip):
        if(type(adm) == str):
            current_adm = int(adm[-1])
        else:
            current_adm = adm
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

def get_folium_featuregroup_color(pdf: pd.DataFrame,
                                  fg_name: str,
                                    fields: list = None,
                                    aliases: list = None,
                                    is_tooltip: bool = True,  # does NOT add weight to map
                                    is_highlighted: bool = True,  # does NOT add weight to map
                                    fill_color:str = 'blue') -> folium.FeatureGroup:
    # Avoid mutable elements
    if fields is None:  # 
        fields = ['ISO_A3', 'ADMIN']
    if aliases is None:
        aliases = ['Country Code:', 'Country Name:']

    fg = folium.FeatureGroup(name=fg_name)

    # Add hover functionality_maps.
    style_function = lambda x: {'fillColor': fill_color,
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
    return fg

from folium import Marker
from jinja2 import Template
class MarkerWithProps(Marker):
    _template = Template(u"""
        {% macro script(this, kwargs) %}
        var {{this.get_name()}} = L.marker(
            [{{this.location[0]}}, {{this.location[1]}}],
            {
                icon: new L.Icon.Default(),
                {%- if this.draggable %}
                draggable: true,
                autoPan: true,
                {%- endif %}
                {%- if this.props %}
                props : {{ this.props }} 
                {%- endif %}
                }
            )
            .addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)
    def __init__(self, location, popup=None, tooltip=None, icon=None,
                 draggable=False, props = None ):
        super(MarkerWithProps, self).__init__(location=location,popup=popup,tooltip=tooltip,icon=icon,draggable=draggable)
        self.props = json.loads(json.dumps(props))    


def gen_markercluster_sum_fg (gdf, name:str, lat, lon, column_sum, ):
    fg_mc = folium.FeatureGroup(name=name)

    icon_create_function = '''
        function(cluster) {
            var markers = cluster.getAllChildMarkers();
            var sum = 0;
            for (var i = 0; i < markers.length; i++) {
                sum += markers[i].options.props.population / 1000000;
                sum = Math.round(sum * 1000) / 1000;
            }
            var avg = sum;

            return L.divIcon({
                html: '<b>' + avg + 'M</b>',
                className: 'marker-cluster marker-cluster-small',
                iconSize: new L.Point(50, 50)
            });
        }
    '''

    marker_cluster = MarkerCluster(icon_create_function=icon_create_function)

    for index, row in gdf.iterrows():
        marker = MarkerWithProps(location=[row[lat], row[lon]], 
                    props={'population': row[column_sum]})
        marker.add_to(marker_cluster)

    marker_cluster.add_to(fg_mc)
    return fg_mc