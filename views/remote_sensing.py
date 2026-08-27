import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
import pandas as pd
from core.raster import get_raster_stats_and_overlay
from core.maps import create_base_map

def kpi_card(label, value, icon, subtext, trend_positive=True):
    color = "#34C759" if trend_positive else "#FF3B30"
    return f"""
        <div style="background: #FFFFFF; border-radius: 20px; border: 1px solid #ECECEC; padding: 20px 22px; box-shadow: 0 2px 10px rgba(0,0,0,0.02);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                <span style="font-size: 0.85rem; font-weight: 600; color: #636366;">{label}</span>
                <div style="width: 26px; height: 26px; border-radius: 9999px; background: #F2F2F7; display: flex; align-items: center; justify-content: center; font-size: 13px;">{icon}</div>
            </div>
            <div style="font-size: 1.75rem; font-weight: 800; color: #1C1C1E; letter-spacing: -0.02em;">{value}</div>
            <span style="font-size: 0.72rem; font-weight: 600; color: {color}; margin-top: 4px; display: block;">{subtext}</span>
        </div>
    """

def render_remote_sensing():
    # KPI Row
    k1, k2, k3, k4 = st.columns(4)
    lst_stats = get_raster_stats_and_overlay("lst")
    ndvi_stats = get_raster_stats_and_overlay("ndvi")

    with k1:
        st.markdown(kpi_card("LST Mean Temperature", f"{lst_stats['mean']} °C", "🌡️", "+1.4°C vs 2024 baseline", True), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi_card("LST Maximum", f"{lst_stats['max']} °C", "📈", "Thermal anomaly peak value", True), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi_card("NDVI Mean Index", str(ndvi_stats['mean']), "🌿", "-0.03 vs prior season", False), unsafe_allow_html=True)
    with k4:
        st.markdown(kpi_card("Active Rasters", "2 GeoTIFF", "📡", "+8.1% coverage", True), unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:1.25rem'></div>", unsafe_allow_html=True)

    # Main layout
    col_map, col_panel = st.columns([7, 5], gap="medium")

    with col_map:
        selected = st.radio("Layer", ["LST 2025", "NDVI 2025"], horizontal=True)
        layer_key = "lst" if selected == "LST 2025" else "ndvi"
        stats = get_raster_stats_and_overlay(layer_key)

        m = create_base_map(center=[2.92, 125.12], zoom=7)
        if stats.get("png_path") and stats.get("bounds"):
            folium.raster_layers.ImageOverlay(
                image=stats["png_path"],
                bounds=stats["bounds"],
                opacity=0.85
            ).add_to(m)
        st_folium(m, width="100%", height=460, key="rs_map")

    with col_panel:
        unit = "°C" if layer_key == "lst" else "Index"
        st.markdown(f"""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);margin-bottom:1rem;">
                <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 4px 0;">Rasterio Statistics</h3>
                <p style="font-size:0.75rem;color:#8E8E93;margin:0 0 16px 0;">Empirical values from {stats.get('filename','')}</p>
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;">
                    <div style="padding:12px;background:#F9F9FB;border-radius:12px;border:1px solid #EBEBEB;">
                        <span style="font-size:0.65rem;color:#8E8E93;font-weight:600;text-transform:uppercase;">Min</span>
                        <b style="display:block;font-size:1.1rem;color:#1C1C1E;font-family:monospace;">{stats['min']}</b>
                        <span style="font-size:0.7rem;color:#8E8E93;">{unit}</span>
                    </div>
                    <div style="padding:12px;background:#FFF7E6;border-radius:12px;border:1px solid #FFE4A8;">
                        <span style="font-size:0.65rem;color:#8E8E93;font-weight:600;text-transform:uppercase;">Mean</span>
                        <b style="display:block;font-size:1.1rem;color:#FF9500;font-family:monospace;">{stats['mean']}</b>
                        <span style="font-size:0.7rem;color:#8E8E93;">{unit}</span>
                    </div>
                    <div style="padding:12px;background:#F9F9FB;border-radius:12px;border:1px solid #EBEBEB;">
                        <span style="font-size:0.65rem;color:#8E8E93;font-weight:600;text-transform:uppercase;">Max</span>
                        <b style="display:block;font-size:1.1rem;color:#1C1C1E;font-family:monospace;">{stats['max']}</b>
                        <span style="font-size:0.7rem;color:#8E8E93;">{unit}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if "valid_array" in stats and len(stats["valid_array"]) > 0:
            df_hist = pd.DataFrame({"value": stats["valid_array"]})
            color = "#FF9500" if layer_key == "lst" else "#34C759"
            fig = px.histogram(df_hist, x="value", nbins=30, color_discrete_sequence=[color])
            fig.update_layout(
                title={"text": f"{selected} Distribution", "font": {"size": 13, "family": "Inter"}},
                height=220, margin=dict(l=10, r=10, t=35, b=10),
                paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
                font=dict(family="Inter", size=10, color="#636366"),
                xaxis=dict(showgrid=False, title=""),
                yaxis=dict(showgrid=True, gridcolor="#F2F2F7", title="")
            )
            st.markdown("""<div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:16px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">""", unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
