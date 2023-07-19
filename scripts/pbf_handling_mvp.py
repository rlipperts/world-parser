#!/usr/bin/env python
import pyrosm

# create a Pyrosm object
pyrosm_data = pyrosm.OSM("data/Bielefeld.osm.pbf")

# specify the bounding box coordinates
north, south, east, west = 52.037379, 8.481789, 52.048387, 8.498805

# extract the roads, buildings, water bodies, and green spaces as GeoDataFrames
roads = pyrosm_data.get_network(network_type="driving")
roads.plot()

# view the resulting GeoDataFrames
