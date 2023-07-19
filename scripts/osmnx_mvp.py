#!/usr/bin/env python
import matplotlib.pyplot as plt
import osmnx as ox

# define bbox
# data needs to be in format north, south, west, east
bielefeld_campus_north = 52.042408, 52.047661, 8.484921, 8.496294
bielefeld_campus = 52.031162, 52.047687, 8.479815, 8.506250

# define data filter
desired_tags = {"landuse": True}

# Loading Data from OSM
# Roughly comparable Overpass API query:
#   nwr(around:1000,52.039320,8.493118)[landuse];
#   (._;>;);
#   out;
data = ox.features.features_from_bbox(
    *bielefeld_campus,
    tags=desired_tags,
)

# color map
color_map = {
    # developed land
    "commercial": "#eecfcf",
    "construction": "#c7c7b4",
    "education": "#000000",
    "fairground": "#000000",
    "industrial": "#e6d1e3",
    "residential": "#fecac5",
    "retail": "#0099ff",
    "institutional": "#000000",
    # rural and agricultural
    "aquaculture": "#000000",
    "allotments": "#cae2c0",
    "farmland": "#eff0d6",
    "farmyard": "#eacca4",
    "flowerbed": "#000000",
    "forest": "#9dca8a",
    "greenhouse_horticulture": "#eff0d6",
    "meadow": "#ceecb1",
    "orchard": "#9edc90",
    "plant_nursery": "#aee0a3",
    "vineyard": "#9edc90",
    # waterbody
    "basin": "#abd4e0",
    "reservoir": "#abd4e0",
    "salt_pond": "#abd4e0",
    # other
    "brownfield": "#c7c7b4",
    "cemetery": "#abccb0",
    "conservation": "#000000",
    "depot": "#000000",
    "garages": "#deddcc",
    "grass": "#ceecb1",
    "greenfield": "#f1eee8",
    "landfill": "b6b690#",
    "miliraty": "#f3e4de",
    "port": "#000000",
    "quarry": "#b7b5b5",
    "railway": "#e6d1e3",
    "recreation_ground": "#e0fce3",
    "religious": "#cecdca",
    "village_green": "#ceecb1",
    "winter_sports": "#000000",
    "user defined": "#000000",
}
colors = [color_map.get(x, "#000000") for x in data["landuse"].array]

# build visualization
fig, axes = plt.subplots()
data.plot(color=colors, ax=axes)
axes.set_title("MVP BBOX Visualization")

# save visualization
fig.savefig("out/bbox_mvp.png")
