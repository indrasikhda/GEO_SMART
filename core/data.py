DATA_SOURCES_INVENTORY = [
    {
        "Data Source": "Land Surface Temperature (LST 2025)",
        "Layer": "LST_BARU.tif",
        "Type": "GeoTIFF Raster",
        "Status": "Available",
        "Role": "Thermal anomaly identification & surface temperature baseline"
    },
    {
        "Data Source": "Normalized Difference Veg. Index (NDVI 2025)",
        "Layer": "GEO_SMART_NDVI_2025.tif",
        "Type": "GeoTIFF Raster",
        "Status": "Available",
        "Role": "Vegetation stress & hydrothermal alteration index"
    },
    {
        "Data Source": "Geological Formation & Lithology",
        "Layer": "Geology_Sulut.lyrx",
        "Type": "GIS Layer",
        "Status": "Pending",
        "Role": "Reservoir rock permeability & volcanic unit mapping"
    },
    {
        "Data Source": "Fault & Fracture Lineaments",
        "Layer": "Fault_Traces.shp",
        "Type": "GIS Layer",
        "Status": "Pending",
        "Role": "Primary structural conduit for fluid migration"
    },
    {
        "Data Source": "Geothermal Manifestation Points",
        "Layer": "Manifestations.geojson",
        "Type": "GIS Layer",
        "Status": "Available",
        "Role": "Surface thermal vents, fumaroles, and boiling springs"
    },
    {
        "Data Source": "Lineament Density Grid",
        "Layer": "Lineaments.tif",
        "Type": "GIS Layer",
        "Status": "Pending",
        "Role": "Secondary structural permeability assessment"
    },
    {
        "Data Source": "Hydrothermal Alteration Zones",
        "Layer": "Alteration.shp",
        "Type": "GIS Layer",
        "Status": "Pending",
        "Role": "Kaolinite/smectite alteration mineral mapping"
    },
    {
        "Data Source": "Micro-Seismicity Epicenters",
        "Layer": "Seismicity.geojson",
        "Type": "GIS Layer",
        "Status": "Pending",
        "Role": "Active faulting & fracture network activity"
    },
    {
        "Data Source": "GMN IoT Telemetry Sensors",
        "Layer": "GMN-01 to GMN-03",
        "Type": "IoT Sensors",
        "Status": "Simulated",
        "Role": "Real-time temperature, pH, and EC telemetry stream"
    }
]

METHODS_STEPS = [
    {
        "step": "1. Satellite Data",
        "title": "Multi-Spectral Data Acquisition",
        "desc": "Acquisition of Landsat 8/9 TIRS thermal bands and Sentinel-2 MSI high-resolution optical channels over North Sulawesi."
    },
    {
        "step": "2. Remote Sensing",
        "title": "Thermal & Vegetation Index Extraction",
        "desc": "Calculation of Land Surface Temperature (LST) and Normalized Difference Vegetation Index (NDVI) rasters."
    },
    {
        "step": "3. Geological Evidence",
        "title": "Structural & Geothermal Evidence Integration",
        "desc": "Overlay of fault lineaments, lithological units, thermal vents, and hydrothermal alteration zones."
    },
    {
        "step": "4. FAHP",
        "title": "Fuzzy Analytic Hierarchy Process",
        "desc": "Expert judgement pairwise comparison matrix normalization and consistency ratio (CR < 0.10) verification."
    },
    {
        "step": "5. Weighted Overlay",
        "title": "Spatial Composite Multi-Criteria Analysis",
        "desc": "Multi-criteria spatial weighted overlay summing individual evidence layers multiplied by calculated FAHP weights."
    },
    {
        "step": "6. GPI",
        "title": "Geothermal Prospectivity Index",
        "desc": "Generation of composite prospectivity index map and classification into High, Moderate, and Low prospect zones."
    },
    {
        "step": "7. Priority Zone",
        "title": "Target Zone Identification & Constraints",
        "desc": "Delineation of target exploration sectors filtered by environmental reserve constraints and accessibility."
    },
    {
        "step": "8. GMN Monitoring",
        "title": "Geothermal Monitoring Node Placement",
        "desc": "Deployment of automated IoT nodes (GMN) at high-priority prospect sweet spots for real-time monitoring."
    }
]
