import json
import os

GEOJSON_PATH = r"d:\SEMESTER 5\PROJEK\Bahan\GEO_SMART_BATAS_SULUT.geojson"

MANIFESTATIONS = [
    {"id": "MF-01", "name": "Lahendong Fumarole Cluster A", "type": "Fumarole Field", "lat": 1.318, "lng": 124.832, "temp": 96.5, "ph": 2.8, "ec": 3800},
    {"id": "MF-02", "name": "Lake Linow Boiling Springs", "type": "Hot Spring & Mud Pool", "lat": 1.309, "lng": 124.821, "temp": 88.2, "ph": 3.1, "ec": 4200},
    {"id": "MF-03", "name": "Pangolombian Thermal Stream", "type": "Thermal Pool", "lat": 1.332, "lng": 124.858, "temp": 72.4, "ph": 6.2, "ec": 1950},
    {"id": "MF-04", "name": "Kasuratan Warm Spring", "type": "Warm Spring", "lat": 1.348, "lng": 124.811, "temp": 48.0, "ph": 6.8, "ec": 920},
    {"id": "MF-05", "name": "Tondangow Solfatara", "type": "Solfatara Vents", "lat": 1.298, "lng": 124.841, "temp": 94.1, "ph": 2.4, "ec": 4600}
]

PRIORITY_ZONES = [
    {"zone": "PZ-01", "gpi": 0.94, "priority": "High", "area": 4.2, "lat": 1.319, "lng": 124.834, "constraint": "Cleared"},
    {"zone": "PZ-02", "gpi": 0.89, "priority": "High", "area": 3.8, "lat": 1.307, "lng": 124.818, "constraint": "Crater Buffer"},
    {"zone": "PZ-03", "gpi": 0.85, "priority": "High", "area": 5.1, "lat": 1.335, "lng": 124.862, "constraint": "Agriculture"},
    {"zone": "PZ-04", "gpi": 0.81, "priority": "High", "area": 3.5, "lat": 1.295, "lng": 124.845, "constraint": "Cleared"},
    {"zone": "PZ-05", "gpi": 0.78, "priority": "High", "area": 4.8, "lat": 1.350, "lng": 124.815, "constraint": "Cleared"},
    {"zone": "PZ-06", "gpi": 0.75, "priority": "High", "area": 6.2, "lat": 1.358, "lng": 124.795, "constraint": "Volcanic Hazard Slope B"},
    {"zone": "PZ-07", "gpi": 0.73, "priority": "Moderate", "area": 4.0, "lat": 1.340, "lng": 124.880, "constraint": "Cleared"},
    {"zone": "PZ-08", "gpi": 0.71, "priority": "Moderate", "area": 3.9, "lat": 1.285, "lng": 124.830, "constraint": "Cleared"},
    {"zone": "PZ-09", "gpi": 0.69, "priority": "Moderate", "area": 2.8, "lat": 1.310, "lng": 124.850, "constraint": "Urban Buffer"},
    {"zone": "PZ-10", "gpi": 0.67, "priority": "Moderate", "area": 5.5, "lat": 1.270, "lng": 124.800, "constraint": "Cleared"},
    {"zone": "PZ-11", "gpi": 0.64, "priority": "Moderate", "area": 4.1, "lat": 1.365, "lng": 124.840, "constraint": "Cleared"},
    {"zone": "PZ-12", "gpi": 0.61, "priority": "Moderate", "area": 3.6, "lat": 1.355, "lng": 124.890, "constraint": "Agriculture Protection"}
]

GMN_NODES = [
    {
        "id": "GMN-01",
        "name": "Lahendong Thermal Vent Core",
        "lat": 1.319, "lng": 124.834,
        "status": "Online",
        "temp": 68.4, "ph": 3.25, "ec": 3840, "battery": 94
    },
    {
        "id": "GMN-02",
        "name": "Linow Lake Margin",
        "lat": 1.307, "lng": 124.818,
        "status": "Online",
        "temp": 54.2, "ph": 2.85, "ec": 4120, "battery": 88
    },
    {
        "id": "GMN-03",
        "name": "Pangolombian Fault Axis",
        "lat": 1.335, "lng": 124.862,
        "status": "Online",
        "temp": 42.8, "ph": 6.45, "ec": 1880, "battery": 96
    }
]

def load_sulut_geojson():
    if os.path.exists(GEOJSON_PATH):
        try:
            with open(GEOJSON_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None
