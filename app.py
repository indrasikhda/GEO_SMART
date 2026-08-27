import streamlit as st

# Page Config
st.set_page_config(
    page_title="GEO-SMART — Geothermal Spatial Intelligence & Monitoring System",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Motokoui Exact Design System CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global Body Background matching Motokoui Screenshot */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F3F3F5 !important;
        color: #1C1C1E !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    [data-testid="stHeader"] {
        background-color: #F3F3F5 !important;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 0.75rem !important;
        padding-bottom: 2rem !important;
        max-width: 1360px !important;
    }

    /* Motokoui Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #F3F3F5 !important;
        border-right: none !important;
        padding-top: 0.5rem !important;
    }

    /* Sidebar Radio Options to match Active Pill Capsule */
    .stRadio > div {
        gap: 0.25rem !important;
    }

    .stRadio label {
        background: transparent !important;
        color: #636366 !important;
        padding: 10px 14px !important;
        border-radius: 12px !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        border: none !important;
        transition: all 0.15s ease !important;
    }

    .stRadio label:hover {
        background: rgba(255, 255, 255, 0.6) !important;
        color: #1C1C1E !important;
    }

    /* Active Nav Item as Pure White Capsule Card */
    .stRadio div[aria-checked="true"] label, .stRadio label[data-checked="true"] {
        background: #FFFFFF !important;
        color: #1C1C1E !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        border-radius: 12px !important;
    }

    /* Motokoui White Dashboard Cards (20px Rounded Corners) */
    div.motokoui-card {
        background: #FFFFFF;
        border-radius: 20px;
        border: 1px solid #ECECEC;
        padding: 22px 24px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
        margin-bottom: 1.25rem;
    }

    /* Black Pill Buttons matching Motokoui 'Buy template' & 'Sign in' */
    .stButton > button {
        background-color: #1C1C1E !important;
        color: #FFFFFF !important;
        border-radius: 9999px !important;
        border: none !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        padding: 0.55rem 1.4rem !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1) !important;
        transition: transform 0.1s ease, background-color 0.15s ease !important;
    }

    .stButton > button:hover {
        background-color: #3A3A3C !important;
        color: #FFFFFF !important;
        transform: translateY(-1px);
    }

    /* Table & Dataframe Styling */
    [data-testid="stDataFrame"] {
        border: 1px solid #EBEBEB !important;
        border-radius: 14px !important;
        background: #FFFFFF !important;
    }

    hr {
        border-color: #E5E5EA !important;
        margin: 1.25rem 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Imports of views
from views.overview import render_overview
from views.remote_sensing import render_remote_sensing
from views.evidence import render_evidence
from views.fahp_gpi import render_fahp_gpi
from views.priority import render_priority
from views.monitoring import render_monitoring
from views.temporal import render_temporal
from views.methods import render_methods
from views.data_sources import render_data_sources

# Motokoui Left Sidebar Structure
with st.sidebar:
    # Top Workspace Switcher matching Motokoui Screenshot
    st.markdown("""
        <div style="padding: 10px 14px; background: #EAEAED; border-radius: 14px; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 24px; height: 24px; background: #1C1C1E; color: #FFFFFF; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px;">G</div>
                <div>
                    <div style="font-weight: 700; font-size: 12px; color: #1C1C1E; line-height: 1.2;">GEO-SMART</div>
                    <div style="font-size: 10px; color: #8E8E93;">Minahasa Sector</div>
                </div>
            </div>
            <span style="font-size: 12px; color: #8E8E93;">↕</span>
        </div>
        <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #8E8E93; letter-spacing: 0.05em; padding-left: 6px; margin-bottom: 6px;">General</div>
    """, unsafe_allow_html=True)

    nav_selection = st.radio(
        "Navigation",
        [
            "Overview",
            "Remote Sensing",
            "Geological Evidence",
            "FAHP & GPI",
            "Priority Zones",
            "GMN Monitoring",
            "Temporal Monitoring",
            "Methods",
            "Data Sources"
        ],
        label_visibility="collapsed"
    )

    # Bottom Black Pill Button matching Motokoui 'Buy template' button
    st.markdown("""
        <div style="margin-top: 3rem; padding: 0 4px;">
            <div style="background: #1C1C1E; color: #FFFFFF; text-align: center; padding: 12px; border-radius: 9999px; font-size: 13px; font-weight: 700; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                🌋 GEO-SMART V0.1
            </div>
        </div>
    """, unsafe_allow_html=True)

# Motokoui Top Header Bar (Matching Screenshots 1 & 2)
col_header_left, col_header_right = st.columns([7, 5])

with col_header_left:
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 0.5rem;">
            <div style="width: 32px; height: 32px; background: #FFFFFF; border-radius: 10px; border: 1px solid #E5E5EA; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 14px;">📖</div>
            <h1 style="font-size: 1.85rem; font-weight: 800; color: #1C1C1E; margin: 0; letter-spacing: -0.02em;">
                {nav_selection}
            </h1>
            <div style="display: flex; background: #EAEAED; padding: 3px; border-radius: 9999px; font-size: 12px; font-weight: 600; color: #636366;">
                <span style="padding: 4px 12px; color: #636366;">This week</span>
                <span style="padding: 4px 14px; background: #FFFFFF; color: #1C1C1E; border-radius: 9999px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); font-weight: 700;">This month</span>
                <span style="padding: 4px 12px; color: #636366;">This quarter</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_header_right:
    st.markdown("""
        <div style="display: flex; align-items: center; justify-content: flex-end; gap: 12px; margin-top: 4px;">
            <div style="display: flex; align-items: center; background: #FFFFFF; border: 1px solid #E5E5EA; padding: 6px 14px; border-radius: 9999px; font-size: 12px; color: #8E8E93; gap: 8px; width: 190px;">
                <span>🔍 Search...</span>
                <span style="margin-left: auto; background: #F2F2F7; border: 1px solid #E5E5EA; padding: 1px 5px; border-radius: 4px; font-size: 10px; font-weight: 700; color: #8E8E93;">⌘K</span>
            </div>
            <div style="width: 32px; height: 32px; background: #FFFFFF; border-radius: 9999px; border: 1px solid #E5E5EA; display: flex; align-items: center; justify-content: center; font-size: 13px; position: relative;">
                🔔
                <span style="position: absolute; top: -2px; right: -2px; width: 14px; height: 14px; background: #1C1C1E; color: #FFFFFF; border-radius: 9999px; font-size: 9px; font-weight: 800; display: flex; align-items: center; justify-content: center;">3</span>
            </div>
            <div style="width: 32px; height: 32px; background: #FFFFFF; border-radius: 9999px; border: 1px solid #E5E5EA; display: flex; align-items: center; justify-content: center; font-size: 13px;">
                🎨
            </div>
            <div style="background: #1C1C1E; color: #FFFFFF; padding: 7px 16px; border-radius: 9999px; font-size: 12px; font-weight: 700; cursor: pointer;">
                Prototype
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 1.25rem;'></div>", unsafe_allow_html=True)

# Page Routing
if nav_selection == "Overview":
    render_overview()
elif nav_selection == "Remote Sensing":
    render_remote_sensing()
elif nav_selection == "Geological Evidence":
    render_evidence()
elif nav_selection == "FAHP & GPI":
    render_fahp_gpi()
elif nav_selection == "Priority Zones":
    render_priority()
elif nav_selection == "GMN Monitoring":
    render_monitoring()
elif nav_selection == "Temporal Monitoring":
    render_temporal()
elif nav_selection == "Methods":
    render_methods()
elif nav_selection == "Data Sources":
    render_data_sources()
