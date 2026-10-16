import json
import os
import streamlit as st

GEOJSON_PATH = r"d:\SEMESTER 5\PROJEK\Bahan\GEO_SMART_BATAS_SULUT.geojson"

# ============================================================
# GEOTHERMAL MANIFESTATIONS
# ============================================================
MANIFESTATIONS = [
    {
        "id": "MF-01",
        "name": "Air Madidi (Minahasa Utara)",
        "type": "Hot Spring",
        "lat": 1.428,
        "lng": 124.981,
        "temp": 70.0,
        "status": "REAL"
    },
    {
        "id": "MF-02",
        "name": "Lahendong (Kota Tomohon)",
        "type": "Fumarole",
        "lat": 1.318,
        "lng": 124.832,
        "temp": 95.0,
        "status": "REAL"
    },
    {
        "id": "MF-03",
        "name": "Tompaso (Minahasa)",
        "type": "Hot Spring",
        "lat": 1.233,
        "lng": 124.817,
        "temp": 85.0,
        "status": "REAL"
    },
    {
        "id": "MF-04",
        "name": "Gunung Ambang (Bolaang Mongondow Timur)",
        "type": "Fumarole",
        "lat": 0.760,
        "lng": 124.410,
        "temp": 90.0,
        "status": "REAL"
    },
    {
        "id": "MF-05",
        "name": "Kotamobagu (Bolaang Mongondow)",
        "type": "Hot Spring",
        "lat": 0.720,
        "lng": 124.320,
        "temp": 80.0,
        "status": "REAL"
    },
    {
        "id": "MF-06",
        "name": "Kaleosan - Kalawat (Minahasa Utara)",
        "type": "Hot Spring",
        "lat": 1.460,
        "lng": 124.940,
        "temp": 65.0,
        "status": "REAL"
    },
    {
        "id": "MF-07",
        "name": "Tanggari (Minahasa Utara)",
        "type": "Hot Spring",
        "lat": 1.415,
        "lng": 124.960,
        "temp": 75.0,
        "status": "REAL"
    },
    {
        "id": "MF-08",
        "name": "Wineru (Minahasa Utara)",
        "type": "Hot Spring",
        "lat": 1.620,
        "lng": 125.100,
        "temp": 60.0,
        "status": "REAL"
    },
    {
        "id": "MF-09",
        "name": "Duasudara (Kota Bitung)",
        "type": "Hot Spring",
        "lat": 1.530,
        "lng": 125.150,
        "temp": 68.0,
        "status": "REAL"
    },
    {
        "id": "MF-10",
        "name": "Sangihe (Kepulauan Sangihe)",
        "type": "Hot Spring",
        "lat": 3.600,
        "lng": 125.500,
        "temp": 85.0,
        "status": "REAL"
    }
]

# ============================================================
# PRIORITY ZONES
# ============================================================
PRIORITY_ZONES = [
    {"zone": "PZ-01", "gpi": 0.94, "priority": "High", "area": 4.2, "lat": 1.319, "lng": 124.834, "constraint": "Cleared / Unconstrained", "status": "PROTOTYPE"},
    {"zone": "PZ-02", "gpi": 0.89, "priority": "High", "area": 3.8, "lat": 1.307, "lng": 124.818, "constraint": "Crater Buffer (500m)", "status": "PROTOTYPE"},
    {"zone": "PZ-03", "gpi": 0.85, "priority": "High", "area": 5.1, "lat": 1.335, "lng": 124.862, "constraint": "Agricultural Buffer", "status": "PROTOTYPE"},
    {"zone": "PZ-04", "gpi": 0.81, "priority": "High", "area": 3.5, "lat": 1.295, "lng": 124.845, "constraint": "Cleared / Unconstrained", "status": "PROTOTYPE"},
    {"zone": "PZ-05", "gpi": 0.78, "priority": "High", "area": 4.8, "lat": 1.350, "lng": 124.815, "constraint": "Cleared / Unconstrained", "status": "PROTOTYPE"},
    {"zone": "PZ-06", "gpi": 0.75, "priority": "High", "area": 6.2, "lat": 1.358, "lng": 124.795, "constraint": "Volcanic Hazard Slope B", "status": "PROTOTYPE"},
    {"zone": "PZ-07", "gpi": 0.73, "priority": "Moderate", "area": 4.0, "lat": 1.340, "lng": 124.880, "constraint": "Cleared / Unconstrained", "status": "PROTOTYPE"},
    {"zone": "PZ-08", "gpi": 0.71, "priority": "Moderate", "area": 3.9, "lat": 1.285, "lng": 124.830, "constraint": "Cleared / Unconstrained", "status": "PROTOTYPE"},
    {"zone": "PZ-09", "gpi": 0.69, "priority": "Moderate", "area": 2.8, "lat": 1.310, "lng": 124.850, "constraint": "Urban Buffer (1km)", "status": "PROTOTYPE"},
    {"zone": "PZ-10", "gpi": 0.67, "priority": "Moderate", "area": 5.5, "lat": 1.270, "lng": 124.800, "constraint": "Cleared / Unconstrained", "status": "PROTOTYPE"},
    {"zone": "PZ-11", "gpi": 0.64, "priority": "Moderate", "area": 4.1, "lat": 1.365, "lng": 124.840, "constraint": "Cleared / Unconstrained", "status": "PROTOTYPE"},
    {"zone": "PZ-12", "gpi": 0.61, "priority": "Moderate", "area": 3.6, "lat": 1.355, "lng": 124.890, "constraint": "Agriculture Protection", "status": "PROTOTYPE"}
]

# ============================================================
# GMN — GEOTHERMAL MONITORING NETWORK (11 PARAMETERS)
# ============================================================
GMN_NODES = [
    {
        "id": "GMN-01",
        "name": "Lahendong Thermal Vent Core",
        "lat": 1.319,
        "lng": 124.834,
        "status": "Proposed Node",
        "purpose": "Primary ground-temperature, gas concentration, and environmental monitoring at high-prospect geothermal vent.",
        
        # 11 Parameters
        "shallow_soil_temp": 68.4,
        "deep_soil_temp": 74.2,
        "air_temp": 29.6,
        "air_humidity": 78.2,
        "soil_moisture": 42.5,
        "ph_level": 2.8,
        "ec_meter": 3800,
        "h2s_gas": 14.2,
        "co2_gas": 850,
        "time_source": "DS3231 RTC / GNSS",
        "position": "u-blox NEO-M8N GNSS",
        
        "battery": 94,
        "last_update": "Not deployed"
    },
    {
        "id": "GMN-02",
        "name": "Linow Lake Margin",
        "lat": 1.307,
        "lng": 124.818,
        "status": "Proposed Node",
        "purpose": "Hydrothermal fluid dynamics, acidity, and gas degassing monitoring around Lake Linow.",
        
        # 11 Parameters
        "shallow_soil_temp": 54.2,
        "deep_soil_temp": 61.8,
        "air_temp": 28.9,
        "air_humidity": 81.4,
        "soil_moisture": 47.8,
        "ph_level": 3.1,
        "ec_meter": 4200,
        "h2s_gas": 18.5,
        "co2_gas": 1120,
        "time_source": "DS3231 RTC / GNSS",
        "position": "u-blox NEO-M8N GNSS",
        
        "battery": 88,
        "last_update": "Not deployed"
    },
    {
        "id": "GMN-03",
        "name": "Pangolombian Fault Axis",
        "lat": 1.335,
        "lng": 124.862,
        "status": "Proposed Node",
        "purpose": "Ground-temperature and permeability fluid leakage along the Pangolombian fault zone.",
        
        # 11 Parameters
        "shallow_soil_temp": 42.8,
        "deep_soil_temp": 48.5,
        "air_temp": 27.8,
        "air_humidity": 76.5,
        "soil_moisture": 39.6,
        "ph_level": 6.2,
        "ec_meter": 1950,
        "h2s_gas": 4.1,
        "co2_gas": 410,
        "time_source": "DS3231 RTC / GNSS",
        "position": "u-blox NEO-M8N GNSS",
        
        "battery": 96,
        "last_update": "Not deployed"
    }
]

# ============================================================
# LIGHTWEIGHT GEOJSON LOADERS & DATA PATHS
# ============================================================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
LITO_DIR = os.path.join(DATA_DIR, "lito")
GEOSTRUK_DIR = os.path.join(DATA_DIR, "geostruk")

def _rdp_simplify(points, epsilon=0.0008):
    """Fast Ramer-Douglas-Peucker line simplification in pure Python."""
    if len(points) <= 2:
        return points
    start, end = points[0], points[-1]
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    mag_sq = dx * dx + dy * dy

    max_dist_sq = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        p = points[i]
        if mag_sq == 0:
            dist_sq = (p[0] - start[0]) ** 2 + (p[1] - start[1]) ** 2
        else:
            u = ((p[0] - start[0]) * dx + (p[1] - start[1]) * dy) / mag_sq
            u = max(0.0, min(1.0, u))
            proj_x = start[0] + u * dx
            proj_y = start[1] + u * dy
            dist_sq = (p[0] - proj_x) ** 2 + (p[1] - proj_y) ** 2
        if dist_sq > max_dist_sq:
            max_dist_sq = dist_sq
            index = i

    if (max_dist_sq ** 0.5) > epsilon:
        left = _rdp_simplify(points[:index + 1], epsilon)
        right = _rdp_simplify(points[index:], epsilon)
        return left[:-1] + right
    else:
        return [start, end]

def _simplify_geometry(geom: dict, epsilon: float = 0.0008, precision: int = 4) -> dict:
    """Simplifies polygon/line geometry to drastically reduce JSON payload size for Folium."""
    if not geom or "type" not in geom or "coordinates" not in geom:
        return geom
    gtype = geom["type"]
    coords = geom["coordinates"]

    try:
        if gtype == "LineString":
            simp = _rdp_simplify(coords, epsilon)
            return {"type": gtype, "coordinates": [[round(x, precision), round(y, precision)] for x, y in simp]}
        elif gtype == "MultiLineString":
            simp = [_rdp_simplify(line, epsilon) for line in coords]
            return {"type": gtype, "coordinates": [[[round(x, precision), round(y, precision)] for x, y in line] for line in simp]}
        elif gtype == "Polygon":
            simp_poly = []
            for ring in coords:
                s_ring = _rdp_simplify(ring, epsilon)
                if len(s_ring) < 4:
                    s_ring = ring[:4]
                simp_poly.append([[round(x, precision), round(y, precision)] for x, y in s_ring])
            return {"type": gtype, "coordinates": simp_poly}
        elif gtype == "MultiPolygon":
            simp_mp = []
            for poly in coords:
                poly_simp = []
                for ring in poly:
                    s_ring = _rdp_simplify(ring, epsilon)
                    if len(s_ring) < 4:
                        s_ring = ring[:4]
                    poly_simp.append([[round(x, precision), round(y, precision)] for x, y in s_ring])
                simp_mp.append(poly_simp)
            return {"type": gtype, "coordinates": simp_mp}
    except Exception:
        return geom
    return geom

@st.cache_data(show_spinner=False)
def load_geojson_folder(folder_path: str, simplify: bool = True) -> dict:
    """
    Reads and merges GeoJSON files from a folder into a minimal, high-performance
    FeatureCollection with stripped non-essential metadata and simplified coordinates.
    """
    combined = {
        "type": "FeatureCollection",
        "features": []
    }
    
    if not os.path.exists(folder_path):
        return combined

    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith((".json", ".geojson")):
            filepath = os.path.join(folder_path, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    raw_features = []
                    if data.get("type") == "FeatureCollection" and "features" in data:
                        raw_features = data["features"]
                    elif data.get("type") == "Feature":
                        raw_features = [data]

                    for feat in raw_features:
                        # Extract ONLY minimal essential attributes to keep payload tiny
                        props = feat.get("properties", {})
                        namobj = str(props.get("NAMOBJ") or "").strip()
                        remark = str(props.get("REMARK") or "").strip()
                        klsstr = str(props.get("KLSSTR") or "").strip()
                        simobj = str(props.get("SIMOBJ") or "").strip()

                        minimal_props = {
                            "NAMOBJ": namobj if namobj else "Geological Unit",
                            "REMARK": remark if remark else "No Description",
                            "KLSSTR": klsstr if klsstr else "Structure",
                            "SIMOBJ": simobj
                        }

                        geom = feat.get("geometry", {})
                        if simplify:
                            geom = _simplify_geometry(geom, epsilon=0.0008, precision=4)

                        combined["features"].append({
                            "type": "Feature",
                            "properties": minimal_props,
                            "geometry": geom
                        })
            except Exception:
                pass

    return combined

@st.cache_data(show_spinner=False)
def get_lito_geojson() -> dict:
    """Returns cached lightweight lithology GeoJSON for North Sulawesi."""
    return load_geojson_folder(LITO_DIR, simplify=True)

@st.cache_data(show_spinner=False)
def get_geostruk_geojson() -> dict:
    """Returns cached lightweight fault & lineament GeoJSON for North Sulawesi."""
    return load_geojson_folder(GEOSTRUK_DIR, simplify=True)

def load_sulut_geojson():
    if os.path.exists(GEOJSON_PATH):
        try:
            with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None