import streamlit as st
import core.io as io
import core.maps as maps
import core.raster as raster
import core.data as data
import views.overview as overview
import views.remote_sensing as remote_sensing
import views.evidence as evidence
import views.fahp_gpi as fahp_gpi
import views.priority as priority
import views.monitoring as monitoring
import views.temporal as temporal
import views.methods as methods
import views.data_sources as data_sources

print("All modules imported successfully!")

# Test IO functions
lito = io.get_lito_geojson()
geostruk = io.get_geostruk_geojson()
print("Lito loaded features:", len(lito.get("features", [])))
print("Geostruk loaded features:", len(geostruk.get("features", [])))

# Test Map creation
m = maps.create_base_map()
print("Map created successfully with layers:", [layer.layer_name for layer in m._children.values() if hasattr(layer, 'layer_name')])

# Test direct folder loader
lito_folder = io.load_geojson_folder(io.LITO_DIR)
geostruk_folder = io.load_geojson_folder(io.GEOSTRUK_DIR)
print("load_geojson_folder lito features:", len(lito_folder.get("features", [])))
print("load_geojson_folder geostruk features:", len(geostruk_folder.get("features", [])))
