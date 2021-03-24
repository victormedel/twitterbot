import what3words
import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

# Create API object
geocoder = what3words.Geocoder(str(cfg['what3words']['api_key']))

# Three words to coordinates test
res = geocoder.convert_to_coordinates('bad.girl.white')

print(res['coordinates']['lat'])
print(res['coordinates']['lng'])
print(res['nearestPlace'])