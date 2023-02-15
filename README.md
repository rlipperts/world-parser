# osm rasterize
_Transform OSM environment data into a grid_

## installation
Currently no pipy release!

### manual
For installation with pip directly from this GitHub repository simply open a terminal and type
```
pip install git+ssh://git@github.com/rlipperts/osm-rasterize.git
``` 

### setup.py
To automatically install the logging configurator with your python package include these lines in your setup.py
```python
install_requires = [
    'world_parser @ git+ssh://git@github.com/rlipperts/world-parser.
                       git@master#egg=world_parser-0.0.0',
],
```
Make sure you update the version in the `egg=world_parser-...` portion to the correct version 
specified in the logging-configurators setup.py. This might not work if you plan on publishing your package on PyPI.

## Overview

1. Spiellogik und -grafik
2. Spielweltgenerierung
3. __Echtwelt Datenaufarbeitung__

## Link Dump

* OSM Data parsing
    * [OSMnx](https://github.com/gboeing/osmnx) to retrieve OSM-data from Overpass API and parso into Geopandas format (but it seems to be focussed on network data)
    *  [Pyrosm](https://pyrosm.readthedocs.io/en/latest/) to parse OSM-data from `.osm.pbf` formatted files into Geopandas format
    *  [Geofabrik](http://download.geofabrik.de/) to obtain `.osm.pbf` data for the whole world (roughly 55GB overall) --> can be obtained by Pyrosm's `get_data()
* Map Transformations
    * For the beginning use whatever [Geopandas](https://geopandas.org/en/stable/docs.html) provides 
    * [Geodesic Grid as alternative to square-based representations?](https://en.wikipedia.org/wiki/Geodesic_grid)
    * [Better square mapping](https://en.wikipedia.org/wiki/Quadrilateralized_spherical_cube)
    * [Geospatial Indexing Tools Overview](https://github.com/sacridini/Awesome-Geospatial#python=)
    * [Quadtree](https://en.wikipedia.org/wiki/Quadtree)
    * [Python Bindings (but: small project)](https://github.com/EL-BID/BabelGrid) for [google s2geometry](http://s2geometry.io/about/overview)
* Tools
    * [Tile Map Editor](https://www.mapeditor.org/)
    * [Overpass Query online interpreter](https://overpass-turbo.eu/)
* Ressources
    * [Tuxemon - open source tiles and pokemon](https://github.com/Tuxemon/Tuxemon/tree/development/mods/tuxemon/gfx/tilesets)
    * [Building outlines in Africa](https://sites.research.google/open-buildings/)
    * [CAD-Files for Building 3D outlines](https://cadmapper.com/) BUT: Not fully open source! Building outlines for large cities can be obtained for free though
* Polygons, Shapes and Points with x, y Coordinates
    * [Map polygons to tiles w/ Geopandas and Shapely](https://www.matecdev.com/posts/point-in-polygon.html)
    * Use [Shapely](https://github.com/shapely/shapely) for general Geometry data stuff (Points, Polygons, Path-Extrusion, ..)
    
## Examples (mostly created with chatgpt and unchecked)

* pyrosm download data and extract certain aspects into geodataframe format
```python
import pyrosm

# create a Pyrosm object
pyrosm_data = pyrosm.OSM("data.osm.pbf")

# specify the bounding box coordinates
north, south, east, west = 52.53, 52.5, 13.4, 13.37

# download the OpenStreetMap data for the bounding box
pyrosm_data.download_pbf(
    filepath="data.osm.pbf",
    north=north, south=south, east=east, west=west
)

# extract the roads, buildings, water bodies, and green spaces as GeoDataFrames
roads_gdf = pyrosm_data.get_network(as_gdf=True)
buildings_gdf = pyrosm_data.get_buildings(as_gdf=True)
water_gdf = pyrosm_data.get_pois("natural", "water", as_gdf=True)
green_gdf = pyrosm_data.get_pois("leisure", ["park", "garden"], as_gdf=True)

# view the resulting GeoDataFrames
print(roads_gdf.head())
print(buildings_gdf.head())
print(water_gdf.head())
print(green_gdf.head())
```
