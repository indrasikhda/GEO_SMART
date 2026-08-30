import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="GEO-SMART — Geothermal Spatial Intelligence & Monitoring System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════
# EXPLORATION COMMAND CENTER - DESIGN SYSTEM
# Light Professional Theme for Geothermal Monitoring & Decision Support
# ═══════════════════════════════════════════════════════════════════════

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    /* ─────────────────────────────────────────────────────────────────── */
    /* Global Layout & Base Colors */
    /* ─────────────────────────────────────────────────────────────────── */
    :root {
        --color-primary: #0891B2;        /* Teal - Energy/Geothermal accent */
        --color-primary-dark: #0E7490;
        --color-success: #059669;         /* Green - Active/Valid */
        --color-warning: #D97706;         /* Amber - Caution */
        --color-danger: #DC2626;          /* Red - Critical */
        --color-info: #2563EB;            /* Blue - Info */
        --color-neutral: #64748B;         /* Slate - Secondary text */
        
        --bg-app: #F8FAFC;                /* App background */
        --bg-card: #FFFFFF;               /* Card background */
        --bg-sidebar: #FFFFFF;            /* Sidebar background */
        
        --border-color: #E2E8F0;          /* Default border */
        --border-color-hover: #CBD5E1;
        
        --text-primary: #0F172A;          /* Primary text */
        --text-secondary: #475569;        /* Secondary text */
        --text-tertiary: #64748B;         /* Tertiary text */
        
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -2px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.06);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-app) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    [data-testid="stHeader"] {
        background-color: var(--bg-app) !important;
    }

    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px !important;
    }

    /* ─────────────────────────────────────────────────────────────────── */
    /* Typography System */
    /* ─────────────────────────────────────────────────────────────────── */
    h1, h2, h3, .stHeadingContainer h1, .stHeadingContainer h2, .stHeadingContainer h3 {
        font-weight: 800 !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em !important;
    }

    h1, .stHeadingContainer h1 {
        font-size: 2rem !important;
        margin-bottom: 0.5rem !important;
    }

    h2, .stHeadingContainer h2 {
        font-size: 1.5rem !important;
        margin-bottom: 0.75rem !important;
    }

    h3, .stHeadingContainer h3 {
        font-size: 1.125rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* ─────────────────────────────────────────────────────────────────── */
    /* KPI Metric Cards - Command Center Style */
    /* ─────────────────────────────────────────────────────────────────── */
    [data-testid="stMetric"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        padding: 1.25rem !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    [data-testid="stMetric"]:hover {
        box-shadow: var(--shadow-md) !important;
        border-color: var(--color-primary) !important;
        transform: translateY(-2px) !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        color: var(--text-tertiary) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        margin-bottom: 0.5rem !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 900 !important;
        color: var(--text-primary) !important;
        line-height: 1 !important;
        letter-spacing: -0.02em !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        margin-top: 0.5rem !important;
        padding: 0.25rem 0.5rem !important;
        border-radius: 4px !important;
        display: inline-block !important;
    }

    [data-testid="stMetricDelta"] svg {
        display: none !important;
    }

    /* ─────────────────────────────────────────────────────────────────── */
    /* Badge System - Status Pills */
    /* ─────────────────────────────────────────────────────────────────── */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .badge-success {
        background-color: #D1FAE5;
        color: #065F46;
        border: 1px solid #A7F3D0;
    }

    .badge-warning {
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FDE68A;
    }

    .badge-danger {
        background-color: #FEE2E2;
        color: #991B1B;
        border: 1px solid #FCA5A5;
    }

    .badge-info {
        background-color: #DBEAFE;
        color: #1E3A8A;
        border: 1px solid #BFDBFE;
    }

    .badge-neutral {
        background-color: #F1F5F9;
        color: #475569;
        border: 1px solid #E2E8F0;
    }

    .badge-primary {
        background-color: #CFFAFE;
        color: #164E63;
        border: 1px solid #A5F3FC;
    }

    /* ─────────────────────────────────────────────────────────────────── */
    /* Section Headers with Icons */
    /* ─────────────────────────────────────────────────────────────────── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid var(--border-color);
    }

    .section-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        color: white;
        flex-shrink: 0;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0;
    }

    .section-subtitle {
        font-size: 0.8rem;
        color: var(--text-tertiary);
        margin: 0;
        font-weight: 500;
    }

    /* ─────────────────────────────────────────────────────────────────── */
    /* Data Cards - Content Containers */
    /* ─────────────────────────────────────────────────────────────────── */
    .data-card {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: var(--shadow-sm);
        margin-bottom: 1.25rem;
    }

    .data-card-header {
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ─────────────────────────────────────────────────────────────────── */
    /* Sidebar Navigation - Clean & Professional */
    /* ─────────────────────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar) !important;
        border-right: 2px solid var(--border-color) !important;
        padding-top: 1rem !important;
    }

    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.35rem !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        background: transparent !important;
        color: var(--text-secondary) !important;
        padding: 0.65rem 1rem !important;
        border-radius: 6px !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        border: 1px solid transparent !important;
        transition: all 0.15s ease !important;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: #F8FAFC !important;
        color: var(--text-primary) !important;
        border-color: var(--border-color) !important;
    }

    [data-testid="stSidebar"] .stRadio div[aria-checked="true"] label {
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-color: var(--color-primary-dark) !important;
        box-shadow: var(--shadow-md) !important;
    }

    /* ─────────────────────────────────────────────────────────────────── */
    /* Buttons - Primary Action Style */
    /* ─────────────────────────────────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%) !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        border: none !important;
        font-size: 0.875rem !important;
        font-weight: 700 !important;
        padding: 0.625rem 1.5rem !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    .stButton > button:hover {
        box-shadow: var(--shadow-md) !important;
        transform: translateY(-1px) !important;
    }

    /* ─────────────────────────────────────────────────────────────────── */
    /* Alert Boxes - Minimal Design */
    /* ─────────────────────────────────────────────────────────────────── */
    [data-testid="stAlert"] {
        border-radius: 8px !important;
        border-width: 1px !important;
        font-size: 0.85rem !important;
        padding: 0.75rem 1rem !important;
    }

    /* ─────────────────────────────────────────────────────────────────── */
    /* DataFrames & Tables */
    /* ─────────────────────────────────────────────────────────────────── */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        background: var(--bg-card) !important;
        font-size: 0.85rem !important;
    }

    /* ─────────────────────────────────────────────────────────────────── */
    /* Dividers */
    /* ─────────────────────────────────────────────────────────────────── */
    hr {
        border-color: var(--border-color) !important;
        margin: 1.5rem 0 !important;
        border-width: 1px !important;
    }

    /* ─────────────────────────────────────────────────────────────────── */
    /* Expander - Collapsed Details */
    /* ─────────────────────────────────────────────────────────────────── */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        color: var(--text-secondary) !important;
    }

    /* ─────────────────────────────────────────────────────────────────── */
    /* Page Header Style */
    /* ─────────────────────────────────────────────────────────────────── */
    .page-header {
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--border-color);
    }

    .page-breadcrumb {
        font-size: 0.75rem;
        color: var(--text-tertiary);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }

    .page-title {
        font-size: 2rem;
        font-weight: 900;
        color: var(--text-primary);
        margin: 0;
        letter-spacing: -0.02em;
    }

    .page-description {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
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

# Sidebar Navigation Structure
with st.sidebar:
    # Brand Header - Clean & Professional
    st.markdown("""
        <div style="text-align:center;padding:1.5rem 0 1rem 0;border-bottom:2px solid #E2E8F0;">
            <div style="width:48px;height:48px;margin:0 auto 0.75rem;background:linear-gradient(135deg, #0891B2 0%, #0E7490 100%);border-radius:10px;display:flex;align-items:center;justify-content:center;">
                <span style="font-size:1.5rem;color:#FFFFFF;">⚡</span>
            </div>
            <h2 style="margin:0;font-size:1.25rem;font-weight:900;color:#0F172A;letter-spacing:-0.02em;">GEO-SMART</h2>
            <p style="margin:0.25rem 0 0 0;font-size:0.7rem;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">
                Geothermal Intelligence System
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")

    nav_selection = st.radio(
        "Navigation",
        [
            "Overview",
            "Remote Sensing",
            "Multi-Source Evidence",
            "AHP & GPI",
            "Priority Zones",
            "GMN Monitoring",
            "Temporal Monitoring",
            "Methods",
            "Data Sources"
        ],
        label_visibility="collapsed"
    )

    st.write("")
    
    # System Status - Compact Badge Display
    st.markdown("""
        <div style="padding:0.75rem;background:#F8FAFC;border-radius:8px;border:1px solid #E2E8F0;">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
                <span class="status-badge badge-primary">STAGE</span>
                <span style="font-size:0.75rem;font-weight:600;color:#475569;">Prototype</span>
            </div>
            <div style="display:flex;align-items:center;gap:0.5rem;">
                <span class="status-badge badge-info">REGION</span>
                <span style="font-size:0.75rem;font-weight:600;color:#475569;">Sulawesi Utara</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption("v1.0 | 2025")

# Top Header Area
NAV_CATEGORIES = {
    "Overview": "System Dashboard",
    "Remote Sensing": "Spatial Data",
    "Multi-Source Evidence": "Evidence Layers",
    "Data Sources": "Data Management",
    "AHP & GPI": "Decision Engine",
    "Priority Zones": "Exploration Zones",
    "GMN Monitoring": "Field Network",
    "Temporal Monitoring": "Time Series",
    "Methods": "Methodology"
}

category = NAV_CATEGORIES.get(nav_selection, "Command Center")

# Page Header with breadcrumb
st.markdown(f"""
    <div class="page-header">
        <div class="page-breadcrumb">GEOSMART / {category.upper()}</div>
        <h1 class="page-title">{nav_selection}</h1>
    </div>
""", unsafe_allow_html=True)

# Page Routing
if nav_selection == "Overview":
    render_overview()
elif nav_selection == "Remote Sensing":
    render_remote_sensing()
elif nav_selection == "Multi-Source Evidence":
    render_evidence()
elif nav_selection == "AHP & GPI":
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