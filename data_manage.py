import requests
import json
import pandas as pd
import numpy as np
import geopandas
import folium

publica_con_key ='RB0SBVcmCKdEmsBWcjLTO2vrPYJ8sLYspzizWkcN'
state_fs_num = {
    "02":"AK","01":"AL","05":"AR","60":"AS","04":"AZ","06":"CA",
    "08":"CO","09":"CT","11":"DC","10":"DE","12":"FL","13":"GA",
    "66":"GU","15":"HI","19":"IA","16":"ID","17":"IL","18":"IN",
    "20":"KS","21":"KY","22":"LA","25":"MA","24":"MD","23":"ME",
    "26":"MI","27":"MN","29":"MO","28":"MS","30":"MT","37":"NC",
    "38":"ND","31":"NE","33":"NH","34":"NJ","35":"NM","32":"NV",
    "36":"NY","39":"OH","40":"OK","41":"OR","42":"PA","72":"PR",
    "44":"RI","45":"SC","46":"SD","47":"TN","48":"TX","49":"UT",
    "51":"VA","78":"VI","50":"VT","53":"WA","55":"WI","54":"WV",
    "56":"WY"
}

def switch_fs_let(state_fs_num):
    state_fs_let = dict([[v,k] for k,v in state_fs_num.items()])
    return state_fs_let

def member_dataframe(congress='115',chamber="senate"):
    
    headers = {'X-Api-Key': publica_con_key}
    response = requests.get("https://api.propublica.org/congress/v1/"+congress+"/"+chamber+"/members.json",
                            headers = headers)
    decoded = json.loads(response.text)
    dec = decoded['results'][0]['members']
    print(dec)
    df = pd.DataFrame.from_dict(dec)
    return df


def load_shape(congress):
    if congress == "house":
        geodf = geopandas.read_file("Shapefiles/"+congress+"/cb_2016_us_cd115_500k.shp")
    else:
        geodf = geopandas.read_file("Shapefiles/"+congress+"/states.shp")
        
    geodf['STATEFP_let'] = geodf['STATEFP']
    geodf = geodf.replace({"STATEFP_let": state_fs_num})    
    
    return geodf

def simple_map_html(gdf, outname):
    
    def style_function(feature):
        return {
            'fillColor': 'red',
            'color': 'black',
            'weight': .5
        }
    
    b = folium.Map([40.7, -74],
                   zoom_start=3,
                   tiles='cartodbpositron',
                   world_copy_jump=True,
                   detect_retina = True)
    
    c = folium.GeoJson(gdf,style_function=style_function)
    b.add_child(c)
    b.save(outname)

def member_img(bioguide):
    img_url ="https://theunitedstates.io/images/congress/original/"+ bioguide +".jpg"
    img_data = requests.get(img_url).content
    with open('mem_img/'+bioguide+".jpg", 'wb') as handler:
        handler.write(img_data)











    