import streamlit as st

# ── Konfigurasi halaman (harus paling atas) ──────────────────────────────
st.set_page_config(
    page_title="GEO-SMART — Geothermal Spatial Intelligence & Monitoring",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Inject design system CSS ─────────────────────────────────────────────
from ui.theme import inject_css
inject_css()

# ── Import semua view ─────────────────────────────────────────────────────
from views.overview import render_overview
from views.remote_sensing import render_remote_sensing
from views.evidence import render_evidence
from views.data_sources import render_data_sources
from views.fahp_gpi import render_fahp_gpi
from views.priority import render_priority
from views.monitoring import render_monitoring
from views.temporal import render_temporal
from views.methods import render_methods

# ═══════════════════════════════════════════════════════════════════════════
# DEFINISI HALAMAN & NAVIGASI TUNGGAL (st.navigation)
# Tanpa emoji di sidebar agar tampilan bersih dan profesional
# ═══════════════════════════════════════════════════════════════════════════
pages = {
    "Ringkasan": [
        st.Page(render_overview, title="Ringkasan", default=True),
    ],
    "Data & Bukti": [
        st.Page(render_remote_sensing, title="Penginderaan Jauh"),
        st.Page(render_evidence, title="Bukti Multi-Sumber"),
        st.Page(render_data_sources, title="Sumber Data"),
    ],
    "Analisis": [
        st.Page(render_fahp_gpi, title="FAHP & GPI"),
        st.Page(render_priority, title="Zona Prioritas"),
    ],
    "Pemantauan": [
        st.Page(render_monitoring, title="Monitoring GMN"),
        st.Page(render_temporal, title="Monitoring Temporal"),
    ],
    "Referensi": [
        st.Page(render_methods, title="Metode"),
    ],
}

# Inisialisasi router navigasi resmi Streamlit
pg = st.navigation(pages, position="sidebar")

# ── Konten Sidebar Tambahan: Brand & Status Footer ────────────────────────
with st.sidebar:
    # Brand Box dengan icon SVG minimalis (tanpa emoji)
    st.markdown("""
        <div class="sidebar-brand-box">
            <div class="sidebar-brand-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 3L2 20H22L12 3Z" stroke="#FFFFFF" stroke-width="2.2" stroke-linejoin="round"/>
                    <path d="M12 11L7 20H17L12 11Z" fill="#FFFFFF" fill-opacity="0.9"/>
                </svg>
            </div>
            <div class="sidebar-brand-text">
                <div class="sidebar-brand-title">GEO-SMART</div>
                <div class="sidebar-brand-subtitle">Sulawesi Utara</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Status footer dengan avatar SVG minimalis (tanpa emoji)
    st.markdown("""
        <div class="sidebar-user-footer">
            <div class="sidebar-footer-avatar">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="2" y1="12" x2="22" y2="12"></line>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                </svg>
            </div>
            <div class="sidebar-footer-info">
                <div class="sidebar-footer-title">Sulawesi Utara</div>
                <div class="sidebar-footer-sub">Prototype · v1.0</div>
            </div>
            <div class="sidebar-footer-status-dot" title="Sistem Aktif"></div>
        </div>
    """, unsafe_allow_html=True)

# Jalankan halaman yang dipilih
pg.run()
