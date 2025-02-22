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
# from functionality_maps import Defs
# from functionality_maps import paths
from src.functionality_maps import Defs, paths

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

def get_folium_geojson(pdf: pd.DataFrame,
                        fields: list = None,
                        aliases: list = None,
                        is_tooltip: bool = True,  # does NOT add weight to map
                        is_highlighted: bool = True  # does NOT add weight to map
                        ) -> folium.GeoJson:
    # Avoid mutable elements
    if fields is None and aliases is None:
        fields = ['ISO_A3', 'ADMIN']
        aliases = ['Country Code:', 'Country Name:']

    # Add hover functionality_maps.
    style_function = lambda x: {'fillColor': 'blue',
                                'color': 'black',
                                'line_color': 'red',
                                'fillOpacity': 0.3,
                                'weight': 0.1}
    if is_tooltip:
        tooltip = folium.features.GeoJsonTooltip(
            fields=fields,
            aliases=aliases
        )
    else:
        tooltip = None

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
    return gj

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

from functools import partial
import pyproj
from shapely.geometry import Point
from shapely.ops import transform
from pyproj import Transformer

def transform_wgs84_aeqd(lon, lat) :
    point_transformed =Transformer.from_crs(4326, 3857, always_xy=True).transform(float(lat),float(lon))
    return point_transformed

def transform_aeqd_wgs84(y,x) :
    point_transformed = Transformer.from_crs(3857, 4326, always_xy=True).transform(y,x)
    return point_transformed

# create a circle with a specified radius in meters around a point defined using latitude and longitude
import pyproj
from shapely import geometry
from pyproj import Transformer
import shapely#.ops import transform
import geopandas as gpd

def circle_latlon(lon, lat, radius) : 
    # print(f'lon:{lon}, lat:{lat}, radius:{radius}')
    proj_wgs84 = pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs")
    proj_aeqd = pyproj.Proj("+proj=aeqd +R=6371000 +units=m +lat_0={} +lon_0={}".format(lat, lon))
    transformer_wgs84_aeqd = Transformer.from_proj(proj_wgs84, proj_aeqd)
    transformer_aeqd_wgs84 = Transformer.from_proj(proj_aeqd, proj_wgs84)
    
    x,y = transformer_wgs84_aeqd.transform(float(lon), float(lat))
    # print(f'x:{x}, y:{y}')
    point_transformed = geometry.Point(x, y)
    # print(f'point_transformed:{point_transformed}')
    buffer = point_transformed.buffer(radius)
    # print(f'buffer={buffer}')
    
    circle_poly = shapely.ops.transform(transformer_aeqd_wgs84.transform, buffer)
    # print(f'circle_poly:{circle_poly}')

    return circle_poly


def circle_around_lat_lon_point(lon, lat, radius) : 
    # lon, lat = 0, 42  # Example coordinates for San Francisco
    # radius = 30000  # Radius in meters

    local_azimuthal_projection = "+proj=aeqd +R=6371000 +units=m +lat_0={} +lon_0={}".format(lat, lon)
    wgs84_to_aeqd = partial(pyproj.transform, pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs"), pyproj.Proj(local_azimuthal_projection))
    aeqd_to_wgs84 = partial(pyproj.transform, pyproj.Proj(local_azimuthal_projection), pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs"))

    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857")
    
    center = Point(float(lon), float(lat))
    point_transformed = transform(wgs84_to_aeqd, center)
    # print(f'x{point_transformed.x}, y={point_transformed.y}')


def get_gdf_circle(df:pd.DataFrame, radius_km:int, color:str='blue') -> gpd.GeoDataFrame:
    geometry = df.apply(lambda x: circle_latlon(x['lon'], x['lat'], radius = 1000 * radius_km), axis=1)
    df_out = gpd.GeoDataFrame(df, geometry=geometry ,crs="EPSG:4326")
    return df_out

from geopy.distance import geodesic


def compute_dist_to_lat_lon(gdf,lon,lat,col_out:str='dist',units:str='km',round_dec:int=2):
    point_of_interest = (lat,lon)
    if units == 'km':
        gdf[col_out] = gdf.geometry.apply(
            lambda row: geodesic(point_of_interest, (row.y, row.x)).kilometers)
    elif units == 'm':
        gdf[col_out] = gdf.geometry.apply(
            lambda row: geodesic(point_of_interest, (row.y, row.x)).meters)
    elif units == 'mi':
        gdf[col_out] = gdf.geometry.apply(
            lambda row: geodesic(point_of_interest, (row.y, row.x)).miles)
    else:
        raise ValueError("units must be one of the following [km,m,mi]")
    gdf[col_out] = round(gdf[col_out], round_dec)
    return gdf

def overlay_shapes(gdf_circle: gpd.GeoDataFrame,
                   col_perc:str,
                   d_columns:dict,
                   epsg:int=6933, num_dec:int=2) -> gpd.GeoDataFrame:
    
    for k,v in d_columns.items():
        key = k + '_int'
        if v['is_norm']:
            gdf_circle[key] = gdf_circle[k] * gdf_circle[col_perc]

        if v['is_int']:
            gdf_circle[key] = gdf_circle[key].astype(int)

    return gdf_circle
    

def merge_shapes(gdf_circle: gpd.GeoDataFrame,
                 l_col_percs:list,
                 d_percs:dict, perc_prefix:str='perc',
                 epsg:int=6933, num_dec:int=2, is_logging:bool=False) -> gpd.GeoDataFrame:
    
    l_new_columns = []
    # Generate the Merged [Polygon, DataFrame]
    poly_merged = gdf_circle.geometry.union_all()
    gdf_merged = gpd.GeoSeries([poly_merged]).to_frame(name='geometry').set_crs(epsg=epsg)

    for col in l_col_percs:
        gdf_merged[col] = round(gdf_circle[col].sum(), num_dec)
        col_int = col + '_int'
        gdf_merged[col_int] = round(gdf_circle[col_int].sum(), num_dec)
        l_new_columns.append(col)
        l_new_columns.append(col_int)

    for k,v in d_percs.items():
        col_key = f'{perc_prefix}_{k}'
        col_num = f'{v}_int'
        col_den = v
        gdf_merged[col_key] = round(gdf_merged[col_num] / gdf_merged[col_den], num_dec)
        l_new_columns.append(col_key)
    
    if is_logging:
        for col in l_new_columns:
            print(f'{col} = {gdf_merged.iloc[0][col]}')
    return gdf_merged

def get_markers_polygon(gdf:gpd.GeoDataFrame,l_tooltip:list,
                        col_lat:str='lat', col_lon:str='lon',
                        name:str='Markers',
                        color:str='blue') -> folium.FeatureGroup:

    fg = folium.FeatureGroup(name=name)
    for index, row in gdf.iterrows():
        l_msg = [f'{elem}: {row[elem]}' for elem in l_tooltip]
        tooltip = ','.join(l_msg)
        # tooltip = folium.Tooltip(f"Locality: {row['GEN']} <br> Distance[Km]: {row['dist']}")
        # popup = folium.Popup(f"lat: {row['lat']}\nLon: {row['lon']}")
        folium.Marker(location=[row[col_lat], row[col_lon]],
                        # popup=popup,
                        icon=folium.Icon(color=color),
                        tooltip=tooltip
                        ).add_to(fg)
    return fg

def get_fg_markers(df:pd.DataFrame,
                   name:str, l_tooltip:list=None, l_popup:list=None,
                   color:str='blue') -> folium.FeatureGroup:

    fg = folium.FeatureGroup(name=name)
    tooltip, popup = None, None
    for index, row in df.iterrows():
        if l_popup is not None:
            df_contains_www = df[l_popup].apply(lambda col: col.astype(str).str.contains('www').any(), axis=0)
            true_columns = df_contains_www.all()
            if true_columns:
                l_msg = ''
                for elem in l_popup:
                    link = f'''<a href={row[elem]}>{row[elem]}</a>'''
                    l_msg = [f'{elem}: {link}']
            else:
                l_msg = [f'{elem}: {row[elem]}' for elem in l_popup]
            popup = folium.Popup(''.join(l_msg))

        if l_tooltip is not None:
            l_msg = [f'{elem}: {row[elem]}' for elem in l_tooltip]
            tooltip = folium.Tooltip('<br>'.join(l_msg))
            
        folium.Marker(location=[row.lat, row.lon],
                        popup=popup,
                        icon=folium.Icon(color=color),
                        tooltip=tooltip
                        ).add_to(fg)
    return fg

def load_germany(l_levels:list, is_logging:bool=False) -> dict:
    d_ger = dict()
    for level in l_levels:
        if level == 'census':
            d_ger['census'] = gpd.read_file('./JupNB/DE_Data/VG250_GEM_WGS84.shp')
            if is_logging:
                print(f'Census is loaded!')
        else:
            d_ger[level] = load_gdf_from_csv(path=paths.csv[paths.d_map_gadm_name[level]])
            if is_logging:
                print(f'Level [{level}-{paths.d_map_gadm_name[level]}] loaded!')
    return d_ger


d_ISO_characters = {'Ã¼': 'ü', 'Ã¶':'ö', 'Ã¤':'ä', 'ÃŸ':'ß'}
# def fix_ISO_characters():

def fix_dict_ISO_characters(d:dict) -> dict:
    for k,v in d.items():
        d[k] = v.replace(d_ISO_characters, regex=True)
    return d




    # gdf_geom[col_name] = gdf_geom.geometry.apply(
    #     lambda row: gdf_poly.geometry.contains(row).any())
    # if is_logging:
    #     print(f'overlay_shapes: {gdf_geom[col_name].value_counts()}')
    # return gdf_geom