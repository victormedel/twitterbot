import what3words
import requests
import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

# get three random words - should be a function


def get_coords(words):
    # convert the words to coordinates - should be a function
    # ToDo: error handling needs to be added
    geocoder = what3words.Geocoder(str(cfg['what3words']['api_key']))
    coords = geocoder.convert_to_coordinates(words)
    return coords

def get_map_url(coords):
    # get image map of coordinates - should be a function
    center = str(coords['coordinates']['lat']) + ',' + str(coords['coordinates']['lng'])
    zoom = 15
    size = "800x400"
    maptype = "roadmap"
    url = "https://maps.googleapis.com/maps/api/staticmap?" + "center=" + center + "&zoom=" + \
        str(zoom) + "&size=" + size + "&maptype=" + maptype + "&key=" + cfg['google_static_map']['api_key']

    img_url = "<img src=" + url + ">"

    # once code is working the below will not be needed
    r = requests.get(url) 

    # wb mode is stand for write binary mode 
    f = open('map_results.png', 'wb') 
    
    # r.content gives content, 
    # in this case gives image 
    f.write(r.content) 
    
    # close method of file object 
    # save and close the file 
    f.close() 

    # SCRIPT SHOULD RETURN IMAGE AND METADETA INFO
    return img_url, 


if __name__ == '__main__':
    words = 'filled.count.soap' # these words will be generated randomly from wordnik
    coords = get_coords(words)
    image_url = get_map_url(coords)
