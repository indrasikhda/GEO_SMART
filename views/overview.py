import streamlit as st
import folium
from streamlit_folium import st_folium

from core.maps import create_base_map
from core.io import MANIFESTATIONS, GMN_NODES, PRIORITY_ZONES
from core.fahp import calculate_fahp_weights
from core.data import DATA_SOURCES_INVENTORY, CURRENT_FAHP_CRITERIA, SUPPORTING_EVIDENCE
from ui.components import (
    page_header,
    kpi_card,
    card_header,
    dark_highlight_card,
    badge,
)

# ════════════════════════════════════════════════════════════════════════════
# Halaman: Ringkasan
# Semua angka diturunkan dari core/ (tidak ada angka yang diketik manual).
# Pola: header → 4 KPI → [kartu peta 7 | kolom kartu 5] → expander
# ════════════════════════════════════════════════════════════════════════════

PRIORITY_LABEL = {"High": "Tinggi", "Moderate": "Sedang", "Low": "Rendah"}

# (warna latar, border, teks label, teks angka)
TILE_STYLE = {
    "High": ("#F0FDF4", "#BBF7D0", "#15803D", "#166534"),
    "Moderate": ("#FEFCE8", "#FEF08A", "#854D0E", "#713F12"),
    "Low": ("#F8FAFC", "#E2E8F0", "#64748B", "#334155"),
}

# Kriteria → nama entri di DATA_SOURCES_INVENTORY (core/data.py)
CRITERIA_SOURCE = {
    "manifestation": "Geothermal Manifestation Points",
    "geology": "Geology / Lithological Units",
    "alteration": "Hydrothermal Alteration Zones",
    "lineament": "Fault & Lineament Structures",
    "lst": "Land Surface Temperature (LST 2025)",
}
SUPPORTING_SOURCE = {
    "ndvi": "Normalized Difference Vegetation Index (NDVI 2025)",
}
ID_NAMES = {
    "manifestation": "Manifestasi panas bumi",
    "geology": "Geologi / litologi",
    "alteration": "Alterasi hidrotermal",
    "lineament": "Sesar & kelurusan",
    "lst": "Suhu permukaan (LST)",
    "ndvi": "NDVI (pendukung)",
}


def _status_badge(status: str) -> str:
    if status == "REAL":
        return badge("Data nyata", "success")
    if status == "PENDING":
        return badge("Menunggu", "neutral")
    return badge(status.title(), "neutral")


def render_overview():
    # ── Data turunan dari core ───────────────────────────────────────────────
    fahp = calculate_fahp_weights()
    cr = fahp["CR"]
    cr_text = "konsisten" if fahp["is_consistent"] else "tidak konsisten"

    zones = sorted(PRIORITY_ZONES, key=lambda z: z["gpi"], reverse=True)
    top = zones[0]
    by_class = {}
    for z in zones:
        by_class.setdefault(z["priority"], []).append(z)
    high = by_class.get("High", [])
    high_min = min((z["gpi"] for z in high), default=None)

    src_status = {d["Data Source"]: d["Status"] for d in DATA_SOURCES_INVENTORY}
    crit_status = [
        (c["id"], src_status.get(CRITERIA_SOURCE.get(c["id"], ""), "N/A"))
        for c in CURRENT_FAHP_CRITERIA
    ]
    n_total = len(crit_status)
    n_ready = sum(1 for _, s in crit_status if s == "REAL")
    pending = [ID_NAMES.get(cid, cid) for cid, s in crit_status if s != "REAL"]

    temps = [m["temp"] for m in MANIFESTATIONS]

    # ── Header ───────────────────────────────────────────────────────────────
    page_header(
        title="Ringkasan Sistem",
        subtitle="Temuan utama dan sebaran zona prospek panas bumi Sulawesi Utara.",
        badge_text="● Prototipe",
        badge_tooltip=(
            "Bobot FAHP berbasis literatur (Şener & Şener, 2021). "
            "Zona prioritas dan node GMN masih berstatus prototipe/usulan."
        ),
    )

    # ── Baris KPI (mini bar = data nyata) ────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card(
            "Zona Prioritas", str(len(zones)),
            subtext=(f"{len(high)} prospek tinggi (GPI ≥ {high_min:.2f})"
                     if high_min is not None else "Belum ada prospek tinggi"),
            spark=[z["gpi"] for z in zones], spark_hi=0,
        )
    with c2:
        kpi_card(
            "Kriteria FAHP", str(len(CURRENT_FAHP_CRITERIA)),
            subtext=f"CR {cr:.3f} · {cr_text}",
            spark=fahp["weights"], spark_hi=0,
        )
    with c3:
        kpi_card(
            "Kesiapan Bukti", f"{n_ready}/{n_total}",
            subtext=(f"{', '.join(pending)} belum tersedia"
                     if pending else "Semua kriteria tersedia"),
        )
    with c4:
        kpi_card(
            "Titik Manifestasi", str(len(MANIFESTATIONS)),
            subtext=f"Suhu {min(temps):.0f}–{max(temps):.0f} °C",
            spark=temps,
        )

    st.write("")

    col_map, col_right = st.columns([7, 5], gap="medium")

    # ── Kartu peta ───────────────────────────────────────────────────────────
    with col_map:
        with st.container(key="card_map"):
            card_header(
                "Peta Sebaran",
                f"{len(zones)} zona prioritas, {len(MANIFESTATIONS)} manifestasi termal, "
                f"{len(GMN_NODES)} usulan node GMN",
            )

            m = create_base_map(center=[1.35, 124.85], zoom=8)

            # Zona prioritas (digambar paling bawah)
            for z in zones:
                is_high = z["priority"] == "High"
                folium.CircleMarker(
                    location=[z["lat"], z["lng"]],
                    radius=6,
                    color="#16A34A" if is_high else "#D97706",
                    fill=True,
                    fillColor="#22C55E" if is_high else "#F59E0B",
                    fillOpacity=0.8,
                    weight=1.5,
                    popup=(f"<b>{z['zone']}</b><br>GPI {z['gpi']:.2f} · "
                           f"{PRIORITY_LABEL.get(z['priority'], z['priority'])}<br>"
                           f"{z['constraint']}"),
                    tooltip=f"{z['zone']} · GPI {z['gpi']:.2f}",
                ).add_to(m)

            for mf in MANIFESTATIONS:
                folium.CircleMarker(
                    location=[mf["lat"], mf["lng"]],
                    radius=7,
                    color="#DC2626",
                    fill=True,
                    fillColor="#EF4444",
                    fillOpacity=0.85,
                    weight=1.5,
                    popup=f"<b>{mf['name']}</b><br>{mf['type']} · {mf['temp']:.0f} °C",
                    tooltip=mf["name"],
                ).add_to(m)

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
                    tooltip=f"{node['id']} (usulan)",
                ).add_to(m)

            folium.LayerControl().add_to(m)
            st_folium(
                m,
                width="100%",
                height=470,
                key="overview_main_map",
                returned_objects=[],
            )

            n_mod = len(by_class.get("Moderate", []))
            st.markdown(
                '<div style="display:flex;flex-wrap:wrap;gap:0.4rem 1.25rem;font-size:0.75rem;'
                'color:#475569;font-weight:600;">'
                '<span style="display:flex;align-items:center;gap:0.4rem;">'
                '<span style="width:10px;height:10px;border-radius:50%;background:#22C55E;"></span>'
                f'Zona prospek tinggi ({len(high)})</span>'
                '<span style="display:flex;align-items:center;gap:0.4rem;">'
                '<span style="width:10px;height:10px;border-radius:50%;background:#F59E0B;"></span>'
                f'Zona prospek sedang ({n_mod})</span>'
                '<span style="display:flex;align-items:center;gap:0.4rem;">'
                '<span style="width:10px;height:10px;border-radius:50%;background:#EF4444;"></span>'
                f'Manifestasi ({len(MANIFESTATIONS)})</span>'
                '<span style="display:flex;align-items:center;gap:0.4rem;">'
                '<span style="width:10px;height:10px;border-radius:50%;background:#38BDF8;"></span>'
                f'Node GMN ({len(GMN_NODES)})</span>'
                '</div>',
                unsafe_allow_html=True,
            )

    # ── Kolom kanan: sorotan, distribusi, kesiapan ──────────────────────────
    with col_right:
        dark_highlight_card(
            title="Zona prioritas tertinggi",
            main_stat=top["zone"],
            sub_stat=f"GPI {top['gpi']:.2f} · Prospek {PRIORITY_LABEL.get(top['priority'], top['priority'])}",
            desc=f"Luas {top['area']} km² · {top['constraint']}",
            tag="ZONA TERATAS",
        )

        with st.container(key="card_dist"):
            card_header("Distribusi Zona Prospek", f"{len(zones)} zona berdasarkan skor GPI")

            tiles, n_tiles = "", 0
            for key in ("High", "Moderate", "Low"):
                items = by_class.get(key, [])
                if not items:
                    continue
                bg, bd, c_label, c_num = TILE_STYLE[key]
                lo = min(z["gpi"] for z in items)
                hi = max(z["gpi"] for z in items)
                tiles += (
                    f'<div style="background:{bg};border:1px solid {bd};border-radius:12px;'
                    'padding:0.75rem 0.5rem;text-align:center;">'
                    f'<div style="font-size:0.68rem;font-weight:700;color:{c_label};'
                    f'text-transform:uppercase;">{PRIORITY_LABEL[key]}</div>'
                    f'<div style="font-size:1.6rem;font-weight:800;color:{c_num};line-height:1.2;">'
                    f'{len(items)}</div>'
                    f'<div style="font-size:0.65rem;color:{c_label};font-weight:600;">'
                    f'GPI {lo:.2f}–{hi:.2f}</div></div>'
                )
                n_tiles += 1
            st.markdown(
                f'<div style="display:grid;grid-template-columns:repeat({max(n_tiles, 1)},1fr);'
                f'gap:0.75rem;">{tiles}</div>',
                unsafe_allow_html=True,
            )

        with st.container(key="card_ready"):
            card_header("Kesiapan Lapisan Spasial", "Status data kriteria GPI")

            rows = ""
            for cid, status in crit_status:
                rows += (
                    f'<div class="stat-row"><span class="l">{ID_NAMES.get(cid, cid)}</span>'
                    f'<span class="v">{_status_badge(status)}</span></div>'
                )
            for item in SUPPORTING_EVIDENCE:
                status = src_status.get(SUPPORTING_SOURCE.get(item["id"], ""), item.get("status", "N/A"))
                rows += (
                    f'<div class="stat-row"><span class="l">{ID_NAMES.get(item["id"], item["name"])}</span>'
                    f'<span class="v">{_status_badge(status)}</span></div>'
                )
            st.markdown(f'<div>{rows}</div>', unsafe_allow_html=True)

    # ── Catatan tertutup ─────────────────────────────────────────────────────
    with st.expander("Tentang alur kerja sistem", expanded=False):
        st.markdown(
            f"""
- **Alur analisis:** penginderaan jauh (LST/NDVI) → bukti multi-sumber → pembobotan FAHP → skor GPI → zona prioritas → node monitoring GMN.
- **Basis data:** {len(MANIFESTATIONS)} titik manifestasi (inventaris survei), data litologi dan struktur geologi Sulawesi Utara, serta citra Landsat 8/9 dan Sentinel-2.
- **Status model:** bobot FAHP berbasis literatur (Şener & Şener, 2021) dan belum divalidasi pakar lokal; zona prioritas masih prototipe; node GMN masih usulan.
            """
        )