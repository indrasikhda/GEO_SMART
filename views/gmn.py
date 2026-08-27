import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
import pandas as pd
import numpy as np
from core.io import GMN_NODES

def render_gmn():
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; items-center; gap: 0.75rem;">
                <h1 style="font-size: 2rem; font-weight: 700; color: #1F1E1D; margin: 0;">GMN Monitoring</h1>
                <span style="font-size: 0.75rem; font-weight: 600; color: #B25900; background: #FFF4E5; padding: 4px 8px; border-radius: 4px; align-self: center;">
                    SIMULATED SENSOR DATA
                </span>
            </div>
            <p style="font-size: 1rem; color: #6B6864; margin-top: 0.2rem;">Concept design for geothermal environmental monitoring.</p>
        </div>
    """, unsafe_allow_html=True)

    col_map, col_nodes = st.columns([6, 6], gap="large")

    with col_nodes:
        st.markdown("<h3 style='font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #8C8882; margin-bottom: 0.75rem;'>Proposed Monitoring Nodes</h3>", unsafe_allow_html=True)

        for node in GMN_NODES:
            st.markdown(f"""
                <div style="padding: 1.25rem; background: #FAF8F5; border-radius: 8px; border: 1px solid #E6E4DF; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 1rem; font-weight: 700; color: #1F1E1D; font-family: monospace;">{node['id']}</span>
                        <span style="font-size: 0.72rem; color: #2E6B38; background: #EAF4EC; padding: 2px 6px; border-radius: 4px; font-weight: 600;">{node['status']}</span>
                    </div>
                    <span style="font-size: 0.85rem; color: #6B6864; display: block; margin-bottom: 0.75rem;">{node['name']}</span>
                    
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; text-align: center; font-family: monospace; font-size: 0.85rem;">
                        <div style="background: #F4F1EA; padding: 6px; border-radius: 4px;">
                            <span style="font-size: 0.65rem; color: #8C8882; display: block;">Temp</span>
                            <b style="color: #D95A2B;">{node['temp']}°C</b>
                        </div>
                        <div style="background: #F4F1EA; padding: 6px; border-radius: 4px;">
                            <span style="font-size: 0.65rem; color: #8C8882; display: block;">pH</span>
                            <b style="color: #1F1E1D;">{node['ph']}</b>
                        </div>
                        <div style="background: #F4F1EA; padding: 6px; border-radius: 4px;">
                            <span style="font-size: 0.65rem; color: #8C8882; display: block;">EC</span>
                            <b style="color: #1F1E1D;">{node['ec']} µS</b>
                        </div>
                        <div style="background: #F4F1EA; padding: 6px; border-radius: 4px;">
                            <span style="font-size: 0.65rem; color: #8C8882; display: block;">Battery</span>
                            <b style="color: #2E6B38;">{node['battery']}%</b>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with col_map:
        m = folium.Map(
            location=[1.325, 124.845], 
            zoom_start=12, 
            tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", 
            attr="&copy; OpenStreetMap &copy; CARTO"
        )

        for node in GMN_NODES:
            folium.Marker(
                location=[node["lat"], node["lng"]],
                popup=f"<b>{node['id']}</b>: {node['name']}<br>Temp: {node['temp']}°C | pH: {node['ph']}",
                icon=folium.Icon(color="green", icon="signal")
            ).add_to(m)

        st_folium(m, width="100%", height=440, key="gmn_map")

    # Clean Minimal Plotly Trends
    st.markdown("<div style='margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #E6E4DF;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size: 1.1rem; font-weight: 600; color: #1F1E1D; margin-bottom: 1rem;'>Telemetry Trends</h3>", unsafe_allow_html=True)

    dates = pd.date_range("2025-01-01", periods=12, freq="MS")
    df_trend = pd.DataFrame({
        "Month": dates.strftime("%b %Y"),
        "Temperature (°C)": [66.2, 66.8, 67.4, 68.0, 68.4, 69.1, 70.2, 71.0, 69.8, 68.6, 67.9, 67.1],
        "pH Level": [3.32, 3.30, 3.28, 3.26, 3.25, 3.21, 3.18, 3.15, 3.20, 3.24, 3.27, 3.31],
        "EC (µS/cm)": [3750, 3780, 3810, 3830, 3840, 3890, 3940, 3980, 3910, 3850, 3800, 3760]
    })

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        fig1 = px.line(df_trend, x="Month", y="Temperature (°C)", title="Temperature Trend")
        fig1.update_traces(line_color="#D95A2B", line_width=2)
        fig1.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False, title=""), yaxis=dict(showgrid=True, gridcolor="#E6E4DF"))
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        fig2 = px.line(df_trend, x="Month", y="pH Level", title="pH Level Trend")
        fig2.update_traces(line_color="#B25900", line_width=2)
        fig2.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False, title=""), yaxis=dict(showgrid=True, gridcolor="#E6E4DF"))
        st.plotly_chart(fig2, use_container_width=True)

    with c3:
        fig3 = px.line(df_trend, x="Month", y="EC (µS/cm)", title="EC Trend")
        fig3.update_traces(line_color="#2E6B38", line_width=2)
        fig3.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False, title=""), yaxis=dict(showgrid=True, gridcolor="#E6E4DF"))
        st.plotly_chart(fig3, use_container_width=True)
