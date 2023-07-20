#!/usr/bin/env python
import json
from pathlib import Path

import matplotlib.pyplot as plt
import osmnx as ox

# define bbox
# data needs to be in format north, south, west, east
bielefeld_campus_north = 52.042408, 52.047661, 8.484921, 8.496294
bielefeld_campus = 52.031162, 52.047687, 8.479815, 8.506250

# define data filter
landuse_tags = {"landuse": True}
buildings_tags = {"building": True}

# load data from OSM
# Roughly comparable Overpass API query:
#   nwr(around:1000,52.039320,8.493118)[landuse];
#   (._;>;);
#   out;
landuse_data = ox.features.features_from_bbox(
    *bielefeld_campus,
    tags=landuse_tags,
)
building_data = ox.features.features_from_bbox(
    *bielefeld_campus,
    tags=buildings_tags,
)
road_data = ox.graph_from_bbox(
    *bielefeld_campus,
    network_type="drive",
)

# prepare colors
with Path("data/osm_color_map.json").open(encoding="utf8") as color_map_file:
    data = json.load(color_map_file)

landuse_color_map = data["landuse"]
landuse_fallback_color = landuse_color_map["default"]
landuse_colors = [
    landuse_color_map.get(x, landuse_fallback_color) for x in landuse_data["landuse"].array
]

building_color_map = data["buildings"]
building_fallback_color = building_color_map["default"]
building_colors = [
    building_color_map.get(x, building_fallback_color) for x in building_data["building"].array
]


# build visualization
fig, axes = plt.subplots()
axes.axis("off")
landuse_data.plot(color=landuse_colors, ax=axes)
building_data.plot(color=building_colors, ax=axes)
ox.plot_graph(road_data, axes, edge_color="#666666", node_color="#666666", node_size=0.5)

# save visualization
fig.savefig("out/bbox_mvp.png", dpi=300, bbox_inches="tight")
