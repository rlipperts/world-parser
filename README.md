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
    * [Building 3D geometry generator Buildify for Blender](https://paveloliva.gumroad.com/l/buildify)
* Polygons, Shapes and Points with x, y Coordinates
    * [Map polygons to tiles w/ Geopandas and Shapely](https://www.matecdev.com/posts/point-in-polygon.html)
    * Use [Shapely](https://github.com/shapely/shapely) for general Geometry data stuff (Points, Polygons, Path-Extrusion, ..)
* Inspiration
    * [Moonstone Island](https://store.steampowered.com/app/1658150/Moonstone_Island/)
    * [TemTem](https://store.steampowered.com/app/745920/Temtem/)
* Procedural generation
    * [Wave Function Collapse](https://robertheaton.com/2018/12/17/wavefunction-collapse-algorithm/)
    * [Perlin Noise](https://spin.atomicobject.com/2015/05/03/infinite-procedurally-generated-world/)
    
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

* download data with pyrosm and store in PostGIS database

```python
import pyrosm
import psycopg2

# Connect to PostGIS database
conn = psycopg2.connect(database="my_database", user="my_user", password="my_password", host="localhost", port="5432")

# Create Pyrosm parser object
parser = pyrosm.OsmParser()

# Download OSM data for a bounding box and write it to the PostGIS database
bbox = (xmin, ymin, xmax, ymax)
parser.download_and_parse(bbox, filepath="", db_conn=conn, db_schema="public", db_name="my_database", db_user="my_user", db_password="my_password", db_host="localhost", db_port="5432")
```

* query a postgis database for certain datapoints
```python
import psycopg2
import geopandas as gpd

# Connect to PostGIS database
conn = psycopg2.connect(database="my_database", user="my_user", password="my_password", host="localhost", port="5432")

# Define the bounding box of the area to query
xmin, ymin, xmax, ymax = 8.3719, 51.8963, 8.6752, 52.0902

# Define the OSM tags to query for
building_tags = ['building']
road_tags = ['highway']
tree_tags = ['natural', 'landuse']
leisure_tags = ['leisure']
forest_tags = ['landuse', 'natural']
water_tags = ['water', 'waterway']

# Define the SQL query for each tag
building_query = f"SELECT osm_id, way, building FROM planet_osm_polygon WHERE building IN {tuple(building_tags)} AND ST_Intersects(way, ST_MakeEnvelope({xmin}, {ymin}, {xmax}, {ymax}, 4326))"
road_query = f"SELECT osm_id, way, highway FROM planet_osm_line WHERE highway IN {tuple(road_tags)} AND ST_Intersects(way, ST_MakeEnvelope({xmin}, {ymin}, {xmax}, {ymax}, 4326))"
tree_query = f"SELECT osm_id, way, COALESCE(natural, landuse) AS type FROM planet_osm_polygon WHERE (natural IN {tuple(tree_tags)} OR landuse IN {tuple(tree_tags)}) AND ST_Intersects(way, ST_MakeEnvelope({xmin}, {ymin}, {xmax}, {ymax}, 4326))"
leisure_query = f"SELECT osm_id, way, leisure FROM planet_osm_polygon WHERE leisure IN {tuple(leisure_tags)} AND ST_Intersects(way, ST_MakeEnvelope({xmin}, {ymin}, {xmax}, {ymax}, 4326))"
forest_query = f"SELECT osm_id, way, COALESCE(natural, landuse) AS type FROM planet_osm_polygon WHERE (natural IN {tuple(forest_tags)} OR landuse IN {tuple(forest_tags)}) AND ST_Intersects(way, ST_MakeEnvelope({xmin}, {ymin}, {xmax}, {ymax}, 4326))"
water_query = f"SELECT osm_id, way, COALESCE(water, waterway) AS type FROM planet_osm_polygon WHERE (water IN {tuple(water_tags)} OR waterway IN {tuple(water_tags)}) AND ST_Intersects(way, ST_MakeEnvelope({xmin}, {ymin}, {xmax}, {ymax}, 4326))"

# Execute the SQL queries and load the results into GeoDataFrames
buildings_gdf = gpd.read_postgis(building_query, conn, geom_col='way')
roads_gdf = gpd.read_postgis(road_query, conn, geom_col='way')
trees_gdf = gpd.read_postgis(tree_query, conn, geom_col='way')
leisure_gdf = gpd.read_postgis(leisure_query, conn, geom_col='way')
forests_gdf = gpd.read_postgis(forest_query, conn, geom_col='way')
water_gdf = gpd.read_postgis(water_query, conn, geom_col='way')
``
