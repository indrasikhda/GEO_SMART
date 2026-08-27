import streamlit as st
import folium
from streamlit_folium import st_folium
from core.maps import create_base_map
from core.io import MANIFESTATIONS, GMN_NODES
from core.raster import get_raster_stats_and_overlay

# Shared card CSS injected once
CARD_CSS = """
<style>
.moto-card {
    background: #FFFFFF;
    border-radius: 20px;
    border: 1px solid #ECECEC;
    padding: 20px 22px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    margin-bottom: 4px;
}
.moto-card-title {
    font-size: 0.875rem;
    font-weight: 600;
    color: #636366;
    margin: 0 0 6px 0;
}
.moto-card-value {
    font-size: 1.75rem;
    font-weight: 800;
    color: #1C1C1E;
    line-height: 1.1;
    margin: 0 0 4px 0;
}
.moto-card-trend-green  { font-size: 0.72rem; font-weight: 600; color: #34C759; }
.moto-card-trend-red    { font-size: 0.72rem; font-weight: 600; color: #FF3B30; }
.moto-card-trend-orange { font-size: 0.72rem; font-weight: 600; color: #FF9500; }
</style>
"""

def _kpi(label, value, icon, trend_text, trend_cls="moto-card-trend-green"):
    return f"""
    <div class="moto-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <p class="moto-card-title">{label}</p>
            <span style="font-size:14px;opacity:0.5;">{icon}</span>
        </div>
        <p class="moto-card-value">{value}</p>
        <span class="{trend_cls}">{trend_text}</span>
    </div>"""


def render_overview():
    st.markdown(CARD_CSS, unsafe_allow_html=True)

    # ── 4 KPI CARDS ──────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(_kpi("Prospectivity Zones", "12", "🎯",
                         "+12.4% vs prior baseline"), unsafe_allow_html=True)
    with k2:
        st.markdown(_kpi("Remote Sensing", "2 Layers", "📡",
                         "+8.1% vs prior"), unsafe_allow_html=True)
    with k3:
        st.markdown(_kpi("Evidence Layers", "7 Layers", "⚙️",
                         "-2.3% vs prior", "moto-card-trend-red"), unsafe_allow_html=True)
    with k4:
        st.markdown(_kpi("GMN Nodes", "3 Active", "%",
                         "+0.4% vs prior"), unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:1.25rem'></div>", unsafe_allow_html=True)

    # ── MAIN ROW: Map (left) + Right side cards ───────────────────────────────
    col_map, col_right = st.columns([7, 5], gap="medium")

    # ── MAP CARD ─────────────────────────────────────────────────────────────
    with col_map:
        st.markdown("""
            <div class="moto-card" style="padding-bottom:12px;">
                <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px;">
                    <div>
                        <p style="font-size:1.05rem;font-weight:800;color:#1C1C1E;margin:0;">Study Area Map</p>
                        <p style="font-size:0.75rem;color:#8E8E93;margin:2px 0 10px 0;">Minahasa Hydrothermal Sector</p>
                    </div>
                    <code style="font-size:0.7rem;color:#8E8E93;background:#F2F2F7;padding:3px 7px;border-radius:6px;">WGS84 EPSG:4326</code>
                </div>
            </div>""", unsafe_allow_html=True)

        m = create_base_map(center=[1.325, 124.845], zoom=12)
        for pt in MANIFESTATIONS:
            folium.CircleMarker(
                location=[pt["lat"], pt["lng"]],
                radius=6, color="#FF9500", fill=True,
                fill_color="#FF9500", fill_opacity=0.85,
                popup=f"<b>{pt['name']}</b><br>Temp: {pt['temp']}°C | pH: {pt['ph']}"
            ).add_to(m)
        for node in GMN_NODES:
            folium.Marker(
                location=[node["lat"], node["lng"]],
                popup=f"<b>{node['id']}</b>: {node['name']}",
                icon=folium.Icon(color="green", icon="info-sign")
            ).add_to(m)
        st_folium(m, width="100%", height=400, key="overview_map")

    # ── RIGHT SIDE CARDS ──────────────────────────────────────────────────────
    with col_right:

        # ── PROSPECTIVITY OVERVIEW CARD (native Streamlit) ────────────────────
        with st.container():
            st.markdown("""
                <div class="moto-card" style="padding-bottom:16px;">
                    <p style="font-size:1.05rem;font-weight:800;color:#1C1C1E;margin:0 0 2px 0;">Prospectivity overview</p>
                    <p style="font-size:0.75rem;color:#8E8E93;margin:0 0 14px 0;">12 target priority zones evaluated in dataset</p>
                </div>""", unsafe_allow_html=True)

            # Progress bar using native Streamlit (3 coloured segments via columns)
            bar_col1, bar_col2, bar_col3 = st.columns([67, 25, 8])
            with bar_col1:
                st.markdown("""
                    <div style="height:10px;background:#007AFF;border-radius:9999px 0 0 9999px;"></div>
                """, unsafe_allow_html=True)
            with bar_col2:
                st.markdown("""
                    <div style="height:10px;background:#34C759;"></div>
                """, unsafe_allow_html=True)
            with bar_col3:
                st.markdown("""
                    <div style="height:10px;background:#FF2D55;border-radius:0 9999px 9999px 0;"></div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)

            # Legend row using native Streamlit columns
            leg1, leg2, leg3 = st.columns(3)
            with leg1:
                st.markdown("""
                    <div style="display:flex;align-items:center;gap:6px;">
                        <span style="width:8px;height:8px;border-radius:50%;background:#007AFF;display:inline-block;flex-shrink:0;"></span>
                        <span style="font-size:0.78rem;color:#636366;">High <b style="color:#1C1C1E;">6</b> <span style="color:#8E8E93;">67%</span></span>
                    </div>""", unsafe_allow_html=True)
            with leg2:
                st.markdown("""
                    <div style="display:flex;align-items:center;gap:6px;">
                        <span style="width:8px;height:8px;border-radius:50%;background:#34C759;display:inline-block;flex-shrink:0;"></span>
                        <span style="font-size:0.78rem;color:#636366;">Mod <b style="color:#1C1C1E;">5</b> <span style="color:#8E8E93;">25%</span></span>
                    </div>""", unsafe_allow_html=True)
            with leg3:
                st.markdown("""
                    <div style="display:flex;align-items:center;gap:6px;">
                        <span style="width:8px;height:8px;border-radius:50%;background:#FF2D55;display:inline-block;flex-shrink:0;"></span>
                        <span style="font-size:0.78rem;color:#636366;">Low <b style="color:#1C1C1E;">1</b> <span style="color:#8E8E93;">8%</span></span>
                    </div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)

        # ── REMOTE SENSING BASELINE CARD ──────────────────────────────────────
        lst_stats  = get_raster_stats_and_overlay("lst")
        ndvi_stats = get_raster_stats_and_overlay("ndvi")

        st.markdown(f"""
            <div class="moto-card">
                <p style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 12px 0;">Remote Sensing Baseline</p>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                    <div style="padding:12px;background:#F9F9FB;border-radius:12px;border:1px solid #EBEBEB;">
                        <span style="font-size:0.65rem;color:#8E8E93;font-weight:600;text-transform:uppercase;display:block;">LST Mean</span>
                        <span style="font-size:1.2rem;font-weight:800;color:#FF9500;">{lst_stats['mean']} °C</span>
                    </div>
                    <div style="padding:12px;background:#F9F9FB;border-radius:12px;border:1px solid #EBEBEB;">
                        <span style="font-size:0.65rem;color:#8E8E93;font-weight:600;text-transform:uppercase;display:block;">NDVI Mean</span>
                        <span style="font-size:1.2rem;font-weight:800;color:#34C759;">{ndvi_stats['mean']}</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── RECENT ACTIVITY CARD (native Streamlit) ───────────────────────────────
    st.markdown("<div style='margin-top:1.25rem'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="moto-card" style="padding-bottom:8px;">
            <p style="font-size:1.05rem;font-weight:800;color:#1C1C1E;margin:0 0 2px 0;">Recent activity</p>
            <p style="font-size:0.75rem;color:#8E8E93;margin:0 0 14px 0;">Latest updates across evidence rasters, FAHP weights, and IoT telemetry events</p>
        </div>""", unsafe_allow_html=True)

    # Activity items using native st.columns
    ACTIVITIES = [
        {
            "icon": "📄",
            "title": "LST_BARU.tif & GEO_SMART_NDVI_2025.tif Integrated",
            "subtitle": "Rasterio empirical bounds verified · good",
            "time": "1 hour ago",
        },
        {
            "icon": "⚖️",
            "title": "FAHP Row Geometric Mean Engine Calculated",
            "subtitle": "Consistency Ratio CR = 0.042 (CR < 0.10 — Acceptable)",
            "time": "1 day ago",
        },
        {
            "icon": "📡",
            "title": "GMN-01 · GMN-02 · GMN-03 Node Config Drafted",
            "subtitle": "SIMULATED — physical deployment pending",
            "time": "2 days ago",
        },
    ]

    for act in ACTIVITIES:
        c_icon, c_body, c_time = st.columns([1, 14, 3])
        with c_icon:
            st.markdown(f"""
                <div style="width:34px;height:34px;background:#F2F2F7;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:15px;margin-top:4px;">
                    {act['icon']}
                </div>""", unsafe_allow_html=True)
        with c_body:
            st.markdown(f"""
                <p style="font-size:0.875rem;font-weight:700;color:#1C1C1E;margin:0 0 2px 0;">{act['title']}</p>
                <p style="font-size:0.75rem;color:#8E8E93;margin:0;">{act['subtitle']}</p>""",
                unsafe_allow_html=True)
        with c_time:
            st.markdown(f"""
                <p style="font-size:0.72rem;color:#8E8E93;text-align:right;margin-top:6px;">{act['time']}</p>""",
                unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#F2F2F7;margin:8px 0;'>", unsafe_allow_html=True)
