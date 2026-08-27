import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from core.io import PRIORITY_ZONES

def render_priority_zone():
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; items-center; gap: 0.75rem;">
                <h1 style="font-size: 2rem; font-weight: 700; color: #1F1E1D; margin: 0;">Priority Exploration Zones</h1>
                <span style="font-size: 0.75rem; font-weight: 600; color: #B25900; background: #FFF4E5; padding: 4px 8px; border-radius: 4px; align-self: center;">
                    DEMO DATA
                </span>
            </div>
            <p style="font-size: 1rem; color: #6B6864; margin-top: 0.2rem;">Spatial constraint filtering and target prospect ranking.</p>
        </div>
    """, unsafe_allow_html=True)

    col_map, col_table = st.columns([6, 6], gap="large")

    df_zones = pd.DataFrame(PRIORITY_ZONES)[["zone", "gpi", "priority", "area", "constraint"]]
    df_zones.columns = ["Zone", "GPI Score", "Priority", "Area (km²)", "Constraint"]

    with col_table:
        st.markdown("<h3 style='font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #8C8882; margin-bottom: 0.75rem;'>Priority Zones Table</h3>", unsafe_allow_html=True)
        st.dataframe(df_zones, use_container_width=True, hide_index=True)

    with col_map:
        m = folium.Map(
            location=[1.325, 124.845], 
            zoom_start=12, 
            tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", 
            attr="&copy; OpenStreetMap &copy; CARTO"
        )

        for z in PRIORITY_ZONES:
            color = "#C8322B" if z["priority"] == "High" else "#D9822B"
            folium.Circle(
                location=[z["lat"], z["lng"]],
                radius=z["area"] * 250,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.3,
                popup=f"<b>{z['zone']}</b><br>GPI: {z['gpi']} ({z['priority']})<br>Area: {z['area']} km²"
            ).add_to(m)

        st_folium(m, width="100%", height=480, key="priority_map")
