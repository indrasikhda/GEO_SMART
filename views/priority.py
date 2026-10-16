import streamlit as st
import folium
from streamlit_folium import st_folium
import textwrap
from core.io import PRIORITY_ZONES
from core.maps import create_base_map
from ui.components import page_header, kpi_card

def render_priority():
    # ── Header Halaman Ringkas (Anggaran Teks) ──────────────────────────────
    page_header(
        title="Zona Prioritas",
        subtitle="Peringkat dan zonasi prospek eksplorasi berdasarkan Geothermal Prospectivity Index (GPI).",
        badge_text="● 12 Kandidat Zona",
        badge_tooltip="Klasifikasi multikriteria berdasarkan skor GPI dan evaluasi kendala spasial"
    )

    high = sum(1 for z in PRIORITY_ZONES if z['priority'] == 'High')
    moderate = sum(1 for z in PRIORITY_ZONES if z['priority'] == 'Moderate')
    low = sum(1 for z in PRIORITY_ZONES if z['priority'] == 'Low')

    # ── Baris KPI Bento (Maksimal 4 kartu) ──────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Total Kandidat", f"{len(PRIORITY_ZONES)}", subtext="Wilayah prospek")
    with k2:
        kpi_card("Prioritas Tinggi", f"{high}", trend="GPI ≥ 0.75", trend_type="success")
    with k3:
        kpi_card("Prioritas Sedang", f"{moderate}", trend="0.60–0.74", trend_type="warning")
    with k4:
        kpi_card("Prioritas Rendah", f"{low}", subtext="GPI < 0.60")

    st.write("")

    # ── Layout Konten: Ranking Bento (5) + Peta Bento (7) ───────────────────
    col_table, col_map = st.columns([5, 7], gap="medium")

    with col_table:
        st.markdown(textwrap.dedent("""
<div class="bento-card">
<div class="bento-card-header">
<div>
<div class="bento-card-title">Peringkat Zona Eksplorasi</div>
<div class="bento-card-sub">Urutan kandidat berdasarkan skor GPI tertinggi</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

        sorted_zones = sorted(PRIORITY_ZONES, key=lambda x: x['gpi'], reverse=True)

        for zone in sorted_zones:
            p_val = zone['priority']
            badge_bg = "#DCFCE7" if p_val == "High" else ("#FEF3C7" if p_val == "Moderate" else "#F1F5F9")
            badge_color = "#15803D" if p_val == "High" else ("#B45309" if p_val == "Moderate" else "#64748B")
            p_label = "TINGGI" if p_val == "High" else ("SEDANG" if p_val == "Moderate" else "RENDAH")
            constraint_html = f'<div style="margin-top:0.3rem;font-size:0.68rem;color:#DC2626;font-weight:600;">⚠ {zone["constraint"]}</div>' if zone.get('constraint') else ''

            st.markdown(textwrap.dedent(f"""
<div style="padding:0.6rem 0.8rem;margin-bottom:0.4rem;border:1px solid #E2E8F0;border-radius:10px;background:#FFFFFF;">
<div style="display:flex;justify-content:space-between;align-items:center;">
<span style="font-size:0.86rem;font-weight:700;color:#0F172A;">{zone['zone']}</span>
<span style="font-size:0.62rem;font-weight:700;padding:0.12rem 0.5rem;border-radius:9999px;background:{badge_bg};color:{badge_color};">{p_label}</span>
</div>
<div style="display:flex;gap:1.25rem;font-size:0.72rem;color:#64748B;margin-top:0.25rem;">
<div><b>GPI:</b> {zone['gpi']}</div>
<div><b>Luas:</b> {zone['area']} km²</div>
</div>
{constraint_html}
</div>
""").strip(), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col_map:
        st.markdown(textwrap.dedent("""
<div class="bento-card" style="padding-bottom:1rem;">
<div class="bento-card-header">
<div>
<div class="bento-card-title">Peta Sebaran Zona Prioritas</div>
<div class="bento-card-sub">Distribusi spasial titik kandidat eksplorasi di Sulawesi Utara</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

        m = create_base_map(center=[1.35, 124.85], zoom=8)

        priority_colors_map = {
            'High': '#16A34A',
            'Moderate': '#D97706',
            'Low': '#64748B'
        }

        for zone in PRIORITY_ZONES:
            color = priority_colors_map.get(zone['priority'], '#64748B')
            folium.CircleMarker(
                location=[zone['lat'], zone['lng']],
                radius=8,
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.8,
                weight=2,
                popup=f"""
                    <b>{zone['zone']}</b><br>
                    Prioritas: {zone['priority']}<br>
                    Skor GPI: {zone['gpi']}<br>
                    Luas: {zone['area']} km²
                    {f"<br><span style='color:#DC2626;'>⚠ {zone['constraint']}</span>" if zone.get('constraint') else ''}
                """,
                tooltip=f"{zone['zone']} ({zone['priority']})"
            ).add_to(m)

        folium.LayerControl().add_to(m)
        st_folium(m, width="100%", height=480, key="priority_zones_map")

        # Legenda ringkas
        st.markdown(textwrap.dedent("""
<div style="display:flex;gap:1.5rem;margin-top:0.6rem;padding:0.25rem 0.5rem;font-size:0.75rem;">
<div style="display:flex;align-items:center;gap:0.4rem;">
<div style="width:10px;height:10px;border-radius:50%;background:#16A34A;"></div>
<span style="color:#475569;font-weight:600;">Prioritas Tinggi (6)</span>
</div>
<div style="display:flex;align-items:center;gap:0.4rem;">
<div style="width:10px;height:10px;border-radius:50%;background:#D97706;"></div>
<span style="color:#475569;font-weight:600;">Prioritas Sedang (5)</span>
</div>
<div style="display:flex;align-items:center;gap:0.4rem;">
<div style="width:10px;height:10px;border-radius:50%;background:#64748B;"></div>
<span style="color:#475569;font-weight:600;">Prioritas Rendah (1)</span>
</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

    # ── Expander Kriteria Klasifikasi ────────────────────────────────────────
    with st.expander("ℹ️ Kriteria & Ambang Batas Klasifikasi GPI", expanded=False):
        st.markdown("""
            - **Prioritas Tinggi:** Skor GPI &ge; 0.75 tanpa kendala lingkungan kritis.
            - **Prioritas Sedang:** Skor GPI 0.60 &ndash; 0.74, atau zona dengan kendala buffer yang memerlukan mitigasi.
            - **Prioritas Rendah:** Skor GPI &lt; 0.60.
            - **Evaluasi Kendala:** Buffer cagar alam / hutan lindung, kawasan pemukiman, radius kawah aktif, dan koridor infrastruktur.
        """)