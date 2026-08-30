"""
GEO-SMART
Global Data Inventory and Methodological Workflow Definitions

Project:
Geothermal Spatial Intelligence & Monitoring System

Purpose:
Central inventory for data sources, methodological stages,
and prototype status transparency.

Important:
The prototype distinguishes between:
- REAL DATA
- LITERATURE-INFORMED
- CALCULATED
- PROPOSED
- SIMULATED
- PENDING
- FUTURE STAGE
"""

# ============================================================
# DATA SOURCES INVENTORY
# ============================================================

DATA_SOURCES_INVENTORY = [

    # --------------------------------------------------------
    # REMOTE SENSING — REAL DATA
    # --------------------------------------------------------

    {
        "Data Source": "Land Surface Temperature (LST 2025)",
        "Layer": "LST_BARU.tif",
        "Type": "GeoTIFF Raster",
        "Source": "Satellite / GEE-derived",
        "Status": "REAL",
        "Role": (
            "Thermal anomaly identification and "
            "surface thermal baseline evidence"
        ),
    },

    {
        "Data Source": "Normalized Difference Vegetation Index (NDVI 2025)",
        "Layer": "GEO_SMART_NDVI_2025.tif",
        "Type": "GeoTIFF Raster",
        "Source": "Satellite / GEE-derived",
        "Status": "REAL",
        "Role": (
            "Vegetation stress and environmental "
            "baseline supporting evidence"
        ),
    },

    # --------------------------------------------------------
    # MULTI-SOURCE EVIDENCE
    # --------------------------------------------------------

    {
        "Data Source": "Geothermal Manifestation Points",
        "Layer": "Manifestations.geojson",
        "Type": "Vector Point",
        "Source": "Geological Survey / Field Inventory",
        "Status": "REAL",
        "Role": (
            "Surface geothermal indicators including "
            "hot springs, fumaroles, and thermal manifestations"
        ),
    },

    {
        "Data Source": "Geology / Lithological Units",
        "Layer": "data/lito/*.json (15 Districts)",
        "Type": "Vector Polygon",
        "Source": "Regional Geological Map (Sulawesi Utara)",
        "Status": "REAL",
        "Role": (
            "Lithological evidence representing volcanic "
            "host rocks and potential reservoir formations"
        ),
    },

    {
        "Data Source": "Hydrothermal Alteration Zones",
        "Layer": "Alteration.shp",
        "Type": "Vector Polygon",
        "Source": "Geological / Remote Sensing Analysis",
        "Status": "PENDING",
        "Role": (
            "Evidence of hydrothermal mineral alteration "
            "associated with geothermal systems"
        ),
    },

    {
        "Data Source": "Fault & Lineament Structures",
        "Layer": "data/geostruk/*.json (10 Districts)",
        "Type": "Vector LineString",
        "Source": "Structural Geology Survey (Sulawesi Utara)",
        "Status": "REAL",
        "Role": (
            "Structural permeability and potential "
            "fluid migration pathways"
        ),
    },

    # --------------------------------------------------------
    # LITERATURE-INFORMED DECISION MODEL
    # --------------------------------------------------------

    {
        "Data Source": "Preliminary FAHP Weights",
        "Layer": "Literature-Informed FAHP Matrix",
        "Type": "Fuzzy Decision Model",
        "Source": "Şener & Şener (2021)",
        "Status": "LITERATURE-INFORMED",
        "Role": (
            "Preliminary criterion weighting prior to "
            "local expert validation"
        ),
    },

    # --------------------------------------------------------
    # STANDARDIZED EVIDENCE
    # --------------------------------------------------------

    {
        "Data Source": "Standardized Evidence Layers",
        "Layer": "0–1 Evidence Scores",
        "Type": "Standardized Spatial Criteria",
        "Source": "Evidence-specific normalization rules",
        "Status": "METHODOLOGICAL FRAMEWORK",
        "Role": (
            "Transformation of heterogeneous evidence "
            "into comparable 0–1 prospectivity scores"
        ),
    },

    # --------------------------------------------------------
    # GPI
    # --------------------------------------------------------

    {
        "Data Source": "Geothermal Prospectivity Index (GPI)",
        "Layer": "Spatial Weighted Overlay",
        "Type": "Composite Spatial Index",
        "Source": (
            "FAHP-derived weights + standardized "
            "multi-source evidence"
        ),
        "Status": "PRELIMINARY",
        "Role": (
            "Spatial representation of relative geothermal "
            "prospectivity"
        ),
    },

    # --------------------------------------------------------
    # PRIORITY ZONES
    # --------------------------------------------------------

    {
        "Data Source": "Priority Exploration Zones",
        "Layer": "PZ-01 to PZ-12",
        "Type": "Spatial Target Zones",
        "Source": (
            "GPI prospectivity + spatial constraint concept"
        ),
        "Status": "PRELIMINARY",
        "Role": (
            "Candidate areas for prioritized geothermal "
            "exploration and monitoring"
        ),
    },

    # --------------------------------------------------------
    # GMN
    # --------------------------------------------------------

    {
        "Data Source": "Geothermal Monitoring Network (GMN)",
        "Layer": "GMN-01 to GMN-03",
        "Type": "Spatial Monitoring Nodes",
        "Source": "Prototype Node Placement",
        "Status": "PROPOSED",
        "Role": (
            "Proposed monitoring locations within "
            "priority exploration areas"
        ),
    },

    # --------------------------------------------------------
    # IoT
    # --------------------------------------------------------

    {
        "Data Source": "IoT Ground Telemetry",
        "Layer": "Sensor Telemetry Stream",
        "Type": "Time Series / Telemetry",
        "Source": "Prototype IoT Architecture",
        "Status": "SIMULATED",
        "Role": (
            "Demonstration of continuous temperature, "
            "pH, EC, and system-status monitoring"
        ),
    },

]


# ============================================================
# CURRENT FAHP CRITERIA
# ============================================================

CURRENT_FAHP_CRITERIA = [

    {
        "id": "manifestation",
        "name": "Geothermal Manifestation",
        "weight": 0.447,
        "status": "LITERATURE-INFORMED",
    },

    {
        "id": "geology",
        "name": "Geology / Lithology",
        "weight": 0.273,
        "status": "LITERATURE-INFORMED",
    },

    {
        "id": "alteration",
        "name": "Hydrothermal Alteration",
        "weight": 0.149,
        "status": "LITERATURE-INFORMED",
    },

    {
        "id": "lineament",
        "name": "Fault & Lineament Density",
        "weight": 0.079,
        "status": "LITERATURE-INFORMED",
    },

    {
        "id": "lst",
        "name": "Land Surface Temperature",
        "weight": 0.052,
        "status": "LITERATURE-INFORMED",
    },

]


# ============================================================
# SUPPORTING EVIDENCE
# ============================================================

SUPPORTING_EVIDENCE = [

    {
        "id": "ndvi",
        "name": "NDVI",
        "status": "REAL",
        "role": (
            "Supporting environmental and vegetation "
            "stress evidence"
        ),
    },

]


# ============================================================
# METHODOLOGICAL WORKFLOW
# ============================================================

METHODS_STEPS = [

    # --------------------------------------------------------
    # 1. REMOTE SENSING
    # --------------------------------------------------------

    {
        "step": "1. Remote Sensing",

        "title": "Satellite Thermal & Optical Acquisition",

        "desc": (
            "Acquisition and processing of satellite-derived "
            "Land Surface Temperature (LST) and Normalized "
            "Difference Vegetation Index (NDVI) over the "
            "target geothermal area."
        ),

        "status": "REAL DATA",
    },

    # --------------------------------------------------------
    # 2. MULTI-SOURCE EVIDENCE
    # --------------------------------------------------------

    {
        "step": "2. Multi-Source Evidence",

        "title": "Spatial Evidence Layer Integration",

        "desc": (
            "Compilation of geothermal manifestations, "
            "geology/lithology, hydrothermal alteration, "
            "fault and lineament density, and LST as the "
            "five current weighted criteria. NDVI is retained "
            "as supporting environmental evidence."
        ),

        "status": "REAL / PENDING INTEGRATION",
    },

    # --------------------------------------------------------
    # 3. LITERATURE-INFORMED FAHP
    # --------------------------------------------------------

    {
        "step": "3. Literature-Informed Preliminary FAHP",

        "title": "Preliminary Criteria Weighting",

        "desc": (
            "A literature-informed preliminary fuzzy "
            "pairwise comparison framework based on "
            "Şener & Şener (2021) is used to establish "
            "initial criterion weights before future "
            "local expert validation."
        ),

        "status": "LITERATURE-INFORMED",
    },

    # --------------------------------------------------------
    # 4. STANDARDIZED SUBCRITERIA
    # --------------------------------------------------------

    {
        "step": "4. Standardized Subcriteria",

        "title": "Evidence Normalization to 0–1",

        "desc": (
            "Each evidence layer is transformed into a "
            "comparable 0–1 prospectivity scale using "
            "criterion-specific normalization and "
            "proximity/anomaly rules."
        ),

        "status": "METHODOLOGICAL FRAMEWORK",
    },

    # --------------------------------------------------------
    # 5. WEIGHTED OVERLAY + GPI
    # --------------------------------------------------------

    {
        "step": "5. Weighted Overlay & GPI",

        "title": "Geothermal Prospectivity Index",

        "desc": (
            "Standardized evidence scores are combined "
            "using the preliminary FAHP weights according "
            "to GPI(x,y) = Σ [wi × Si(x,y)]."
        ),

        "status": "PRELIMINARY CALCULATION",
    },

    # --------------------------------------------------------
    # 6. PRIORITY ZONES
    # --------------------------------------------------------

    {
        "step": "6. Priority Zones",

        "title": "Exploration Priority Delineation",

        "desc": (
            "Potential exploration targets are derived "
            "from geothermal prospectivity and subsequently "
            "considered together with spatial constraints "
            "such as environmental sensitivity, hazards, "
            "and accessibility."
        ),

        "status": "PRELIMINARY TARGETING",
    },

    # --------------------------------------------------------
    # 7. GMN
    # --------------------------------------------------------

    {
        "step": "7. GMN Node Placement",

        "title": "Proposed Geothermal Monitoring Network",

        "desc": (
            "Proposed monitoring nodes are positioned "
            "within selected priority areas to establish "
            "a conceptual ground-monitoring network."
        ),

        "status": "PROPOSED",
    },

    # --------------------------------------------------------
    # 8. IoT
    # --------------------------------------------------------

    {
        "step": "8. IoT Ground Monitoring",

        "title": "Continuous Ground Telemetry",

        "desc": (
            "The prototype demonstrates the expected "
            "IoT monitoring architecture for temperature, "
            "pH, electrical conductivity, and system "
            "status. Current telemetry is simulated."
        ),

        "status": "SIMULATED TELEMETRY",
    },

    # --------------------------------------------------------
    # 9. TEMPORAL ANALYSIS
    # --------------------------------------------------------

    {
        "step": "9. Temporal Analysis",

        "title": "Spatial–Temporal Monitoring",

        "desc": (
            "Temporal analysis is designed to compare "
            "changes in satellite-derived environmental "
            "indicators and future GMN ground observations "
            "over time."
        ),

        "status": "DEMONSTRATION / FUTURE DATA",
    },

    # --------------------------------------------------------
    # 10. DECISION SUPPORT + EXPERT VALIDATION
    # --------------------------------------------------------

    {
        "step": "10. Decision Support & Expert Validation",

        "title": "Future Local Expert Validation",

        "desc": (
            "The preliminary literature-informed model "
            "provides a decision-support framework. "
            "Future implementation will incorporate "
            "local multi-expert judgement, Delphi/AHP "
            "validation, and field verification."
        ),

        "status": "FUTURE VALIDATION",
    },

    # --------------------------------------------------------
    # 11. NET ZERO
    # --------------------------------------------------------

    {
        "step": "11. Net Zero Contribution",

        "title": "Sustainable Geothermal Development",

        "desc": (
            "GEO-SMART supports geothermal development "
            "by improving spatial targeting, reducing "
            "unnecessary exploration activities, and "
            "enabling continuous environmental and "
            "geothermal monitoring."
        ),

        "status": "STRATEGIC IMPACT",
    },

]