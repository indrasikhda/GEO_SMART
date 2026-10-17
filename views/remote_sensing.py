import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import numpy as np

from core.raster import get_raster_stats_and_overlay
from core.maps import create_base_map
from ui.components import (
    page_header,
    kpi_card,
    card_header,
    stat_rows,
    dark_highlight_card,
)

# ════════════════════════════════════════════════════════════════════════════
# Halaman: Penginderaan Jauh (LST & NDVI)
# Pola halaman: header → 4 KPI → [kartu peta 7 | kartu statistik 5] → expander
# ════════════════════════════════════════════════════════════════════════════

LAYER_OPTIONS = {
    "Suhu Permukaan (LST)": "lst",
    "Indeks Vegetasi (NDVI)": "ndvi",
}
LAYER_TITLE = {
    "lst": "Suhu Permukaan (LST)",
    "ndvi": "Indeks Vegetasi (NDVI)",
}
NDVI_DENSE_THRESHOLD = 0.6  # ambang kanopi lebat; ubah di sini bila perlu


# ── Pemuatan data (di-cache agar tidak membaca raster tiap interaksi) ────────
@st.cache_data(show_spinner="Memuat data raster…")
def _load_layer(kind: str) -> dict:
    """
    Ambil statistik raster lalu ringkas semua turunan yang dibutuhkan UI.
    valid_array (besar) TIDAK disimpan di cache; hanya hasil ringkasnya.
    """
    stats = get_raster_stats_and_overlay(kind)
    arr = stats.get("valid_array")
    out = {k: v for k, v in stats.items() if k != "valid_array"}

    if arr is not None and len(arr) > 0:
        mean_v = float(np.mean(arr))
        std_v = float(np.std(arr))
        out["std"] = std_v
        out["count"] = int(len(arr))

        c20, e20 = np.histogram(arr, bins=20)
        out["hist"] = (c20.tolist(), e20.tolist())

        c8, e8 = np.histogram(arr, bins=8)
        out["spark"] = c8.tolist()
        out["spark_edges"] = e8.tolist()

        if kind == "lst":
            out["hi_pct"] = float(np.mean(arr > mean_v + 2 * std_v) * 100)
        else:
            out["hi_pct"] = float(np.mean(arr > NDVI_DENSE_THRESHOLD) * 100)
    else:
        out["std"] = 0.0
        out["count"] = 0
        out["hist"] = None
        out["spark"] = None
        out["spark_edges"] = None
        out["hi_pct"] = None

    return out


def _spark_index(stats: dict, at: str = "mean"):
    """Indeks batang mini-bar yang disorot (bin tempat nilai KPI berada)."""
    counts, edges = stats.get("spark"), stats.get("spark_edges")
    if not counts or not edges:
        return None
    if at == "max":
        return len(counts) - 1
    idx = int(np.digitize(stats["mean"], edges)) - 1
    return int(np.clip(idx, 0, len(counts) - 1))


def _legend_html(layer_key: str, s: dict) -> str:
    """Legenda gradien warna di dasar kartu peta (satu baris HTML)."""
    if layer_key == "lst":
        title, tail, tail_color = "Gradien Termal LST (°C)", "Hotspot anomali →", "#DC2626"
        grad = ("linear-gradient(90deg,#0369A1 0%,#0284C7 20%,#38BDF8 40%,"
                "#FEF08A 55%,#F59E0B 70%,#DC2626 85%,#7F1D1D 100%)")
        left = f"Min {s['min']:.1f} °C"
        mid = f"Rata-rata {s['mean']:.1f} °C"
        right = f"Maks {s['max']:.1f} °C"
        right_color = "#DC2626"
    else:
        title, tail, tail_color = "Skala Kerapatan NDVI", "Kanopi rapat →", "#047857"
        grad = ("linear-gradient(90deg,#92400E 0%,#D97706 20%,#FACC15 40%,"
                "#4ADE80 60%,#16A34A 80%,#064E3B 100%)")
        left = f"{s['min']:.2f} (tanah terbuka)"
        mid = f"Rata-rata {s['mean']:.2f}"
        right = f"{s['max']:.2f} (kanopi lebat)"
        right_color = "#047857"

    return (
        '<div style="padding:0.6rem 0.85rem;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;">'
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.35rem;">'
        f'<span style="font-size:0.75rem;font-weight:700;color:#0F172A;">{title}</span>'
        f'<span style="font-size:0.68rem;font-weight:700;color:{tail_color};">{tail}</span>'
        '</div>'
        f'<div style="height:10px;border-radius:5px;background:{grad};"></div>'
        '<div style="display:flex;justify-content:space-between;font-size:0.7rem;color:#475569;'
        'font-weight:600;margin-top:0.3rem;">'
        f'<span>{left}</span><span>{mid}</span>'
        f'<span style="color:{right_color};font-weight:700;">{right}</span>'
        '</div></div>'
    )


def _histogram_fig(stats: dict, layer_key: str):
    """Histogram frekuensi piksel NYATA (np.histogram dari raster, bukan data acak)."""
    hist = stats.get("hist")
    if not hist:
        return None
    counts, edges = hist
    edges = np.asarray(edges)
    centers = ((edges[:-1] + edges[1:]) / 2).tolist()

    if layer_key == "lst":
        colorscale = [[0, "#38BDF8"], [0.55, "#FEF08A"], [1, "#DC2626"]]
        unit = " °C"
    else:
        colorscale = [[0, "#FEF08A"], [0.5, "#4ADE80"], [1, "#065F46"]]
        unit = ""

    fig = go.Figure(
        go.Bar(
            x=centers,
            y=counts,
            marker=dict(color=centers, colorscale=colorscale, line=dict(width=0)),
            hovertemplate="Nilai ≈ %{x:.2f}" + unit + "<br>Piksel: %{y:,}<extra></extra>",
        )
    )
    fig.update_layout(
        height=170,
        showlegend=False,
        bargap=0.08,
        margin=dict(l=0, r=0, t=4, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, Inter, sans-serif", size=10, color="#64748B"),
        xaxis=dict(showgrid=False, zeroline=False, title=""),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False, title="", showticklabels=False),
    )
    return fig


# ── Halaman ──────────────────────────────────────────────────────────────────
def render_remote_sensing():
    page_header(
        title="Penginderaan Jauh",
        subtitle="Citra satelit LST dan NDVI untuk deteksi anomali geotermal.",
        badge_text="● Data Satelit Nyata",
        badge_tooltip=(
            "Landsat 8/9 TIRS (Band 10, 30 m) + Sentinel-2 MSI (10 m). "
            "Statistik dihitung dari dataset GeoTIFF aktual."
        ),
    )

    lst = _load_layer("lst")
    ndvi = _load_layer("ndvi")

    # ── Baris KPI (4 kartu, mini bar = sebaran piksel nyata) ─────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("LST Rata-Rata", f"{lst['mean']:.2f} °C",
                 subtext="Suhu permukaan dasar",
                 spark=lst["spark"], spark_hi=_spark_index(lst, "mean"))
    with k2:
        kpi_card("LST Maksimum", f"{lst['max']:.2f} °C",
                 trend="Anomali termal", trend_type="warning",
                 spark=lst["spark"], spark_hi=_spark_index(lst, "max"))
    with k3:
        kpi_card("NDVI Rata-Rata", f"{ndvi['mean']:.2f}",
                 subtext="Kerapatan kanopi",
                 spark=ndvi["spark"], spark_hi=_spark_index(ndvi, "mean"))
    with k4:
        kpi_card("Rentang NDVI", f"{ndvi['max'] - ndvi['min']:.2f}",
                 subtext="Variabilitas vegetasi")

    st.write("")

    # ── Baris utama: kartu peta (kiri) + kartu statistik (kanan) ─────────────
    col_map, col_stats = st.columns([7, 5], gap="medium")

    # Kartu peta: judul + kontrol + peta + legenda, semuanya DI DALAM kartu
    with col_map:
        with st.container(key="card_map"):
            card_header(
                "Distribusi Spasial",
                "Overlay raster pada peta dasar Sulawesi Utara",
            )

            c_layer, c_opacity = st.columns([3, 2], gap="medium")
            with c_layer:
                selected = st.radio(
                    "Lapisan citra",
                    list(LAYER_OPTIONS.keys()),
                    horizontal=True,
                    label_visibility="collapsed",
                )
            with c_opacity:
                opacity = st.slider("Opasitas", 0.2, 1.0, 0.65, 0.05)

            layer_key = LAYER_OPTIONS[selected]
            current = lst if layer_key == "lst" else ndvi

            m = create_base_map(center=[1.35, 124.85], zoom=8)
            if current.get("png_path") and current.get("bounds"):
                folium.raster_layers.ImageOverlay(
                    image=current["png_path"],
                    bounds=current["bounds"],
                    opacity=opacity,
                    name=LAYER_TITLE[layer_key],
                ).add_to(m)
            folium.LayerControl().add_to(m)

            st_folium(
                m,
                width="100%",
                height=420,
                key=f"rs_map_{layer_key}_{opacity}",
                returned_objects=[],  # jangan rerun halaman saat peta digeser/zoom
            )

            st.markdown(_legend_html(layer_key, current), unsafe_allow_html=True)

    # Kartu statistik: ringkasan + histogram nyata, lalu kartu sorotan gelap
    with col_stats:
        with st.container(key="card_stats"):
            card_header(
                "Ringkasan Statistik",
                f"Piksel valid · {LAYER_TITLE[layer_key]}",
            )
            stat_rows([
                ("Minimum", f"{current['min']:.2f}"),
                ("Maksimum", f"{current['max']:.2f}"),
                ("Rata-rata", f"{current['mean']:.2f}"),
                ("Simpangan baku", f"{current['std']:.2f}"),
            ])

            st.markdown(
                '<div style="font-size:0.78rem;font-weight:700;color:#334155;margin-top:0.25rem;">'
                'Sebaran nilai piksel</div>',
                unsafe_allow_html=True,
            )
            fig = _histogram_fig(current, layer_key)
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True,
                                config={"displayModeBar": False})
            else:
                st.caption("Data piksel valid tidak tersedia.")

        if current.get("hi_pct") is not None:
            if layer_key == "lst":
                dark_highlight_card(
                    title="Area anomali termal",
                    main_stat=f"{current['hi_pct']:.1f}%",
                    sub_stat="piksel di atas rata-rata + 2σ",
                    tag="ANOMALI TERMAL",
                )
            else:
                dark_highlight_card(
                    title="Kanopi lebat",
                    main_stat=f"{current['hi_pct']:.1f}%",
                    sub_stat=f"piksel dengan NDVI > {NDVI_DENSE_THRESHOLD}",
                    tag="VEGETASI",
                )

    # ── Detail teknis disembunyikan (tidak memenuhi permukaan halaman) ───────
    with st.expander("Detail data & pemrosesan", expanded=False):
        st.markdown(
            f"""
- **Sumber:** Landsat 8/9 TIRS Band 10 (30 m) dan Sentinel-2 MSI (10 m), proyeksi WGS84 (EPSG:4326).
- **Masking NoData:** piksel awan dan laut difilter otomatis.
- **Downsampling:** raster dioptimasi agar peta tampil cepat; statistik dihitung dari piksel valid.
- **File aktif:** `{current.get('filename', 'N/A')}` ({current.get('count', 0):,} piksel valid).
- **Cakupan koordinat:** `{current.get('bounds', 'N/A')}`.
            """
        )