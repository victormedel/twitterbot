import requests
import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

 
# url variable store url 
url = "https://maps.googleapis.com/maps/api/staticmap?"
  
# center defines the center of the map, 
# equidistant from all edges of the map.  
center = "-9.097335,-56.44464"

# zoom defines the zoom 
# level of the map 
zoom = 15
  
# get method of requests module 
# return response object 
r = requests.get(url + "center=" + center + "&zoom=" + str(zoom) + "&size=800x400" + "&maptype=roadmap" +
                "&key=" + cfg['google_static_map']['api_key']) 

  
# wb mode is stand for write binary mode 
f = open('map_results.png', 'wb') 
  
# r.content gives content, 
# in this case gives image 
f.write(r.content) 
  
# close method of file object 
# save and close the file 
f.close() 