import dash
from dash import html, dcc
from dash import Input, Output, State, callback
import dash_bootstrap_components as dbc
import base64

import sys, os

sys.path.append('/Users/User/PycharmProjects/ditto_v2/')
from functionality_maps import Maps
from assets import run_relevant_variables
company_name = run_relevant_variables.company_name
file_used = run_relevant_variables.file_used
logging_Home = run_relevant_variables.logging_Home

# from functionality_maps import paths

dash.register_page(__name__, path='/')

if logging_Home:
    print(f'company={company_name}')
    print(f'file_used={file_used}')

companyLogo = 'logo.png'
companyUser = 'user.jpg'

filename_without_extension = os.path.basename(__file__).split('.')[0]

path_to_default_companyLogo = f'assets/{company_name}/{filename_without_extension}/{companyLogo}'
path_to_default_companyUser = f'assets/{company_name}/{filename_without_extension}/{companyUser}'

base64_decoded_company_image = base64.b64encode(open(path_to_default_companyLogo, "rb").read()).decode()
base64_decoded_user_image = base64.b64encode(open(path_to_default_companyUser, "rb").read()).decode()


## 2.b. Components              [comp1 = dcc.Markdown("Hello World!"))]

### ACCOUNT INFORMATION###
comp_text_accountInformation = html.H3('Account Information')
comp_div_accountName = html.Div(id="div_accountName",
    children=[
        dcc.Input(
            id='text_accountName',
            placeholder='Enter the Account name...',
            style={
                'width': '80%',
                'height': '100% '
            },
        ),
        html.Button(
            id='button_edit_accountName',
            children='Save',
            style={
                'width': '20%',
                'height': '100% '
            },
        )
    ],
)
comp_output_accountName = html.Div(id='output_accountName')
comp_drag_and_drop_accountImage = html.Div([
    dcc.Upload(
        id='dragdrop_accountImage',
        children=[
            html.Img(
                src=f'data:image/jpg;base64, {base64_decoded_company_image}',
                style={
                    'width': '100%'
                }
            ),
        ]
    )],)
comp_div_accountImage = html.Div(id='div_accountImage')

## USER INFORMATION ###
comp_text_userInformation = html.H3('User Information')
comp_div_userName = html.Div(id="div_userName",
    children=[
        dcc.Input(
            id='text_userName',
            placeholder='Enter the User name...',
            style={
                'width': '80%',
                'height': '100% '
            },
        ),
        html.Button(
            id='button_edit_userName',
            children='Save',
            style={
                'width': '20%',
                'height': '100% '
            },
        )
    ]
)

comp_output_userName = html.Div(id='output_userName')
comp_div_userImage = html.Div(id='div_userImage',
    # src='../../assets/default_user.jpg'
    # src=dash.get_asset_url('default_user.jpg')
)
comp_drag_and_drop_userImage = html.Div([
    dcc.Upload(id='dragdrop_userImage',
        children=[
            html.Img(
                src=f'data:image/jpg;base64, {base64_decoded_user_image}',
                style={
                    'width': '100%'
                }
            ),
        ]
    )])

# 2.c. Layout                  [app.layout = dbc.Container(comp1)]

comp_colAccountUser = dbc.Col([
    comp_text_accountInformation,
    comp_div_accountName,
    comp_output_accountName,
    comp_drag_and_drop_accountImage,
    comp_div_accountImage,

    comp_text_userInformation,
    comp_div_userName,
    comp_output_userName,
    comp_drag_and_drop_userImage,
    comp_div_userImage,
    ],
    width={'size': 2},
    xs=12, sm=12, md=12, lg=2, xl=2,
)

## COMPANY LOCATIONS
comp_colLocations = dbc.Col([
    html.H3('Location Information'),
    html.Div(html.Button(id='button_map',children='Load map!')),
    html.Div(id='map_company_locations')
    ],
    width={'size': 8},
    xs=12, sm=12, md=12, lg=8, xl=8,
)


row_accountUser = dbc.Row([
    # comp_colUser,
    comp_colAccountUser,
    comp_colLocations
],
    style={
        'height': 30
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
def update_account_name(div_account_name,n_clicks):
    size_div_elems = len(div_account_name)
    if logging_Home:
        print()
        print(f'div_account={div_account_name}')
        print(f'length div = {size_div_elems}')

    if size_div_elems == 2:
        data_input = div_account_name[0]
        data_button = div_account_name[1]['props']

        data_input_props = data_input['props']
    else:
        return dash.no_update

    data_input_type = data_input['type']
    if logging_Home:
        print(f'  data_input={data_input}')
        print(f'  data_button={data_button}')
        print(f'data_input_type={data_input_type}')


    if data_input_type == 'Input':
        data_input_value = data_input_props['value']
        data_button_text = data_button['children']
    elif data_input_type.startswith('H'):
        data_input_value = data_input_props['children']
        data_button_text = data_button['children']
    else:
        data_input_value = 'EMTPY'
        data_button_text = 'EMTPY'

    if logging_Home:
        print(f'   data_input_value={data_input_value}')
        print(f'   data_button_text={data_button_text}')

    children = dash.no_update
    if data_button_text == 'Edit':
        children = [
            dcc.Input(
                id='text_accountName',
                placeholder='Enter the Account name...',
                value=data_input_value,
            ),
            html.Button(
                id='button_edit_accountName',
                children='Save')
        ]
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
    Input('dragdrop_accountImage', 'contents'),
    config_prevent_initial_callbacks=True
)
def update_account_image(contents):
    drag_and_drop_children = [
        html.Img(src=f'data:image/jpg;base64, {base64_decoded_user_image}'),
    ]
    if logging_Home:
        print(f'contents:{contents}')
    if contents is not None:
        drag_and_drop_children = [
            html.Img(src=contents,
                     style={
                         'height': '100%',
                         'width': '100%'
                     }),
        ]
    return drag_and_drop_children


## USER CALLBACKS ##
@callback(
    Output(component_id='div_userName', component_property='children'),
    Input(component_id='div_userName', component_property='children'),
    Input('button_edit_userName', 'n_clicks'),
    config_prevent_initial_callbacks=True
)
def update_user_name(div_user_name, n_clicks):
    size_div_elements = len(div_user_name)
    if logging_Home:
        print()
        print(f'div_account={div_user_name}')
        print(f'length div = {size_div_elements}')

    if size_div_elements == 2:
        data_input = div_user_name[0]
        data_button = div_user_name[1]['props']

        data_input_props = data_input['props']
    else:
        return dash.no_update

    data_input_type = data_input['type']
    if logging_Home:
        print(f'  data_input={data_input}')
        print(f'  data_button={data_button}')
        print(f'data_input_type={data_input_type}')

    if data_input_type == 'Input':
        data_input_value = data_input_props['value']
        data_button_text = data_button['children']
    elif data_input_type.startswith('H'):
        data_input_value = data_input_props['children']
        data_button_text = data_button['children']
    else:
        data_input_value = 'EMTPY'
        data_button_text = 'EMTPY'

    if logging_Home:
        print(f'   data_input_value={data_input_value}')
        print(f'   data_button_text={data_button_text}')

    children = dash.no_update
    if data_button_text == 'Edit':
        children = [
            dcc.Input(
                id='text_userName',
                placeholder='Enter the User name...',
                value=data_input_value,
            ),
            html.Button(
                id='button_edit_userName',
                children='Save')
        ]
    if data_button_text == 'Save':
        children = [
            html.H4(data_input_value),
            html.Button(
                id='button_edit_userName',
                children='Edit')
        ]
    return children


@callback(
    Output('dragdrop_userImage', 'children'),
    Input('dragdrop_userImage', 'contents'),
    config_prevent_initial_callbacks=True
)
def update_user_image(contents):
    drag_and_drop_children = [
        html.Img(src=f'data:image/jpg;base64, {base64_decoded_user_image}')
    ]
    if logging_Home:
        print(f'contents:{contents}')
    if contents is not None:
        drag_and_drop_children = [
            html.Img(src=contents,
                     style={
                         'height': '100%',
                         'width': '100%'
                     }),
        ]
    return drag_and_drop_children


@callback(Output('map_company_locations', 'children'),
          Input('button_map', 'n_clicks'),
          config_prevent_initial_callbacks=True
          )
def update_company_map(contents):
    fm = Maps.get_folium_map_countries(
        [],
        Maps.read_dict_temp(file_used)
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
