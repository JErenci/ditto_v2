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
import dash_bootstrap_components as dbc
import pandas as pd
import dash_auth


#################
### 2. DEFINE ###
#################
## 2.a. App/server              [app = Dash(__name__), server = app.server]
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__,
    # external_stylesheets=external_stylesheets,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}],  # Responsive to MOBILE
    use_pages=True
)
server = app.server
logging = True

## 2.b. Components              [comp1 = dcc.Markdown("Hello World!"))]

### APPLICATION ###
comp_Welcome = html.Div(
    "Data 1s Telling This, 0k?",
    style={'fontSize': 50, 'textAlign': 'center'}
)
comp_Auth = html.H3('You are successfully authorized')

comp_PageReg = html.Div([
    dcc.Link(page['name'] + "  |  ", href=page['path'])
    for page in dash.page_registry.values()
])
comp_separator = html.Hr()
comp_pageCtr = dash.page_container

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
