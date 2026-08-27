import streamlit as st
import folium
from streamlit_folium import st_folium
from core.io import MANIFESTATIONS
from core.maps import create_base_map

EVIDENCE_LAYERS = [
    {"id": "geology",       "name": "Geology",                  "icon": "🪨", "connected": False},
    {"id": "fault",         "name": "Fault Traces",             "icon": "📐", "connected": False},
    {"id": "manifestation", "name": "Geothermal Manifestation", "icon": "♨️", "connected": True},
    {"id": "lineament",     "name": "Lineament Density",        "icon": "〰️", "connected": False},
    {"id": "alteration",    "name": "Hydrothermal Alteration",  "icon": "🧪", "connected": False},
    {"id": "seismicity",    "name": "Seismicity",               "icon": "📳", "connected": False},
    {"id": "lst",           "name": "LST 2025 (Landsat)",       "icon": "🌡️", "connected": True},
    {"id": "ndvi",          "name": "NDVI 2025 (Sentinel-2)",   "icon": "🌿", "connected": True},
]

def render_evidence():
    col_map, col_layers = st.columns([7, 5], gap="medium")

    with col_layers:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 4px 0;">Evidence Layer Toggles</h3>
                <p style="font-size:0.75rem;color:#8E8E93;margin:0 0 16px 0;">8 geological & environmental evidence layers</p>
        """, unsafe_allow_html=True)

        selected_toggles = {}
        for layer in EVIDENCE_LAYERS:
            c1, c2 = st.columns([3, 7])
            with c1:
                active = st.checkbox(f"{layer['icon']} {layer['name']}", value=layer["connected"], key=f"ev_{layer['id']}")
                selected_toggles[layer["id"]] = active
            with c2:
                if layer["connected"]:
                    st.markdown("""<span style="font-size:0.7rem;color:#34C759;background:#E8FAF0;padding:2px 8px;border-radius:9999px;font-weight:600;">● Connected</span>""", unsafe_allow_html=True)
                else:
                    st.markdown("""<span style="font-size:0.7rem;color:#FF9500;background:#FFF4E0;padding:2px 8px;border-radius:9999px;font-weight:600;">● Pending</span>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Stats Summary
        connected = sum(1 for l in EVIDENCE_LAYERS if l["connected"])
        pending = len(EVIDENCE_LAYERS) - connected
        st.markdown(f"""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:18px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);margin-top:1rem;">
                <h3 style="font-size:0.85rem;font-weight:800;color:#1C1C1E;margin:0 0 12px 0;">Layer Status</h3>
                <div style="width:100%;height:8px;background:#F2F2F7;border-radius:9999px;overflow:hidden;display:flex;margin-bottom:12px;">
                    <div style="width:{connected/len(EVIDENCE_LAYERS)*100:.0f}%;height:100%;background:#34C759;"></div>
                    <div style="width:{pending/len(EVIDENCE_LAYERS)*100:.0f}%;height:100%;background:#FF9500;"></div>
                </div>
                <div style="display:flex;gap:16px;font-size:0.78rem;">
                    <div style="display:flex;align-items:center;gap:6px;">
                        <span style="width:8px;height:8px;border-radius:9999px;background:#34C759;"></span>
                        <span style="color:#636366;">Connected <b style="color:#1C1C1E;">{connected}</b></span>
                    </div>
                    <div style="display:flex;align-items:center;gap:6px;">
                        <span style="width:8px;height:8px;border-radius:9999px;background:#FF9500;"></span>
                        <span style="color:#636366;">Pending <b style="color:#1C1C1E;">{pending}</b></span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_map:
        m = create_base_map(center=[1.325, 124.845], zoom=12)
        if selected_toggles.get("manifestation"):
            for pt in MANIFESTATIONS:
                folium.CircleMarker(
                    location=[pt["lat"], pt["lng"]],
                    radius=7,
                    color="#FF9500",
                    fill=True, fill_color="#FF9500", fill_opacity=0.85,
                    popup=f"<b>{pt['name']}</b><br>Type: {pt['type']}<br>Temp: {pt['temp']}°C | pH: {pt['ph']}"
                ).add_to(m)
        st_folium(m, width="100%", height=560, key="evidence_map")
