import folium

# company['icon']= f'Assets\{company["name"]}\Company\logo.png'


path_map_empty ='./assets/Geo/Map_empty.html'
path_wca='./assets/Geo/world_country_area.csv'
stores = 'pdf_all_stores.json'

d_stores_logo = {
    'sportscheck' : 'assets/SportScheck/1_Home/logo.png',
    'decathlon' : 'assets/Decathlon/1_Home/Decathlon_Logo.jpg',
    'intersport' : 'assets/Intersport/1_Home/logo.jpg'
}

fields_wca=['ADMIN',	'ISO_A3',	'Area_total_km2']
aliases_wca=['Code','Country','Area [km\u00b2]']

## MAPBOX ##

## CartoDB ##
layer_cartodb = [folium.TileLayer(tiles='CartoDB positron')]

## Openstreetmap ##
layer_openstreet = [folium.TileLayer('openstreetmap')]

## Mapbox ##
mapbox_token = 'pk.eyJ1Ijoiam9ndWVycmVybyIsImEiOiJjbGNmdng1dmEwOGRoM29xdTZxbXFtZWw2In0.T8KtUQv-OlNDyt3-mstJxg'
mapbox_style_streets = 'streets-v12' # Select one of this list ['outdoors-v12', 'light-v11', 'dark-v11', ...] https://docs.mapbox.com/api/maps/styles/
mapbox_style_sat_streets = 'satellite-streets-v12' # Select one of this list ['outdoors-v12', 'light-v11', 'dark-v11', ...] https://docs.mapbox.com/api/maps/styles/
l_mapbox_tile_style = [mapbox_style_streets, mapbox_style_sat_streets]
l_mapbox_api_calls  = [f'https://api.mapbox.com/styles/v1/mapbox/{mapbox_tile}/tiles/{{z}}/{{x}}/{{y}}' for
                        mapbox_tile in l_mapbox_tile_style]
l_mapbox_tile_names = ['streets', 'Satellite and streets']

layers_mapbox = [folium.TileLayer(tiles=f'{x}?access_token={mapbox_token}',
                                               name=y,#'Mapbox',
                                               attr='mapbox attr'
                                               ) for x,y in
                      zip(l_mapbox_api_calls, l_mapbox_tile_names)]


l_tilelayer = layer_openstreet
new_filed = ' Test '

l_d_dropdown_map = ['Country', 'State', 'Region', 'District', 'Locality']
l_d_dropdown_country = 'Deutschland'

d_map_gadm_name = {
    'D1' : 'Country', 
    'D2' : 'State', 
    'D3' : 'Region', 
    'D4' : 'District', 
    'ZIP': 'Locality'
}
# l_d_dropdown_world =   ['DEU', 'ESP', 'ITA', 'CHE', 'USA']

# csv = {
#     l_d_dropdown_map[0]: f'./assets/Geo/Germany/D0_{l_d_dropdown_country}_{l_d_dropdown_map[0]}.csv',
#     l_d_dropdown_map[1]: f'./assets/Geo/Germany/D1_{l_d_dropdown_country}_{l_d_dropdown_map[1]}.csv',
#     l_d_dropdown_map[2]: f'./assets/Geo/Germany/D2_{l_d_dropdown_country}_{l_d_dropdown_map[2]}.csv',
#     l_d_dropdown_map[3]: f'./assets/Geo/Germany/D3_{l_d_dropdown_country}_{l_d_dropdown_map[3]}.csv',
#     l_d_dropdown_map[4]: f'./assets/Geo/Germany/D4_{l_d_dropdown_country}_{l_d_dropdown_map[4]}.csv'
# }

csv = {
    l_d_dropdown_map[0]: f'./assets/Geo/Germany/D1_{l_d_dropdown_country}_{l_d_dropdown_map[0]}_clean.csv',
    l_d_dropdown_map[1]: f'./assets/Geo/Germany/D2_{l_d_dropdown_country}_{l_d_dropdown_map[1]}_clean.csv',
    l_d_dropdown_map[2]: f'./assets/Geo/Germany/D3_{l_d_dropdown_country}_{l_d_dropdown_map[2]}_clean.csv',
    l_d_dropdown_map[3]: f'./assets/Geo/Germany/D4_{l_d_dropdown_country}_{l_d_dropdown_map[3]}_clean.csv',
    l_d_dropdown_map[4]: f'./assets/Geo/Germany/ZIP_{l_d_dropdown_country}_{l_d_dropdown_map[4]}_clean.csv'
}

fields = {
    l_d_dropdown_map[0]: ['ISO','NAME_ENGLI'],
    l_d_dropdown_map[1]: ['id','name'],
    l_d_dropdown_map[2]: ['NAME_0','NAME_1', 'NAME_2'],
    l_d_dropdown_map[3]: ['NAME_0', 'NAME_1', 'NAME_2', 'NAME_3'],
    l_d_dropdown_map[4]: ['postcode', 'locality']
}

aliases = {
    l_d_dropdown_map[0]: ['Code', 'Country'],
    l_d_dropdown_map[1]: ['ID', 'Bundesland'],
    l_d_dropdown_map[2]: ['Country', 'Bundesland', 'Bezirk'],
    l_d_dropdown_map[3]: ['Country', 'Bundesland', 'Bezirk', 'Kreis'],
    l_d_dropdown_map[4]: ['Locality/ZIP', 'Name']
}
