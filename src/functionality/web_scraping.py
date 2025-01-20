from urllib.request import urlopen

# pip install beautifulsoup4
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import folium
import folium.plugins

def get_dict_branches(url:str, selected_row:int, logging:bool= False) -> dict:
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.find('h2').get_text())

    className = 'landingpage-text__inner landingpage-text--centered'
    results = soup.find_all('div', {'class': className})

    tag = results[selected_row]
    l_branches = tag.find_all('a')

    l_links = [branch.get('href') for branch in l_branches]
    l_cities = [branch.text for branch in l_branches]
    
    if logging: # l_links
        print(f'length l_links={len(l_links)}')
        print(f'length l_cities={len(l_cities)}')

    output = {}
    for key, value in zip(l_links, l_cities):
        output.setdefault(key, []).append(value)
    
    if logging:
        print(output)
    return output


def find_index(lis:list, substring:str):
    indices = [i for i, element in enumerate(lis) if substring in element.lower()]
    if indices:
        # print(f"Found '{substring}' at indices {indices}")
        return indices[0]
    else:
        # print(f"'{substring}' not found in the list")
        return -1

def get_info_branch(it:int, branch_url:str, location_city:str, selected_row:int, path_logo:str, logging:bool= False) :
    page = urlopen(branch_url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    if logging:
        print(soup.find('h2').get_text())
    
    className = 'landingpage-text__inner landingpage-text--centered'
    results = soup.find_all('div', {'class': className})
    # print(type(results))
    tag = results[selected_row]
    # print(type(tag))
    if logging:
        print(tag.text)
    s2=tag.text.split('\n')
    s2.remove('\xa0')

    # print(f's2={s2}')
    
    idx_start = find_index(s2,'sportscheck')
    end_row = find_index(s2,'mail')

    if idx_start==-1:
        print(f'Invalid start_row={idx_start}')
        return None,None,None
    if end_row == -1:
        print(f'Invalid end_row={start_row}')
        return [None,None,None]

    start_row = idx_start + 1
    address = " ".join(s2[start_row:end_row])
        
    sub_str = ['shopping','center','mall','plaza']
    if any(x in s2[start_row].lower() for x in sub_str):
        print(f'Found mall={s2[start_row]}')
        start_row = start_row + 1
        
    
    # print(f'start_row:{start_row}')
    # print(f'end_row:{end_row}')
        
    address = " ".join(s2[start_row:end_row])
    
    if 'sss' in address:
        address = address.replace("sss", "ss")
        print(f'sss={s2[start_row]}')
    print(f'address={address}')
    
    locator = Nominatim(user_agent="google") # https://github.com/geopy/geopy/tree/master/geopy/geocoders
    location_with_address = locator.geocode(address)
    print(f'  1.location_with_address={location_with_address}')
    
    # print(f'location:{location}')

    location_with_osm = None
    for elem in location_city:
        if elem:
            print(f'elem={elem}')
            osm_address = f'SportScheck {elem}'
            location_with_osm = locator.geocode(osm_address)
            if location_with_osm is not None:
                print(f'location_with_osm={location_with_osm}')
                print(f'Found directly the SportScheck in {elem}')
                continue

    if location_with_address is None:
        print(f'location_with_address invalid={address}')
        location = location_with_osm
    else:
        location = location_with_address

    if location is None:
        print('No Location whatsoever')
        return [None,None,None]
    
    print(f'url={url}')
    print(f'location={location}')
    
    link = f'''<a href={branch_url}>{branch_url}</a>'''

    l_fg_address = folium.FeatureGroup(name=f'[#{it}] SportScheck {location_city}/Address')    
    if location_with_address is not None:
        print(f'  3.location_with_address={location_with_address}')
        points = [[location_with_address.raw['boundingbox'][0],location_with_address.raw['boundingbox'][2]],[location_with_address.raw['boundingbox'][1],location_with_address.raw['boundingbox'][3]]]
        rect = folium.Rectangle(bounds=points, color='#ff7800', fill=True, fill_color='#ffff00', fill_opacity=0.2, 
                                tooltip=location_with_address.address,
                                popup=link)
        l_fg_address.add_child(rect)

    
    l_fg_osm = folium.FeatureGroup(name=f'[#{it}] SportScheck {location_city}/OSM')
    if location_with_osm is not None:
        print(f'  2.location_with_osm={location_with_osm}')
        points = [[location_with_osm.raw['boundingbox'][0],location_with_osm.raw['boundingbox'][2]],[location_with_osm.raw['boundingbox'][1],location_with_osm.raw['boundingbox'][3]]]
        rect_with_city = folium.Rectangle(bounds=points, color='blue', fill=True, fill_color='#ffff00', fill_opacity=0.2, 
                        tooltip=location_with_osm.address,
                        popup=link)
        l_fg_osm.add_child(rect_with_city)
        
    
    l_fg_marker = folium.FeatureGroup(name=f'[#{it}] SportScheck {location_city}/Marker')
    marker = folium.Marker(location=[location.raw['lat'], location.raw["lon"]],
                              tooltip=location.address,
                              popup=link,
                              icon=folium.features.CustomIcon(icon_image=path_logo,
                                                              icon_size=(50, 15)
                                                             )
                              )
    l_fg_marker.add_child(marker)

    return [l_fg_osm,l_fg_address,l_fg_marker]