import html
import math

import pandas as pd
import streamlit as st

from core.data import DATA_SOURCES_INVENTORY
from ui.components import page_header, kpi_card, card_header

# ════════════════════════════════════════════════════════════════════════════
# Halaman: Sumber Data & Provenance
# Pola: header → 4 KPI → [katalog dengan filter 7 | komposisi status 5] → expander
# Semua dataset dikelompokkan ke 4 kelompok status, jadi total KPI selalu cocok.
# ════════════════════════════════════════════════════════════════════════════

# kelompok → (label, latar badge, teks badge, warna donut)
GROUPS = {
    "real": ("Data nyata", "#DCFCE7", "#15803D", "#22C55E"),
    "model": ("Model & indeks", "#EFF6FF", "#1D4ED8", "#3B82F6"),
    "plan": ("Usulan & simulasi", "#FEF3C7", "#B45309", "#F59E0B"),
    "pending": ("Menunggu", "#F1F5F9", "#64748B", "#94A3B8"),
}
GROUP_ORDER = ("real", "model", "plan", "pending")

STATUS_GROUP = {
    "REAL": "real",
    "LITERATURE-INFORMED": "model",
    "METHODOLOGICAL FRAMEWORK": "model",
    "PRELIMINARY": "model",
    "CALCULATED": "model",
    "PROPOSED": "plan",
    "SIMULATED": "plan",
    "PENDING": "pending",
}
STATUS_LABEL = {
    "REAL": "Data nyata",
    "LITERATURE-INFORMED": "Literatur",
    "METHODOLOGICAL FRAMEWORK": "Kerangka metode",
    "PRELIMINARY": "Awal",
    "CALCULATED": "Hasil hitung",
    "PROPOSED": "Usulan",
    "SIMULATED": "Simulasi",
    "PENDING": "Menunggu",
}


def _e(value) -> str:
    return html.escape(str(value), quote=True)


def _group_of(item: dict) -> str:
    return STATUS_GROUP.get(item.get("Status", ""), "model")


def _donut_svg(counts: dict, total: int) -> str:
    r = 42
    circ = 2 * math.pi * r
    offset = 0.0
    arcs = ""
    for key in GROUP_ORDER:
        n = counts.get(key, 0)
        if n <= 0 or total <= 0:
            continue
        length = n / total * circ
        arcs += (
            f'<circle cx="60" cy="60" r="{r}" fill="none" stroke="{GROUPS[key][3]}" '
            f'stroke-width="14" stroke-dasharray="{length:.2f} {circ - length:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}" transform="rotate(-90 60 60)"/>'
        )
        offset += length
    return (
        '<svg width="150" height="150" viewBox="0 0 120 120">'
        f'<circle cx="60" cy="60" r="{r}" fill="none" stroke="#EEF2F0" stroke-width="14"/>'
        f'{arcs}'
        f'<text x="60" y="60" text-anchor="middle" font-size="24" font-weight="800" fill="#0F172A">{total}</text>'
        '<text x="60" y="76" text-anchor="middle" font-size="9" fill="#64748B">dataset</text>'
        '</svg>'
    )


def _rows_html(items) -> str:
    clamp = ("display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden;")
    rows = ""
    for it in items:
        status = it.get("Status", "")
        g = _group_of(it)
        _, bg, fg, _ = GROUPS[g]
        label = STATUS_LABEL.get(status, status.title())
        role = it.get("Role", "")
        rows += (
            '<div style="padding:0.65rem 0;border-bottom:1px solid #F1F5F9;">'
            '<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:0.75rem;">'
            '<div style="min-width:0;">'
            f'<div style="font-size:0.86rem;font-weight:700;color:#0F172A;">{_e(it.get("Data Source", ""))}</div>'
            f'<div title="{_e(role)}" style="font-size:0.74rem;color:#64748B;margin-top:0.1rem;{clamp}">{_e(role)}</div>'
            '</div>'
            f'<span title="{_e(status)}" style="flex-shrink:0;font-size:0.62rem;font-weight:700;'
            f'padding:0.12rem 0.5rem;border-radius:9999px;background:{bg};color:{fg};">{_e(label)}</span>'
            '</div>'
            '<div style="display:flex;flex-wrap:wrap;gap:0.25rem 1.25rem;font-size:0.7rem;'
            'color:#64748B;margin-top:0.35rem;">'
            f'<span><b>Layer:</b> {_e(it.get("Layer", "N/A"))}</span>'
            f'<span><b>Sumber:</b> {_e(it.get("Source", "N/A"))}</span>'
            '</div></div>'
        )
    return f'<div style="max-height:640px;overflow-y:auto;padding-right:4px;">{rows}</div>'


def render_data_sources():
    items = DATA_SOURCES_INVENTORY
    df_raw = pd.DataFrame(items)

    counts = {k: 0 for k in GROUP_ORDER}
    for it in items:
        counts[_group_of(it)] += 1
    total = len(items)
    not_real = counts["plan"] + counts["pending"]

    # ── Header ───────────────────────────────────────────────────────────────
    page_header(
        title="Sumber Data & Provenance",
        subtitle="Inventaris dataset, sumber, dan status verifikasinya.",
        badge_text="● Transparansi Data",
        badge_tooltip=(
            "Setiap dataset diberi status (data nyata, berbasis literatur, hitungan awal, "
            "usulan, simulasi, atau menunggu) agar asal dan tingkat kepastiannya jelas."
        ),
    )

    # ── KPI (empat kelompok = total) ─────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Total Dataset", str(total), subtext="Basis data spasial & model")
    with k2:
        kpi_card("Data Nyata", str(counts["real"]),
                 trend=f"{counts['real'] / total * 100:.0f}% dari total" if total else "",
                 trend_type="success")
    with k3:
        kpi_card("Model & Indeks", str(counts["model"]), subtext="Literatur dan hitungan awal")
    with k4:
        kpi_card("Usulan, Simulasi, Menunggu", str(not_real), subtext="Belum berupa data nyata")

    st.write("")

    col_cat, col_side = st.columns([7, 5], gap="medium")

    # ── Katalog dengan filter ────────────────────────────────────────────────
    with col_cat:
        with st.container(key="card_catalog"):
            card_header("Katalog Dataset", "Filter berdasarkan kelompok status")

            options = ["all", *GROUP_ORDER]
            labels = {"all": f"Semua ({total})"}
            labels.update({k: f"{GROUPS[k][0]} ({counts[k]})" for k in GROUP_ORDER})
            choice = st.radio("Kelompok status", options, format_func=labels.get,
                              horizontal=True, label_visibility="collapsed", key="ds_filter")

            shown = items if choice == "all" else [it for it in items if _group_of(it) == choice]
            if shown:
                st.markdown(_rows_html(shown), unsafe_allow_html=True)
            else:
                st.caption("Tidak ada dataset pada kelompok ini.")

    # ── Komposisi status + unduh ─────────────────────────────────────────────
    with col_side:
        with st.container(key="card_composition"):
            card_header("Komposisi Status", f"{total} dataset terdaftar")

            legend = "".join(
                '<div class="stat-row"><span class="l" style="display:flex;align-items:center;gap:0.5rem;">'
                f'<span style="width:10px;height:10px;border-radius:50%;background:{GROUPS[k][3]};"></span>'
                f'{GROUPS[k][0]}</span><span class="v">{counts[k]}</span></div>'
                for k in GROUP_ORDER
            )
            st.markdown(
                '<div style="display:flex;justify-content:center;padding:0.25rem 0 0.5rem;">'
                f'{_donut_svg(counts, total)}</div><div>{legend}</div>',
                unsafe_allow_html=True,
            )

            st.download_button(
                label="Unduh katalog (CSV)",
                data=df_raw.to_csv(index=False).encode("utf-8-sig"),
                file_name="geosmart_data_inventory.csv",
                mime="text/csv",
                key="data_sources_download_csv",
                use_container_width=True,
            )

    # ── Tabel lengkap ────────────────────────────────────────────────────────
    with st.expander("Lihat tabel katalog lengkap", expanded=False):
        st.dataframe(df_raw, use_container_width=True, hide_index=True)