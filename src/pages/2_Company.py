import dash
import folium
import numpy as np
import pandas as pd
import plotly.express as px
from dash import callback, html, dcc, Input, Output, dash_table, no_update
import dash_bootstrap_components as dbc
from geopy.geocoders import Nominatim

from shapely import geometry

# from functionality_maps import f_maps
import sys
# sys.path.append('/Users/User/PycharmProjects/ditto_v2/')
# if __name__ == '__main__':
from functionality_maps import f_maps, f_gadm
from functionality_maps import paths

import geopandas as gpd

from assets import run_relevant_variables
from src.functionality import colors
from src.functionality_maps import Defs
company_name = run_relevant_variables.company_name
file_used = run_relevant_variables.file_used

dash.register_page(__name__)

path_map_empty = '/assets/Geo/Map_empty.html'
path_wca = '/assets/Geo/world_country_area.csv'
fields_wca = ['ADMIN', 'ISO_A3', 'Area_total_km2']
aliases_wca = ['Code', 'Country', 'Area [km\u00b2]']

gdf_world = f_maps.load_gdf_from_csv(path=paths.path_wca)
pdf_d1 = f_maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[1]])
pdf_d2 = f_maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[2]])
pdf_d3 = f_maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[3]])
pdf_d4 = f_maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[4]])
pdf_zips = pdf_d4['postcode']  # For indexing

pdf_d1 = pdf_d1.replace({'Ã¼': 'ü', 'Ã¶':'ö', 'Ã¤':'ä', 'ÃŸ':'ß'}, regex=True) 
pdf_d2 = pdf_d2.replace({'Ã¼': 'ü', 'Ã¶':'ö', 'Ã¤':'ä', 'ÃŸ':'ß'}, regex=True) 
pdf_d3 = pdf_d3.replace({'Ã¼': 'ü', 'Ã¶':'ö', 'Ã¤':'ä', 'ÃŸ':'ß'}, regex=True) 
pdf_d4 = pdf_d4.replace({'Ã¼': 'ü', 'Ã¶':'ö', 'Ã¤':'ä', 'ÃŸ':'ß'}, regex=True) 

pdf_stores = pd.read_json(paths.stores, orient='records', lines=True)
# Load the saved GeoJSON file into a new GeoDataFrame
gdf_zensus_de = gpd.read_file('JupNB\DE_Data\VG250_GEM_WGS84.shp')


company_name = 'D1tt0'

comp_text_Geo = html.H3('Geo Data')
comp_dropCountry = dcc.Dropdown(
                id='dropdown_country_filter0',
                options=gdf_world.ADMIN.unique(),
                value=[],
                multi=True,
                searchable=True,
                persistence=False,
                persistence_type='memory',  # session
                placeholder=f"Select {paths.l_d_dropdown_map[0]}",
            )
comp_dropState = dcc.Dropdown(
                id='dropdown_country_filter1',
                options=pdf_d1['name'].unique(),
                value=[],
                multi=True,
                searchable=True,
                persistence=False,
                persistence_type='memory',  # session
                placeholder=f"Select {paths.l_d_dropdown_map[1]}(s)",
            )
comp_dropRegion = dcc.Dropdown(
                id='dropdown_country_filter2',
                options=pdf_d2['NAME_2'].unique(),
                value=[],
                multi=True,
                searchable=True,
                persistence=False,
                persistence_type='memory',  # session
                placeholder=f"Select {paths.l_d_dropdown_map[2]}(s)",
            )
comp_dropDistrict = dcc.Dropdown(
                id='dropdown_country_filter3',
                options=pdf_d3['NAME_3'].unique(),
                value=[],
                multi=True,
                searchable=True,
                persistence=False,
                persistence_type='memory',  # session
                placeholder=f"Select {paths.l_d_dropdown_map[3]}(s)",
            )
comp_dropZIP = dcc.Dropdown(
                id='dropdown_country_filter4',
                options=pdf_d4['postcode'].unique(),
                value=[],
                multi=True,
                searchable=True,
                persistence=False,
                persistence_type='memory',  # session
                placeholder=f"Select {paths.l_d_dropdown_map[4]}(s)",
            )


comp_text_Sales = html.H3('Sales Data')
comp_dropSales = dcc.Dropdown(
                id='dropdown_sales',
                options=pdf_stores['store'].unique(),
                value=[],
                multi=True,
                searchable=True,
                persistence=False,
                persistence_type='memory',  # session
                placeholder=f"Select Store(s)",
            )

comp_text_metadata = html.H3('Metadata')
comp_dropMetadata = dcc.Dropdown(
                id='dropdown_metadata',
                options=['EWZ', 'KFL', 'EPK'],
                value=[],
                multi=True,
                searchable=True,
                persistence=False,
                persistence_type='memory',  # session
                placeholder=f"Select Variable(s)",
            )
comp_text_coverage = html.H3('Geographic coverage')
comp_dropCoverage = dcc.Dropdown(
                id='dropdown_coverage',
                options=[1,5,10,20,30,50],
                value=[30],
                multi=False,
                searchable=True,
                persistence=False,
                persistence_type='memory',  # session
                placeholder=f"Select Area of Influece around Store[Km]",
            )

comp_pdf_found = html.Div(id='pdf_world_found')
comp_fig = html.Div(id='fig_bottom')
comp_map = html.Div(id='map_figure_right')

# layout = dbc.Container(
layout = dbc.Container(
[
    # dcc.Markdown('# This will be the content of Page Company'),
    html.Div(id='image_customer', children=''),
    dbc.Row(
        dbc.Col(html.H1("World Dashboard",
                        className='text-center text-primary',),
                width=12)
    ),

    dbc.Row([
        dbc.Col([
            comp_text_Geo,      # Geo component separaton
            comp_dropCountry,   # COUNTRY
            comp_dropState,     # STATE
            comp_dropRegion,    # REGION
            comp_dropDistrict,  # DISTRICT
            comp_dropZIP,       # ZIP

            comp_text_Sales,    # Sales component separaton
            comp_dropSales,      # Sales
            comp_text_metadata,  # Metatdata component separation
            comp_dropMetadata,   # Metadata,
            comp_text_coverage,  # Store Coverage text separator
            comp_dropCoverage,   # Store Coverage [Km]
            comp_fig
        ], width={'size': 5}),
        dbc.Col([
            comp_pdf_found,     # MAP
            comp_map            # MAP
        ], width={'size': 7}),
    ], justify='start'),  # Horizontal:start,center,end,between,around
],
fluid=True,     # Stretch to use all screen
)

@callback(
# Output(component_id='pdf_world_found', component_property='children'),
Output(component_id='map_figure_right', component_property='children'),
# Output(component_id='fig_bottom', component_property='children'),
Input(component_id='dropdown_country_filter0', component_property='value'),#COUNTRY
Input(component_id='dropdown_country_filter1', component_property='value'),#STATE
Input(component_id='dropdown_country_filter2', component_property='value'),#REGION
Input(component_id='dropdown_country_filter3', component_property='value'),#DISTRICT
Input(component_id='dropdown_country_filter4', component_property='value'),#ZIP
Input(component_id='dropdown_sales', component_property='value'),#Stores
Input(component_id='dropdown_metadata', component_property='value'),#Metadata
Input(component_id='dropdown_coverage', component_property='value'),#Store coverage
prevent_initial_call=True
)
def gen_map_countryX(l_countries, l_states, l_regions, l_districts, l_zips, 
                     l_stores, l_metadata, l_coverage):
    dropdown_value = paths.l_d_dropdown_map
    fig = None

    print(f'gen_map_country')
    print(f'')

    print(f'dropdown_value:{dropdown_value}')
    print(f'')

    print(f'country = {l_countries}')
    print(f'state =   {l_states[0:5]}')
    print(f'region =  {l_regions[0:5]}')
    print(f'district ={l_districts[0:5]}')
    print(f'zip =     {l_zips[0:5]}')
    print(f'')

    # Initialize list of feature_groups
    l_fg = []

    #COUNTRY
    category = paths.l_d_dropdown_map[0]
    print(f'l_countries={l_countries}')

    print('gdf_world')
    print(gdf_world)
    print(gdf_world.columns.to_list())

    pdf_world = gdf_world['ADMIN']
    print('pdf_world')
    print(pdf_world)
    print(f'type={type(pdf_world)}')
    # print(pdf_world.columns.to_list())

    # pred1 = pdf_world.isin([l_countries])
    # print(f'pred1={pred1}')
    # pdf1 = gdf_world[pred1]
    # print('pdf1')
    # print(pdf1.shape)
    # print(f'Countries found={pdf1.shape[0]}')

    print(f'l_countries={l_countries}')
    pred2 = pdf_world.isin(l_countries)
    print(f'pred2={pred2}')
    pdf = gdf_world[pred2]
    print('pdf2')
    print(pdf.head())
    pdf_countriesNo = pdf.shape[0]
    print(f'Countries found={pdf_countriesNo}')
    if l_countries:
        fg_countries = f_maps.get_feature_group_countries(gdf_world=pdf,
                                                        l_countries=l_countries,
                                                        key_filter='ADMIN',
                                                        fields=paths.fields_wca,
                                                        aliases=paths.aliases_wca)
        if fg_countries is not None:
            l_fg.append(fg_countries)
    # print(308)
    #STATES
    if l_states:
        category = paths.l_d_dropdown_map[1]
        pdf_states = pdf_d1['name']  # For indexing
        pdf = pdf_d1[pdf_states.isin(l_states)]

        print(f'States found={pdf.shape[0]}')
        fg_state = f_maps.get_feature_group(pdf, category)
        if fg_state is not None:
            l_fg.append(fg_state)

    #REGION
    if l_regions:
        category = paths.l_d_dropdown_map[2]
        pdf_regions = pdf_d2['NAME_2']  # For indexing
        pdf = pdf_d2[pdf_regions.isin(l_regions)]
        print(f'Regions found={pdf.shape[0]}')
        fg_region = f_maps.get_feature_group(pdf, category)
        if fg_region is not None:
            l_fg.append(fg_region)

    #DISTRICT
    if l_districts:
        category = paths.l_d_dropdown_map[3]
        pdf_districts = pdf_d3['NAME_3']  # For indexing
        pdf = pdf_d3[pdf_districts.isin(l_districts)]
        print(f'Districts found={pdf.shape[0]}')
        fg_district = f_maps.get_feature_group(pdf, category)
        if fg_district is not None:
            l_fg.append(fg_district)

    #         l_fg.append(fg)
    #         print(l_fg)

    #ZIP
    if(l_zips):
        category = paths.l_d_dropdown_map[4]
        pdf_zips = pdf_d4['postcode']  # For indexing
        pdf = pdf_d4[pdf_zips.isin(l_zips)]
        print(f'l_zips:{l_zips}')
        print(f'Zips found={pdf.shape[0]}')
        fg_zip = f_maps.get_feature_group(pdf, category)
        if fg_zip is not None:
            l_fg.append(fg_zip)

    if (l_stores):
        print(pdf_stores.head(1))
        pdf = pdf_stores[pdf_stores['store'].isin(l_stores)]

        
        if l_states:
            pdf = pdf[pdf['GADM_1'].isin(l_states)]
        if l_regions:
            pdf = pdf[pdf['GADM_2'].isin(l_regions)]
        if l_districts:
            pdf = pdf[pdf['GADM_3'].isin(l_districts)]

        print(f'l_stores:{l_stores}')
        print(f'Stores total={pdf_stores.shape[0]}')
        print(f'Stores found={pdf.shape[0]}')
        l_fg_stores = f_gadm.get_fg_store(pdf, l_stores)
        if l_fg_stores is not None:
            l_fg.extend(l_fg_stores)

    if (l_metadata):
        print(f'l_metadata:{l_metadata}')
        print(f'Metadata found={len(l_metadata)}')

        l_bundeslaender = [Defs.dict_bundeslaender_id[x] for x in l_states]
        print(f'l_bundeslaender:{l_bundeslaender}')
        
        gdf_zensus_de = gpd.read_file('JupNB\DE_Data\VG250_GEM_WGS84.shp')
        print(f'gdf_zensus_de:{gdf_zensus_de.shape}')
        gdf_map = gdf_zensus_de[gdf_zensus_de['SN_L'].isin(l_bundeslaender)]
        print(f'After filtering States, gdf_map.shape:{gdf_map.shape}')


        gdf_map = gdf_map.drop(['BEGINN','WSK'],axis=1)
        gdf_map = gdf_map.reset_index(drop=True)
        print(f'gdf_map:{gdf_map.shape}')

        
        # Norm to max value
        print(f'Max EPK={gdf_map["EPK"].max()}')
        gdf_map['EPK_norm'] = gdf_map['EPK'] / gdf_map['EPK'].max()

        gdf_map['EPK'] = gdf_map['EPK'].fillna(0)
        gdf_map['EPK_norm'] = gdf_map['EPK_norm'].fillna(0)
        print(f'Max EPK_norm={gdf_map["EPK_norm"].max()}')
        print(f'Min EPK_norm={gdf_map["EPK_norm"].min()}')

        # Replace Inf values with NaN in 'column1'
        gdf_map['EPK_norm'] = gdf_map['EPK_norm'].replace([np.inf, -np.inf], np.nan)
        print(f'gdf_map shape={gdf_map.shape}')

        # Drop rows with NaN values in 'column1'
        gdf_map = gdf_map.dropna(subset=['EPK_norm'])
        print(f'gdf_map shape={gdf_map.shape}')

        # Apply the function to create RGBA tuples for column C
        gdf_map['color_rgba_detailed'] = colors.rgba_from_value(gdf_map, 'blue', 'EPK_norm', 1.0)

        # Define custom quantile boundaries
        l_quantiles = [0, 0.1, 0.5, 0.9, 1.0]

        # Use pd.qcut() to create uneven quantiles
        gdf_map['quantile'] = pd.qcut(gdf_map['EPK_norm'], q=l_quantiles, labels=False, duplicates='drop')
        print(f'max={gdf_map['quantile'].max()}')
        # Ensure alpha is between 0 and 1
        alpha = 1.0 * (1/len(l_quantiles))

        print(f'alpha={alpha}')
        gdf_map['color_rgba_tuple'] = colors.rgba_from_value(gdf_map, 'blue', 'quantile', alpha)

        gdf_map['color'] = gdf_map['quantile'].map(Defs.dict_tuple_colors)
        gdf_map['color_norm'] = gdf_map['quantile'].map(Defs.dict_tuple_colors_norm)

        l_fg_metadata = []
        for it,i in enumerate(l_quantiles):
            print(f'Processing quantile [{it}/{len(l_quantiles)}]')
            gdf_quantile = gdf_map[gdf_map['quantile'] == it]
            print(f'color={Defs.dict_colors[it]}, len gdf_map [{len(gdf_quantile)}]')
            if (gdf_quantile.empty is not True):
                fg = f_maps.get_folium_featuregroup_color(
                    pdf=gdf_quantile, 
                    fg_name=f'{it+1} Quantile  [{i*100}%] [{len(gdf_quantile)}]',
                    fields=['GEN','BEZ','EWZ','ARS', 'EWZ', 'KFL', 'EPK', 'EPK_norm', 'quantile'],
                    aliases=['Name','Type','Pop','ARS', 'EinwohnerZahl', 'Area [Km2]', 'Density', 'Normed density', 'Quantile'],
                    fill_color=Defs.dict_colors[it]
                )
                l_fg_metadata.append(fg)
        
        print(f'l_fg_metadata:{len(l_fg_metadata)}')

        # Compute the centroid of each geometry
        gdf_map['centroid'] = gdf_map['geometry'].centroid

        # Extract latitude and longitude from the Point geometries
        gdf_map['lon'] = gdf_map['centroid'].x
        gdf_map['lat'] = gdf_map['centroid'].y

        if l_fg_metadata is not None:
            l_fg.extend(l_fg_metadata)

            gdf_map = gdf_map.sort_values(by='EPK', ascending=True)
            gdf_map['quantile'] = gdf_map['quantile'].astype('str')#.drop_duplicates().values


            print('MarketClusters')
            fg_mc = f_maps.gen_markercluster_sum_fg(gdf=gdf_map, name='Einwohnerzahl',
                                    lat='lat', lon='lon', column_sum = 'EWZ')
            if fg_mc is not None:
                l_fg.extend([fg_mc])

    if(l_coverage):
        round_dec=2
        print(f'l_coverage:{l_coverage} Km')
        #### PARSING VARIABLES ###
        radius_km = int(l_coverage)
        
        
        gdf_zensus_de = gpd.read_file('JupNB\DE_Data\VG250_GEM_WGS84.shp')
        print('Removing non-serializable columns...')
        l_cols_non_serializable = ['WSK','BEGINN']
        for col in l_cols_non_serializable:
            if col in gdf_zensus_de.columns:
                gdf_zensus_de = gdf_zensus_de.drop(col,axis=1)
        # gpd_zensus_filt = gpd_zensus[gpd_zensus['SN_L'].isin(l_bundeslaender)]




        pdf = pdf_stores[pdf_stores['store'].isin(l_stores)]
        gpd_zensus = gdf_zensus_de
        print(f'Stores total={pdf.shape[0]}')        
        
        if l_states:
            pdf = pdf[pdf['GADM_1'].isin(l_states)]
            print(f'l_states - Stores total={pdf.shape[0]}')  
                
            l_bundeslaender = [Defs.dict_bundeslaender_id[x] for x in l_states]
            print(f'  gdf_zensus_filt:{gpd_zensus.shape[0]}')
            gpd_zensus = gpd_zensus[gpd_zensus['SN_L'].isin(l_bundeslaender)]      
        if l_regions:
            pdf = pdf[pdf['GADM_2'].isin(l_regions)]
            print(f'l_regions - Stores total={pdf.shape[0]}')        

        if l_districts:
            pdf = pdf[pdf['GADM_3'].isin(l_districts)]
            print(f'l_districts - Stores total={pdf_stores_filt.shape[0]}')

        
        gdf_geom_6993 = gpd_zensus.to_crs(epsg=6933)
        gdf_geom_6993['KFL_GPD'] = round(gdf_geom_6993.geometry.area / 10**6, 2)
        gdf_geom_4326 = gpd_zensus.to_crs(epsg=4326)
        gdf_geom_6993['lat'] = gdf_geom_4326.geometry.centroid.y
        gdf_geom_6993['lon'] = gdf_geom_4326.geometry.centroid.x     
        print(f'gdf_geom_6993={gdf_geom_6993.shape[0]}')

        pdf_stores_filt= pdf
        print(f'After all filters - Stores total={pdf_stores_filt.shape[0]}')        
        l_center_points = list(zip(pdf_stores_filt['lat'], 
                                   pdf_stores_filt['lon']))
        print(l_center_points)
        # l_fg = []
        num_inside_towns, num_partly_towns = 0, 0
        sum_ewz,sum_kfl, sum_area_geom_int = 0, 0, 0
        sum_int_kfl, sum_int_ewz, sum_int_geom = 0, 0, 0

        l_gdf_circles = []
        l_gdf_merged_circles = []
        fg_point = folium.FeatureGroup(
            name=f'Center points [{len(l_center_points)}]')
        fg_circle = folium.FeatureGroup(name=f'Circles [r={radius_km} Km, \
                                        Area={round(3.1415 * radius_km**2, 2)} Km2]')
        fg_int = folium.FeatureGroup(name=f'Intersections')
        fg_inside = folium.FeatureGroup(name=f'Markers - Inside towns')
        fg_partly = folium.FeatureGroup(name=f'Markers - Partly towns')
        fg_outside = folium.FeatureGroup(name=f'Markers - Outside towns')
        fg_overlay = folium.FeatureGroup(name=f'Overlay - Summary inside')

        for i,center_point in enumerate(l_center_points):
            print(f'Processing [{i+1}/{len(l_center_points)}] {center_point}')

            geom_center_point = geometry.Point(center_point[1], center_point[0])
            # gdf_point = gpd.GeoDataFrame(geometry=[geom_center_point], crs=f'EPSG:4326')
            gjson_point = folium.Marker(location=[geom_center_point.y, geom_center_point.x], 
                                        icon=folium.Icon(color="red"),
                                        tooltip=folium.features.GeoJsonTooltip(fields=['geometry'], values=['coordinates'])
                                        )

            gjson_point.add_to(fg_point)
            print(f'Processing [{i+1}/{len(l_center_points)}] {geom_center_point}')

            ############# CIRCLE PROJECTION IN 4326 ####################
            lon = center_point[1]
            lat = center_point[0]
            # Convert the Shapely circle to a geoDataFrame
            poly_circle = f_maps.circle_around_lat_lon_point(
                lon=lon, lat=lat, radius=1000 * radius_km)
            gdf = gpd.GeoSeries([poly_circle])
            gdf_overlay = gdf.to_frame(name='geometry').set_crs(epsg=4326)
            gdf_circle_6933 = gdf_overlay.to_crs(epsg=6933)
            l_gdf_circles.append(gdf_circle_6933.iloc[0].geometry)

            # Generate the FeatureGroup and add it to the list
            # fg_circle = folium.FeatureGroup(name=f'Circle [lat={lat}, lon ={lon}, r={radius_km} Km]')
            gjson_circle = folium.GeoJson(gdf_overlay, color='red')
            gjson_circle.add_to(fg_circle)
            # l_fg_circle.append(fg_circle)

            ############# INTERSECTION ####################
            gdf_de_int = gpd.sjoin(gdf_geom_4326, gdf_overlay, 
                                how="inner", predicate="intersects") #\
                                    # .drop(l_cols_non_serializable, axis=1)
                                    # 

            gdf_de_int['KFL_GPD'] = round(gdf_geom_6993.geometry.area / 10**6, 2)
            int_kfl = gdf_de_int.KFL.sum()
            int_ewz =gdf_de_int.EWZ.sum()
            int_geom = round(gdf_de_int.KFL_GPD.sum(), 2)
            sum_int_kfl += int_kfl
            sum_int_ewz += int_ewz
            sum_int_geom += int_geom

            print(f'int_kfl={int_kfl}Km2, int_geom={int_geom}Km2, int_ewz={int_ewz}')

            gjson = f_maps.get_folium_geojson(gdf_de_int, 
                                            fields=['GEN', 'EWZ', 'KFL', 'KFL_GPD'],
                                                aliases = ['Name', 'Population', 'Area_KFL', 'Area_Geom'])
            gjson.add_to(fg_int)

            ############# OVERLAY / individual ####################

            col_perc = 'PERC_int'

            # Set the column used for NORMALIZATION (denominator)
            gdf_geom_6993['area_geom'] = round(gdf_geom_6993['geometry'].area / 10**6, 2)
            # Overlay geometry with polygon  
            gdf_overlay = gpd.overlay(gdf_geom_6993, gdf_circle_6933, how='intersection')

            # Set the column used for NORMALIZATION (numerator)
            gdf_overlay['area'] = round(gdf_overlay['geometry'].area / 10**6, 2)
            gdf_overlay[col_perc] = gdf_overlay['area'] / gdf_overlay['area_geom']
            
            
            d_columns = {
                'area_geom':{'alias' : 'area',        'is_norm': True,  'is_int':False},
                'KFL':     {'alias' : 'area_data',    'is_norm': True,  'is_int':False},
                'EWZ':     {'alias' : 'Population',   'is_norm': True,  'is_int':True}
            }
            
            gdf_overlay = f_maps.overlay_shapes(gdf_circle=gdf_overlay, 
                                                col_perc=col_perc, 
                                                d_columns=d_columns)


            # ################### Distance to point of interest ##########
            gdf = pd.DataFrame(gdf_overlay[['ARS','lat','lon','PERC_int','GEN']])
            gdf = gpd.GeoDataFrame(gdf, crs='epsg:4326', 
                                geometry=[geometry.Point(xy) for xy in zip(gdf['lon'], gdf['lat'])])
            gdf = f_maps.compute_dist_to_lat_lon(gdf, lon=geom_center_point.x, lat=geom_center_point.y, round_dec=2, units='km')

            #######################  Gemeinde Markers  ##########################
            
            gdf_inside = gdf[gdf[col_perc] == 1.0]
            num_inside_towns += gdf_inside.shape[0]
            print(f'Inside ={ gdf_inside.shape[0]}')
            fg_inside_circle = f_maps.get_markers_polygon(gdf_inside,
                                                    l_tooltip=['GEN','dist'], 
                                                    name=f'Markers inside {gdf_inside.shape[0]}', color='darkgreen')
            fg_inside_circle.add_to(fg_inside)

            gdf_partly = gdf[gdf[col_perc] != 1.0]
            num_partly_towns += gdf_partly.shape[0]
            fg_partly_circle = f_maps.get_markers_polygon(gdf_partly,
                                                    l_tooltip=['GEN','dist'], 
                                                    name=f'Markers partly {gdf_partly.shape[0]}', color='orange')
            fg_partly_circle.add_to(fg_partly)


            # gdf_outside = gdf[gdf[col_perc] != 1.0]
            
            ############# OVERLAY / merged ####################

            l_cols_percentaged = ['area_geom', 'EWZ', 'KFL']
            gdf_merge = f_maps.merge_shapes(gdf_overlay, l_col_percs=l_cols_percentaged,
                                            d_percs={'data':'KFL', 'geom':'area_geom'}, 
                                            num_dec=round_dec, is_logging=True)

            gdf_merge['num_in'] = gdf_inside.shape[0]
            gdf_merge['num_part'] = gdf_partly.shape[0]

            l_gdf_merged_circles.append(gdf_merge)
            
            gjson = f_maps.get_folium_geojson(
                gdf_merge, 
                fields=[
                    'perc_data', 
                    'KFL_int', 'KFL',
                    'perc_geom',
                    'area_geom_int', 'area_geom',
                    'EWZ_int', 'EWZ',
                    'num_in', 'num_part', 
                    ],
                aliases = [
                    'Percentage data', 
                    'Area_data intersection [Km2]', 'Area_data shape [Km2]',
                    'Percentage geometry',
                    'Area_geom intersection [Km2]', 'Area_geom shape [Km2]',
                    'Population intersection', 'Population shape',
                    '# Localities inside', 
                    '# Localities partially inside',
                    ])
            gjson.add_to(fg_overlay)
            sum_ewz += gdf_merge['EWZ_int'].sum()
            sum_kfl += gdf_merge['KFL_int'].sum()
            sum_area_geom_int += gdf_merge['area_geom_int'].sum()
            print(f'area_geom_int= {sum_area_geom_int}\n')


        l_fg_candidates = [fg_point, fg_circle, fg_int, 
              fg_overlay, #fg_overlay_all, 
                fg_inside,fg_partly,
                fg_outside
                ]
        for fg in l_fg_candidates:
            if (fg is not None):
                l_fg.append(fg)

        


    print(f'Feature Groups!')
    if l_fg: #list of feature groups is NOT empty
        print(f"l_fg:{l_fg}")
        print("Generating map!")

        fm = f_maps.get_folium_map_countries(l_fg,d_company=f_maps.read_dict_temp(file_used))

        print(f'fm:{fm}, type:{type(fm)}')
        print('Writing map')
        name_map = 'map_right'
        f_maps.write_map_temp(fm, name_map=name_map)
        map_fig = html.Iframe(srcDoc=open(f"{name_map}.txt", "r").read(),
                           width='100%',
                           height='750'
                           )

        # im = dash_table.DataTable(pdf_world.to_dict('records'), page_size=10)
        return map_fig
    else:
        return html.Iframe("Empty map!")