import dash
import folium
import pandas as pd
from dash import callback, html, dcc, Input, Output, dash_table, no_update
import dash_bootstrap_components as dbc
from geopy.geocoders import Nominatim

# from functionality_maps import Maps
import sys
sys.path.append('/Users/User/PycharmProjects/ditto_v2/')
from functionality_maps import Maps
from functionality_maps import paths
# import Maps
# C:\Users\User\PycharmProjects\ditto_v2
# sys.path.insert(1, '/functionality_maps')
# .Maps. import load_gdf_from_csv, write_map_temp, get_folium_map_countries, get_feature_group_countries

dash.register_page(__name__)

path_map_empty = 'assets/Geo/Map_empty.html'
path_wca = 'assets/Geo/world_country_area.csv'
fields_wca = ['ADMIN', 'ISO_A3', 'Area_total_km2']
aliases_wca = ['Code', 'Country', 'Area [km\u00b2]']

gdf_world = Maps.load_gdf_from_csv(path=paths.path_wca)
pdf_d1 = Maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[1]])
pdf_d2 = Maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[2]])
pdf_d3 = Maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[3]])
pdf_d4 = Maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[4]])
pdf_zips = pdf_d4['postcode']  # For indexing

d_company = 'D1tt0'

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
comp_pdf_found = html.Div(id='pdf_world_found')
comp_map = html.Div(id='map_figure_right')

# layout = dbc.Container(
layout = dbc.Container(
    [
        # dcc.Markdown('# This will be the content of Page Company'),
        html.Div(id='image_customer', children=''),
        dbc.Row(
            dbc.Col(html.H1("Stock Market Dashboard",
                            className='text-center text-primary',),
                    width=12)
        ),

        dbc.Row([
            dbc.Col([
                comp_dropCountry,   # COUNTRY
                comp_dropState,     # STATE
                comp_dropRegion,    # REGION
                comp_dropDistrict,  # DISTRICT
                comp_dropZIP,       # ZIP
            ], width={'size': 5}),
            dbc.Col([
                comp_pdf_found,     # MAP
                comp_map            # MAP
            ], width={'size': 7}),
        ], justify='start'),  # Horizontal:start,center,end,between,around
    ],
    # fluid=True,     # Stretch to use all screen
)

@callback(
    # Output(component_id='pdf_world_found', component_property='children'),
    Output(component_id='map_figure_right', component_property='children'),
    Input(component_id='dropdown_country_filter0', component_property='value'),#COUNTRY
    Input(component_id='dropdown_country_filter1', component_property='value'),#STATE
    Input(component_id='dropdown_country_filter2', component_property='value'),#REGION
    Input(component_id='dropdown_country_filter3', component_property='value'),#DISTRICT
    Input(component_id='dropdown_country_filter4', component_property='value'),#ZIP
    prevent_initial_call=True
)
def gen_map_countryX(l_countries, l_states, l_regions, l_districts, l_zips):
    dropdown_value = paths.l_d_dropdown_map

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
        fg_countries = Maps.get_feature_group_countries(gdf_world=pdf,
                                                        l_countries=l_countries,
                                                        key_filter='ADMIN',
                                                        fields=paths.fields_wca,
                                                        aliases=paths.aliases_wca)
        if fg_countries is not None:
            l_fg.append(fg_countries)
    print(308)
    #STATES
    if l_states:
        category = paths.l_d_dropdown_map[1]
        pdf_states = pdf_d1['name']  # For indexing
        pdf = pdf_d1[pdf_states.isin(l_states)]

        print(f'States found={pdf.shape[0]}')
        fg_state = Maps.get_feature_group(pdf, category)
        if fg_state is not None:
            l_fg.append(fg_state)

    #REGION
    if l_regions:
        category = paths.l_d_dropdown_map[2]
        pdf_regions = pdf_d2['NAME_2']  # For indexing
        pdf = pdf_d2[pdf_regions.isin(l_regions)]
        print(f'Regions found={pdf.shape[0]}')
        fg_region = Maps.get_feature_group(pdf, category)
        if fg_region is not None:
            l_fg.append(fg_region)

    #DISTRICT
    if l_districts:
        category = paths.l_d_dropdown_map[3]
        pdf_districts = pdf_d3['NAME_3']  # For indexing
        pdf = pdf_d3[pdf_districts.isin(l_districts)]
        print(f'Districts found={pdf.shape[0]}')
        fg_district = Maps.get_feature_group(pdf, category)
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
        fg_zip = Maps.get_feature_group(pdf, category)
        if fg_zip is not None:
            l_fg.append(fg_zip)

    if l_fg: #list of feature groups is NOT empty
        print(f"l_fg:{l_fg}")
        print("Generating map!")

        # company = request.authorization['username']
        # print(f'company: {company}')
        # # d_company = Defs.company[company]
        # try:
        #     path = f'data_loaded_{company}.json'
        #     print(f'path={path}')
        #     # d_company = json.loads(path)
        #     d_company = Maps.read_dict_temp(path)
        #     print(f'd_company: {d_company}')
        # except Exception as ex:
        #     print(ex)

        company = Maps.try_read_dict_temp()[0]

        fm = Maps.get_folium_map_countries(l_fg,
                                           d_company=Maps.read_dict_temp(f'data_loaded.json')
                                           )
        # fm = folium.Map()

        print(f'fm:{fm}, type:{type(fm)}')
        print(270)
        name_map = 'map_right'
        Maps.write_map_temp(fm, name_map=name_map)
        map_fig = html.Iframe(srcDoc=open(f"{name_map}.txt", "r").read(),
                           width='100%',
                           height='750'
                           )

        # im = dash_table.DataTable(pdf_world.to_dict('records'), page_size=10)
        return map_fig
    else:
        return html.Iframe("Empty map!")















# # import dash
# # import folium
# # import pandas as pd
# # from dash import callback, html, dcc, Input, Output, dash_table, no_update
# # import dash_bootstrap_components as dbc
# # from geopy.geocoders import Nominatim
# #
# # # from functionality_maps import Maps
# # import sys
# # sys.path.append('/Users/User/PycharmProjects/ditto_v2/')
# # from functionality_maps import Maps
# # from functionality_maps import paths
# # # import Maps
# # # C:\Users\User\PycharmProjects\ditto_v2
# # # sys.path.insert(1, '/functionality_maps')
# # # .Maps. import load_gdf_from_csv, write_map_temp, get_folium_map_countries, get_feature_group_countries
# #
# # dash.register_page(__name__)
# #
# # path_map_empty = 'assets/Geo/Map_empty.html'
# # path_wca = 'assets/Geo/world_country_area.csv'
# # fields_wca = ['ADMIN', 'ISO_A3', 'Area_total_km2']
# # aliases_wca = ['Code', 'Country', 'Area [km\u00b2]']
# #
# # gdf_world = Maps.load_gdf_from_csv(path=paths.path_wca)
# # pdf_d1 = Maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[1]])
# # pdf_d2 = Maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[2]])
# # pdf_d3 = Maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[3]])
# # pdf_d4 = Maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[4]])
# # pdf_zips = pdf_d4['postcode']  # For indexing
# #
# # d_company = 'D1tt0'
# #
# # comp_dropCountry = dcc.Dropdown(
# #                     id='dropdown_country_filter0',
# #                     options=gdf_world.ADMIN.unique(),
# #                     value=[],
# #                     multi=True,
# #                     searchable=True,
# #                     persistence=False,
# #                     persistence_type='memory',  # session
# #                     placeholder=f"Select {paths.l_d_dropdown_map[0]}",
# #                 )
# # comp_dropState = dcc.Dropdown(
# #                     id='dropdown_country_filter1',
# #                     options=pdf_d1['name'].unique(),
# #                     value=[],
# #                     multi=True,
# #                     searchable=True,
# #                     persistence=False,
# #                     persistence_type='memory',  # session
# #                     placeholder=f"Select {paths.l_d_dropdown_map[1]}(s)",
# #                 )
# # comp_dropRegion = dcc.Dropdown(
# #                     id='dropdown_country_filter2',
# #                     options=pdf_d2['NAME_2'].unique(),
# #                     value=[],
# #                     multi=True,
# #                     searchable=True,
# #                     persistence=False,
# #                     persistence_type='memory',  # session
# #                     placeholder=f"Select {paths.l_d_dropdown_map[2]}(s)",
# #                 )
# # comp_dropDistrict = dcc.Dropdown(
# #                     id='dropdown_country_filter3',
# #                     options=pdf_d3['NAME_3'].unique(),
# #                     value=[],
# #                     multi=True,
# #                     searchable=True,
# #                     persistence=False,
# #                     persistence_type='memory',  # session
# #                     placeholder=f"Select {paths.l_d_dropdown_map[3]}(s)",
# #                 )
# # comp_dropZIP = dcc.Dropdown(
# #                     id='dropdown_country_filter4',
# #                     options=pdf_d4['postcode'].unique(),
# #                     value=[],
# #                     multi=True,
# #                     searchable=True,
# #                     persistence=False,
# #                     persistence_type='memory',  # session
# #                     placeholder=f"Select {paths.l_d_dropdown_map[4]}(s)",
# #                 )
# # comp_pdf_found = html.Div(id='pdf_world_found')
# # comp_map = html.Div(id='map_figure_right')
# #
# # # layout = dbc.Container(
# # layout = dbc.Container(
# #     [
# #         # dcc.Markdown('# This will be the content of Page Company'),
# #         html.Div(id='image_customer', children=''),
# #         dbc.Row(
# #             dbc.Col(html.H1("Customer map",
# #                             className='text-center text-primary',),
# #                     width=12)
# #         ),
# #
# #         dbc.Row([
# #             dbc.Col([
# #                 comp_dropCountry,   # COUNTRY
# #                 comp_dropState,     # STATE
# #                 comp_dropRegion,    # REGION
# #                 comp_dropDistrict,  # DISTRICT
# #                 comp_dropZIP,       # ZIP
# #             ], width={'size': 5}),
# #             dbc.Col([
# #                 comp_pdf_found,     # MAP
# #                 comp_map            # MAP
# #             ], width={'size': 7}),
# #         ], justify='start'),  # Horizontal:start,center,end,between,around
# #     ],
# #     fluid=True,     # Stretch to use all screen
# # )
# #
# # # @callback(
# # #     # Output(component_id='pdf_world_found', component_property='children'),
# # #     Output(component_id='map_figure_right', component_property='children'),
# # #     Input(component_id='dropdown_country_filter0', component_property='value'),#COUNTRY
# # #     Input(component_id='dropdown_country_filter1', component_property='value'),#STATE
# # #     Input(component_id='dropdown_country_filter2', component_property='value'),#REGION
# # #     Input(component_id='dropdown_country_filter3', component_property='value'),#DISTRICT
# # #     Input(component_id='dropdown_country_filter4', component_property='value'),#ZIP
# # #     prevent_initial_call=True
# # # )
# # # def gen_map_countryX(l_countries, l_states, l_regions, l_districts, l_zips):
# # #     dropdown_value = paths.l_d_dropdown_map
# # #
# # #     print(f'gen_map_countryX')
# # #     print(f'')
# # #
# # #     print(f'dropdown_value:{dropdown_value}')
# # #     print(f'')
# # #
# # #     print(f'country = {l_countries}')
# # #     print(f'state =   {l_states[0:5]}')
# # #     print(f'region =  {l_regions[0:5]}')
# # #     print(f'district ={l_districts[0:5]}')
# # #     print(f'zip =     {l_zips[0:5]}')
# # #     print(f'')
# # #
# # #     # Initialize list of feature_groups
# # #     l_fg = []
# # #
# # #     #COUNTRY
# # #     category = paths.l_d_dropdown_map[0]
# # #     print(f'l_countries={l_countries}')
# # #
# # #     print('gdf_world')
# # #     print(gdf_world)
# # #     print(gdf_world.columns.to_list())
# # #
# # #     pdf_world = gdf_world['ADMIN']
# # #     print('pdf_world')
# # #     print(pdf_world)
# # #     print(f'type={type(pdf_world)}')
# # #     # print(pdf_world.columns.to_list())
# # #
# # #     pred1 = pdf_world.isin([l_countries])
# # #     print(f'pred1={pred1}')
# # #     pdf1 = gdf_world[pred1]
# # #     print('pdf1')
# # #     print(pdf1.shape)
# # #     print(f'Countries found={pdf1.shape[0]}')
# # #
# # #     print(f'l_countries={l_countries}')
# # #     pred2 = pdf_world.isin(l_countries)
# # #     print(f'pred2={pred2}')
# # #     pdf = gdf_world[pred2]
# # #     print('pdf2')
# # #     print(pdf.head())
# # #     pdf_countriesNo = pdf.shape[0]
# # #     print(f'Countries found={pdf_countriesNo}')
# # #     if l_countries:
# # #         fg_countries = Maps.get_feature_group_countries(gdf_world=pdf,
# # #                                                         l_countries=l_countries,
# # #                                                         key_filter='ADMIN',
# # #                                                         fields=paths.fields_wca,
# # #                                                         aliases=paths.aliases_wca)
# # #         if fg_countries is not None:
# # #             l_fg.append(fg_countries)
# # #     print(308)
# # #     #STATES
# # #     if l_states:
# # #         category = paths.l_d_dropdown_map[1]
# # #         pdf_states = pdf_d1['name']  # For indexing
# # #         pdf = pdf_d1[pdf_states.isin(l_states)]
# # #
# # #         print(f'States found={pdf.shape[0]}')
# # #         fg_state = Maps.get_feature_group(pdf, category)
# # #         if fg_state is not None:
# # #             l_fg.append(fg_state)
# # #
# # #     #REGION
# # #     if l_regions:
# # #         category = paths.l_d_dropdown_map[2]
# # #         pdf_regions = pdf_d2['NAME_2']  # For indexing
# # #         pdf = pdf_d2[pdf_regions.isin(l_regions)]
# # #         print(f'Regions found={pdf.shape[0]}')
# # #         fg_region = Maps.get_feature_group(pdf, category)
# # #         if fg_region is not None:
# # #             l_fg.append(fg_region)
# # #
# # #     #DISTRICT
# # #     if l_districts:
# # #         category = paths.l_d_dropdown_map[3]
# # #         pdf_districts = pdf_d3['NAME_3']  # For indexing
# # #         pdf = pdf_d3[pdf_districts.isin(l_districts)]
# # #         print(f'Districts found={pdf.shape[0]}')
# # #         fg_district = Maps.get_feature_group(pdf, category)
# # #         if fg_district is not None:
# # #             l_fg.append(fg_district)
# # #
# # #     #         l_fg.append(fg)
# # #     #         print(l_fg)
# # #
# # #     #ZIP
# # #     if(l_zips):
# # #         category = paths.l_d_dropdown_map[4]
# # #         pdf_zips = pdf_d4['postcode']  # For indexing
# # #         pdf = pdf_d4[pdf_zips.isin(l_zips)]
# # #         print(f'l_zips:{l_zips}')
# # #         print(f'Zips found={pdf.shape[0]}')
# # #         fg_zip = Maps.get_feature_group(pdf, category)
# # #         if fg_zip is not None:
# # #             l_fg.append(fg_zip)
# # #
# # #     if l_fg: #list of feature groups is NOT empty
# # #         print(f"l_fg:{l_fg}")
# # #         print("Generating map!")
# # #
# # #         # company = request.authorization['username']
# # #         # print(f'company: {company}')
# # #         # # d_company = Defs.company[company]
# # #         # try:
# # #         #     path = f'data_loaded_{company}.json'
# # #         #     print(f'path={path}')
# # #         #     # d_company = json.loads(path)
# # #         #     d_company = Maps.read_dict_temp(path)
# # #         #     print(f'd_company: {d_company}')
# # #         # except Exception as ex:
# # #         #     print(ex)
# # #
# # #         # company = Maps.try_read_dict_temp()[0]
# # #
# # #         fm = Maps.get_folium_map_countries(l_fg,
# # #                                            d_company=Maps.read_dict_temp(f'data_loaded_baumgartner.json')
# # #                                            )
# # #         # fm = folium.Map()
# # #
# # #         print(f'fm:{fm}, type:{type(fm)}')
# # #         print(270)
# # #         name_map = 'map_right'
# # #         Maps.write_map_temp(fm, name_map=name_map)
# # #         map_fig = html.Iframe(srcDoc=open(f"{name_map}.txt", "r").read(),
# # #                            width='100%',
# # #                            height='750'
# # #                            )
# # #
# # #         # im = dash_table.DataTable(pdf_world.to_dict('records'), page_size=10)
# # #         return map_fig
# # #     else:
# # #         return html.Iframe("Empty map!")
# #
# # @callback(
# #     Output(component_id='map_figure_right', component_property='children'),
# #     Input(component_id='dropdown_country_filter0', component_property='value'),  # COUNTRY
# # )
# # def cell_clicked(derived_virtual_selected_rows):
# #     print(1)
# #     # print(f'active_cell:{active_cell}')
# #     # print(f'derived_virtual_selected_rows:{derived_virtual_selected_rows}')
# #     #
# #     # if active_cell is None:
# #     #     return no_update
# #     #
# #     # row = active_cell["row"]
# #     # print(f"row id: {row}")
# #
# #     if derived_virtual_selected_rows is None:
# #         derived_virtual_selected_rows = []
# #
# #     df = pd.read_csv('''C:\\Users\\User\\PycharmProjects\\ditto_v2\\assets\\Sample_csv_semicolon_separated.csv''')
# #     customer_id = df.at[row, "Nr."]
# #     person = df.at[row, "Vorname"] + " " + df.at[row, 'Nachname']
# #     address = df.at[row, "Straße"] + " " + df.at[row, "Hausnummer"]
# #     city = df.at[row, "Stadt"]
# #     country = 'Germany'
# #
# #     img_customer = html.Img(src='''C:\\Users\\User\\PycharmProjects\\ditto_v2\\assets\\anna_smith.jpg''')
# #     # img_customer = html.Img(src=f'/assets/{company}/Customers/{customer_id}.jpg',
# #     #                         title=f'{person}',
# #     #                         width='100%'
# #     #                         )
# #
# #     # Initialize list of feature_groups
# #     l_fg = []
# #
# #     l_countries = country
# #
# #     gdf_world = Maps.load_gdf_from_csv(path=path_wca)
# #     pdf_world = gdf_world['ADMIN']
# #     # print(f'pdf_world:{pdf_world}')
# #     arg = pdf_world.isin([l_countries])
# #     # print(f'arg:{arg}')
# #     pdf = gdf_world[pdf_world.isin([l_countries])]
# #
# #     # print(f'pdf: {pdf}')
# #     if l_countries:
# #         # print(f'l_countries:{l_countries}')
# #
# #         fg_countries = Maps.get_feature_group_countries(gdf_world=pdf,
# #                                                         l_countries=[l_countries],
# #                                                         key_filter='ADMIN',
# #                                                         fields=fields_wca,
# #                                                         aliases=aliases_wca)
# #
# #         l_fg.append(fg_countries)
# #
# #         fm = Maps.get_folium_map_countries(l_fg,
# #                                            d_company=d_company)
# #
# #         # if derived_virtual_selected_rows is not None:
# #         #     print(2)
# #         #     fg_images_customers = folium.FeatureGroup(name='images_customers')
# #         #     for row in derived_virtual_selected_rows:
# #         #         customer_id = df.at[row, "Nr."]
# #         #         person = df.at[row, "Vorname"] + " " + df.at[row, 'Nachname']
# #         #         address = df.at[row, "Straße"] + " " + df.at[row, "Hausnummer"]
# #         #         city = df.at[row, "Stadt"]
# #         #         country = 'Germany'
# #         #
# #         #         print(f'address:{address}')
# #         #         print(f'city:{city}')
# #         #         print(f'country:{country}')
# #         #         print(f'person:{person}')
# #         #
# #         #         locator = Nominatim(user_agent="myGeocoder")
# #         #         location = locator.geocode(f"{address}, {city}, {country}")
# #         #
# #         #         print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
# #         #
# #         #         f_marker = folium.Marker(location=[location.latitude, location.longitude],
# #         #                                  popup=address,
# #         #                                  tooltip=person,
# #         #                                  icon=folium.features.CustomIcon(
# #         #                                      icon_image='''C:\\Users\\User\\PycharmProjects\\ditto_v2\\assets\\icon_transparent.png''',
# #         #                                      icon_size=(25, 25))
# #         #                                  )
# #         #         print(f"Added {person} to feature_group!")
# #         #         print()
# #         #         fm.add_child(f_marker)
# #         #         # fg_images_customers.add_child(f_marker)
# #         #     # fm.add_child(fg_images_customers)
# #
# #         name_map = 'map_customer'
# #         Maps.write_map_temp(fm, name_map=name_map)
# #         map_customer = html.Iframe(srcDoc=open(f"{name_map}.txt", "r").read(),
# #                                    width='100%',
# #                                    height='520')
# #         return [img_customer, map_customer]
# #
# #     else:
# #         return [html.Iframe("Empty customer!"), html.Iframe("Empty map!")]
#
# import dash
# import folium
# import pandas as pd
# from dash import callback, html, dcc, Input, Output, dash_table, no_update
# import dash_bootstrap_components as dbc
# from geopy.geocoders import Nominatim
#
# # from functionality_maps import Maps
# import sys
# sys.path.append('/Users/User/PycharmProjects/ditto_v2/')
# from functionality_maps import Maps
# from functionality_maps import paths
# # import Maps
# # C:\Users\User\PycharmProjects\ditto_v2
# # sys.path.insert(1, '/functionality_maps')
# # .Maps. import load_gdf_from_csv, write_map_temp, get_folium_map_countries, get_feature_group_countries
#
# dash.register_page(__name__)
#
# path_map_empty = 'assets/Geo/Map_empty.html'
# path_wca = 'assets/Geo/world_country_area.csv'
# fields_wca = ['ADMIN', 'ISO_A3', 'Area_total_km2']
# aliases_wca = ['Code', 'Country', 'Area [km\u00b2]']
#
# gdf_world = Maps.load_gdf_from_csv(path=paths.path_wca)
# pdf_d1 = Maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[1]])
# pdf_d2 = Maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[2]])
# pdf_d3 = Maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[3]])
# pdf_d4 = Maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[4]])
# pdf_zips = pdf_d4['postcode']  # For indexing
#
# d_company = 'D1tt0'
#
# comp_dropCountry = dcc.Dropdown(
#                     id='dropdown_country_filter0',
#                     options=gdf_world.ADMIN.unique(),
#                     value=[],
#                     multi=True,
#                     searchable=True,
#                     persistence=False,
#                     persistence_type='memory',  # session
#                     placeholder=f"Select {paths.l_d_dropdown_map[0]}",
#                 )
# comp_dropState = dcc.Dropdown(
#                     id='dropdown_country_filter1',
#                     options=pdf_d1['name'].unique(),
#                     value=[],
#                     multi=True,
#                     searchable=True,
#                     persistence=False,
#                     persistence_type='memory',  # session
#                     placeholder=f"Select {paths.l_d_dropdown_map[1]}(s)",
#                 )
# comp_dropRegion = dcc.Dropdown(
#                     id='dropdown_country_filter2',
#                     options=pdf_d2['NAME_2'].unique(),
#                     value=[],
#                     multi=True,
#                     searchable=True,
#                     persistence=False,
#                     persistence_type='memory',  # session
#                     placeholder=f"Select {paths.l_d_dropdown_map[2]}(s)",
#                 )
# comp_dropDistrict = dcc.Dropdown(
#                     id='dropdown_country_filter3',
#                     options=pdf_d3['NAME_3'].unique(),
#                     value=[],
#                     multi=True,
#                     searchable=True,
#                     persistence=False,
#                     persistence_type='memory',  # session
#                     placeholder=f"Select {paths.l_d_dropdown_map[3]}(s)",
#                 )
# comp_dropZIP = dcc.Dropdown(
#                     id='dropdown_country_filter4',
#                     options=pdf_d4['postcode'].unique(),
#                     value=[],
#                     multi=True,
#                     searchable=True,
#                     persistence=False,
#                     persistence_type='memory',  # session
#                     placeholder=f"Select {paths.l_d_dropdown_map[4]}(s)",
#                 )
# comp_pdf_found = html.Div(id='pdf_world_found')
# comp_map = html.Div(id='map_figure_right')
#
# # layout = dbc.Container(
# layout = dbc.Container(
#     [
#         # dcc.Markdown('# This will be the content of Page Company'),
#         html.Div(id='image_customer', children=''),
#         dbc.Row(
#             dbc.Col(html.H1("Customer map",
#                             className='text-center text-primary',),
#                     width=12)
#         ),
#
#         dbc.Row([
#             dbc.Col([
#                 comp_dropCountry,   # COUNTRY
#                 comp_dropState,     # STATE
#                 comp_dropRegion,    # REGION
#                 comp_dropDistrict,  # DISTRICT
#                 comp_dropZIP,       # ZIP
#             ], width={'size': 5}),
#             dbc.Col([
#                 comp_pdf_found,     # MAP
#                 comp_map            # MAP
#             ], width={'size': 7}),
#         ], justify='start'),  # Horizontal:start,center,end,between,around
#     ],
#     fluid=True,     # Stretch to use all screen
# )
#
# @callback(
#     # Output(component_id='pdf_world_found', component_property='children'),
#     Output(component_id='map_figure_right', component_property='children'),
#     Input(component_id='dropdown_country_filter0', component_property='value'),#COUNTRY
#     Input(component_id='dropdown_country_filter1', component_property='value'),#STATE
#     Input(component_id='dropdown_country_filter2', component_property='value'),#REGION
#     Input(component_id='dropdown_country_filter3', component_property='value'),#DISTRICT
#     Input(component_id='dropdown_country_filter4', component_property='value'),#ZIP
#     prevent_initial_call=True
# )
# def gen_map_countryX(l_countries, l_states, l_regions, l_districts, l_zips):
#     dropdown_value = paths.l_d_dropdown_map
#
#     print(f'gen_map_countryX')
#     print(f'')
#
#     print(f'dropdown_value:{dropdown_value}')
#     print(f'')
#
#     print(f'country = {l_countries}')
#     print(f'state =   {l_states[0:5]}')
#     print(f'region =  {l_regions[0:5]}')
#     print(f'district ={l_districts[0:5]}')
#     print(f'zip =     {l_zips[0:5]}')
#     print(f'')
#
#     # Initialize list of feature_groups
#     l_fg = []
#
#     #COUNTRY
#     category = paths.l_d_dropdown_map[0]
#     print(f'l_countries={l_countries}')
#
#     print('gdf_world')
#     print(gdf_world)
#     print(gdf_world.columns.to_list())
#
#     pdf_world = gdf_world['ADMIN']
#     print('pdf_world')
#     print(pdf_world)
#     print(f'type={type(pdf_world)}')
#     # print(pdf_world.columns.to_list())
#
#     # pred1 = pdf_world.isin([l_countries])
#     # print(f'pred1={pred1}')
#     # pdf1 = gdf_world[pred1]
#     # print('pdf1')
#     # print(pdf1.shape)
#     # print(f'Countries found={pdf1.shape[0]}')
#
#     print(f'l_countries={l_countries}')
#     pred2 = pdf_world.isin(l_countries)
#     print(f'pred2={pred2}')
#     pdf = gdf_world[pred2]
#     print('pdf2')
#     print(pdf.head())
#     pdf_countriesNo = pdf.shape[0]
#     print(f'Countries found={pdf_countriesNo}')
#     if l_countries:
#         fg_countries = Maps.get_feature_group_countries(gdf_world=pdf,
#                                                         l_countries=l_countries,
#                                                         key_filter='ADMIN',
#                                                         fields=paths.fields_wca,
#                                                         aliases=paths.aliases_wca)
#         if fg_countries is not None:
#             l_fg.append(fg_countries)
#     print(308)
#     #STATES
#     if l_states:
#         category = paths.l_d_dropdown_map[1]
#         pdf_states = pdf_d1['name']  # For indexing
#         pdf = pdf_d1[pdf_states.isin(l_states)]
#
#         print(f'States found={pdf.shape[0]}')
#         fg_state = Maps.get_feature_group(pdf, category)
#         if fg_state is not None:
#             l_fg.append(fg_state)
#
#     #REGION
#     if l_regions:
#         category = paths.l_d_dropdown_map[2]
#         pdf_regions = pdf_d2['NAME_2']  # For indexing
#         pdf = pdf_d2[pdf_regions.isin(l_regions)]
#         print(f'Regions found={pdf.shape[0]}')
#         fg_region = Maps.get_feature_group(pdf, category)
#         if fg_region is not None:
#             l_fg.append(fg_region)
#
#     #DISTRICT
#     if l_districts:
#         category = paths.l_d_dropdown_map[3]
#         pdf_districts = pdf_d3['NAME_3']  # For indexing
#         pdf = pdf_d3[pdf_districts.isin(l_districts)]
#         print(f'Districts found={pdf.shape[0]}')
#         fg_district = Maps.get_feature_group(pdf, category)
#         if fg_district is not None:
#             l_fg.append(fg_district)
#
#     #         l_fg.append(fg)
#     #         print(l_fg)
#
#     #ZIP
#     if(l_zips):
#         category = paths.l_d_dropdown_map[4]
#         pdf_zips = pdf_d4['postcode']  # For indexing
#         pdf = pdf_d4[pdf_zips.isin(l_zips)]
#         print(f'l_zips:{l_zips}')
#         print(f'Zips found={pdf.shape[0]}')
#         fg_zip = Maps.get_feature_group(pdf, category)
#         if fg_zip is not None:
#             l_fg.append(fg_zip)
#
#     if l_fg: #list of feature groups is NOT empty
#         print(f"l_fg:{l_fg}")
#         print("Generating map!")
#
#         # company = request.authorization['username']
#         # print(f'company: {company}')
#         # # d_company = Defs.company[company]
#         # try:
#         #     path = f'data_loaded_{company}.json'
#         #     print(f'path={path}')
#         #     # d_company = json.loads(path)
#         #     d_company = Maps.read_dict_temp(path)
#         #     print(f'd_company: {d_company}')
#         # except Exception as ex:
#         #     print(ex)
#
#         # company = Maps.read_dict_temp(f'data_loaded_baumgartner.json')
#         company = Maps.read_dict_temp(f'data_loaded_vaude.json')
#
#         fm = Maps.get_folium_map_countries(
#             l_fg=l_fg,
#             d_company=company
#         )
#         # fm = folium.Map()
#
#         print(f'fm:{fm}, type:{type(fm)}')
#         print(270)
#         name_map = 'map_right'
#         Maps.write_map_temp(fm, name_map=name_map)
#         map_fig = html.Iframe(srcDoc=open(f"{name_map}.txt", "r").read(),
#                            width='100%',
#                            height='750'
#                            )
#
#         # im = dash_table.DataTable(pdf_world.to_dict('records'), page_size=10)
#         return map_fig
#     else:
#         return html.Iframe("Empty map!")