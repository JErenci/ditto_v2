#################
### 1. IMPORT ###
#################
## 1.a. Libraries               [from dash import Dash]
import base64
import datetime
import io

import dash
from dash import html, dcc
import secret
from dash import Input, Output, State, callback, dash_table
import pandas as pd
import dash_auth

#################
### 2. DEFINE ###
#################
## 2.a. App/server              [app = Dash(__name__), server = app.server]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    use_pages=True
)
server = app.server
logging = True

## 2.b. Components              [comp1 = dcc.Markdown("Hello World!"))]
comp_Welcome = html.Div(
    "D1tt0",
    style={'fontSize': 50, 'textAlign': 'center'}
)
comp_Auth = html.H3('You are successfully authorized')
comp_PageReg = html.Div([
    dcc.Link(page['name'] + "  |  ", href=page['path'])
    for page in dash.page_registry.values()
])
comp_separator = html.Hr()
comp_pageCtr = dash.page_container
comp_upload = dcc.Upload(
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
    # Allow multiple files to be uploaded
    multiple=True
)

# 2.c. Layout                  [app.layout = dbc.Container(comp1)]
app.layout = html.Div(
    [
        comp_Welcome,  # HEADER/App Welcome component
        comp_Auth,  # HEADER/Authorization
        comp_PageReg,  # HEADER/Clickable link within a multi-page app.
        comp_separator,  # BODY/Line separating HEADER and BODY
        comp_pageCtr  # PAGE/content of each page
    ]
)


def parse_contents(contents, filename, date, logging: bool = False):
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
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        im,
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        }),
    ]

    return html.Div(div)


## 2.d. Functions               [def function(input)]
def authorization_function(username, password,
                           verbose: bool = False):
    if verbose:
        print(f'username:{username}, password:{password}')

    if username in list(secret.VALID_USERNAME_PASSWORD_PAIRS.keys()):
        if verbose:
            print('Valid key')
        if password == secret.VALID_USERNAME_PASSWORD_PAIRS[username]:
            if verbose:
                print('Valid key-value-pair')
            return True
    else:
        return False


## 2.f. Logic                   []
# Using authorization function
auth = dash_auth.BasicAuth(
    app=app,
    auth_func=authorization_function,
    user_groups=secret.dict_user_groups,
    secret_key="Test"
)

# ##############
# ### 3. RUN ###
# ##############
## 3.a. Application             [if __name__ == '__main__': app.run()]
if __name__ == "__main__":
    app.run(
        debug=True,
        port=8051
    )
