import streamlit as st
import folium
from streamlit_folium import st_folium
import textwrap
from core.io import MANIFESTATIONS
from core.maps import create_base_map, add_geological_layers
from core.raster import get_raster_stats_and_overlay
from ui.components import page_header, kpi_card

EVIDENCE_LAYERS = [
    {
        "name": "Land Surface Temperature",
        "type": "Raster",
        "status": "Connected",
        "source": "Landsat 8/9 TIRS",
        "badge": "success"
    },
    {
        "name": "NDVI Vegetation Index",
        "type": "Raster",
        "status": "Connected",
        "source": "Sentinel-2 MSI",
        "badge": "success"
    },
    {
        "name": "Geothermal Manifestations",
        "type": "Point",
        "status": "Connected",
        "source": "Field Survey",
        "badge": "success"
    },
    {
        "name": "Geology / Lithology",
        "type": "Polygon",
        "status": "Connected",
        "source": "Regional Geological Map (1:100k)",
        "badge": "success"
    },
    {
        "name": "Fault & Lineament",
        "type": "Line",
        "status": "Connected",
        "source": "Structural Geology (1:100k)",
        "badge": "success"
    },
    {
        "name": "Lineament Density",
        "type": "Raster",
        "status": "Pending",
        "source": "DEM Analysis",
        "badge": "neutral"
    },
    {
        "name": "Hydrothermal Alteration",
        "type": "Polygon",
        "status": "Pending",
        "source": "ASTER/Sentinel-2",
        "badge": "neutral"
    },
    {
        "name": "Micro-Seismicity",
        "type": "Point",
        "status": "Pending",
        "source": "Seismic Network",
        "badge": "neutral"
    }
]

def render_evidence():
    # ── Header Halaman Ringkas (Anggaran Teks) ──────────────────────────────
    page_header(
        title="Bukti Multi-Sumber",
        subtitle="Integrasi lapisan spasial geologi, sesar, manifestasi, dan penginderaan jauh.",
        badge_text="● 5 dari 8 Terhubung",
        badge_tooltip="5 lapisan data spasial aktif siap di-overlay"
    )

    connected = sum(1 for layer in EVIDENCE_LAYERS if layer["status"] == "Connected")
    pending = len(EVIDENCE_LAYERS) - connected

    # ── Baris KPI Bento (Maksimal 4 kartu) ──────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Total Lapisan", f"{len(EVIDENCE_LAYERS)}", subtext="Kriteria multikriteria")
    with k2:
        kpi_card("Lapisan Terhubung", f"{connected}", trend=f"{(connected/len(EVIDENCE_LAYERS)*100):.1f}%", trend_type="success")
    with k3:
        kpi_card("Dalam Antrean", f"{pending}", subtext="Integrasi lanjutan")
    with k4:
        kpi_card("Format Data", "3", subtext="GeoTIFF, GeoJSON, Tabular")

    st.write("")

    # ── Layout Konten: Inventaris Lapisan (5) + Peta Overlay (7) ────────────
    col_layers, col_map = st.columns([5, 7], gap="medium")

    with col_layers:
        st.markdown(textwrap.dedent("""
<div class="bento-card">
<div class="bento-card-header">
<div>
<div class="bento-card-title">Inventaris Lapisan Spasial</div>
<div class="bento-card-sub">Pilih lapisan aktif untuk ditampilkan pada peta</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

        selected_layers = []
        for layer in EVIDENCE_LAYERS:
            is_available = layer["status"] == "Connected"
            col_check, col_info = st.columns([1, 11])

            with col_check:
                if is_available:
                    default_checked = layer["name"] in ["Land Surface Temperature", "NDVI Vegetation Index", "Geothermal Manifestations"]
                    checked = st.checkbox("", value=default_checked, key=f"layer_{layer['name']}", label_visibility="collapsed")
                    if checked:
                        selected_layers.append(layer["name"])
                else:
                    st.markdown('<div style="padding:0.25rem;"></div>', unsafe_allow_html=True)

            with col_info:
                badge_bg = "#DCFCE7" if is_available else "#F1F5F9"
                badge_color = "#15803D" if is_available else "#64748B"
                badge_txt = "AKTIF" if is_available else "PENDING"
                name_color = "#0F172A" if is_available else "#94A3B8"
                st.markdown(textwrap.dedent(f"""
<div style="padding:0.45rem 0.65rem;margin-bottom:0.4rem;border:1px solid #E2E8F0;border-radius:10px;background:{'#F8FAFC' if not is_available else '#FFFFFF'};">
<div style="display:flex;justify-content:space-between;align-items:center;">
<span style="font-size:0.8rem;font-weight:600;color:{name_color};">{layer['name']}</span>
<span style="font-size:0.62rem;font-weight:700;padding:0.12rem 0.45rem;border-radius:9999px;background:{badge_bg};color:{badge_color};">{badge_txt}</span>
</div>
<div style="font-size:0.68rem;color:#64748B;margin-top:0.15rem;">
Tipe: {layer['type']} &bull; Sumber: {layer['source']}
</div>
</div>
""").strip(), unsafe_allow_html=True)

        st.markdown(textwrap.dedent("""
<div style="padding:0.65rem 0.85rem;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;margin-top:0.6rem;font-size:0.75rem;color:#475569;">
<div style="font-weight:700;color:#0F172A;margin-bottom:0.25rem;">Kemajuan Integrasi: 62.5%</div>
<div style="width:100%;height:6px;background:#E2E8F0;border-radius:9999px;overflow:hidden;">
<div style="width:62.5%;height:100%;background:linear-gradient(90deg,#22C55E,#16A34A);"></div>
</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

    with col_map:
        st.markdown(textwrap.dedent("""
<div class="bento-card" style="padding-bottom:1rem;">
<div class="bento-card-header">
<div>
<div class="bento-card-title">Peta Integrasi Spasial (Overlay)</div>
<div class="bento-card-sub">Kombinasi layer terpilih untuk delineasi prospek panas bumi</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

        m = create_base_map(center=[1.35, 124.85], zoom=8, include_geology=False)

        show_lito = "Geology / Lithology" in selected_layers
        show_geostruk = "Fault & Lineament" in selected_layers
        add_geological_layers(m, show_lito=show_lito, show_geostruk=show_geostruk)

        lst_overlay = None
        if "Land Surface Temperature" in selected_layers:
            lst_overlay = get_raster_stats_and_overlay("lst")
            if lst_overlay.get("png_path") and lst_overlay.get("bounds"):
                folium.raster_layers.ImageOverlay(
                    image=lst_overlay["png_path"],
                    bounds=lst_overlay["bounds"],
                    opacity=0.65,
                    name="LST"
                ).add_to(m)

        ndvi_overlay = None
        if "NDVI Vegetation Index" in selected_layers:
            ndvi_overlay = get_raster_stats_and_overlay("ndvi")
            if ndvi_overlay.get("png_path") and ndvi_overlay.get("bounds"):
                folium.raster_layers.ImageOverlay(
                    image=ndvi_overlay["png_path"],
                    bounds=ndvi_overlay["bounds"],
                    opacity=0.65,
                    name="NDVI"
                ).add_to(m)

        if "Geothermal Manifestations" in selected_layers:
            for manifest in MANIFESTATIONS:
                name_val = manifest.get('name', 'Titik Manifestasi')
                type_val = manifest.get('type', 'Manifestasi')
                temp_val = manifest.get('temp', '-')
                ph_val = manifest.get('ph_level', manifest.get('ph', '-'))
                folium.CircleMarker(
                    location=[manifest["lat"], manifest["lng"]],
                    radius=7,
                    color="#DC2626",
                    fill=True,
                    fillColor="#EF4444",
                    fillOpacity=0.85,
                    weight=1.5,
                    popup=f"<b>{name_val}</b><br>Tipe: {type_val}<br>Suhu: {temp_val}°C | pH: {ph_val}",
                    tooltip=name_val
                ).add_to(m)

        folium.LayerControl().add_to(m)
        st_folium(m, width="100%", height=440, key="evidence_overlay_map")

        has_lst = "Land Surface Temperature" in selected_layers and lst_overlay
        has_ndvi = "NDVI Vegetation Index" in selected_layers and ndvi_overlay

        if has_lst or has_ndvi:
            leg_col1, leg_col2 = st.columns(2 if (has_lst and has_ndvi) else 1)

            if has_lst:
                target_col = leg_col1 if (has_lst and has_ndvi) else st
                with target_col:
                    st.markdown(textwrap.dedent(f"""
<div style="padding:0.5rem 0.75rem;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;margin-top:0.5rem;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.2rem;">
<span style="font-size:0.72rem;font-weight:700;color:#0F172A;">🌡️ LST Thermal Gradient</span>
<span style="font-size:0.65rem;font-weight:700;color:#DC2626;">Hotspot</span>
</div>
<div style="height:8px;border-radius:4px;background:linear-gradient(90deg, #0369A1 0%, #38BDF8 35%, #FEF08A 55%, #F59E0B 75%, #DC2626 90%, #7F1D1D 100%);"></div>
<div style="display:flex;justify-content:space-between;font-size:0.68rem;color:#64748B;font-weight:600;margin-top:0.2rem;">
<span>{lst_overlay['min']:.1f}°C</span>
<span>Rata-Rata: {lst_overlay['mean']:.1f}°C</span>
<span style="color:#DC2626;">{lst_overlay['max']:.1f}°C</span>
</div>
</div>
""").strip(), unsafe_allow_html=True)

            if has_ndvi:
                target_col = leg_col2 if (has_lst and has_ndvi) else st
                with target_col:
                    st.markdown(textwrap.dedent(f"""
<div style="padding:0.5rem 0.75rem;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;margin-top:0.5rem;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.2rem;">
<span style="font-size:0.72rem;font-weight:700;color:#0F172A;">🌿 NDVI Kerapatan Kanopi</span>
<span style="font-size:0.65rem;font-weight:700;color:#047857;">Lebat</span>
</div>
<div style="height:8px;border-radius:4px;background:linear-gradient(90deg, #92400E 0%, #D97706 20%, #FACC15 40%, #4ADE80 65%, #16A34A 85%, #064E3B 100%);"></div>
<div style="display:flex;justify-content:space-between;font-size:0.68rem;color:#64748B;font-weight:600;margin-top:0.2rem;">
<span>{ndvi_overlay['min']:.2f}</span>
<span>Rata-Rata: {ndvi_overlay['mean']:.2f}</span>
<span style="color:#047857;">{ndvi_overlay['max']:.2f}</span>
</div>
</div>
""").strip(), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Expander Informasi Data ─────────────────────────────────────────────
    with st.expander("ℹ️ Detail Rencana Integrasi Lapisan Lanjutan", expanded=False):
        st.markdown("""
            - **Densitas Kelurusan (Lineament Density):** Ekstraksi sesar otomatis dari DEM SRTM 30m.
            - **Alterasi Hidrotermal:** Band ratio mineral ASTER (Al-OH, Fe-oxide, silika).
            - **Mikro-Seismisitas:** Katalog gempa tektonik lokal BMKG Sulawesi Utara.
        """)
