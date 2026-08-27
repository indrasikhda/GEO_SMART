import folium

def create_base_map(center=[1.325, 124.845], zoom=12):
    """
    Creates a clean, light basemap with no API key requirement.
    """
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors &copy; <a href='https://carto.com/attributions'>CARTO</a>"
    )
    return m
