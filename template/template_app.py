#################
### 1. IMPORT ###
#################
## 1.a. IMPORT Libraries               [from dash import Dash]
import dash
from dash import html, dcc

## 1.b. IMPORT Data


################
### 2. BUILD ###
################
## 2.a. Stylesheet              [app = Dash(__name__)]
app = dash.Dash(
    __name__,
    use_pages=True
)

## 2.b. Components              [comp1 = dcc.Markdown("Hello World!"))]
comp_Welcome = html.Div("Template")
comp_PageReg = html.Div([
    dcc.Link(page['name'] + "  |  ", href=page['path'])
    for page in dash.page_registry.values()
])
comp_separator = html.Hr()
comp_pageCtr = dash.page_container



# 2.c. Layout                  [app.layout = dbc.Container(comp1)]
app.layout = html.Div(
    [
        comp_Welcome,       # HEADER/Top component
        comp_PageReg,       # HEADER/Clickable link within a multi-page app.
        comp_separator,     # BODY/Line separating HEADER and BODY
        comp_pageCtr        # PAGE/content of each page
    ]
)


# #################
# ### 3. DEFINE ###
# #################
# # ## 3.a. Variables/server    [pages_foldername = "pages"]
# # pages_foldername = "pages"
# # VALID_USERNAME_PASSWORD_PAIRS = {
# #     'Baumgartner': 'garten',
# #     'Lindinger'  : 'immo',
# #     'D1TT0'      : 'ditto',
# # }
# #
# # server = app.server
#
#
# ## 3.b. Callback                [@app.callback(Output,Input,State)]
#
# ## 3.c. Callback functions      [def function(input)]
# ##############
# ### 4. RUN ###
# ##############
# ## 4.a. Application             [if __name__ == '__main__': app.run()]
# if __name__ == "__main__":
#     app.run(port=8051)
#
#
#
# ## DECLARATIONS ##
#
#
# # external_stylesheets = [ 'https://codepen.io/chriddyp/pen/bWLwgP.css']
#
#
# # pages_folder=os.path.join(os.path.dirname(__name__), pages_foldername)
# # print(pages_foldername)
#
#
# # ## AUTHENTICATION ##
# # auth = dash_auth.BasicAuth(
# #     app,
# #     VALID_USERNAME_PASSWORD_PAIRS
# # )
# # print(f'2{pages_foldername}')
#
# # LAYOUT (pages) ##
# #
# # ## LAYOUT (authentication) ##
# # app.layout = html.Div([
# #     # html.H1(f'Welcome to the App, You are successfully authorized!'),
# #     html.Div([
# #         dcc.Link(page['name'] + "  |  ", href=page['path'])
# #         for page in dash.page_registry.values()
# #     ]),
# #     html.Hr(),
# #     dash.page_container
# #
# # ], className='container')
# #
# # print(f'4{pages_foldername}')
# #

if __name__ == "__main__":
    app.run(
        debug=True,
        port=8051
    )