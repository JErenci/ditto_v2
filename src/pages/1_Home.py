import dash
from dash import html, dcc
from dash import Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io

import sys

sys.path.append('/Users/User/PycharmProjects/ditto_v2/')
from functionality_maps import Maps
# from functionality_maps import paths

dash.register_page(__name__, path='/')
d_company = Maps.read_dict_temp('data_loaded.json')
company = d_company['name']

app_logging = True

## 2.b. Components              [comp1 = dcc.Markdown("Hello World!"))]
comp_imageUser = html.Img(
    # src='../../assets/default_avatar.jpg'
    src=dash.get_asset_url('../../assets/default_avatar.jpg')
)
comp_upload = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True  # Allow multiple files to be uploaded
    )],
    style= {
        'display': 'block' # Visible
        # 'display': 'none'  --> NOT Visible
    }
)
comp_uploaded = html.Div(id='output-image-upload')
comp_input_accountName = dcc.Input(
    id='input_accountName',
    # placeholder='Enter the company name...',
    value='Company',
    # style={'width': '100%'},
    type='text'
)
comp_text_accountName = html.Div('Account:')
comp_output_accountName = html.Div(id='output_accountName')
comp_button_editAccountName = dbc.Button(
    id='button_editAccountName',
    children="Edit",
    external_link=True,
    color="primary",
)
comp_button_changeUserImage = dbc.Button(
    id='button_changeUserImage',
    children="Change Image",
    external_link=True,
    color="primary",
)
comp_text_userName = html.Div('User:')
# comp_accountUser = dcc.Input(id='account_user',
#     placeholder='Enter a value...',
#     type='text',
#     value='')

# comp_imgCust = html.Div(id='image_customer', children='')

# 2.c. Layout                  [app.layout = dbc.Container(comp1)]
layout = dbc.Container(
    [
        dbc.Row([comp_text_accountName]),
        dbc.Row([
            dbc.Col([
                comp_input_accountName,
                comp_button_editAccountName,
                comp_output_accountName,

            ], width={'size': 5}),
            dbc.Col([
                comp_text_userName,
                comp_imageUser,
                comp_upload,
                comp_uploaded,
                comp_button_changeUserImage
            ], width={'size': 7}),
        ]),

        # comp_accountUser,

    ],
    fluid=True
)


def parse_contents(contents, filename,
                   date,
                   logging: bool = False):

    # if logging:
    #     print('contents:', contents)
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    img_ext = ['png', 'jpg']
    is_image = [ele for ele in img_ext if (ele in filename)]

    if logging:
        print(f'filename:{filename}')

    im = html.Img(src=contents)
    try:
        if 'csv' in filename:
            if logging:
                print(f'{filename} contains csv')
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            im = dash_table.DataTable(df.to_dict('records'), page_size=10)
        elif 'xls' in filename:
            if logging:
                print(f'{filename} contains xls')
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            if logging:
                print(df)
            im = dash_table.DataTable(df.to_dict('records'), page_size=10)
        elif is_image:
            if logging:
                print(f'{filename} contains an image')

    except Exception as e:
        print(e)
        output = f'There was an error processing file {filename}'
        return html.Div([output])

    div = [
        # html.H5(filename),
        # html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        im,
        # html.Hr(),
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # }),
    ]

    return html.Div(div)


# 2.d. Callback                [@app.callback(Output,Input,State)]
@callback(Output('output-image-upload', 'children'),
          # Output('tbl', 'data'),
          Input('upload-image', 'contents'),
          State('upload-image', 'filename'),
          State('upload-image', 'last_modified'),
          prevent_initial_callback=True)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d, logging=app_logging) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

# @callback(Output('output-image-upload', 'children'),
#           # Input('button_changeUserImage', 'n_clicks'),
#           Input('upload-image', 'contents'),
#           prevent_initial_callback=True)
# def update_userImage(image):
#     # if n_clicks & n_clicks>0:
#     if image is not None:
#         print(image)
#         im = html.Img(src=image)
#         return html.Div([im])


@callback(
    Output(component_id='output_accountName', component_property='children'),
    Input('button_editAccountName', 'n_clicks'),
    Input(component_id='input_accountName', component_property='value')
)
def update_accountName(n_clicks,input_value):
    if n_clicks & n_clicks>0:
        n_clicks = 0
        return input_value
