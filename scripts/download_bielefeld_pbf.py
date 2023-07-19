#!/usr/bin/env python
import pyrosm

bielefeld_data = pyrosm.get_data("Bielefeld", update=True, directory="data")
