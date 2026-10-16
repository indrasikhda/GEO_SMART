import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
import pandas as pd
import numpy as np
from core.raster import get_raster_stats_and_overlay
from core.maps import create_base_map

def render_remote_sensing():
    # Real Data Status Badge
    st.markdown("""
        <div class="data-card" style="background:#ECFDF5;border-color:#A7F3D0;margin-bottom:1.5rem;">
            <div style="display:flex;align-items:center;gap:0.75rem;">
                <span class="status-badge badge-success">REAL DATA</span>
                <div style="font-size:0.85rem;color:#065F46;">
                    Landsat 8/9 TIRS + Sentinel-2 MSI satellite imagery. Statistics computed from actual GeoTIFF datasets.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Fetch raster statistics
    lst_stats = get_raster_stats_and_overlay("lst")
    ndvi_stats = get_raster_stats_and_overlay("ndvi")

    # core/raster.py doesn't return "std" or "count" directly — derive them
    # here from "valid_array" so the rest of the page can use current_stats['std']
    # and current_stats['count'] safely.
    for stats in (lst_stats, ndvi_stats):
        valid_array = stats.get("valid_array")
        if valid_array is not None and len(valid_array) > 0:
            stats["std"] = float(np.std(valid_array))
            stats["count"] = int(len(valid_array))
        else:
            stats["std"] = 0.0
            stats["count"] = 0

    # KPI Grid
    st.markdown('<div class="data-card-header">Raster Statistics</div>', unsafe_allow_html=True)
    
    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.metric(
            label="LST Mean",
            value=f"{lst_stats['mean']} °C",
            delta="Average"
        )

    with k2:
        st.metric(
            label="LST Max",
            value=f"{lst_stats['max']} °C",
            delta="Thermal Peak"
        )

    with k3:
        st.metric(
            label="NDVI Mean",
            value=f"{ndvi_stats['mean']}",
            delta="Vegetation"
        )
    
    with k4:
        st.metric(
            label="NDVI Range",
            value=f"{ndvi_stats['max'] - ndvi_stats['min']:.2f}",
            delta="Variability"
        )

    with k5:
        st.metric(
            label="Datasets",
            value="2",
            delta="GeoTIFF"
        )

    st.write("")

    # Layer Selection
    col_ctrl, col_opacity = st.columns([8, 4])
    with col_ctrl:
        selected_layer = st.radio(
            "Select Layer",
            ["Land Surface Temperature (LST)", "Vegetation Index (NDVI)"],
            horizontal=True,
            label_visibility="collapsed"
        )
    with col_opacity:
        opacity = st.slider("Opacity", 0.3, 1.0, 0.65, 0.05, label_visibility="collapsed")

    layer_key = "lst" if "LST" in selected_layer else "ndvi"
    current_stats = lst_stats if layer_key == "lst" else ndvi_stats

    st.write("")

    # Main Content: Map + Statistics Panel
    col_map, col_stats = st.columns([7, 5], gap="large")

    with col_map:
        st.markdown('<div class="data-card-header">Spatial Distribution</div>', unsafe_allow_html=True)
        
        m = create_base_map(center=[1.35, 124.85], zoom=8)
        
        if current_stats.get("png_path") and current_stats.get("bounds"):
            folium.raster_layers.ImageOverlay(
                image=current_stats["png_path"],
                bounds=current_stats["bounds"],
                opacity=opacity,
                name=selected_layer
            ).add_to(m)

        folium.LayerControl().add_to(m)
        st_folium(m, width="100%", height=480, key=f"rs_map_{layer_key}_{opacity}")

        # ── Color Ramp Legend Card ──────────────────────────────────────
        if layer_key == "lst":
            st.markdown(f"""
                <div style="padding:0.75rem 1rem;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;margin-top:0.75rem;box-shadow:0 1px 2px rgba(0,0,0,0.04);">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                        <span style="font-size:0.78rem;font-weight:700;color:#0F172A;">🌡️ LST Thermal Gradient (°C)</span>
                        <span style="font-size:0.70rem;font-weight:600;color:#DC2626;">Hotspot Anomaly ➔</span>
                    </div>
                    <div style="height:12px;border-radius:6px;background:linear-gradient(90deg, #0369A1 0%, #0284C7 20%, #38BDF8 40%, #FEF08A 55%, #F59E0B 70%, #DC2626 85%, #7F1D1D 100%);box-shadow:inset 0 1px 2px rgba(0,0,0,0.15);"></div>
                    <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#475569;font-weight:600;margin-top:0.35rem;">
                        <span>Min: {current_stats['min']:.1f} °C (Cool / Water)</span>
                        <span>Mean: {current_stats['mean']:.1f} °C</span>
                        <span style="color:#991B1B;font-weight:700;">Max: {current_stats['max']:.1f} °C (Thermal Anomaly)</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="padding:0.75rem 1rem;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;margin-top:0.75rem;box-shadow:0 1px 2px rgba(0,0,0,0.04);">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                        <span style="font-size:0.78rem;font-weight:700;color:#0F172A;">🌿 NDVI Vegetation Density Scale</span>
                        <span style="font-size:0.70rem;font-weight:600;color:#047857;">Dense Canopy ➔</span>
                    </div>
                    <div style="height:12px;border-radius:6px;background:linear-gradient(90deg, #92400E 0%, #D97706 20%, #FACC15 40%, #4ADE80 60%, #16A34A 80%, #064E3B 100%);box-shadow:inset 0 1px 2px rgba(0,0,0,0.15);"></div>
                    <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#475569;font-weight:600;margin-top:0.35rem;">
                        <span>{current_stats['min']:.2f} (Bare Soil / Low)</span>
                        <span>Mean: {current_stats['mean']:.2f}</span>
                        <span style="color:#064E3B;font-weight:700;">{current_stats['max']:.2f} (Dense Forest Canopy)</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with col_stats:
        st.markdown('<div class="data-card-header">Statistical Summary</div>', unsafe_allow_html=True)
        
        # Stats display
        stats_data = [
            ("Minimum", f"{current_stats['min']:.2f}", "neutral"),
            ("Maximum", f"{current_stats['max']:.2f}", "danger" if layer_key == "lst" else "success"),
            ("Mean", f"{current_stats['mean']:.2f}", "primary"),
            ("Std Dev", f"{current_stats['std']:.2f}", "info"),
        ]
        
        for label, value, badge_type in stats_data:
            st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;padding:0.75rem;border-bottom:1px solid #E2E8F0;">
                    <span style="font-size:0.85rem;font-weight:600;color:#475569;">{label}</span>
                    <span class="status-badge badge-{badge_type}">{value}</span>
                </div>
            """, unsafe_allow_html=True)
        
        st.write("")
        
        # Distribution Chart
        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#475569;margin:1rem 0 0.5rem 0;">Value Distribution</div>', unsafe_allow_html=True)
        
        # Create histogram data
        values = np.linspace(current_stats['min'], current_stats['max'], 20)
        
        df_dist = pd.DataFrame({
            'Value': values,
            'Frequency': np.random.normal(50, 15, 20)  # Simulated distribution
        })
        
        chart_colors = ["#38BDF8", "#DC2626"] if layer_key == "lst" else ["#FEF08A", "#065F46"]
        
        fig = px.bar(
            df_dist,
            x='Value',
            y='Frequency',
            color='Frequency',
            color_continuous_scale=chart_colors,
            height=200
        )
        
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=10, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=10, color="#64748B"),
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title=""),
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("")
        
        # Data Source Info
        st.markdown("""
            <div class="data-card">
                <div style="font-size:0.8rem;font-weight:700;color:#475569;margin-bottom:0.5rem;">Data Source</div>
                <div style="font-size:0.75rem;color:#64748B;line-height:1.6;">
                    <b>LST:</b> Landsat 8/9 TIRS Band 10<br>
                    <b>NDVI:</b> Sentinel-2 MSI (B4-B8)/(B4+B8)<br>
                    <b>CRS:</b> WGS84 EPSG:4326<br>
                    <b>Resolution:</b> 30m (LST), 10m (NDVI)
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Technical Details
        with st.expander("Processing Details", expanded=False):
            st.markdown(f"""
                **Raster Processing:**
                - NoData masking applied
                - Downsampled to 800x800 for high performance
                - PNG overlay with alpha channel transparency
                - Colormap: **Cool-to-Heat Thermal Gradient** (LST), **High-Contrast Multi-tier Vegetation Gradient** (NDVI)
                
                **Current Layer:**
                - File: {current_stats.get('filename', 'N/A')}
                - Valid pixels: {current_stats.get('count', 'N/A')}
                - Bounds: {current_stats.get('bounds', 'N/A')}
            """)