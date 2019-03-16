import sys
import openpyxl
import json
import numpy as np
from osmread import parse_file, Way, Node
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def main():
    if (len(sys.argv) != 3):
        print("Usage: main.py [osm file] [geoJson file]")
        return 0

    lons_lats_vect, nodeList = [], []
    count = 1

    book = openpyxl.Workbook()
    sheet = book.active

    with open (sys.argv[2], 'r', encoding='utf-8') as f:
        jsonData = json.load(f)

    for feature in jsonData['features']:
        if feature['geometry']['type'] == 'Polygon':
            lons_lats_vect = np.array(feature['geometry']['coordinates'][0])

    polygon = Polygon(lons_lats_vect)

    print("Parsing Nodes...")
    for entity in parse_file(sys.argv[1]):
        if isinstance(entity, Node):
            nodeAttributes = {}
            nodeAttributes = {'id': entity.id, 'lon': entity.lon, 'lat': entity.lat}
            nodeList.append(nodeAttributes)

    print("Starting...")
    for entity in parse_file(sys.argv[1]):
        if isinstance(entity, Way) and 'addr:housenumber' in entity.tags:
            if entity.tags.get("building") != 'garage':
                lon, lat, first = 0, 0, 0
                last = len(nodeList)-1
                while (True):
                    mid = (first+last)//2
                    if nodeList[mid].get('id') == entity.nodes[0]:
                        lat = nodeList[mid].get('lat')
                        lon = nodeList[mid].get('lon')
                        break
                    elif nodeList[mid].get('id') < entity.nodes[0]:
                        first = mid
                    elif nodeList[mid].get('id') > entity.nodes[0]:
                        last = mid
                point = Point(lon, lat)

                if lat != 0 and polygon.contains(point):
                    sheet['A'+str(count)] = entity.tags.get('addr:city') 
                    sheet['B'+str(count)] = entity.tags.get('addr:street')
                    sheet['C'+str(count)] = entity.tags.get('addr:housenumber')
                    sheet['E'+str(count)] = lat
                    sheet['F'+str(count)] = lon
                    count += 1
                    print(str(count), "found", end='\r')
                else:
                    print("{} {} not there.".format(entity.tags.get('addr:street'), entity.tags.get('addr:housenumber')))
                
    book.save('output.xlsx')
    print("%d found" % count)
    print("Finish.")


if __name__ == "__main__":
    main()