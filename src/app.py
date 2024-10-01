#################
### 1. IMPORT ###
#################
## 1.a. IMPORT Libraries               [from dash import Dash]
import dash
from dash import html, dcc
import secret
import dash_auth

# import dash_bootstrap_components as dbc
#
#
# ## 1.b. IMPORT Data
#

################
### 2. BUILD ###
################
## 2.a. Stylesheet              [app = Dash(__name__)]
# pages_foldername = "pages"
# external_stylesheets = [dbc.themes.LUX]
app = dash.Dash(
    __name__,
    use_pages=True
)
server = app.server

def authorization_function(username, password,
                           verbose:bool=False):
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

# Using authorization function
auth = dash_auth.BasicAuth(
    app=app,
    auth_func=authorization_function,
    user_groups=secret.dict_user_groups,
    secret_key="Test"
)

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

# 2.c. Layout                  [app.layout = dbc.Container(comp1)]
app.layout = html.Div(
    [
        comp_Welcome,   # HEADER/App Welcome component
        comp_Auth,      # HEADER/Authorization
        comp_PageReg,   # HEADER/Clickable link within a multi-page app.
        comp_separator, # BODY/Line separating HEADER and BODY
        comp_pageCtr    # PAGE/content of each page
    ]
)

################
## 3. DEFINE ###
################
## 3.a. Variables/server    [pages_foldername = "pages"]

## 3.b. Callback                [@app.callback(Output,Input,State)]

## 3.c. Callback functions      [def function(input)]


# ##############
# ### 4. RUN ###
# ##############
## 4.a. Application             [if __name__ == '__main__': app.run()]
if __name__ == "__main__":
    app.run(
        debug=True,
        port=8051
    )
