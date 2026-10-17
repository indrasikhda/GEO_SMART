import streamlit as st
import folium
from streamlit_folium import st_folium

from core.io import PRIORITY_ZONES
from core.maps import create_base_map
from ui.components import page_header, kpi_card, card_header

# ════════════════════════════════════════════════════════════════════════════
# Halaman: Zona Prioritas
# Semua angka dan legenda dihitung dari PRIORITY_ZONES (core/io.py).
# Pola: header → 4 KPI → [kartu peringkat 5 | kartu peta 7] → expander
# ════════════════════════════════════════════════════════════════════════════

# (latar badge, teks badge, label)
PRIORITY_STYLE = {
    "High": ("#DCFCE7", "#15803D", "TINGGI"),
    "Moderate": ("#FEF3C7", "#B45309", "SEDANG"),
    "Low": ("#F1F5F9", "#64748B", "RENDAH"),
}
BAR_COLOR = {"High": "#22C55E", "Moderate": "#F59E0B", "Low": "#94A3B8"}
MARKER_COLOR = {"High": "#16A34A", "Moderate": "#D97706", "Low": "#64748B"}
CLASS_ORDER = ("High", "Moderate", "Low")
MAP_HEIGHT = 540


def _has_constraint(constraint) -> bool:
    """True bila zona punya kendala nyata (bukan 'Cleared / Unconstrained')."""
    return bool(constraint) and not str(constraint).strip().lower().startswith("cleared")


def _rank_list_html(zones) -> str:
    """Daftar peringkat dalam SATU blok HTML, bisa di-scroll agar tinggi sejajar dengan peta."""
    rows = ""
    for i, z in enumerate(zones, 1):
        p = z["priority"]
        bg, fg, label = PRIORITY_STYLE.get(p, PRIORITY_STYLE["Low"])
        bar = BAR_COLOR.get(p, BAR_COLOR["Low"])
        pct = max(0.0, min(100.0, z["gpi"] * 100))

        meta = f'{z["area"]} km²'
        if _has_constraint(z.get("constraint")):
            meta += (f' · <span style="color:#B45309;font-weight:600;">'
                     f'{z["constraint"]}</span>')

        rows += (
            '<div style="padding:0.6rem 0;border-bottom:1px solid #F1F5F9;">'
            '<div style="display:flex;align-items:center;gap:0.6rem;">'
            f'<span style="width:22px;font-size:0.72rem;font-weight:700;color:#94A3B8;">{i}</span>'
            f'<span style="font-size:0.86rem;font-weight:700;color:#0F172A;flex:1;">{z["zone"]}</span>'
            f'<span style="font-size:0.62rem;font-weight:700;padding:0.12rem 0.5rem;'
            f'border-radius:9999px;background:{bg};color:{fg};">{label}</span>'
            f'<span style="font-size:0.9rem;font-weight:800;color:#0F172A;min-width:38px;'
            f'text-align:right;">{z["gpi"]:.2f}</span>'
            '</div>'
            f'<div style="margin:0.4rem 0 0.3rem 28px;height:6px;border-radius:3px;background:#EEF2F0;">'
            f'<div style="width:{pct:.0f}%;height:100%;border-radius:3px;background:{bar};"></div></div>'
            f'<div style="margin-left:28px;font-size:0.7rem;color:#64748B;">{meta}</div>'
            '</div>'
        )
    return f'<div style="max-height:{MAP_HEIGHT}px;overflow-y:auto;padding-right:4px;">{rows}</div>'


def render_priority():
    zones = sorted(PRIORITY_ZONES, key=lambda z: z["gpi"], reverse=True)
    by_class = {}
    for z in zones:
        by_class.setdefault(z["priority"], []).append(z)

    high = by_class.get("High", [])
    moderate = by_class.get("Moderate", [])
    low = by_class.get("Low", [])
    n_clear = sum(1 for z in zones if not _has_constraint(z.get("constraint")))
    n_constrained = len(zones) - n_clear

    def _range(items):
        return (min(z["gpi"] for z in items), max(z["gpi"] for z in items)) if items else None

    r_high, r_mod = _range(high), _range(moderate)

    # ── Header ───────────────────────────────────────────────────────────────
    page_header(
        title="Zona Prioritas",
        subtitle="Peringkat kandidat zona eksplorasi berdasarkan skor GPI.",
        badge_text=f"● {len(zones)} Kandidat Zona",
        badge_tooltip=(
            "Zona masih berstatus prototipe: skor GPI awal dengan bobot FAHP "
            "berbasis literatur. Kendala spasial dicatat per zona."
        ),
    )

    # ── Baris KPI ────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card(
            "Total Kandidat", str(len(zones)),
            subtext=(f"{len(low)} prioritas rendah" if low else "Wilayah prospek"),
            spark=[z["gpi"] for z in zones], spark_hi=0,
        )
    with k2:
        kpi_card(
            "Prioritas Tinggi", str(len(high)),
            trend=(f"GPI ≥ {r_high[0]:.2f}" if r_high else ""), trend_type="success",
        )
    with k3:
        kpi_card(
            "Prioritas Sedang", str(len(moderate)),
            trend=(f"GPI {r_mod[0]:.2f}–{r_mod[1]:.2f}" if r_mod else ""), trend_type="warning",
        )
    with k4:
        kpi_card(
            "Tanpa Kendala", f"{n_clear}/{len(zones)}",
            subtext=f"{n_constrained} zona memiliki kendala spasial",
        )

    st.write("")

    col_rank, col_map = st.columns([5, 7], gap="medium")

    # ── Kartu peringkat ──────────────────────────────────────────────────────
    with col_rank:
        with st.container(key="card_rank"):
            card_header("Peringkat Zona", "Urut dari skor GPI tertinggi")
            st.markdown(_rank_list_html(zones), unsafe_allow_html=True)

    # ── Kartu peta ───────────────────────────────────────────────────────────
    with col_map:
        with st.container(key="card_map"):
            card_header("Peta Sebaran", "Lokasi kandidat zona eksplorasi di Sulawesi Utara")

            m = create_base_map(center=[1.35, 124.85], zoom=8)
            for z in zones:
                p = z["priority"]
                color = MARKER_COLOR.get(p, MARKER_COLOR["Low"])
                label = PRIORITY_STYLE.get(p, PRIORITY_STYLE["Low"])[2].title()
                popup = (f"<b>{z['zone']}</b><br>GPI {z['gpi']:.2f} · {label}"
                         f"<br>Luas {z['area']} km²")
                if _has_constraint(z.get("constraint")):
                    popup += f"<br>Kendala: {z['constraint']}"
                folium.CircleMarker(
                    location=[z["lat"], z["lng"]],
                    radius=8,
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.8,
                    weight=2,
                    popup=popup,
                    tooltip=f"{z['zone']} · GPI {z['gpi']:.2f}",
                ).add_to(m)

            folium.LayerControl().add_to(m)
            st_folium(
                m,
                width="100%",
                height=MAP_HEIGHT,
                key="priority_zones_map",
                returned_objects=[],
            )

            legend = ""
            for key in CLASS_ORDER:
                items = by_class.get(key, [])
                if not items:
                    continue
                label = PRIORITY_STYLE[key][2].title()
                legend += (
                    '<span style="display:flex;align-items:center;gap:0.4rem;">'
                    f'<span style="width:10px;height:10px;border-radius:50%;'
                    f'background:{MARKER_COLOR[key]};"></span>'
                    f'Prioritas {label} ({len(items)})</span>'
                )
            st.markdown(
                '<div style="display:flex;flex-wrap:wrap;gap:0.4rem 1.25rem;font-size:0.75rem;'
                f'color:#475569;font-weight:600;">{legend}</div>',
                unsafe_allow_html=True,
            )

    # ── Catatan klasifikasi ──────────────────────────────────────────────────
    with st.expander("Dasar klasifikasi zona", expanded=False):
        lines = []
        if r_high:
            lines.append(f"- **Prioritas tinggi:** skor GPI ≥ {r_high[0]:.2f}.")
        if r_mod:
            lines.append(f"- **Prioritas sedang:** skor GPI {r_mod[0]:.2f}–{r_mod[1]:.2f}.")
        if low:
            lo_r = _range(low)
            lines.append(f"- **Prioritas rendah:** skor GPI {lo_r[0]:.2f}–{lo_r[1]:.2f}.")
        lines.append(
            "- **Kendala spasial** (mis. zona penyangga kawah, pertanian, perkotaan, lereng bahaya "
            "vulkanik) dicatat per zona dan terpisah dari kelas prospek."
        )
        lines.append(
            "- **Status:** zona masih prototipe; bobot FAHP berbasis literatur "
            "(Şener & Şener, 2021) dan belum divalidasi pakar lokal."
        )
        st.markdown("\n".join(lines))