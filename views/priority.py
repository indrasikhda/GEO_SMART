import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from core.io import PRIORITY_ZONES
from core.maps import create_base_map

def render_priority():
    st.markdown("""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:1.25rem;">
            <span style="font-size:0.75rem;font-weight:700;color:#FF9500;background:#FFF4E0;padding:4px 12px;border-radius:9999px;">DEMO DATA</span>
            <span style="font-size:0.85rem;color:#636366;">Target prospect identification and spatial constraint ranking</span>
        </div>
    """, unsafe_allow_html=True)

    # KPI Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">High Priority</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#FDE8E8;display:flex;align-items:center;justify-content:center;font-size:13px;">🔴</div>
                </div>
                <div style="font-size:1.75rem;font-weight:800;color:#1C1C1E;">6</div>
                <span style="font-size:0.72rem;font-weight:600;color:#FF3B30;">High prospect sectors</span>
            </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">Moderate Priority</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#FFF4E0;display:flex;align-items:center;justify-content:center;font-size:13px;">🟡</div>
                </div>
                <div style="font-size:1.75rem;font-weight:800;color:#1C1C1E;">5</div>
                <span style="font-size:0.72rem;font-weight:600;color:#FF9500;">Moderate prospect sectors</span>
            </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">Low Priority</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#E8FAF0;display:flex;align-items:center;justify-content:center;font-size:13px;">🟢</div>
                </div>
                <div style="font-size:1.75rem;font-weight:800;color:#1C1C1E;">1</div>
                <span style="font-size:0.72rem;font-weight:600;color:#34C759;">Low prospect sectors</span>
            </div>
        """, unsafe_allow_html=True)

    with k4:
        total_area = sum(z["area"] for z in PRIORITY_ZONES)
        st.markdown(f"""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">Total Coverage</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#F2F2F7;display:flex;align-items:center;justify-content:center;font-size:13px;">📏</div>
                </div>
                <div style="font-size:1.75rem;font-weight:800;color:#1C1C1E;">{total_area} km²</div>
                <span style="font-size:0.72rem;font-weight:600;color:#34C759;">+4.2% vs last survey</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:1.25rem'></div>", unsafe_allow_html=True)

    col_map, col_table = st.columns([7, 5], gap="medium")

    with col_map:
        m = create_base_map(center=[1.325, 124.845], zoom=12)
        for z in PRIORITY_ZONES:
            color = "#FF3B30" if z["priority"] == "High" else "#FF9500"
            folium.Circle(
                location=[z["lat"], z["lng"]],
                radius=z["area"] * 250,
                color=color, fill=True, fill_color=color, fill_opacity=0.3,
                popup=f"<b>{z['zone']}</b><br>GPI: {z['gpi']} ({z['priority']})<br>Area: {z['area']} km²"
            ).add_to(m)
        st_folium(m, width="100%", height=480, key="priority_saas_map")

    with col_table:
        df = pd.DataFrame(PRIORITY_ZONES)
        df["Rank"] = range(1, len(df) + 1)
        df_show = df[["Rank", "zone", "gpi", "area", "priority", "constraint"]]
        df_show.columns = ["Rank", "Zone", "GPI", "Area (km²)", "Priority", "Constraint"]
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 4px 0;">Zone Ranking Table</h3>
                <p style="font-size:0.75rem;color:#8E8E93;margin:0 0 12px 0;">Priority zones sorted by GPI score</p>
        """, unsafe_allow_html=True)
        st.dataframe(df_show, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
