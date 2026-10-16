import streamlit as st
import folium
from streamlit_folium import st_folium
import textwrap
from core.maps import create_base_map
from core.io import MANIFESTATIONS, GMN_NODES
from ui.components import page_header, kpi_card, dark_highlight_card

def render_overview():
    # ── Header Halaman Ringkas (Anggaran Teks) ──────────────────────────────
    page_header(
        title="Ringkasan Sistem",
        subtitle="Temuan utama, kesiapan data spasial, dan distribusi zona prospek panas bumi Sulawesi Utara.",
        badge_text="● Sistem Aktif",
        badge_tooltip="Modul analisis dan data satelit terhubung"
    )

    # ── Baris KPI Bento (Maksimal 4 kartu, tanpa pill redundan) ────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Lapisan Bukti", "8", subtext="5 lapisan aktif terhubung")
    with c2:
        kpi_card("Kriteria FAHP", "5", subtext="CR = 0.042 (Konsisten)")
    with c3:
        kpi_card("Zona Prioritas", "12", subtext="6 prospek tinggi (≥0.75)")
    with c4:
        kpi_card("Kesiapan Data", "62.5%", subtext="GeoTIFF & GeoJSON valid")

    st.write("")

    # ── Grid Konten Utama: Peta Spasial (7) + Panel Metrik Bento (5) ────────
    col_map, col_metrics = st.columns([7, 5], gap="medium")

    with col_map:
        # Bento Card Pembungkus Peta
        st.markdown(textwrap.dedent("""
<div class="bento-card" style="padding-bottom:1rem;">
<div class="bento-card-header">
<div>
<div class="bento-card-title">Peta Sebaran &amp; Area Studi</div>
<div class="bento-card-sub">10 lokasi manifestasi termal dan 3 usulan stasiun monitoring GMN</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

        m = create_base_map(center=[1.35, 124.85], zoom=8)

        # Marker manifestasi termal
        for manifest in MANIFESTATIONS:
            folium.CircleMarker(
                location=[manifest["lat"], manifest["lng"]],
                radius=7,
                color="#DC2626",
                fill=True,
                fillColor="#EF4444",
                fillOpacity=0.85,
                weight=1.5,
                popup=f"<b>{manifest['name']}</b><br>{manifest['type']}",
                tooltip=manifest["name"]
            ).add_to(m)

        # Marker usulan node GMN
        for node in GMN_NODES:
            folium.CircleMarker(
                location=[node["lat"], node["lng"]],
                radius=6,
                color="#0284C7",
                fill=True,
                fillColor="#38BDF8",
                fillOpacity=0.9,
                weight=1.5,
                popup=f"<b>{node['id']}</b><br>{node['name']}",
                tooltip=f"{node['id']} (Proposed Node)"
            ).add_to(m)

        folium.LayerControl().add_to(m)
        st_folium(m, width="100%", height=420, key="overview_main_map")

        # Legenda ringkas inline
        st.markdown(textwrap.dedent("""
<div style="display:flex;gap:1.5rem;margin-top:0.6rem;padding:0.25rem 0.5rem;font-size:0.75rem;">
<div style="display:flex;align-items:center;gap:0.4rem;">
<div style="width:10px;height:10px;border-radius:50%;background:#EF4444;"></div>
<span style="color:#475569;font-weight:600;">Manifestasi Panas Bumi (10)</span>
</div>
<div style="display:flex;align-items:center;gap:0.4rem;">
<div style="width:10px;height:10px;border-radius:50%;background:#0284C7;"></div>
<span style="color:#475569;font-weight:600;">Node Monitoring GMN (3)</span>
</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

    with col_metrics:
        # 1. Dark Accent Bento Card (gaya AeuxGlobal)
        dark_highlight_card(
            title="Zona Prioritas Tertinggi",
            main_stat="Kotamobagu",
            sub_stat="GPI: 0.842 · Kategori Prospek Tinggi",
            desc="Anomali termal kuat, densitas sesar tinggi (0.4 km), dan litologi vulkanik kuarter yang mendukung sistem hidrotermal.",
            tag="TOP PROSPEK"
        )

        # 2. Bento Card: Distribusi Tingkat Prospek
        st.markdown(textwrap.dedent("""
<div class="bento-card">
<div class="bento-card-header">
<div>
<div class="bento-card-title">Distribusi Zona Prospek</div>
<div class="bento-card-sub">Klasifikasi 12 zona eksplorasi berdasarkan skor GPI</div>
</div>
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.75rem;text-align:center;padding:0.25rem 0;">
<div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:12px;padding:0.75rem 0.5rem;">
<div style="font-size:0.68rem;font-weight:700;color:#15803D;text-transform:uppercase;">Tinggi</div>
<div style="font-size:1.6rem;font-weight:800;color:#166534;line-height:1.2;">6</div>
<div style="font-size:0.65rem;color:#15803D;font-weight:600;">&ge; 0.75 GPI</div>
</div>
<div style="background:#FEFCE8;border:1px solid #FEF08A;border-radius:12px;padding:0.75rem 0.5rem;">
<div style="font-size:0.68rem;font-weight:700;color:#854D0E;text-transform:uppercase;">Sedang</div>
<div style="font-size:1.6rem;font-weight:800;color:#713F12;line-height:1.2;">5</div>
<div style="font-size:0.65rem;color:#854D0E;font-weight:600;">0.60 &ndash; 0.74</div>
</div>
<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:0.75rem 0.5rem;">
<div style="font-size:0.68rem;font-weight:700;color:#64748B;text-transform:uppercase;">Rendah</div>
<div style="font-size:1.6rem;font-weight:800;color:#334155;line-height:1.2;">1</div>
<div style="font-size:0.65rem;color:#64748B;font-weight:600;">&lt; 0.60 GPI</div>
</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

        # 3. Bento Card: Status Integrasi Bukti Spasial
        evidence_status = [
            ("LST Raster (Landsat 8/9)", "Terhubung", "success"),
            ("NDVI Raster (Sentinel-2)", "Terhubung", "success"),
            ("Manifestasi Panas Bumi", "Terhubung", "success"),
            ("Geologi Regional & Litologi", "Terhubung", "success"),
            ("Sesar & Kelurusan Struktur", "Terhubung", "success"),
            ("Densitas Kelurusan (Lineament)", "Antrean", "neutral"),
        ]

        rows_html = ""
        for layer, status, badge_type in evidence_status:
            badge_bg = "#DCFCE7" if badge_type == "success" else "#F1F5F9"
            badge_color = "#15803D" if badge_type == "success" else "#64748B"
            rows_html += f"""
<div style="display:flex;justify-content:space-between;align-items:center;padding:0.4rem 0;border-bottom:1px solid #F1F5F9;">
<span style="font-size:0.78rem;font-weight:500;color:#334155;">{layer}</span>
<span style="font-size:0.65rem;font-weight:700;padding:0.15rem 0.5rem;border-radius:9999px;background:{badge_bg};color:{badge_color};">{status}</span>
</div>
"""

        st.markdown(textwrap.dedent(f"""
<div class="bento-card">
<div class="bento-card-header">
<div>
<div class="bento-card-title">Kesiapan Lapisan Spasial</div>
<div class="bento-card-sub">Status integrasi data untuk komputasi multikriteria</div>
</div>
</div>
{rows_html}
</div>
""").strip(), unsafe_allow_html=True)

    # ── Catatan Metodologi Tertutup (Expander) ──────────────────────────────
    with st.expander("ℹ️ Tentang Alur Kerja Sistem GEO-SMART", expanded=False):
        st.markdown("""
            **Alur Analisis:** Penginderaan Jauh (LST/NDVI) &rarr; Integrasi Bukti Multi-Sumber &rarr; Pembobotan FAHP &rarr; Komputasi Skor GPI &rarr; Zonasi Prioritas &rarr; Pemantauan Stasiun GMN.
            
            **Basis Data:** Citra satelit aktual (Landsat 8/9 TIRS & Sentinel-2 MSI), 10 titik manifestasi terdokumentasi ESDM, serta data spasial geologi & struktur sesar regional Sulawesi Utara.
        """)
