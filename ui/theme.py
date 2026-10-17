import streamlit as st

# ════════════════════════════════════════════════════════════════════════════
# GEO-SMART DESIGN SYSTEM — ui/theme.py
# Clean Bento Style & Dark Forest Green Sidebar inspired by AeuxGlobal
# ════════════════════════════════════════════════════════════════════════════

GEO_SMART_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap');

/* ─────────────────────────────────────────────────────────────────────────
   DESIGN TOKENS
───────────────────────────────────────────────────────────────────────── */
:root {
    --sidebar-bg:           #0D2B22;
    --sidebar-border:       #153D30;
    --sidebar-text:         #A8C5B5;
    --sidebar-text-muted:   #6B9B82;
    --sidebar-group:        #4E8268;
    --sidebar-active-bg:    #163D2E;
    --sidebar-active-text:  #FFFFFF;
    --sidebar-active-bar:   #22C55E;
    --sidebar-hover-bg:     rgba(255, 255, 255, 0.06);

    --bg-app:               #F1F7F4;
    --bg-card:              #FFFFFF;
    --bg-card-dark:         #0D2B22;

    --accent-green:         #22C55E;
    --accent-green-dark:    #16A34A;
    --accent-green-light:   #DCFCE7;
    --accent-orange:        #F97316;
    --accent-red:           #EF4444;

    --text-primary:         #0F172A;
    --text-secondary:       #334155;
    --text-muted:           #64748B;
    --text-light:           #94A3B8;

    --border-color:         #E2E8F0;
    --border-subtle:        #F1F5F9;
    --radius-sm:            8px;
    --radius-md:            12px;
    --radius-lg:            20px;
    --radius-pill:          9999px;

    --shadow-card:          0 1px 3px rgba(13, 43, 34, 0.05), 0 4px 12px rgba(13, 43, 34, 0.03);
    --shadow-hover:         0 8px 24px rgba(34, 197, 94, 0.1), 0 2px 6px rgba(0, 0, 0, 0.04);
}

/* ─────────────────────────────────────────────────────────────────────────
   BASE LAYOUT & TOOLBAR REMOVAL
───────────────────────────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-app) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
}

[data-testid="stHeader"] {
    background-color: transparent !important;
    height: 0.5rem !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

footer {
    display: none !important;
}

#MainMenu {
    visibility: hidden !important;
}

/* Container utama: selector lama (.main) + baru (stMainBlockContainer) */
.main .block-container,
[data-testid="stMainBlockContainer"] {
    padding-top: 1rem !important;
    padding-bottom: 2.5rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1420px !important;
}

/* ─────────────────────────────────────────────────────────────────────────
   SIDEBAR: DARK FOREST GREEN & 3-PART FLEXBOX
───────────────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: var(--sidebar-bg) !important;
    border-right: 1px solid var(--sidebar-border) !important;
    width: 260px !important;
    min-width: 260px !important;
}

[data-testid="stSidebar"] > div:first-child {
    background-color: var(--sidebar-bg) !important;
    padding: 0 !important;
    display: flex !important;
    flex-direction: column !important;
    height: 100vh !important;
    overflow: hidden !important;
}

[data-testid="stSidebarHeader"] {
    display: none !important;
}

[data-testid="stSidebarContent"] {
    display: contents !important;
}

[data-testid="stSidebarUserContent"] {
    display: contents !important;
}

/* 1. Brand Box fixed at top of sidebar */
.sidebar-brand-box {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 260px !important;
    height: 64px !important;
    z-index: 100 !important;
    box-sizing: border-box !important;
    padding: 0.85rem 1.15rem !important;
    border-bottom: 1px solid var(--sidebar-border) !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
    background: var(--sidebar-bg) !important;
}

.sidebar-brand-icon {
    width: 34px !important;
    height: 34px !important;
    border-radius: 9px !important;
    background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1.1rem !important;
    box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3) !important;
    flex-shrink: 0 !important;
}

.sidebar-brand-text {
    display: flex !important;
    flex-direction: column !important;
}

.sidebar-brand-title {
    font-size: 1rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    letter-spacing: -0.02em !important;
    line-height: 1.2 !important;
}

.sidebar-brand-subtitle {
    font-size: 0.6rem !important;
    font-weight: 600 !important;
    color: var(--sidebar-text-muted) !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* 2. Navigation items in middle */
[data-testid="stSidebarNav"] {
    margin-top: 64px !important;
    margin-bottom: 64px !important;
    padding: 0.25rem 0.5rem 0.5rem 0.5rem !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    flex: 1 1 auto !important;
}

[data-testid="stSidebarNav"]::-webkit-scrollbar {
    width: 4px;
}
[data-testid="stSidebarNav"]::-webkit-scrollbar-thumb {
    background: var(--sidebar-border);
    border-radius: 4px;
}

/* Group Headers */
[data-testid="stSidebarNav"] span,
[data-testid="stSidebarNavSectionHeader"] {
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--sidebar-group) !important;
    padding: 0.85rem 0.75rem 0.25rem 0.75rem !important;
    display: block !important;
}

/* Links List */
[data-testid="stSidebarNav"] ul {
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

[data-testid="stSidebarNav"] li {
    margin: 2px 0 !important;
}

/* Nav Item Link */
[data-testid="stSidebarNavLink"] {
    display: flex !important;
    align-items: center !important;
    gap: 0.65rem !important;
    height: 36px !important;
    padding: 0 0.85rem !important;
    border-radius: 9px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: var(--sidebar-text) !important;
    text-decoration: none !important;
    transition: all 0.15s ease !important;
    background-color: transparent !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

[data-testid="stSidebarNavLink"]:hover {
    background-color: var(--sidebar-hover-bg) !important;
    color: #FFFFFF !important;
}

/* Active Nav Item */
[data-testid="stSidebarNavLink"][aria-current="page"] {
    background-color: var(--sidebar-active-bg) !important;
    color: var(--sidebar-active-text) !important;
    font-weight: 600 !important;
    box-shadow: inset 3px 0 0 var(--sidebar-active-bar) !important;
}

[data-testid="stSidebarNavLink"] span {
    color: inherit !important;
    font-size: 0.82rem !important;
    padding: 0 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
}

/* 3. Status Footer fixed at bottom of sidebar */
.sidebar-user-footer {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    width: 260px !important;
    height: 60px !important;
    z-index: 100 !important;
    box-sizing: border-box !important;
    padding: 0.75rem 1.15rem !important;
    border-top: 1px solid var(--sidebar-border) !important;
    background: #09211A !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.7rem !important;
}

.sidebar-footer-avatar {
    width: 32px !important;
    height: 32px !important;
    border-radius: 8px !important;
    background: #153D30 !important;
    border: 1px solid #1F5241 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 0.95rem !important;
    flex-shrink: 0 !important;
}

.sidebar-footer-info {
    flex: 1 !important;
    min-width: 0 !important;
}

.sidebar-footer-title {
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

.sidebar-footer-sub {
    font-size: 0.62rem !important;
    color: var(--sidebar-text-muted) !important;
}

.sidebar-footer-status-dot {
    width: 8px !important;
    height: 8px !important;
    border-radius: 50% !important;
    background: #22C55E !important;
    box-shadow: 0 0 6px rgba(34, 197, 94, 0.6) !important;
    flex-shrink: 0 !important;
}

/* ─────────────────────────────────────────────────────────────────────────
   CLEAN PAGE HEADER (NO CARD WRAPPER, COMPACT)
───────────────────────────────────────────────────────────────────────── */
.clean-page-header {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    margin-bottom: 1.25rem !important;
    padding: 0.25rem 0 !important;
}

.header-title-col {
    display: flex !important;
    flex-direction: column !important;
}

.header-title-row {
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
}

.clean-page-title {
    font-size: 1.55rem !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    margin: 0 !important;
    padding: 0 !important;
    letter-spacing: -0.02em !important;
    line-height: 1.2 !important;
}

.clean-page-subtitle {
    font-size: 0.82rem !important;
    color: var(--text-muted) !important;
    margin-top: 0.2rem !important;
    line-height: 1.4 !important;
}

.header-status-badge {
    display: inline-flex !important;
    align-items: center !important;
    padding: 0.2rem 0.6rem !important;
    background: #DCFCE7 !important;
    color: #15803D !important;
    border: 1px solid #BBF7D0 !important;
    border-radius: var(--radius-pill) !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    cursor: help !important;
}

.header-action-col {
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

/* ─────────────────────────────────────────────────────────────────────────
   BENTO KPI CARDS (CLEAN, NO REDUNDANT PILLS)
───────────────────────────────────────────────────────────────────────── */
.bento-kpi {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.15rem 1.35rem !important;
    box-shadow: var(--shadow-card) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    min-height: 105px !important;
}

.bento-kpi:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-hover) !important;
}

.bento-kpi.dark {
    background: var(--bg-card-dark) !important;
    border-color: #1A4335 !important;
}

/* Label KPI: huruf normal, gaya referensi */
.kpi-label {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    margin-bottom: 0.35rem !important;
}

.bento-kpi.dark .kpi-label {
    color: var(--sidebar-text-muted) !important;
}

.kpi-main {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 0.75rem;
}

.kpi-spark {
    flex-shrink: 0;
    line-height: 0;
}

.kpi-value {
    font-size: 1.95rem !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.025em !important;
    line-height: 1.1 !important;
}

.bento-kpi.dark .kpi-value {
    color: var(--accent-green) !important;
}

.kpi-footer-row {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    margin-top: 0.4rem !important;
    font-size: 0.72rem !important;
}

.kpi-subtext {
    color: var(--text-muted) !important;
}

.bento-kpi.dark .kpi-subtext {
    color: var(--sidebar-text-muted) !important;
}

.kpi-trend {
    font-weight: 700 !important;
    padding: 0.15rem 0.5rem !important;
    border-radius: var(--radius-pill) !important;
}
.kpi-trend.success { background: #DCFCE7 !important; color: #15803D !important; }
.kpi-trend.neutral { background: #F1F5F9 !important; color: var(--text-muted) !important; }
.kpi-trend.warning { background: #FEF3C7 !important; color: #B45309 !important; }

/* ─────────────────────────────────────────────────────────────────────────
   BENTO CONTENT CARDS (HTML murni, tanpa widget di dalamnya)
───────────────────────────────────────────────────────────────────────── */
.bento-card {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.25rem 1.4rem !important;
    box-shadow: var(--shadow-card) !important;
    margin-bottom: 1rem !important;
}

.bento-card-header {
    display: flex !important;
    align-items: flex-start !important;
    justify-content: space-between !important;
    margin-bottom: 0.85rem !important;
    padding-bottom: 0.65rem !important;
    border-bottom: 1px solid var(--border-subtle) !important;
}

.bento-card-title {
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.01em !important;
}

.bento-card-sub {
    font-size: 0.75rem !important;
    color: var(--text-muted) !important;
    margin-top: 0.15rem !important;
}

.card-header-badge {
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    padding: 0.15rem 0.55rem !important;
    border-radius: var(--radius-pill) !important;
    background: #DCFCE7 !important;
    color: #15803D !important;
}

/* Dark Highlight Bento Card (AeuxGlobal accent style) */
.bento-card-dark-highlight {
    background: linear-gradient(145deg, #0D2B22 0%, #081C16 100%) !important;
    border: 1px solid #1E503F !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.25rem 1.4rem !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 16px rgba(13, 43, 34, 0.15) !important;
    margin-bottom: 1rem !important;
}

.dark-card-top-row {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    margin-bottom: 0.5rem !important;
}

.dark-card-tag {
    font-size: 0.62rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    background: #194635 !important;
    color: #22C55E !important;
    padding: 0.2rem 0.55rem !important;
    border-radius: var(--radius-pill) !important;
}

.dark-card-title {
    font-size: 0.8rem !important;
    color: #9EB3A8 !important;
    margin-bottom: 0.25rem !important;
}

.dark-card-stat {
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    letter-spacing: -0.02em !important;
}

.dark-card-substat {
    font-size: 0.75rem !important;
    color: #22C55E !important;
    font-weight: 600 !important;
    margin-top: 0.2rem !important;
}

.dark-card-desc {
    font-size: 0.72rem !important;
    color: #7A9E8D !important;
    margin-top: 0.4rem !important;
    line-height: 1.4 !important;
}

/* ─────────────────────────────────────────────────────────────────────────
   CONTROLS BAR (FOR MAP LAYERS & SLIDERS)
───────────────────────────────────────────────────────────────────────── */
.bento-controls-bar {
    background: #FFFFFF !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.65rem 1rem !important;
    margin-bottom: 1rem !important;
    display: flex !important;
    align-items: center !important;
    gap: 1.5rem !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
}

/* ─────────────────────────────────────────────────────────────────────────
   CARD SYSTEM: st.container(key="card_...") → kartu sungguhan
   Pakai key berawalan: card_ (putih), cardmint_ (mint), carddark_ (gelap)
───────────────────────────────────────────────────────────────────────── */
[class*="st-key-card"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-card) !important;
    padding: 1.15rem 1.3rem !important;
    gap: 0.75rem !important;
}
[class*="st-key-cardmint"] {
    background: #E6F4EC !important;
    border-color: #CDE8D8 !important;
    box-shadow: none !important;
}
[class*="st-key-carddark"] {
    background: linear-gradient(145deg, #0D2B22 0%, #081C16 100%) !important;
    border-color: #1E503F !important;
    color: #FFFFFF !important;
}

/* Judul kartu (dipakai card_header) */
.card-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.75rem;
}
.card-head-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.01em;
}
.card-head-sub {
    font-size: 0.74rem;
    color: var(--text-muted);
    margin-top: 0.1rem;
}

/* Baris statistik bersih (label kiri, nilai kanan) */
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border-subtle);
}
.stat-row:last-child { border-bottom: none; }
.stat-row .l { font-size: 0.8rem; color: var(--text-muted); }
.stat-row .v { font-size: 0.9rem; font-weight: 700; color: var(--text-primary); }

/* Tooltip info inline */
.geo-tooltip-wrap { display: inline-flex; align-items: center; gap: 0.2rem; }
.geo-info-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #E2E8F0;
    color: var(--text-muted);
    font-size: 0.6rem;
    font-weight: 700;
    cursor: help;
}

/* Radio horizontal → pill toggle (berlaku untuk semua st.radio di area konten) */
div[role="radiogroup"] { gap: 0.4rem !important; }
div[role="radiogroup"] > label {
    background: #F1F7F4;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-pill);
    padding: 0.3rem 0.9rem;
    margin: 0 !important;
    cursor: pointer;
    transition: all 0.15s ease;
}
div[role="radiogroup"] > label > div:first-of-type { display: none !important; }
div[role="radiogroup"] > label p {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
}
div[role="radiogroup"] > label:has(input:checked) {
    background: var(--bg-card-dark);
    border-color: var(--bg-card-dark);
}
div[role="radiogroup"] > label:has(input:checked) p { color: #FFFFFF !important; }

/* ─────────────────────────────────────────────────────────────────────────
   LEGACY COMPATIBILITY
───────────────────────────────────────────────────────────────────────── */
.geo-badge { display: inline-flex; align-items: center; padding: 0.2rem 0.6rem; border-radius: var(--radius-pill); font-size: 0.68rem; font-weight: 700; text-transform: uppercase; }
.geo-badge.success { background: #DCFCE7; color: #15803D; }
.geo-badge.neutral { background: #F1F5F9; color: var(--text-muted); }
.status-badge { display: inline-flex; align-items: center; padding: 0.2rem 0.6rem; border-radius: var(--radius-pill); font-size: 0.68rem; font-weight: 700; text-transform: uppercase; }
.badge-success { background: #DCFCE7; color: #15803D; }
.badge-primary { background: #DCFCE7; color: #15803D; }
.badge-danger { background: #FEE2E2; color: #991B1B; }
.data-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 1.25rem; box-shadow: var(--shadow-card); margin-bottom: 1rem; }
.data-card-header { font-size: 0.82rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; }

</style>
"""


def inject_css():
    """Inject the GEO-SMART design system CSS into the Streamlit app."""
    st.markdown(GEO_SMART_CSS, unsafe_allow_html=True)