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
# comp_image = html.Div(html.Img(src=dash.get_asset_url('logo.png')))
# comp_image2 = html.Img(src='/assets/default_avatar.jpg')

### ACCOUNT INFORMATION###
comp_text_accountInformation = html.H3('Account Information')
comp_input_accountName = dcc.Input(
    id='input_accountName',
    placeholder='Enter the Account name...',
    # value='Company',
    style={'width': '100%'},
    type='text'
)
comp_output_accountName = html.Div(id='output_accountName')
comp_upload_accountImage = html.Div([
    dcc.Upload(
        id='upload_accountImage',
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
comp_div_accountImage = html.Div(id='div_accountImage')

## USER INFORMATION ###
comp_text_userInformation = html.H3('User Information')
comp_input_userName = dcc.Input(
    id='input_userName',
    placeholder='Enter The user name...',
    type='text',
    value='')

comp_output_userName = html.Div(id='output_userName')
comp_div_imageUser = html.Div(
    id='div_userImage',
    # src='../../assets/default_avatar.jpg'
    # src=dash.get_asset_url('default_avatar.jpg')
)
comp_upload_userImage = html.Div([
    dcc.Upload(
        id='upload_userImage',
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

# comp_imgCust = html.Div(id='image_customer', children='')

# 2.c. Layout                  [app.layout = dbc.Container(comp1)]
layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                comp_text_accountInformation,
                comp_input_accountName,
                comp_output_accountName,
                comp_upload_accountImage,
                comp_div_accountImage,
            ],
                width={'size': 5},
                xs=12, sm=12, md=12, lg=5, xl=5,
            ),
            dbc.Col([
                comp_text_userInformation,
                comp_input_userName,
                comp_output_userName,
                comp_upload_userImage,
                comp_div_imageUser,
            ],
                width={'size': 6, 'offset': 1},
                xs=12, sm=12, md=12, lg=6, xl=6,
            ),
        ],
            justify='center',
            align='top',
        ),
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

    # div = [
    #     # html.H5(filename),
    #     # html.H6(datetime.datetime.fromtimestamp(date)),
    #
    #     # HTML images accept base64 encoded strings in the same format
    #     # that is supplied by the upload
    #     # im,
    #     # html.Hr(),
    #     # html.Div('Raw Content'),
    #     # html.Pre(contents[0:200] + '...', style={
    #     #     'whiteSpace': 'pre-wrap',
    #     #     'wordBreak': 'break-all'
    #     # }),
    # ]

    return im#html.Div(div)


# 2.d. Callback                [@app.callback(Output,Input,State)]
@callback(Output('div_userImage', 'children'),
          # Output('tbl', 'data'),
          Input('upload_userImage', 'contents'),
          State('upload_userImage', 'filename'),
          State('upload_userImage', 'last_modified'),
          prevent_initial_callback=True)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d, logging=app_logging) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@callback(Output('div_accountImage', 'children'),
          Input('upload_accountImage', 'contents'),
          State('upload_accountImage', 'filename'),
          State('upload_accountImage', 'last_modified'),
          prevent_initial_callback=True)
def update_outputAccount(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d, logging=app_logging) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


@callback(
    Output(component_id='output_accountName', component_property='children'),
    Input(component_id='input_accountName', component_property='value'),
    prevent_initial_callback=True
)
def update_accountName(input_value):
    return input_value

@callback(
    Output(component_id='output_userName', component_property='children'),
    Input(component_id='input_userName', component_property='value'),
    prevent_initial_callback=True
)
def update_userName(input_value):
    return input_value