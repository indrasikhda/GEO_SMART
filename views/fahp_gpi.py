import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

from core.fahp import (
    calculate_fahp_weights,
    CRITERIA_LIST,
    get_default_pairwise_matrix,
    get_literature_weights,
)
from core.data import DATA_SOURCES_INVENTORY, SUPPORTING_EVIDENCE
from core.maps import create_base_map
from ui.components import page_header, kpi_card, card_header, dark_highlight_card

# Konstanta dan helper dipakai bersama halaman lain agar tampilan konsisten
from views.overview import CRITERIA_SOURCE, SUPPORTING_SOURCE, ID_NAMES, _status_badge
from views.remote_sensing import _load_layer, _legend_html


# ════════════════════════════════════════════════════════════════════════════
# Halaman: FAHP & GPI
# Pola: header → 4 KPI → [matriks 6 | bobot 6] → subkriteria → [status+rumus 5 | peta 7]
# ════════════════════════════════════════════════════════════════════════════

CR_LIMIT = 0.10
MAP_HEIGHT = 480

# Subkriteria berbasis literatur (kerangka awal)
SUBCRITERIA = {
    "manifestation": [
        ("0–2500 m", 0.486),
        ("2500–5000 m", 0.328),
        ("5000–10000 m", 0.130),
        (">10000 m", 0.056),
    ],
    "geology": [
        ("Indicator areas", 0.800),
        ("Other", 0.200),
    ],
    "alteration": [
        ("Indicator areas", 0.800),
        ("Other", 0.200),
    ],
    "lineament": [
        ("0–1000 m", 0.486),
        ("1000–2500 m", 0.328),
        ("2500–5000 m", 0.130),
        (">5000 m", 0.056),
    ],
    "lst": [
        ("45.1–55.04 °C", 0.486),
        ("40.1–45 °C", 0.328),
        ("30.1–40 °C", 0.130),
        ("−0.23–30 °C", 0.056),
    ],
}
SUB_LABEL_ID = {"Indicator areas": "Area indikator", "Other": "Lainnya"}


def format_fuzzy(value):
    """Format Triangular Fuzzy Number (l, m, u) untuk tampilan."""
    if isinstance(value, (tuple, list)) and len(value) == 3:
        return f"({value[0]:.3g}, {value[1]:.3g}, {value[2]:.3g})"
    return str(value)


def _weights_fig(names, calc, lit):
    """Bar horizontal berkelompok: bobot hasil hitung vs bobot literatur."""
    order = sorted(range(len(names)), key=lambda i: calc[i])  # terbesar di atas
    y = [names[i] for i in order]

    fig = go.Figure()
    fig.add_bar(
        y=y,
        x=[lit[i] for i in order],
        orientation="h",
        name="Literatur",
        marker=dict(color="#CFE3D8"),
        hovertemplate="%{y}<br>Literatur: %{x:.1f}%<extra></extra>",
    )
    fig.add_bar(
        y=y,
        x=[calc[i] for i in order],
        orientation="h",
        name="Dihitung",
        marker=dict(color="#22C55E"),
        text=[f"{calc[i]:.1f}%" for i in order],
        textposition="outside",
        hovertemplate="%{y}<br>Dihitung: %{x:.1f}%<extra></extra>",
    )
    fig.update_layout(
        height=310,
        barmode="group",
        bargap=0.35,
        margin=dict(l=0, r=40, t=26, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, Inter, sans-serif", size=11, color="#475569"),
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=1, traceorder="reversed"),
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False, title="",
                   range=[0, max(calc + lit) * 1.2]),
        yaxis=dict(showgrid=False, title=""),
    )
    return fig


def render_fahp_gpi():
    # ── Matriks & perhitungan FAHP ───────────────────────────────────────────
    if "fahp_matrix" not in st.session_state:
        st.session_state.fahp_matrix = get_default_pairwise_matrix()

    current_matrix = st.session_state.fahp_matrix
    fahp_res = calculate_fahp_weights(current_matrix)
    weights = fahp_res["weights"]
    cr = fahp_res["CR"]
    is_ok = fahp_res["is_consistent"]

    ids = [c["id"] for c in CRITERIA_LIST]
    short_names = [ID_NAMES.get(cid, c["name"]) for cid, c in zip(ids, CRITERIA_LIST)]
    top_i = max(range(len(weights)), key=lambda i: weights[i])

    # Status bukti dari core/data.py
    src_status = {d["Data Source"]: d["Status"] for d in DATA_SOURCES_INVENTORY}
    crit_status = [(cid, src_status.get(CRITERIA_SOURCE.get(cid, ""), "N/A")) for cid in ids]
    n_ready = sum(1 for _, s in crit_status if s == "REAL")
    pending = [ID_NAMES.get(cid, cid) for cid, s in crit_status if s != "REAL"]

    # ── Header ───────────────────────────────────────────────────────────────
    page_header(
        title="FAHP & GPI",
        subtitle="Pembobotan kriteria Fuzzy AHP dan dasar perhitungan GPI.",
        badge_text="● Model Konsisten" if is_ok else "● Perlu Review",
        badge_tooltip=f"Consistency Ratio (CR) < {CR_LIMIT:.2f} memenuhi kaidah konsistensi Saaty.",
    )

    # ── KPI ──────────────────────────────────────────────────────────────────
    if not is_ok:
        cr_trend, cr_type = "Perlu review", "warning"
    elif cr >= 0.9 * CR_LIMIT:
        cr_trend, cr_type = "Konsisten · mendekati batas", "warning"
    else:
        cr_trend, cr_type = f"Konsisten (CR < {CR_LIMIT:.2f})", "success"

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Jumlah Kriteria", str(len(CRITERIA_LIST)),
                 subtext="Parameter spasial", spark=weights)
    with k2:
        kpi_card("Rasio Konsistensi", f"{cr:.3f}", trend=cr_trend, trend_type=cr_type)
    with k3:
        kpi_card("Bobot Tertinggi", f"{weights[top_i] * 100:.1f}%", subtext=short_names[top_i])
    with k4:
        kpi_card("Metode", "Fuzzy AHP", subtext="Şener & Şener (2021)")

    st.write("")

    # ── Baris 1: matriks (kiri) + bobot (kanan) ──────────────────────────────
    col_matrix, col_weights = st.columns(2, gap="medium")

    with col_matrix:
        with st.container(key="card_matrix"):
            card_header("Matriks Perbandingan Fuzzy",
                        "Bilangan fuzzy segitiga (bawah, modus, atas)")

            labels = [f"K{i + 1}" for i in range(len(ids))]
            df_matrix = pd.DataFrame(
                [[format_fuzzy(v) for v in row] for row in current_matrix],
                index=[f"{lb} · {nm}" for lb, nm in zip(labels, short_names)],
                columns=labels,
            )
            st.dataframe(df_matrix, use_container_width=True, height=228)

            if st.button("Atur ulang ke matriks literatur", use_container_width=True):
                st.session_state.fahp_matrix = get_default_pairwise_matrix()
                st.rerun()

            with st.expander("Cara membaca bilangan fuzzy", expanded=False):
                st.markdown(
                    "Setiap sel berbentuk **(bawah, modus, atas)**, misalnya **(3, 4, 6)**: "
                    "tingkat kepentingan relatif berupa rentang, bukan satu angka tunggal. "
                    "Matriks ini adalah model awal berbasis literatur."
                )

    with col_weights:
        with st.container(key="card_weights"):
            card_header("Bobot Kriteria", "Hasil hitung dari matriks vs bobot literatur")

            calc = [w * 100 for w in weights]
            lit = [w * 100 for w in get_literature_weights()]
            st.plotly_chart(
                _weights_fig(short_names, calc, lit),
                use_container_width=True,
                config={"displayModeBar": False},
            )

            with st.expander("Peran tiap kriteria", expanded=False):
                st.dataframe(
                    pd.DataFrame({
                        "Kriteria": short_names,
                        "Bobot": [f"{w * 100:.2f}%" for w in weights],
                        "Peran": [c["role"] for c in CRITERIA_LIST],
                    }),
                    use_container_width=True,
                    hide_index=True,
                )

    # ── Subkriteria ──────────────────────────────────────────────────────────
    st.write("")
    with st.container(key="card_sub"):
        card_header("Subkriteria Berbasis Literatur",
                    "Skor standar tiap kelas pada kerangka awal")
        sub_cols = st.columns(len(CRITERIA_LIST), gap="medium")
        for col, cid, nm in zip(sub_cols, ids, short_names):
            with col:
                rows = "".join(
                    f'<div class="stat-row"><span class="l">{SUB_LABEL_ID.get(label, label)}</span>'
                    f'<span class="v">{val:.3f}</span></div>'
                    for label, val in SUBCRITERIA.get(cid, [])
                ) or '<div class="card-head-sub">Belum ada subkriteria.</div>'
                st.markdown(
                    f'<div style="font-size:0.8rem;font-weight:700;color:#0F172A;'
                    f'margin-bottom:0.15rem;">{nm}</div><div>{rows}</div>',
                    unsafe_allow_html=True,
                )

    st.write("")

    # ── Baris GPI: status + rumus + kesiapan (kiri) | peta referensi (kanan) ─
    col_gpi, col_map = st.columns([5, 7], gap="medium")

    with col_gpi:
        dark_highlight_card(
            title="Status model GPI",
            main_stat="Preliminary",
            sub_stat=f"{n_ready}/{len(crit_status)} kriteria bukti tersedia",
            desc=(f"{', '.join(pending)} belum terintegrasi; GPI spasial final menunggu lapisan ini."
                  if pending else "Semua kriteria bukti sudah terintegrasi."),
            tag="STATUS MODEL",
        )

        with st.container(key="card_formula"):
            card_header("Rumus Weighted Overlay")
            st.latex(r"GPI(x,y) = \sum_i w_i \, S_i(x,y)")
            st.markdown(
                '<div class="card-head-sub">wᵢ = bobot FAHP · Sᵢ(x,y) = skor bukti terstandar (0–1)</div>',
                unsafe_allow_html=True,
            )

        with st.container(key="card_evidence"):
            card_header("Status Integrasi Bukti")
            rows = "".join(
                f'<div class="stat-row"><span class="l">{ID_NAMES.get(cid, cid)}</span>'
                f'<span class="v">{_status_badge(status)}</span></div>'
                for cid, status in crit_status
            )
            for item in SUPPORTING_EVIDENCE:
                status = src_status.get(SUPPORTING_SOURCE.get(item["id"], ""), item.get("status", "N/A"))
                rows += (
                    f'<div class="stat-row"><span class="l">{ID_NAMES.get(item["id"], item["name"])}</span>'
                    f'<span class="v">{_status_badge(status)}</span></div>'
                )
            st.markdown(f'<div>{rows}</div>', unsafe_allow_html=True)

    with col_map:
        with st.container(key="card_map"):
            card_header("Referensi Spasial", "Lapisan LST sebagai bukti termal (data nyata)")

            lst = _load_layer("lst")
            m = create_base_map(center=[1.35, 124.85], zoom=8)
            if lst.get("png_path") and lst.get("bounds"):
                folium.raster_layers.ImageOverlay(
                    image=lst["png_path"],
                    bounds=lst["bounds"],
                    opacity=0.65,
                    name="LST",
                ).add_to(m)
            folium.LayerControl().add_to(m)
            st_folium(
                m,
                width="100%",
                height=MAP_HEIGHT,
                key="gpi_reference_map",
                returned_objects=[],
            )

            if lst.get("min") is not None:
                st.markdown(_legend_html("lst", lst), unsafe_allow_html=True)

    # ── Detail teknis ────────────────────────────────────────────────────────
    with st.expander("Detail teknis", expanded=False):
        st.markdown(
            f"""
- **Metode:** Fuzzy AHP berbasis literatur dengan perbandingan berpasangan bilangan fuzzy segitiga.
- **Diagnostik konsistensi:** λmax = {fahp_res["lambda_max"]:.4f}, CI = {fahp_res["CI"]:.4f}, CR = {fahp_res["CR"]:.4f} (batas {CR_LIMIT:.2f}).
- **GPI:** overlay terbobot spasial, GPI(x,y) = Σ [wᵢ × Sᵢ(x,y)]; GPI spasial lengkap memerlukan semua lapisan bukti terstandar.
- **Status:** preliminary, integrasi bukti masih berjalan. Wilayah target: Sulawesi Utara.
            """
        )