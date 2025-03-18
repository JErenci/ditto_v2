import datetime
import dash
import folium
import numpy as np
import pandas as pd
import plotly.express as px
from dash import callback, html, dcc, Input, Output, dash_table, no_update, State
import dash_bootstrap_components as dbc
from geopy.geocoders import Nominatim

from shapely import geometry, wkt

# from functionality_maps import f_maps
import sys
# sys.path.append('/Users/User/PycharmProjects/ditto_v2/')
# if __name__ == '__main__':
from functionality_maps import f_maps, f_gadm, f_osm
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
print(f'pdf_d1.shape[0]={pdf_d1.shape[0]}')

### PDF_STORES ###
pdf_stores = pd.read_json(paths.stores, orient='records', lines=True)
is_logging = True

d_company = f_maps.read_dict_temp(file_used)

# pdf_stores['store_name'] = pdf_stores["store"] +"_" +  pdf_stores["name"]   ## ADD NAME OF STORE
# print(f'STORES/TOTAL = {pdf_stores.shape[0]}')
# pdf_stores = pdf_stores.dropna(subset=['lat','lon'])                        ### FILTER STORES WITH NO COORDS ###
# print(f' STORES/Valid coords = {pdf_stores.shape[0]}')

# Load the saved GeoJSON file into a new GeoDataFrame
gdf_census = gpd.read_file('.\JupNB\DE_Data\VG250_GEM_WGS84.shp')

company_name = 'D1tt0'
log_messages = []

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

                options=['EWZ', 'Mountains', 'Campings', 'Climbing facilities'],
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
check_company = dcc.Checklist(
    id='checklist_company',
    options=[d_company['name']]
)
check_states = dcc.Checklist(
    id='checklist_states',
    options=['All States [DE]']
)
check_countries = dcc.Checklist(
    id='checklist_countries',
    options=['All countries']
)
check_regions = dcc.Checklist(
    id='checklist_regions',
    options=['All regions']
)
check_districts = dcc.Checklist(
    id='checklist_districts',
    options=['All districts']
)
log_window = html.Div(
    id="log_display", 
    style=dict(height='300px',overflow='scroll', whiteSpace= 'pre-wrap')
)
log_interval = dcc.Interval(id='interval_component', interval=1000, n_intervals=0)

comp_pdf_found = html.Div(id='pdf_world_found')
comp_fig = html.Div(id='fig_bottom')
comp_map = html.Div(id='map_figure_right')

layout = dbc.Container(
[
    log_interval,
    # dcc.Markdown('# This will be the content of Page Company'),
    html.Div(id='image_customer', children=''),
    dbc.Row(
        dbc.Col(html.H1("World Dashboard",
                        className='text-center text-primary',),
                width=12)
    ),

    dbc.Row([
        dbc.Col([
            check_company,      # Checkbox with company locations
            comp_text_Geo,      # Geo component separaton
            dbc.Row([
                dbc.Col([
                comp_dropCountry], width={'size': 8}), # COUNTRY
                dbc.Col([
                check_countries], width={'size': 4}
                )
            ], justify='start'),
            dbc.Row([
                dbc.Col([
                comp_dropState], width={'size': 8}), # STATE
                dbc.Col([
                check_states], width={'size': 4}
                )
            ], justify='start'),
            dbc.Row([
                dbc.Col([
                comp_dropRegion], width={'size': 8}), # REGION
                dbc.Col([
                check_regions], width={'size': 4}
                )
            ], justify='start'),
            dbc.Row([
                dbc.Col([
                comp_dropDistrict], width={'size': 8}), #DISTRICT
                dbc.Col([
                check_districts], width={'size': 4}
                )
            ], justify='start'),
            comp_dropZIP,       # ZIP

            comp_text_Sales,    # Sales component separaton
            comp_dropSales,      # Sales
            comp_text_metadata,  # Metatdata component separation
            comp_dropMetadata,   # Metadata,
            comp_text_coverage,  # Store Coverage text separator
            comp_dropCoverage,   # Store Coverage [Km]
            log_window,
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
Input(component_id='checklist_countries', component_property='value'),#All Countries
Input(component_id='checklist_states', component_property='value'),#All States
Input(component_id='checklist_regions', component_property='value'),#All Regions
Input(component_id='checklist_districts', component_property='value'),#All Districts
Input(component_id='checklist_company', component_property='value'),#Company Locations
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
def gen_map_countryX(c_countries, c_states, c_regions, c_districts, c_company, l_countries, l_states, l_regions, l_districts, l_zips, 
                     l_stores, l_metadata, l_coverage):

    print(f'country = {l_countries}')
    print(f'state =   {l_states[0:5]}')
    print(f'region =  {l_regions[0:5]}')
    print(f'district ={l_districts[0:5]}')
    print(f'zip =     {l_zips[0:5]}')
    print(f'')

    # Initialize list of feature_groups
    l_fg = []
    d_roi = {}

    category = paths.l_d_dropdown_map[0]
    #VERBOSITY
    if is_logging:
        pdf_world = gdf_world['ADMIN']
        print('pdf_world')
        print(pdf_world)
        print(f'type={type(pdf_world)}')
        print(f'l_countries={l_countries}')
        pred2 = pdf_world.isin(l_countries)
        print(f'pred2={pred2}')
        pdf = gdf_world[pred2]
        print('pdf2')
        print(pdf.head())
        pdf_countriesNo = pdf.shape[0]
        print(f'Countries found={pdf_countriesNo}')
    
    #COMPANY
    if c_company:
        add_log_message(f'Adding company={d_company['name']}')
        pdf_marker_coords = pd.DataFrame.from_dict(d_company['locations'], orient='index')

        fg_company = folium.FeatureGroup(name=d_company['name'])

        for index, row in pdf_marker_coords.iterrows():
            folium.Marker(location=[row["lat"], row["lon"]],
                          popup=row["address"],
                          tooltip=index,
                          icon=folium.features.CustomIcon(icon_image=d_company['icon'],
                                                          icon_size=(50, 50))
                          ).add_to(fg_company)
        if fg_company is not None:
            l_fg.append(fg_company)

    #COUNTRIES
    if (l_countries or c_countries):

        if c_countries:
            add_log_message(f'Selecting ALL Countries [{pdf_world.shape[0]}]')
            pdf = gdf_world
        else:
            pred2 = pdf_world.isin(l_countries)
            add_log_message(f'Changing # of countries={len(l_countries)}')
            pdf = gdf_world[pred2]

        fg_countries = f_maps.get_feature_group_countries(gdf_world=pdf,
                                                        l_countries=l_countries,
                                                        key_filter='ADMIN',
                                                        fields=paths.fields_wca,
                                                        aliases=paths.aliases_wca)
        if fg_countries is not None:
            l_fg.append(fg_countries)
    
    #STATES
    if (l_states or c_states):
        category = paths.l_d_dropdown_map[1]
        pdf_states = pdf_d1['name']  # For indexing

        if c_states:
            pdf = pdf_d1
            add_log_message(f'Selecting ALL =States={pdf_states.shape[0]}')
        else:
            pdf = pdf_d1[pdf_states.isin(l_states)]
            add_log_message(f'Changing # of States={len(l_states)}')
       
        fg_state = f_maps.get_feature_group(pdf, category)
        if fg_state is not None:
            l_fg.append(fg_state)

    #REGION
    if (l_regions or c_regions):
        category = paths.l_d_dropdown_map[2]
        if c_regions:
            pdf = pdf_d3
            add_log_message(f'Selecting all Region(s)={pdf.shape[0]}')
        else:
            add_log_message(f'Changing # of Region(s)={pdf.shape[0]}')
            pdf_regions = pdf_d2['NAME_2']  # For indexing
            pdf = pdf_d2[pdf_regions.isin(l_regions)]
        
        fg_region = f_maps.get_feature_group(pdf, category)
        if fg_region is not None:
            l_fg.append(fg_region)

    #DISTRICT
    if (l_districts or c_districts):
        category = paths.l_d_dropdown_map[3]
        if c_districts:
            pdf = pdf_d4
            add_log_message(f'Selecting all Districts={pdf.shape[0]}')
        else:
            pdf_districts = pdf_d3['NAME_3']  # For indexing
            pdf = pdf_d3[pdf_districts.isin(l_districts)]
            add_log_message(f'Changing # of District(s)={pdf.shape[0]}')

        fg_district = f_maps.get_feature_group(pdf, category)
        if fg_district is not None:
            l_fg.append(fg_district)

    #ZIP
    if(l_zips):
        category = paths.l_d_dropdown_map[4]
        pdf_zips = pdf_d4['postcode']  # For indexing
        pdf = pdf_d4[pdf_zips.isin(l_zips)]

        add_log_message(f'Changing # of ZIP(s)={pdf.shape[0]}')
        fg_zip = f_maps.get_feature_group(pdf, category)
        if fg_zip is not None:
            l_fg.append(fg_zip)

    #STORES
    if (l_stores):
        pdf_stores = pd.read_json(paths.stores, orient='records', lines=True)
        pdf = pdf_stores[pdf_stores['store'].isin(l_stores)]

        if l_states:
            pdf = pdf[pdf['GADM_1'].isin(l_states)]
        if l_regions:
            pdf = pdf[pdf['GADM_2'].isin(l_regions)]
        if l_districts:
            pdf = pdf[pdf['GADM_3'].isin(l_districts)]

        add_log_message(f'[STORES] selected [{l_stores}]')
        add_log_message(f'Total # of Store(s)={pdf_stores.shape[0]}')
        add_log_message(f'Changing # of Store(s)={pdf.shape[0]}')
        l_fg_stores = f_gadm.get_fg_store(pdf, l_stores)
        if l_fg_stores is not None:
            l_fg.extend(l_fg_stores)

    #POPULATION
    if (l_metadata):
        add_log_message(f'l_metadata [{l_metadata}]')
        if 'EWZ' in l_metadata:
            add_log_message(f'[POPULATION]')
            gdf_census = gpd.read_file('.\JupNB\DE_Data\VG250_GEM_WGS84.shp')
            l_bundeslaender = [Defs.dict_bundeslaender_id[x] for x in l_states]
            gdf_census = gdf_census[gdf_census['SN_L'].isin(l_bundeslaender)]   #### FILTERING CENSUS TO RoI ####
            add_log_message(f'[POPULATION] #Regions [{gdf_census.shape[0]}]')
            l_quantiles = [0, 0.1, 0.5, 0.9, 1.0]   # Define custom quantile boundaries
            col_quant = 'EPK'
            col_out='quantile'
            round_dec = 3

            gdf_census = f_maps.enrich_census(gdf_census)
            
            l_quant_ranges = f_maps.compute_quantile_ranges(gdf=gdf_census, col_quant=col_quant, l_quantiles=l_quantiles, 
                                            round_dec=round_dec)  
            gdf_census = f_maps.add_quantiles_column(gdf=gdf_census, col_quant=col_quant, l_quantiles=l_quantiles, 
                                            round_dec=round_dec, is_logging=is_logging)
            l_fg_census_quant = f_maps.get_fg_quant(gdf=gdf_census, col_quant=col_quant, l_quantiles=l_quantiles, 
                                                    l_quant_ranges=l_quant_ranges, is_logging=is_logging)
            
            if l_fg_census_quant is not None:
                l_fg.extend(l_fg_census_quant)

                gdf_census = gdf_census.sort_values(by=col_quant, ascending=True)
                gdf_census[col_out] = gdf_census[col_out].astype('str')
        if 'Mountains' in l_metadata:
            add_log_message(f'[MOUNTAINS]')
            gdf_census = gpd.read_file('.\JupNB\DE_Data\VG250_GEM_WGS84.shp')
            add_log_message(f'[MOUNTAINS] #Regions [{gdf_census.shape[0]}]')
            l_bundeslaender = [Defs.dict_bundeslaender_id[x] for x in l_states]
            gdf_census = gdf_census[gdf_census['SN_L'].isin(l_bundeslaender)]   #### FILTERING CENSUS TO RoI ####
            
            add_log_message(f'[MOUNTAINS] #Regions [{gdf_census.shape[0]}], l_bundeslaender={l_states}')
            gdf_cm = gdf_census.groupby('SN_L').agg( \
            {'EWZ':'sum', 
            'KFL' : 'sum',
            'geometry': lambda x: x.geometry.union_all(),
            }).set_geometry("geometry").set_crs(4326).reset_index()
            print(f'gdf_head()={gdf_cm.head()}')

            lon_min, lat_min, lon_max, lat_max = gdf_census.union_all().bounds
            add_log_message(f'lon_min, lat_min, lon_max, lat_max = {lon_min, lat_min, lon_max, lat_max}')

            mountains_min_elev = 2500
            gdf_mountains_bound = f_osm.gen_pdf_osm(lat_min, lon_min, lat_max, lon_max, args='natural=peak',
                           l_keys_to_extract = ['name','ele'],
                           l_values_default = ['', 'nan'],
                           d_key_replace = {'ele' : {',' : '.', 'm':''}},
                           d_parse_types = {'lat' : float, 'lon': float, 'ele' : float},
                           l_drop_na=['lat','lon','ele']
                           )
            # Drop columns that are not needed
            gdf_mountains_bound = gdf_mountains_bound.drop(['nodes','tags'], axis=1)
            # Intersect with GDF with Region of Interest
            gdf_mountains = gpd.sjoin(gdf_mountains_bound.to_crs(epsg=4326),
                                            gdf_cm[['geometry']].to_crs(epsg=4326), 
                                            how="inner", predicate="intersects")
            add_log_message(f'[MOUNTAINS] Inside geometry= {gdf_mountains.shape[0]}')

            # # Filter for elevation
            gdf_mountains = gdf_mountains[gdf_mountains['ele']>=mountains_min_elev]
            add_log_message(f'[MOUNTAINS] Above min Elev({mountains_min_elev})= {gdf_mountains.shape[0]}')

            if gdf_mountains.shape[0] > 0:
                fg_mountains = folium.FeatureGroup(name=f'[{gdf_mountains.shape[0]}] Mountains min_elev>{mountains_min_elev}m', show=False)
                for index, row in gdf_mountains.iterrows():
                    folium.Marker(location=[row["lat"], row["lon"]],
                                    popup=f'{row["name"]} \r\n {row["ele"]}m',
                                    tooltip=row["name"],
                                    icon=folium.features.CustomIcon(icon_image='assets/Geo/mountain.png',
                                                                    icon_size=(20, 20))
                                    ).add_to(fg_mountains)
                l_fg.extend([fg_mountains])

            #     gdf_census = gdf_census.sort_values(by=col_quant, ascending=True)
            #     gdf_census[col_out] = gdf_census[col_out].astype('str')
            # d_poi['mountains'] = fg_mountains
            # l_fg_poi += [fg_mountains]

        

    #COVERAGE
    if(l_coverage):
        path_census_D2 = './assets/Geo/Germany/D1_Deutschland_census.json'
        radius_km = int(l_coverage)
        add_log_message(f'Radius [{radius_km} Km]')
        gdf_census_merged = gpd.read_file(path_census_D2)
        gdf_census = gpd.read_file('.\JupNB\DE_Data\VG250_GEM_WGS84.shp')
        round_dec=2
        maps_roi_is_roi = True

        l_fg_roi = []

        l_bundeslaender = [Defs.dict_bundeslaender_id[x] for x in l_states]
        gdf_census = gdf_census[gdf_census['SN_L'].isin(l_bundeslaender)]   #### FILTERING CENSUS TO RoI ####
        add_log_message(f' CENSUS inside RoI: [{gdf_census.shape[0]}]')
        gdf_census = f_maps.enrich_census(gdf_census)

        pdf_stores = pdf_stores[pdf_stores['store'].isin(l_stores)]                 ### FILTER STORES WITH IN l_stores ###
        add_log_message(f' STORES/Selected [{l_stores}]= {pdf_stores.shape[0]}')
        pdf_stores['geometry'] = pdf_stores['point'].apply(wkt.loads)                  ### CONVERTING POINT COL TO GEOM ###
        gdf_stores = gpd.GeoDataFrame(pdf_stores).set_geometry('geometry')
        gdf_stores = gdf_stores.set_crs(4326)

   
        maps_roi_is_roi = True
        maps_roi_is_towns = True
        maps_roi_is_stores = True
        maps_roi_is_circles = True

        if maps_roi_is_roi:
            fg_roi_pop = round(gdf_census_merged.EWZ.sum() / 10**6, round_dec)
            fg_roi_area = gdf_census_merged.area_geom.sum()
            fg_legend = f'[{len(l_states)}] GEOM/REGIONS [Sum(Pop):{fg_roi_pop}M, Sum(Area):{fg_roi_area}Km2]'
            add_log_message(f'Shape={gdf_census_merged.shape[0]}')

            fg_roi_region = folium.FeatureGroup(name=fg_legend)
            gjson_store = f_maps.get_folium_geojson( gdf_census_merged, 
                                            fields=['Bundesland', 'EWZ', 'area_geom'],
                                            aliases = ['Bundesland', 'Pop', 'Area_geom[Km2]']
                                            )
            gjson_store.add_to(fg_roi_region)
            l_fg_roi += [fg_roi_region] 

        if maps_roi_is_towns:
            num_towns = gdf_census.shape[0]
            fg_roi_pop = round(gdf_census.EWZ.sum() / 10**6, round_dec)
            fg_roi_area = gdf_census.to_crs(6933).area_geom.sum()

            legend_roi_town = f'[{num_towns}] GEOM/TOWNS'


            fg_roi_town = folium.FeatureGroup(name=legend_roi_town, show=False)
            gjson_store = f_maps.get_folium_geojson(gdf_census.to_crs(4326), 
                                            fields=['GEN', 'EWZ', 'area_geom', 'KFL'],
                                            aliases = ['Town', 'Pop', 'Area_geom[km2]', 'Area_dbms[Km2]'],
                                            )
            gjson_store.add_to(fg_roi_town)
            l_fg_roi += [fg_roi_town]

        if maps_roi_is_stores:
            add_log_message(f'  # Stores chain selected:{gdf_stores.shape[0]}')
            fg_mk_storeall = f_gadm.get_fg_store(gdf_stores, l_stores)
            l_fg_roi += fg_mk_storeall

        if maps_roi_is_circles:
            add_log_message(f'Shape Circles RoI:{gdf_stores.shape[0]}')
            gdf_circles_stores_all = f_maps.get_gdf_circle(df=gdf_stores, radius_km= radius_km).drop(['point'], axis=1)
            fg_circ_store = f_maps.get_fg_gjson(gdf=gdf_circles_stores_all, fg_name=f'Circles [r={radius_km}Km]',
                                                fields=['store','name', 'address'],
                                                aliases = ['store', 'name', 'address'])
            l_fg_roi +=  [fg_circ_store]


        ### ADDING FG into GroupedLayerControl
        fglc_geom = folium.plugins.GroupedLayerControl(
            groups={'Region of Interest [RoI]': l_fg_roi},
            exclusive_groups=False,
            collapsed=False,
        )
        d_roi = {
            'l_fg' : l_fg_roi,
            'fglc' : fglc_geom
        }


    fm = folium.Map()
    print(f'Feature Groups!')
    if l_fg: #list of feature groups is NOT empty
        print(f"l_fg:{l_fg}")
        print("Generating map!")

        fm = f_maps.get_folium_map_countries(l_fg)


        # 3.1. RoI (Region, Towns, Stores) 
        # print(f'# 3.1. RoI (Region, Towns, Stores) ')
        if bool(d_roi):  ## CHeck that the dict is NOT empty
            for i,fg in enumerate(d_roi['l_fg']):
                print(f'  Adding RoI [{i+1}/{len(d_roi["l_fg"])}]')
                fg.add_to(fm)
            d_roi['fglc'].add_to(fm)


        print(f'fm:{fm}, type:{type(fm)}')

    print('Writing map')
    name_map = 'map_right'
    f_maps.write_map_temp(fm, name_map=name_map)
    map_fig = html.Iframe(srcDoc=open(f"{name_map}.txt", "r").read(),
                        width='100%',
                        height='750'
                        )

    add_log_message(f'LAYERS [{len(l_fg)}] Time:[{datetime.datetime.now()}]')
    add_log_message('')
    return map_fig

@callback(
    Output("log_display", "children"),
    Input("interval_component", "n_intervals")
)
def update_log_display(n_intervals):
    log_texts = "\n".join(log_messages)
    span_logs = html.Span(f"{log_texts} \n[Last update: {datetime.datetime.now()}]")
    return span_logs

def add_log_message(message):
    log_messages.append(message)