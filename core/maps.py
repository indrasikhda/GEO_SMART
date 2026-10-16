import folium
from core.io import get_lito_geojson, get_geostruk_geojson

# ════════════════════════════════════════════════════════════
# DYNAMIC GEOLOGICAL & STRUCTURAL COLOR SCHEMES
# ════════════════════════════════════════════════════════════

PASTEL_PALETTE = [
    ("#FED7AA", "#F97316"),  # Apricot / Orange
    ("#E9D5FF", "#9333EA"),  # Lavender / Purple
    ("#BAE6FD", "#0284C7"),  # Sky / Blue
    ("#BBF7D0", "#16A34A"),  # Mint / Green
    ("#FDE68A", "#D97706"),  # Amber / Ochre
    ("#FECDD3", "#E11D48"),  # Rose / Crimson
    ("#DDD6FE", "#7C3AED"),  # Violet
    ("#CCFBF1", "#0D9488"),  # Teal
]


def get_lithology_style(feature):
    """
    Determines dynamic geological color scheme based on formation/rock type:
    - Volcanic/Pyroclastic Rocks: Warm Orange / Terra-cotta
    - Alluvium / Coastal & River: Pale Yellow / Cream
    - Sedimentary / Limestone: Warm Ochre / Khaki Tan
    - Intrusive / Metamorphic: Soft Lavender / Purple Slate
    - Fallback: Unique deterministic pastel tone
    """
    props = feature.get("properties", {})
    name = str(props.get("NAMOBJ", "")).lower()
    remark = str(props.get("REMARK", "")).lower()
    simobj = str(props.get("SIMOBJ", "")).lower()
    text = f"{name} {remark} {simobj}"

    if any(k in text for k in ["gunung", "api", "vulkanik", "volcanic", "andesit", "basal", "breksi", "tuff", "lava", "lahar", "qhv", "tqv", "qvs", "qvt"]):
        fill_color = "#FB923C"  # Terra-cotta / Soft Red-Orange
        border_color = "#EA580C"
    elif any(k in text for k in ["aluvium", "alluvium", "endapan", "pasir", "kerikil", "lumpur", "pantai", "sungai", "rawa", "qa", "holosen"]):
        fill_color = "#FEF08A"  # Pale Yellow / Cream
        border_color = "#CA8A04"
    elif any(k in text for k in ["sedimen", "gamping", "limestone", "lempung", "konglomerat", "formasi", "tps", "tms", "tmb", "terumbu", "koral"]):
        fill_color = "#FCD34D"  # Warm Ochre / Sand
        border_color = "#D97706"
    elif any(k in text for k in ["diorit", "granit", "terobosan", "plutonik", "metamorf", "sekis", "malihan", "intrusif"]):
        fill_color = "#C4B5FD"  # Soft Lavender / Purple
        border_color = "#7C3AED"
    else:
        idx = abs(hash(name or remark or "lito")) % len(PASTEL_PALETTE)
        fill_color, border_color = PASTEL_PALETTE[idx]

    return {
        "fillColor": fill_color,
        "color": border_color,
        "weight": 0.8,
        "fillOpacity": 0.35,
        "opacity": 0.70
    }


def get_geostruk_style(feature):
    """
    Determines structural line styling:
    - Sesar / Fault Utama: Bold 2.5px Dark Crimson Red (#B91C1C) dashed ('6, 6')
    - Kelurusan / Lineament: Thin 1.5px Deep Purple (#7E22CE) dotted-dashed ('4, 4')
    - Other Structures: 1.8px Jet Slate (#0F172A) dashed ('5, 5')
    """
    props = feature.get("properties", {})
    name = str(props.get("NAMOBJ", "")).lower()
    remark = str(props.get("REMARK", "")).lower()
    klsstr = str(props.get("KLSSTR", "")).lower()
    text = f"{name} {remark} {klsstr}"

    if any(k in text for k in ["sesar", "fault", "patahan", "thrust", "geser", "turun", "naik"]):
        return {
            "color": "#B91C1C",      # Dark Crimson Red
            "weight": 2.5,           # Bold 2.5px line
            "dashArray": "6, 6",     # Bold dashed line
            "opacity": 0.90
        }
    elif any(k in text for k in ["kelurusan", "lineament", "rekahan", "joint", "struktur"]):
        return {
            "color": "#7E22CE",      # Deep Purple / Violet
            "weight": 1.5,           # Thinner 1.5px line
            "dashArray": "4, 4",     # Line-dot pattern
            "opacity": 0.85
        }
    else:
        return {
            "color": "#0F172A",      # Jet Slate
            "weight": 1.8,
            "dashArray": "5, 5",
            "opacity": 0.85
        }


def add_geological_layers(
    m: folium.Map,
    lito_data: dict = None,
    geostruk_data: dict = None,
    show_lito: bool = False,
    show_geostruk: bool = False
) -> folium.Map:
    """
    Adds Geology / Lithology and Fault & Lineament GeoJSON datasets to a Folium map.
    Fault & Lineament is placed on top of Lithology polygons.
    Both FeatureGroups have show=False by default for fast lazy rendering via LayerControl.
    """
    if lito_data is None:
        lito_data = get_lito_geojson()
    if geostruk_data is None:
        geostruk_data = get_geostruk_geojson()

    # 1. Geology / Lithology FeatureGroup (Base Polygon Layer)
    if lito_data and lito_data.get("features"):
        fg_lito = folium.FeatureGroup(name="Geology / Lithology", show=show_lito)
        folium.GeoJson(
            lito_data,
            name="Geology / Lithology",
            style_function=get_lithology_style,
            highlight_function=lambda feature: {
                "fillOpacity": 0.60,
                "weight": 1.5,
                "color": "#78350F"
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["NAMOBJ", "REMARK"],
                aliases=["Formation / Unit:", "Lithology:"],
                localize=True,
                sticky=False
            )
        ).add_to(fg_lito)
        fg_lito.add_to(m)

    # 2. Fault & Lineament FeatureGroup (Top Linestring Layer - rendered over polygons)
    if geostruk_data and geostruk_data.get("features"):
        fg_geostruk = folium.FeatureGroup(name="Fault & Lineament", show=show_geostruk)
        folium.GeoJson(
            geostruk_data,
            name="Fault & Lineament",
            style_function=get_geostruk_style,
            highlight_function=lambda feature: {
                "weight": 3.8,
                "color": "#EF4444"           # Bright Red highlight on hover
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["NAMOBJ", "REMARK"],
                aliases=["Structure Type:", "Remark:"],
                localize=True,
                sticky=False
            )
        ).add_to(fg_geostruk)
        fg_geostruk.add_to(m)

    return m


def create_base_map(
    center=[1.35, 124.85],
    zoom=8,
    tile_name=None,
    include_geology: bool = True
) -> folium.Map:
    """
    Creates a multi-basemap Folium Map (OpenStreetMap, Esri Topo, Esri Satellite, CartoDB Positron)
    with scope set to North Sulawesi, along with lazy-loaded Geology and Structural FeatureGroups.
    """
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles=None
    )

    # 1. OpenStreetMap (Standard Base Layer - Primary / Active)
    folium.TileLayer(
        tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors",
        name="OpenStreetMap (Standard)",
        control=True
    ).add_to(m)

    # 2. Esri World Topographic (Topography & Relief)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles &copy; Esri &mdash; Esri, USGS, GIS Community",
        name="Esri World Topographic",
        control=True
    ).add_to(m)

    # 3. Esri World Imagery (Satellite Photo)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles &copy; Esri &mdash; Maxar, Earthstar Geographics",
        name="Esri World Imagery (Satellite)",
        control=True
    ).add_to(m)

    # 4. CartoDB Positron (Clean Light)
    folium.TileLayer(
        tiles="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png",
        attr="&copy; OpenStreetMap contributors &copy; CARTO",
        name="CartoDB Positron (Light)",
        control=True
    ).add_to(m)

    if include_geology:
        add_geological_layers(m, show_lito=False, show_geostruk=False)

    return m



