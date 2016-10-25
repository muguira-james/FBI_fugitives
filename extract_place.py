import json
import geocoder


fileName = 'fbi_db.json'
fin = open(fileName, 'rb')

print 'lat,lng,POB,Weight,Name'
for el in fin:
    js = json.loads(el)
    if 'Place of Birth' not in js:
        continue
    #print '{} {}'.format(js['Place of Birth'], js['name'])
    g = geocoder.google(js['Place of Birth'])
    if g.latlng:
        lat = g.latlng[0]
        lng = g.latlng[1]
    else:
        lat = 0.0
        lng = 0.0
    if 'Weight' in js:
        weight = js['Weight']
    else:
        weight = 0
    print '{},{},\"{}\",\"{}\",\"{}\"'.format(
        lat, lng, js['Place of Birth'], weight, js['name'])
