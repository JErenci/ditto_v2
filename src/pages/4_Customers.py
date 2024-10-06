import base64
import io

import dash
from dash import html, dcc
from dash import Input, Output, State, callback, dash_table, no_update
import pandas as pd
import dash_bootstrap_components as dbc
import pandas as pd

import sys
sys.path.append('/Users/User/PycharmProjects/ditto_v2/')
from assets import run_relevant_variables
company_name = run_relevant_variables.company_name

dash.register_page(__name__)

customer_name = 1
initial_active_cell = {"row": 0, "column": 0, "column_id": "country", "row_id": 0}
l_fg_layers = ['country', 'ZIP']
logging_datable = True
customer_data_default_path = 'data_customer.csv'

comp_download = dcc.Download(id="download")
comp_upload = dcc.Upload(id='upload_data',
    children=html.Div([
        'Drag and Drop or ', html.A('Select Files')]),
    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px',
    },
    multiple=False     # Allow multiple files to be uploaded
)
comp_uploaded = html.Div(id='output_upload_data')

comp_col_data = dbc.Col([
    comp_download,
    comp_upload,
    comp_uploaded
    ],
    width={'size': 6},
    xs=12, sm=12, md=12, lg=6, xl=6,
)

comp_row_upload = dbc.Row(
    [
        comp_col_data
    ],
    justify='center',
    align='top',
    style={
        'width': '100%'
    }
)
comp_row_download = dbc.Row(
    [
        dbc.Col(
            [
                dcc.Dropdown(id="dropdown",
                             options=[
                                 {"label": "Excel file", "value": "excel"},
                                 {"label": "CSV file", "value": "csv"},
                             ],
                             placeholder="Choose download file type. Default is CSV format!",
                             )
            ],
            width={'size': 5},
            xs=12, sm=12, md=12, lg=5, xl=5,
        ),
        dbc.Col(
            [
                dbc.Button(id="btn_download",
                           children="Download Data",
                           disabled=True
                           ),
            ],
            width={'size': 1},
            xs=12, sm=12, md=12, lg=1, xl=1,
        ),
    ],
    justify='center',
)

comp_store = dcc.Store(id='intermediate-value')     # dcc.Store stores the intermediate value
comp_map = html.Div(id='map_customers')

# 2.c. Layout                  [app.layout = dbc.Container(comp1)]
layout = dbc.Container(
    [
        comp_row_upload,
        comp_row_download,
        comp_store
    ],
    fluid=True
)


def parse_content(contents, filename, date, logging:bool = False) -> pd.DataFrame:
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    df = pd.DataFrame()
    try:
        if 'csv' in filename:
            if logging:
                print(f'{filename} contains csv')
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            if logging:
                print(f'{filename} contains xls')
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            if logging:
                print(df)
        else:
            print(f'File format Not recognised!')

    except Exception as e:
        print(e)
        output = f'There was an error processing file {filename}'
        return df
    return df


@callback(
    Output('output_upload_data', 'children'),
    Output('btn_download', 'disabled'),
    Output('intermediate-value', 'data'),
    Input('upload_data', 'contents'),
    State('upload_data', 'filename'),
    State('upload_data', 'last_modified'),
    config_prevent_initial_callbacks=True
)
def update_output(contents, name, date):
    children = dash.no_update
    download_button_disabled = True
    df = pd.DataFrame()

    if contents:
        df = parse_content(contents, name, date, logging_datable)
        children = [
            dash_table.DataTable(id='customer_datatable',
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
                             'Newsletter', 'Straße', 'Hausnummer'],
                editable=False,
                filter_action='native',
                # filter_options=True,
                page_size=10,
                row_deletable=False,
                row_selectable="multi",
                selected_rows=[customer_name - 1],
                active_cell=initial_active_cell,
                )
        ]

        df.to_csv(path_or_buf=customer_data_default_path)

        download_button_disabled = False
    return [children, download_button_disabled, df.to_json(date_format='iso', orient='split')]


@callback(
    Output("download", "data"),
    Input("btn_download", "n_clicks"),
    Input('intermediate-value', 'data'),
    State("dropdown", "value"),
    config_prevent_initial_callbacks=True,
)
def func(n_clicks, df, download_type):
    print(f'n_clicks:{n_clicks}')
    print(f'{n_clicks is not None}')
    if n_clicks is not None:
        if n_clicks > 0:
            print(f'n_clicks:{n_clicks}')
            dff = pd.read_json(df, orient='split')
            if download_type == "csv":
                return dcc.send_data_frame(dff.to_csv, "mydf.csv")
            else:
                return dcc.send_data_frame(dff.to_excel, "mydf.xlsx")
    
    
# @callback(
#     # Output("image_customer", "children"),
#     Output("map_customers", "children"),
#     Input("customer_datatable", "active_cell"),
#     Input('customer_datatable', "derived_virtual_selected_rows"),
#     prevent_initial_call=True
# )
# def cell_clicked(active_cell, derived_virtual_selected_rows):
#     print(1)
#     print(f'active_cell:{active_cell}')
#     print(f'derived_virtual_selected_rows:{derived_virtual_selected_rows}')
#
#     if active_cell is None:
#         return no_update
#
#     row = active_cell["row"]
#     print(f"row id: {row}")
#
#     if derived_virtual_selected_rows is None:
#         derived_virtual_selected_rows = []
#
#     customer_id = df.at[row,"Nr."]
#     person = df.at[row, "Vorname"] + " " + df.at[row, 'Nachname']
#     address = df.at[row, "Straße"] + " " + df.at[row, "Hausnummer"]
#     city = df.at[row, "Stadt"]
#     print(f'customer={customer_id}, person={person}, address={address}, city={city}')
#     country = 'Germany'
#
#     # img_customer = html.Img(src=f'/assets/{company}/Customers/{customer_id}.jpg',
#     #                         title=f'{person}',
#     #                         width='100%'
#     #                         )
#
#     # Initialize list of feature_groups
#     l_fg = []
#
#     l_countries = country
#     print(f'derived_virtual_selected_rows={derived_virtual_selected_rows}')
#
#     if derived_virtual_selected_rows is not None:
#         print(2)
#         for row in derived_virtual_selected_rows:
#             customer_id = df.at[row, "Nr."]
#             person = df.at[row, "Vorname"] + " " + df.at[row, 'Nachname']
#             address = df.at[row, "Straße"] + " " + df.at[row, "Hausnummer"]
#             city = df.at[row, "Stadt"]
#             zip = df.at[row, "PLZ"]
#             country = 'Germany'
#
#             print(f'customer={customer_id}, person={person}, address={address}, city={city}, zip={zip}')
#
#             # print(f'pdf: {pdf}')
#             # if 'country' in l_fg_layers:
#             #     fg_countries = Maps.get_feature_group_countries(
#             #         gdf_world = Maps.load_gdf_from_csv(path=paths.path_wca),
#             #         l_countries=[l_countries]
#             #     )
#                 # gdf_world = Maps.load_gdf_from_csv(path=paths.path_wca)
#                 # pdf_world = gdf_world['ADMIN']
#                 # # print(f'pdf_world:{pdf_world}')
#                 # arg = pdf_world.isin([l_countries])
#                 # # print(f'arg:{arg}')
#                 # pdf = gdf_world[pdf_world.isin([l_countries])]
#                 # # print(f'l_countries:{l_countries}')
#                 #
#                 # fg_countries = Maps.get_feature_group_countries(gdf_world=pdf,
#                 #                                                 l_countries=[l_countries],
#                 #                                                 key_filter='ADMIN',
#                 #                                                 fields=paths.fields_wca,
#                 #                                                 aliases=paths.aliases_wca)
#                 #
#                 # if fg_countries is not None:
#                 #     l_fg.append(fg_countries)
#
#
#
#
#
#
#             # if findApproach == 'Geocoder':
#             #     fg_images_customers = folium.FeatureGroup(name='images_customers')
#             #     locator = Nominatim(user_agent="myGeocoder")
#             #     location = locator.geocode(f"{address}, {city}, {country}")
#             #
#             #     print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
#             #
#             #     f_marker = folium.Marker(location=[location.latitude, location.longitude],
#             #                   popup=address,
#             #                   tooltip=person,
#             #                   # icon=folium.features.CustomIcon(
#             #                   #     icon_image=f'assets/{company}/Customers/{customer_id}.jpg',
#             #                   #     icon_size=(25, 25))
#             #                   )
#             #     print(f"Added {person} to feature_group!")
#             #     print()
#             #     fm.add_child(f_marker)
#
#             #     fg_images_customers.add_child(f_marker)
#             #     fm.add_child(fg_images_customers)
#
#             if 'ZIP' in l_fg_layers:
#                 pdf_d4 = Maps.load_gdf_from_csv(path=paths.csv[paths.l_d_dropdown_map[4]])
#                 l_zips = [zip]
#                 pdf_zips = pdf_d4['postcode']  # For indexing
#                 pdf = pdf_d4[pdf_zips.isin(l_zips)]
#                 print(f'l_zips:{l_zips}')
#                 print(f'Zips found={pdf.shape[0]}')
#                 fg_zip = Maps.get_feature_group(pdf, paths.l_d_dropdown_map[4])
#                 if fg_zip is not None:
#                     l_fg.append(fg_zip)
#
#         fm = Maps.get_folium_map_countries(l_fg,
#                                            d_company={})
#
#         name_map = 'map_customer'
#         Maps.write_map_temp(fm, name_map=name_map)
#         map_customer = html.Iframe(srcDoc=open(f"{name_map}.txt", "r").read(),
#                            width='50%',
#                            height='50%')
#         return [
#             # img_customer,
#             map_customer
#         ]
#
#     else:
#         return [html.Iframe("Empty customer!"), html.Iframe("Empty map!")]
