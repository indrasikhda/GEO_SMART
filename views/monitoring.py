import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
import pandas as pd
from core.io import GMN_NODES
from core.maps import create_base_map

def render_monitoring():
    st.markdown("""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:1.25rem;">
            <span style="font-size:0.75rem;font-weight:700;color:#007AFF;background:#E3F0FF;padding:4px 12px;border-radius:9999px;">SIMULATED SENSOR DATA</span>
            <span style="font-size:0.85rem;color:#636366;">Physical IoT sensors not yet deployed</span>
        </div>
    """, unsafe_allow_html=True)

    # KPI Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">Online Nodes</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#E8FAF0;display:flex;align-items:center;justify-content:center;font-size:13px;">📡</div>
                </div>
                <div style="font-size:1.75rem;font-weight:800;color:#1C1C1E;">3 / 3</div>
                <span style="font-size:0.72rem;font-weight:600;color:#34C759;">100% nodes online</span>
            </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">Temperature</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#FFF4E0;display:flex;align-items:center;justify-content:center;font-size:13px;">🌡️</div>
                </div>
                <div style="font-size:1.75rem;font-weight:800;color:#1C1C1E;">68.4 °C</div>
                <span style="font-size:0.72rem;font-weight:600;color:#FF9500;">+1.8°C vs prior</span>
            </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">pH Level</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#F2F2F7;display:flex;align-items:center;justify-content:center;font-size:13px;">🧪</div>
                </div>
                <div style="font-size:1.75rem;font-weight:800;color:#1C1C1E;">3.25</div>
                <span style="font-size:0.72rem;font-weight:600;color:#FF3B30;">-0.07 vs prior</span>
            </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">Conductivity (EC)</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#F2F2F7;display:flex;align-items:center;justify-content:center;font-size:13px;">⚡</div>
                </div>
                <div style="font-size:1.75rem;font-weight:800;color:#1C1C1E;">3,840 µS</div>
                <span style="font-size:0.72rem;font-weight:600;color:#34C759;">+90 µS vs prior</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:1.25rem'></div>", unsafe_allow_html=True)

    col_map, col_nodes = st.columns([7, 5], gap="medium")

    with col_map:
        m = create_base_map(center=[1.325, 124.845], zoom=12)
        for node in GMN_NODES:
            folium.Marker(
                location=[node["lat"], node["lng"]],
                popup=f"<b>{node['id']}</b>: {node['name']}<br>Temp: {node['temp']}°C | pH: {node['ph']}",
                icon=folium.Icon(color="green", icon="info-sign")
            ).add_to(m)
        st_folium(m, width="100%", height=440, key="gmn_saas_map")

    with col_nodes:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 4px 0;">Node Telemetry</h3>
                <p style="font-size:0.75rem;color:#8E8E93;margin:0 0 14px 0;">Live readings (simulated)</p>
        """, unsafe_allow_html=True)

        for node in GMN_NODES:
            st.markdown(f"""
                <div style="padding:12px 14px;background:#F9F9FB;border-radius:12px;border:1px solid #EBEBEB;margin-bottom:10px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <span style="font-size:0.9rem;font-weight:800;color:#1C1C1E;font-family:monospace;">{node['id']}</span>
                        <span style="font-size:0.65rem;color:#34C759;background:#E8FAF0;padding:2px 8px;border-radius:9999px;font-weight:700;">● {node['status']}</span>
                    </div>
                    <span style="font-size:0.75rem;color:#636366;display:block;margin-bottom:8px;">{node['name']}</span>
                    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;text-align:center;">
                        <div style="background:#FFFFFF;padding:6px 4px;border-radius:8px;border:1px solid #EBEBEB;">
                            <span style="font-size:0.6rem;color:#8E8E93;display:block;">Temp</span>
                            <b style="font-size:0.8rem;color:#FF9500;">{node['temp']}°C</b>
                        </div>
                        <div style="background:#FFFFFF;padding:6px 4px;border-radius:8px;border:1px solid #EBEBEB;">
                            <span style="font-size:0.6rem;color:#8E8E93;display:block;">pH</span>
                            <b style="font-size:0.8rem;color:#1C1C1E;">{node['ph']}</b>
                        </div>
                        <div style="background:#FFFFFF;padding:6px 4px;border-radius:8px;border:1px solid #EBEBEB;">
                            <span style="font-size:0.6rem;color:#8E8E93;display:block;">EC</span>
                            <b style="font-size:0.8rem;color:#1C1C1E;">{node['ec']}</b>
                        </div>
                        <div style="background:#FFFFFF;padding:6px 4px;border-radius:8px;border:1px solid #EBEBEB;">
                            <span style="font-size:0.6rem;color:#8E8E93;display:block;">Batt</span>
                            <b style="font-size:0.8rem;color:#34C759;">{node['battery']}%</b>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Trend Charts Row
    st.markdown("<div style='margin-top:1.25rem'></div>", unsafe_allow_html=True)
    dates = pd.date_range("2025-01-01", periods=12, freq="MS")
    df_t = pd.DataFrame({
        "Month": dates.strftime("%b"),
        "Temperature (°C)": [66.2, 66.8, 67.4, 68.0, 68.4, 69.1, 70.2, 71.0, 69.8, 68.6, 67.9, 67.1],
        "pH": [3.32, 3.30, 3.28, 3.26, 3.25, 3.21, 3.18, 3.15, 3.20, 3.24, 3.27, 3.31],
        "EC (µS/cm)": [3750, 3780, 3810, 3830, 3840, 3890, 3940, 3980, 3910, 3850, 3800, 3760]
    })

    c1, c2, c3 = st.columns(3, gap="medium")
    for col, y_col, color, title in [
        (c1, "Temperature (°C)", "#FF9500", "Temperature Trend"),
        (c2, "pH", "#1C1C1E", "pH Level Trend"),
        (c3, "EC (µS/cm)", "#34C759", "EC Trend"),
    ]:
        with col:
            fig = px.line(df_t, x="Month", y=y_col, title=title, color_discrete_sequence=[color])
            fig.update_traces(line_width=2.5)
            fig.update_layout(
                height=200, margin=dict(l=10, r=10, t=32, b=10),
                paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
                font=dict(family="Inter", size=10, color="#636366"),
                title_font=dict(size=12, color="#1C1C1E", family="Inter"),
                xaxis=dict(showgrid=False, title=""),
                yaxis=dict(showgrid=True, gridcolor="#F2F2F7", title="")
            )
            st.markdown("""<div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:14px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">""", unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
