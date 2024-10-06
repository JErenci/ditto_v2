import dash
from dash import html, dcc
from dash import Input, Output, State, callback
import dash_bootstrap_components as dbc
import base64

import sys

sys.path.append('/Users/User/PycharmProjects/ditto_v2/')
from functionality_maps import Maps

# from functionality_maps import paths

dash.register_page(__name__, path='/')

d_company = Maps.read_dict_temp('data_loaded_baumgartner.json')
company = d_company['name']
path_to_default_userImage = 'assets/default_user.jpg'
path_to_default_companyLogo = 'assets/default_company.jpg'

base64_decoded_company_image = base64.b64encode(open(path_to_default_companyLogo, "rb").read()).decode()
base64_decoded_user_image = base64.b64encode(open(path_to_default_userImage, "rb").read()).decode()
app_logging = True

## 2.b. Components              [comp1 = dcc.Markdown("Hello World!"))]

### ACCOUNT INFORMATION###
comp_text_accountInformation = html.H3('Account Information')
comp_input_accountName = html.Div(
    id="div_accountName",
    children = [
        dcc.Input(
            id='text_accountName',
            placeholder='Enter the Account name...',
            # value=data_input_value,
            style={'width': '80%'},
        ),
        html.Button(
            id='button_edit_accountName',
            children='Save')
    ],
    # children=[
    #     dcc.Input(
    #         id='input_accountName',
    #         placeholder='Enter the Account name...',
    #         # value='Company',
    #         style={'width': '80%'},
    #         type='text',
    #     ),
    #     # html.Button('Edit')
    #     html.Div([html.Button(id='button_edit_accountName', children='Save')])
    # ],
)
# comp_button_accountName = html.Div(id='button_accountName', children=[html.Button('Change Text')])

comp_output_accountName = html.Div(id='output_accountName')
comp_drag_and_drop_accountImage = html.Div([
    dcc.Upload(
        id='dragdrop_accountImage',
        children=[
            html.Img(src=f'data:image/jpg;base64, {base64_decoded_company_image}'),
            html.Div([html.Button('Change Image')])
        ],
        style={
            'width': '80%',
            # 'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'display': 'block'  # Visible
        },
        multiple=False  # Allow multiple files to be uploaded
    )],
    style={
        'width': '80%',
        # 'display': 'none'  --> NOT Visible
    }
)
comp_div_accountImage = html.Div(
    id='div_accountImage',
    style={
        'width': '50',
        'height': '200px',
        'margin': '10px'
    }
)

## USER INFORMATION ###
comp_text_userInformation = html.H3('User Information')
comp_input_userName = dcc.Input(
    id='input_userName',
    style={'width': '100%'},
    placeholder='Enter The user name...',
    type='text',
    value='')

comp_output_userName = html.Div(id='output_userName')
comp_div_userImage = html.Div(
    id='div_userImage',
    style={
        'width': '100px',
        'height': '200px',
    }
    # src='../../assets/default_user.jpg'
    # src=dash.get_asset_url('default_user.jpg')
)
comp_drag_and_drop_userImage = html.Div([
    dcc.Upload(
        id='dragdrop_userImage',
        children=[
            html.Img(src=f'data:image/jpg;base64, {base64_decoded_user_image}'),
            html.Div([html.Button('Change Image')])
        ],
        style={
            'width': '100%',
            # 'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False  # Allow multiple files to be uploaded
    )],
    style={
        'display': 'block'  # Visible
        # 'display': 'none'  --> NOT Visible
    }
)

# comp_imgCust = html.Div(id='image_customer', children='')

# 2.c. Layout                  [app.layout = dbc.Container(comp1)]

comp_colAccount = dbc.Col([
    comp_text_accountInformation,
    comp_input_accountName,
    # comp_button_accountName,
    comp_output_accountName,
    comp_drag_and_drop_accountImage,
    comp_div_accountImage,
],
    width={'size': 3, 'offset': 1},
    xs=12, sm=12, md=12, lg=3, xl=3,
)


comp_colUser = dbc.Col([
    comp_text_userInformation,
    comp_input_userName,
    comp_output_userName,
    comp_drag_and_drop_userImage,
    comp_div_userImage,
],
    width={'size': 3, 'offset': 1},
    xs=12, sm=12, md=12, lg=3, xl=3,
)

## COMPANY LOCATIONS
comp_colLocations = dbc.Col(
    [
        html.Button(id='button_map',children='Load map!'),
        html.Div(id='map_company_locations')
    ],
    width={'size': 6},
    xs=12, sm=12, md=12, lg=6, xl=6,
)


row_accountUser = dbc.Row([
    comp_colUser,
    comp_colAccount,
    comp_colLocations
],
    style={

    },
    justify='left',
    align='top',
)

# comp_imgCust = html.Div(id='image_customer', children='')

# 2.c. Layout                  [app.layout = dbc.Container(comp1)]
layout = dbc.Container(
    [
        row_accountUser,
    ],
    fluid=True
)


def parse_contents_alone(contents):
    im = html.Img(src=contents)
    return im


def parse_contents(contents, filename,
                   date,
                   logging: bool = False):
    if logging:
        print(f'contents:{contents}')

    im = html.Img(src=contents)
    return im


# 2.d. Callback                [@app.callback(Output,Input,State)]
## ACCOUNT CALLBACKS ##

@callback(
    Output(component_id='div_accountName', component_property='children'),
    Input(component_id='div_accountName', component_property='children'),
    Input('button_edit_accountName', 'n_clicks'),
    config_prevent_initial_callbacks=True
)
# {'props':
#      {
#          'type': 'text',
#           'placeholder': 'Enter the Account name...',
#           'style': {'width': '100%'},
#           'id': 'input_accountName',
#           'value': 'Baumgartner',
#           'n_blur': 2,
#          'n_blur_timestamp': 1728199651349
#       },
#     'type': 'Input', 'namespace': 'dash_core_components'}
def update_account_name(div_account_name,
                        n_clicks
                        ):
    print()
    print(f'div_account={div_account_name}')
    size_div_elems = len(div_account_name)
    print(f'length div = {size_div_elems}')

    if size_div_elems == 2:
        data_input = div_account_name[0]
        data_button = div_account_name[1]['props']

        data_input_props = data_input['props']
    else:
        return dash.no_update

    print(f'  data_input={data_input}')
    print(f'  data_button={data_button}')

    # print(f'n_clicks={n_clicks}')
    data_input_type = data_input['type']
    print(f'data_input_type={data_input_type}')

    if data_input_type == 'Input':
        data_input_value = data_input_props['value']
        print(f'   data_input_value={data_input_value}')
        data_button_text = data_button['children']
        print(f'   data_button_text={data_button_text}')
    elif data_input_type.startswith('H'):
        data_input_value = data_input_props['children']
        print(f'   data_input_value={data_input_value}')
        data_button_text = data_button['children']
        print(f'   data_button_text={data_button_text}')
    else:
        data_input_value = 'EMTPY'
        data_button_text = 'EMTPY'

    children = dash.no_update
    if data_button_text == 'Edit':
        children = [
            dcc.Input(
                id='text_accountName',
                placeholder='Enter the Account name...',
                value=data_input_value,
                style={'width': '80%'},
            ),
            html.Button(
                id='button_edit_accountName',
                children='Save')
        ]
        print()
    if data_button_text == 'Save':
        children = [
            html.H4(data_input_value),
            html.Button(
                id='button_edit_accountName',
                children='Edit')
        ]
    return children


@callback(
    Output('dragdrop_accountImage', 'children'),
    Output('dragdrop_accountImage', 'style'),
    Input('dragdrop_accountImage', 'contents'),
    config_prevent_initial_callbacks=True
)
def update_account_image(contents):
    drag_and_drop_visibility = {
        'width': '100%',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px',
        'display': 'block'  # Visible, # visibility_state == 'on'
    }

    drag_and_drop_children = [
        html.Img(src=f'data:image/jpg;base64, {base64_decoded_company_image}'),
        html.Div([html.Button('Change Image')])
    ]
    print(f'contents:{contents}')
    if contents is not None:
        drag_and_drop_children = [
            html.Img(src=contents,
                     style={
                         # 'height': '100%',
                         'width': '100%'
                     }),
            html.Div([html.Button('Change Image')])
        ]
        drag_and_drop_visibility = {
            'width': '100%',
            'height': '60px',
            'textAlign': 'center',
            'display': 'block'
        }
    return [drag_and_drop_children, drag_and_drop_visibility]


## USER CALLBACKS ##
@callback(
    Output(component_id='output_userName', component_property='children'),
    Input(component_id='input_userName', component_property='value'),
    prevent_initial_callback=True
)
def update_username(input_value: str) -> str:
    """
    Forwards input to output
    :type input_value: str
    """
    return input_value


@callback(Output('dragdrop_userImage', 'children'),
          Output('dragdrop_userImage', 'style'),
          Input('dragdrop_userImage', 'contents'),
          # State('dragdrop_userImage', 'last_modified'),
          config_prevent_initial_callbacks=True
          )
def update_user_image(contents):
    drag_and_drop_visibility = {
        'width': '100%',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px',
        'display': 'block'  # Visible, # visibility_state == 'on'
    }

    drag_and_drop_children = [
        html.Img(src=f'data:image/jpg;base64, {base64_decoded_user_image}'),
        html.Div([html.Button('Change Image')])
    ]
    print(f'contents:{contents}')
    if contents is not None:
        drag_and_drop_children = [
            html.Img(src=contents,
                     style={
                         # 'height': '100%',
                         'width': '100%'
                     }),
            html.Div([html.Button('Change Image')])
        ]
        drag_and_drop_visibility = {
            'width': '100%',
            'height': '60px',
            'textAlign': 'center',
            'display': 'block'
        }
    return [drag_and_drop_children, drag_and_drop_visibility]


@callback(Output('map_company_locations', 'children'),
          Input('button_map', 'n_clicks'),
          config_prevent_initial_callbacks=True
          )
def update_company_map(contents):
    fm = Maps.get_folium_map_countries(
        [],
        Maps.read_dict_temp(f'data_loaded_vaude.json')
    )
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

    # else:
    #     return html.Iframe("Empty map!")
