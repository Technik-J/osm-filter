# Filter OSM files by custom area

This is a tool for extracting address and coordinates of the buildings from .osm file. But OpenStreetMap doesn't allow you to choose custom shape for import, only square shape, so with that tool you can create a shape of the area that you need in Yandex Maps, and it will filter out all the buildings that outside of this shape.

# Usage

First argument should a path to .osm file, second path to the .geojson file from Yandex Maps with the coordinates of the custom shape.

`python main.py [osm file] [geoJson file]`
