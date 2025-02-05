import dash
import folium
import numpy as np
import pandas as pd
import plotly.express as px
from dash import callback, html, dcc, Input, Output, dash_table, no_update
import dash_bootstrap_components as dbc
from geopy.geocoders import Nominatim

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
prevent_initial_call=True
)
def gen_map_countryX(l_countries, l_states, l_regions, l_districts, l_zips, l_stores, l_metadata):
    dropdown_value = paths.l_d_dropdown_map
    fig = None

    print(f'gen_map_countryX')
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

        print(f'gdf_zensus_de:{gdf_zensus_de.shape}')
        gdf_map = gdf_zensus_de[gdf_zensus_de['SN_L'].isin(l_bundeslaender)]
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
                    fields=['GEN','BEZ','EWZ','ARS', 'EWZ', 'EPK', 'EPK_norm', 'quantile'],
                    aliases=['Name','Type','Pop','ARS', 'EinwohnerZahl', 'Density', 'Normed density', 'Quantile'],
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