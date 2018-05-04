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
    
def party_map_html(gdf, outname):
    
    def style_function_rep(feature):
        return {
            'fillColor': 'blue',
            'color': 'black',
            'weight': .5
        }
    
    def style_function_dem(feature):
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
    
    rep = gdf[gdf['party'] == 'R']
    dem = gdf[gdf['party'] == 'D']
    
    rep_map = folium.GeoJson(rep,style_function=style_function_rep)
    dem_map = folium.GeoJson(dem,style_function=style_function_dem)
    
    b.add_child(rep_map)
    b.add_child(dem_map)
    b.save(outname)

def party_map_html_pop(gdf, outname):
    
    html_img = '''
    
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
.card {{
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  max-width: 300px;
  margin: auto;
  text-align: center;
  font-family: arial;
}}

.title {{
  color: grey;
  font-size: 18px;
}}

button {{
  border: none;
  outline: 0;
  display: inline-block;
  padding: 8px;
  color: white;
  background-color: #000;
  text-align: center;
  cursor: pointer;
  width: 100%;
  font-size: 18px;
}}

a {{
  text-decoration: none;
  font-size: 22px;
  color: black;
}}

button:hover, a:hover {{
  opacity: 0.7;
}}
</style>
</head>
<body>
    <div class="card">
      <img src="{}" alt="No image available" style="width:100%">
      <h1>{} {}</h1>
      <p class="title">{}</p>
      <p>{}</p> 
      <a href="https://www.twitter.com/{}"><i class="fa fa-twitter"></i></a> 
      <a href="https://www.facebook.com/{}"><i class="fa fa-facebook-official"></i></a> 
      <a href="https://youtube.com/{}"><i class="fa fa-youtube"></i></a> 
    </div>
</body>
</html>
    '''.format
    
    def style_function_rep(feature):
        return {
            'fillColor': 'blue',
            'color': 'black',
            'weight': .5
        }
    
    def style_function_dem(feature):
        return {
            'fillColor': 'red',
            'color': 'black',
            'weight': .5
        }
    
    b = folium.Map([40.7, -74],
                   zoom_start=4,
                   tiles='cartodbpositron',
                   world_copy_jump=True,
                   detect_retina = True)
    
    rep = gdf[gdf['party'] == 'R']
    dem = gdf[gdf['party'] == 'D']
    
    fg_rep = folium.FeatureGroup(name="Republicans")
    fg_dem = folium.FeatureGroup(name="Democrates")
    
    
    u_id = rep['id'].unique()
    for i_id in u_id:
        #print(i_id)
        rep_map = folium.GeoJson(rep[rep['id']==i_id],style_function=style_function_rep)
        folium.Popup(html_img("mem_img/"+rep[rep['id']==i_id]['id'].min()+".jpg",
                    rep[rep['id']==i_id]['first_name'].min(),
                    str(rep[rep['id']==i_id]['last_name'].min().replace("'"," ")),
                    rep[rep['id']==i_id]['title'].min(),
                    rep[rep['id']==i_id]['party'].min(),
                              rep[rep['id']==i_id]['twitter_account'].min(),
                              rep[rep['id']==i_id]['facebook_account'].min(),
                              rep[rep['id']==i_id]['youtube_account'].min())
                    
                    ).add_to(rep_map)
        rep_map.add_to(fg_rep)
        
    u_id = dem['id'].unique()
    for i_id in u_id:
        #print(i_id)
        dem_map = folium.GeoJson(dem[dem['id']==i_id],style_function=style_function_dem)
        folium.Popup(html_img("mem_img/"+dem[dem['id']==i_id]['id'].min()+".jpg",
                    dem[dem['id']==i_id]['first_name'].min(),
                    str(dem[dem['id']==i_id]['last_name'].min().replace("'"," ")),
                    dem[dem['id']==i_id]['title'].min(),
                    dem[dem['id']==i_id]['party'].min(),
                             dem[dem['id']==i_id]['twitter_account'].min(),
                             dem[dem['id']==i_id]['facebook_account'].min(),
                             dem[dem['id']==i_id]['youtube_account'].min())
                    ).add_to(dem_map)
        dem_map.add_to(fg_dem)
    
    b.add_child(fg_rep)
    b.add_child(fg_dem)
    b.save(outname)    

def member_img(bioguide):
    img_url ="https://theunitedstates.io/images/congress/original/"+ bioguide +".jpg"
    img_data = requests.get(img_url).content
    with open('mem_img/'+bioguide+".jpg", 'wb') as handler:
        handler.write(img_data)











    