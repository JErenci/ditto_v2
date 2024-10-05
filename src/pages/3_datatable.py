import dash
from dash import html, dcc
from dash import Input, Output, State, callback, dash_table, no_update
import pandas as pd
import dash_bootstrap_components as dbc

import sys
sys.path.append('/Users/User/PycharmProjects/ditto_v2/')
from functionality_maps import Maps
from functionality_maps import paths

dash.register_page(__name__)

customer_name = 1
initial_active_cell = {"row": 0, "column": 0, "column_id": "country", "row_id": 0}
l_fg_layers = ['country','ZIP']
df = pd.read_csv(f'assets/Sample_csv_comma_separated.csv',sep=',')

print(df.head())

comp_dataTable = dash_table.DataTable(id='customer_datatable',
                             columns=[{
                                 "name": i,
                                 "id": i,
                                 # "presentation": "markdown",
                                 "deletable": True,
                                 "selectable": True,
                                 "hideable": True
                             } for i in df.columns
                                 # if i not in ['Summary']
                             ],
                             data=df.to_dict('records'),
                             hidden_columns=['Titel', 'Geburtsdatum', 'Telefon', 'Mobil', 'Telefax', 'Eintragsdatum',
                                             'Newsletter'],
                             editable=False,
                             filter_action='native',
                             # filter_options=True,
                             page_size=10,
                             row_deletable=False,
                             row_selectable="multi",
                             selected_rows=[customer_name - 1],
                             active_cell=initial_active_cell,
                             )
comp_map = html.Div(id='map_customers')

# 2.c. Layout                  [app.layout = dbc.Container(comp1)]
layout = dbc.Container(
    [
        comp_dataTable,
        comp_map
    ]
)


@callback(
    # Output("image_customer", "children"),
    Output("map_customers", "children"),
    Input("customer_datatable", "active_cell"),
    Input('customer_datatable', "derived_virtual_selected_rows"),
    prevent_initial_call=True
)
def cell_clicked(active_cell, derived_virtual_selected_rows):
    print(1)
    print(f'active_cell:{active_cell}')
    print(f'derived_virtual_selected_rows:{derived_virtual_selected_rows}')

    if active_cell is None:
        return no_update

    row = active_cell["row"]
    print(f"row id: {row}")

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    customer_id = df.at[row,"Nr."]
    person = df.at[row, "Vorname"] + " " + df.at[row, 'Nachname']
    address = df.at[row, "Straße"] + " " + df.at[row, "Hausnummer"]
    city = df.at[row, "Stadt"]
    print(f'customer={customer_id}, person={person}, address={address}, city={city}')
    country = 'Germany'

    # img_customer = html.Img(src=f'/assets/{company}/Customers/{customer_id}.jpg',
    #                         title=f'{person}',
    #                         width='100%'
    #                         )

    # Initialize list of feature_groups
    l_fg = []

    l_countries = country
    print(f'derived_virtual_selected_rows={derived_virtual_selected_rows}')

    if derived_virtual_selected_rows is not None:
        print(2)
        for row in derived_virtual_selected_rows:
            customer_id = df.at[row, "Nr."]
            person = df.at[row, "Vorname"] + " " + df.at[row, 'Nachname']
            address = df.at[row, "Straße"] + " " + df.at[row, "Hausnummer"]
            city = df.at[row, "Stadt"]
            zip = df.at[row, "PLZ"]
            country = 'Germany'

            print(f'customer={customer_id}, person={person}, address={address}, city={city}, zip={zip}')

            # print(f'pdf: {pdf}')
            # if 'country' in l_fg_layers:
            #     fg_countries = Maps.get_feature_group_countries(
            #         gdf_world = Maps.load_gdf_from_csv(path=paths.path_wca),
            #         l_countries=[l_countries]
            #     )
                # gdf_world = Maps.load_gdf_from_csv(path=paths.path_wca)
                # pdf_world = gdf_world['ADMIN']
                # # print(f'pdf_world:{pdf_world}')
                # arg = pdf_world.isin([l_countries])
                # # print(f'arg:{arg}')
                # pdf = gdf_world[pdf_world.isin([l_countries])]
                # # print(f'l_countries:{l_countries}')
                #
                # fg_countries = Maps.get_feature_group_countries(gdf_world=pdf,
                #                                                 l_countries=[l_countries],
                #                                                 key_filter='ADMIN',
                #                                                 fields=paths.fields_wca,
                #                                                 aliases=paths.aliases_wca)
                #
                # if fg_countries is not None:
                #     l_fg.append(fg_countries)






            # if findApproach == 'Geocoder':
            #     fg_images_customers = folium.FeatureGroup(name='images_customers')
            #     locator = Nominatim(user_agent="myGeocoder")
            #     location = locator.geocode(f"{address}, {city}, {country}")
            #
            #     print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
            #
            #     f_marker = folium.Marker(location=[location.latitude, location.longitude],
            #                   popup=address,
            #                   tooltip=person,
            #                   # icon=folium.features.CustomIcon(
            #                   #     icon_image=f'assets/{company}/Customers/{customer_id}.jpg',
            #                   #     icon_size=(25, 25))
            #                   )
            #     print(f"Added {person} to feature_group!")
            #     print()
            #     fm.add_child(f_marker)

            #     fg_images_customers.add_child(f_marker)
            #     fm.add_child(fg_images_customers)

            if 'ZIP' in l_fg_layers:
                pdf_d4 = Maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[4]])
                l_zips = [zip]
                pdf_zips = pdf_d4['postcode']  # For indexing
                pdf = pdf_d4[pdf_zips.isin(l_zips)]
                print(f'l_zips:{l_zips}')
                print(f'Zips found={pdf.shape[0]}')
                fg_zip = Maps.get_feature_group(pdf, paths.l_d_dropdown_map[4])
                if fg_zip is not None:
                    l_fg.append(fg_zip)

        fm = Maps.get_folium_map_countries(l_fg,
                                           d_company={})

        name_map = 'map_customer'
        Maps.write_map_temp(fm, name_map=name_map)
        map_customer = html.Iframe(srcDoc=open(f"{name_map}.txt", "r").read(),
                           width='50%',
                           height='50%')
        return [
            # img_customer,
            map_customer
        ]

    else:
        return [html.Iframe("Empty customer!"), html.Iframe("Empty map!")]
