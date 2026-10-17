import streamlit as st
import folium
from streamlit_folium import st_folium

from core.io import MANIFESTATIONS
from core.maps import create_base_map, add_geological_layers
from core.data import DATA_SOURCES_INVENTORY, CURRENT_FAHP_CRITERIA
from ui.components import page_header, kpi_card, card_header, badge

# Konstanta/helper dipakai bersama halaman lain agar konsisten
from views.overview import CRITERIA_SOURCE, ID_NAMES
from views.remote_sensing import _load_layer, _legend_html


# ════════════════════════════════════════════════════════════════════════════
# Halaman: Bukti Multi-Sumber
# Pola: header → 4 KPI → [inventaris lapisan 5 | peta overlay 7] → expander
# Status lapisan diambil dari core/data.py (DATA_SOURCES_INVENTORY).
# ════════════════════════════════════════════════════════════════════════════

# "inv" = nama entri di DATA_SOURCES_INVENTORY; None = belum ada di inventaris (dianggap pending)
EVIDENCE_LAYERS = [
    {"id": "lst", "name": "Suhu Permukaan (LST)", "type": "Raster",
     "source": "Landsat 8/9 TIRS", "inv": "Land Surface Temperature (LST 2025)"},
    {"id": "ndvi", "name": "NDVI (Vegetasi)", "type": "Raster",
     "source": "Sentinel-2 MSI", "inv": "Normalized Difference Vegetation Index (NDVI 2025)"},
    {"id": "manifest", "name": "Manifestasi Panas Bumi", "type": "Titik",
     "source": "Survei lapangan", "inv": "Geothermal Manifestation Points"},
    {"id": "geology", "name": "Geologi / Litologi", "type": "Poligon",
     "source": "Peta geologi regional (1:100k)", "inv": "Geology / Lithological Units"},
    {"id": "fault", "name": "Sesar & Kelurusan", "type": "Garis",
     "source": "Geologi struktur (1:100k)", "inv": "Fault & Lineament Structures"},
    {"id": "lineament_density", "name": "Densitas Kelurusan", "type": "Raster",
     "source": "Analisis DEM", "inv": None},
    {"id": "alteration", "name": "Alterasi Hidrotermal", "type": "Poligon",
     "source": "ASTER/Sentinel-2", "inv": "Hydrothermal Alteration Zones"},
    {"id": "microseismic", "name": "Mikro-Seismisitas", "type": "Titik",
     "source": "Jaringan seismik", "inv": None},
]

DEFAULT_ON = {"lst", "ndvi", "manifest"}
MAP_HEIGHT = 420


def render_evidence():
    # ── Status lapisan dari core/data.py ─────────────────────────────────────
    src_status = {d["Data Source"]: d["Status"] for d in DATA_SOURCES_INVENTORY}
    for layer in EVIDENCE_LAYERS:
        layer["connected"] = src_status.get(layer["inv"]) == "REAL" if layer["inv"] else False

    total = len(EVIDENCE_LAYERS)
    connected = sum(1 for l in EVIDENCE_LAYERS if l["connected"])
    pending_layers = [l["name"] for l in EVIDENCE_LAYERS if not l["connected"]]
    pct = connected / total * 100 if total else 0.0

    crit_ids = [c["id"] for c in CURRENT_FAHP_CRITERIA]
    crit_pending = [
        ID_NAMES.get(cid, cid) for cid in crit_ids
        if src_status.get(CRITERIA_SOURCE.get(cid, "")) != "REAL"
    ]
    crit_ready = len(crit_ids) - len(crit_pending)

    # ── Header ───────────────────────────────────────────────────────────────
    page_header(
        title="Bukti Multi-Sumber",
        subtitle="Lapisan spasial geologi, sesar, manifestasi, dan penginderaan jauh.",
        badge_text=f"● {connected} dari {total} Terhubung",
        badge_tooltip=f"{connected} lapisan data spasial aktif dan siap di-overlay.",
    )

    # ── KPI ──────────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Total Lapisan", str(total), subtext="Lapisan bukti spasial")
    with k2:
        kpi_card("Lapisan Terhubung", str(connected),
                 trend=f"{pct:.1f}%", trend_type="success")
    with k3:
        shown = ", ".join(pending_layers[:2])
        extra = f" +{len(pending_layers) - 2}" if len(pending_layers) > 2 else ""
        kpi_card("Dalam Antrean", str(len(pending_layers)),
                 subtext=(shown + extra) if pending_layers else "Tidak ada")
    with k4:
        kpi_card("Kriteria GPI Siap", f"{crit_ready}/{len(crit_ids)}",
                 subtext=(f"{', '.join(crit_pending)} menunggu" if crit_pending
                          else "Semua kriteria tersedia"))

    st.write("")

    col_layers, col_map = st.columns([5, 7], gap="medium")

    # ── Kartu inventaris: checklist lapisan ──────────────────────────────────
    selected = set()
    with col_layers:
        with st.container(key="card_layers"):
            card_header("Inventaris Lapisan", "Pilih lapisan aktif untuk ditampilkan di peta")

            for layer in EVIDENCE_LAYERS:
                c_chk, c_info = st.columns([1, 9], gap="small", vertical_alignment="center")
                with c_chk:
                    if layer["connected"]:
                        if st.checkbox(
                            layer["name"],
                            value=layer["id"] in DEFAULT_ON,
                            key=f"layer_{layer['id']}",
                            label_visibility="collapsed",
                        ):
                            selected.add(layer["id"])
                    else:
                        st.checkbox(
                            layer["name"],
                            value=False,
                            disabled=True,
                            key=f"layer_{layer['id']}",
                            label_visibility="collapsed",
                        )
                with c_info:
                    name_color = "#0F172A" if layer["connected"] else "#94A3B8"
                    status_badge = badge("Aktif", "success") if layer["connected"] else badge("Pending", "neutral")
                    st.markdown(
                        '<div style="display:flex;justify-content:space-between;align-items:center;'
                        'gap:0.5rem;padding:0.35rem 0;border-bottom:1px solid #F1F5F9;">'
                        '<div>'
                        f'<div style="font-size:0.82rem;font-weight:600;color:{name_color};">{layer["name"]}</div>'
                        f'<div style="font-size:0.7rem;color:#64748B;">{layer["type"]} · {layer["source"]}</div>'
                        '</div>'
                        f'{status_badge}'
                        '</div>',
                        unsafe_allow_html=True,
                    )

            st.markdown(
                '<div style="margin-top:0.4rem;">'
                '<div style="display:flex;justify-content:space-between;font-size:0.75rem;'
                'color:#475569;font-weight:600;margin-bottom:0.3rem;">'
                f'<span>Kemajuan integrasi</span><span>{connected}/{total} · {pct:.1f}%</span></div>'
                '<div style="height:6px;background:#E2E8F0;border-radius:9999px;overflow:hidden;">'
                f'<div style="width:{pct:.1f}%;height:100%;'
                'background:linear-gradient(90deg,#22C55E,#16A34A);"></div></div></div>',
                unsafe_allow_html=True,
            )

    # ── Kartu peta overlay ───────────────────────────────────────────────────
    with col_map:
        with st.container(key="card_map"):
            card_header("Peta Overlay Spasial", "Kombinasi lapisan terpilih untuk delineasi prospek")

            m = create_base_map(center=[1.35, 124.85], zoom=8, include_geology=False)
            add_geological_layers(
                m,
                show_lito="geology" in selected,
                show_geostruk="fault" in selected,
            )

            layer_data = {}
            for lid, label in (("lst", "LST"), ("ndvi", "NDVI")):
                if lid in selected:
                    data = _load_layer(lid)
                    layer_data[lid] = data
                    if data.get("png_path") and data.get("bounds"):
                        folium.raster_layers.ImageOverlay(
                            image=data["png_path"],
                            bounds=data["bounds"],
                            opacity=0.65,
                            name=label,
                        ).add_to(m)

            if "manifest" in selected:
                for mf in MANIFESTATIONS:
                    name_val = mf.get("name", "Titik Manifestasi")
                    folium.CircleMarker(
                        location=[mf["lat"], mf["lng"]],
                        radius=7,
                        color="#DC2626",
                        fill=True,
                        fillColor="#EF4444",
                        fillOpacity=0.85,
                        weight=1.5,
                        popup=(f"<b>{name_val}</b><br>Tipe: {mf.get('type', 'Manifestasi')}"
                               f"<br>Suhu: {mf.get('temp', '-')} °C"),
                        tooltip=name_val,
                    ).add_to(m)

            folium.LayerControl().add_to(m)
            st_folium(
                m,
                width="100%",
                height=MAP_HEIGHT,
                key="evidence_overlay_map",
                returned_objects=[],
            )

            for lid in ("lst", "ndvi"):
                data = layer_data.get(lid)
                if data and data.get("min") is not None:
                    st.markdown(
                        f'<div style="margin-top:0.4rem;">{_legend_html(lid, data)}</div>',
                        unsafe_allow_html=True,
                    )

    # ── Rencana integrasi lanjutan ───────────────────────────────────────────
    with st.expander("Rencana integrasi lapisan lanjutan", expanded=False):
        st.markdown(
            """
- **Densitas kelurusan:** ekstraksi sesar otomatis dari DEM SRTM 30 m.
- **Alterasi hidrotermal:** rasio band mineral ASTER (Al-OH, oksida besi, silika).
- **Mikro-seismisitas:** katalog gempa tektonik lokal BMKG Sulawesi Utara.
            """
        )