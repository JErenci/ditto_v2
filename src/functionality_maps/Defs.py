
company = {
    'Baumgartner': {
        'name': 'Baumgartner',
        'icon': 'Assets\Baumgartner\Company\icon_transparent.png',
        'web': 'https://www.gaertnerei-baumgartner.de/',
        'address' : 'Höhenstraße 101, 88142 Wasserburg',
        'locations': {
            'Home': {
                'lat': 47.5618,
                'lon': 9.6662,
                'address': 'Enzisweilerstr 19c 88131 Lindau'
                },
            'Lager': {
                'lat': 47.5648,
                'lon': 9.6549,
                'address': 'Höhenstraße 101 \n 88142 Wasserburg'
                },
            },
        'customers': {
            0: {
                'firstname': 'Anna',
                'lastname': 'Smith',
                'path_image_user': f'Assets/Baumgartner/Users/Anna_smith.png'
            }
        },
    },
    'Lindinger' : {
        'name': 'Lindinger',
        'icon': 'Assets\Lindinger\Company\icon_transparent.png',
        'web': 'https://www.lindinger-immobilien.de/',
        'address' : 'Hemigkofener Str. 14 88079 Kressbronn',
        'locations': {
            'Buero': {
                'lat': 47.5964,
                'lon': 9.6017,
                'address': 'Hemigkofener Str. 14 88079 Kressbronn'
            }
        },
        'customers': {
            0: {
                'firstname' : 'Ian',
                'lastname' : 'Dooley',
                'path_image_user': f'Assets/Lindinger/Users/Ian_Dooley.png',
            },
            1:{
                'firstname': 'Joseph',
                'lastname': 'Gonzalez',
                'path_image_user': f'Assets/Lindinger/Users/Joseph_Gonzalez.png',
            },
        },
    },

    'D1TT0': {
        'name': 'D1TT0',
        'icon': 'Assets\D1TT0\Company\icon_transparent.png',
        'web': 'https://www.d1tt0.de/',
        'address': 'Enzisweilertr. 19c, 88131 Lindau',
        'locations': {
            'Home': {
                'lat': 47.5618,
                'lon': 9.6662,
                'address': 'Enzisweilerstr 19c 88131 Lindau'
            },
        },
        'customers': {
            0: {
                'firstname': 'Anna',
                'lastname': 'Smith',
                'path_image_user': f'Assets/Baumgartner/Users/Anna_smith.png'
            }
        },
    },
}


## FILT info

dict_id_bundeslaender = {
    '01':  'Schleswig-Holstein',
    '02':  'Hamburg',
    '03':  'Niedersachsen',
    '04':  'Bremen',
    '05':  'Nordrhein-Westfalen',
    '06':  'Hessen',
    '07':  'Rheinland-Pfalz',
    '08':  'Baden-Württemberg',
    '09':  'Bayern',
    '10': 'Saarland',
    '11': 'Berlin',
    '12': 'Brandenburg',	
    '13': 'Mecklenburg-Vorpommern',
    '14': 'Sachsen',
    '15': 'Sachsen-Anhalt',
    '16': 'Thüringen'
}

dict_bundeslaender_id = {
    'Schleswig-Holstein'    : '01',
    'Hamburg'               : '02',
    'Niedersachsen'         : '03',
    'Bremen'                : '04',
    'Nordrhein-Westfalen'   : '05',
    'Hessen'                : '06',
    'Rheinland-Pfalz'       : '07',
    'Baden-Württemberg'     : '08',
    'Bayern'                : '09',
    'Saarland'              : '10',
    'Berlin'                : '11',
    'Brandenburg'           : '12',
    'Mecklenburg-Vorpommern': '13',
    'Sachsen'               : '14',
    'Sachsen-Anhalt'        : '15',
    'Thüringen'             : '16'
}


color_green  = (0.0, 128.0, 0, 255.0)
color_yellow = (255.0, 255.0, 0, 255.0)
color_red    = (255.0, 0.0, 0, 255.0)
color_blue   = (0.0, 0.0, 255.0, 255.0)
color_orange = (255.0, 165.0, 0.0, 255.0)
color_light_green = (144.0, 238.0, 144.0, 255.0)
color_dark_green = (0.0, 100.0, 0.0, 255.0)

# Define a function to divide a tuple by a divisor
def divide_tuple(color_tuple, divisor):
    return tuple(value / divisor for value in color_tuple)

dict_colors = {
    4 : 'dark_green',
    3 : 'green',
    2 : 'yellow',
    1 : 'orange',
    0 : 'red',
}


dict_tuple_colors = {
    4 : color_dark_green,
    3 : color_green,
    2 : color_yellow,
    1 : color_orange,
    0 : color_red,
}

dict_tuple_colors_norm = {
    4 : divide_tuple(color_dark_green, 255),
    3 : divide_tuple(color_green, 255),
    2 : divide_tuple(color_yellow,255),
    1 : divide_tuple(color_orange,255),
    0 : divide_tuple(color_red,255),
}

# company = {
#     'name': 'Baumgartner',
#     # 'map' : 'company',
#     'icon': 'Assets\Baumgartner\Company\logo.png',
#     'web' : 'https://www.gaertnerei-baumgartner.de/',
#     'locations': {
#         'Home': {
#             'lat': 47.5618,
#             'lon': 9.6662,
#             'address1': 'Enzisweilerstr 19c',
#             'address2': '88131 Lindau'
#         },
#         'Warehouse': {
#             'lat': 47.5641,
#             'lon': 9.6545,
#             'address1': 'Höhenstraße 101',
#             'address2': '88142 Wasserburg'
#         }
#     }
# }



#
# ## PATHS USER ##
#
# ## PATHS CUSTOMER ##
# name_cust = 'Anna_smith'
# path_image_cust = f'Assets/Baumgartner/Customers/{name_cust}.png'
# qr_string_cust = f'{id}_{name_cust}'
#
# ## PATHS COMPANY ##
# path_image_firma = 'Assets/Baumgartner/Company/logo.png'

# qr_string_user  = 'Baumb'
# qr_image_user = '.png'
