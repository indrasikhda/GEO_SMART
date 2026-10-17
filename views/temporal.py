import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np

from core.io import GMN_NODES
from ui.components import page_header, kpi_card, card_header
from views.monitoring import PARAMS

# ════════════════════════════════════════════════════════════════════════════
# Halaman: Monitoring Temporal
# Grafik beranimasi: garis tergambar bertahap + titik penuntun di ujungnya,
# otomatis berputar saat grafik tampil, dengan tombol "Putar ulang".
# Seluruh deret waktu adalah DATA SIMULASI (bukan hasil pengukuran).
# ════════════════════════════════════════════════════════════════════════════

LABEL = {f: (f"{l} ({u})" if u else l) for f, l, u in PARAMS}

GRANULARITY = {
    "Harian": "D",
    "Mingguan (rata-rata)": "W",
    "Bulanan (rata-rata)": "ME",
}
CATEGORIES = ["Termal", "Lingkungan", "Fluida & Gas", "Ternormalisasi"]

SEED_MAP = {"GMN-01": 42, "GMN-02": 101, "GMN-03": 202}
FRAME_MS = 28          # durasi tiap frame animasi (ms)
MAX_FRAMES = 40
CHART_H = 310
FONT = "Inter, Helvetica, Arial, sans-serif"


# ── Data simulasi ────────────────────────────────────────────────────────────
def _simulate(node: dict) -> pd.DataFrame:
    """Deret waktu harian 2025 (nilai dasar node + pola musiman + derau acak)."""
    dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    n = len(dates)
    t = np.linspace(0, 2 * np.pi, n)

    np.random.seed(SEED_MAP.get(node["id"], 42))

    b = lambda key, default: float(node.get(key, default))

    shallow = b("shallow_soil_temp", 68.4) + 4.0 * np.sin(t) + np.random.normal(0, 1.0, n)
    deep = b("deep_soil_temp", 74.2) + 2.5 * np.sin(t) + np.random.normal(0, 0.6, n)
    air_t = b("air_temp", 28.5) + 2.5 * np.sin(t + np.pi / 4) + np.random.normal(0, 0.7, n)
    air_h = b("air_humidity", 78.0) + 8.0 * np.sin(t + np.pi / 2) + np.random.normal(0, 1.8, n)
    soil_m = b("soil_moisture", 42.0) + 7.0 * np.sin(t + np.pi / 3) + np.random.normal(0, 2.0, n)
    ph = b("ph_level", 2.8) + 0.2 * np.cos(t) + np.random.normal(0, 0.04, n)
    ec = b("ec_meter", 3800) + 250 * np.sin(t) + np.random.normal(0, 40, n)
    h2s = b("h2s_gas", 14.2) + 2.0 * np.sin(np.linspace(0, 4 * np.pi, n)) + np.random.normal(0, 0.5, n)
    co2 = b("co2_gas", 850) + 100 * np.cos(np.linspace(0, 3 * np.pi, n)) + np.random.normal(0, 20, n)

    return pd.DataFrame({
        "Date": dates,
        "shallow_soil_temp": shallow,
        "deep_soil_temp": deep,
        "air_temp": air_t,
        "air_humidity": air_h,
        "soil_moisture": soil_m,
        "ph_level": ph,
        "ec_meter": ec,
        "h2s_gas": h2s,
        "co2_gas": co2,
    })


# ── Pembuat grafik beranimasi ────────────────────────────────────────────────
def _rng(vals):
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.1 or 1.0
    return [lo - pad, hi + pad]


def _spec(col, color, axis="y"):
    return {"col": col, "name": LABEL[col], "color": color, "axis": axis}


def _build_fig(df, specs, animate, y_title=""):
    x = df["Date"].dt.strftime("%Y-%m-%d").tolist()
    n = len(x)
    ys = [np.round(df[s["col"]].to_numpy(dtype=float), 3).tolist() for s in specs]

    ks = sorted({int(v) for v in np.linspace(2, n, min(MAX_FRAMES, n))}) if n > 2 else [n]
    k0 = ks[0] if animate else n

    fig = go.Figure()
    for s, y in zip(specs, ys):
        fig.add_trace(go.Scatter(
            x=x[:k0], y=y[:k0], mode="lines", name=s["name"], yaxis=s["axis"],
            line=dict(color=s["color"], width=2.2),
            hovertemplate="%{y:.2f}<extra>" + s["name"] + "</extra>",
        ))
        if animate:  # titik penuntun di ujung garis
            fig.add_trace(go.Scatter(
                x=[x[k0 - 1]], y=[y[k0 - 1]], mode="markers", yaxis=s["axis"],
                marker=dict(color=s["color"], size=8, line=dict(color="#FFFFFF", width=2)),
                showlegend=False, hoverinfo="skip",
            ))

    if animate:
        trace_ids = list(range(len(fig.data)))
        frames = []
        for k in ks:
            data = []
            for y in ys:
                data.append(go.Scatter(x=x[:k], y=y[:k]))
                data.append(go.Scatter(x=[x[k - 1]], y=[y[k - 1]]))
            frames.append(go.Frame(name=str(k), data=data, traces=trace_ids))
        fig.frames = frames

    y1 = [v for s, y in zip(specs, ys) if s["axis"] == "y" for v in y]
    y2 = [v for s, y in zip(specs, ys) if s["axis"] == "y2" for v in y]
    first, second = specs[0], next((s for s in specs if s["axis"] == "y2"), None)

    def _axis(title, color=None, **extra):
        font = dict(color=color) if color else {}
        return dict(title=dict(text=title, font=dict(size=11, **font)),
                    tickfont=dict(size=10, **font), zeroline=False, **extra)

    layout = dict(
        height=CHART_H,
        margin=dict(l=8, r=8, t=46, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, size=11, color="#64748B"),
        hovermode="x unified",
        legend=dict(orientation="h", x=1, xanchor="right", y=1.14, yanchor="top", title=""),
        xaxis=dict(type="date", range=[x[0], x[-1]], showgrid=False, title=""),
        yaxis=_axis(
            first["name"] if second else y_title,
            color=first["color"] if second else None,
            range=_rng(y1), showgrid=True, gridcolor="#F1F5F9",
        ),
    )
    if second:
        layout["yaxis2"] = _axis(
            second["name"], color=second["color"],
            range=_rng(y2), overlaying="y", side="right", showgrid=False,
        )
    if animate:
        layout["updatemenus"] = [dict(
            type="buttons", direction="left", showactive=False,
            x=0, y=1.14, xanchor="left", yanchor="top",
            bgcolor="#F1F7F4", bordercolor="#E2E8F0",
            font=dict(size=11, color="#334155"),
            buttons=[dict(
                label="▶ Putar ulang", method="animate",
                args=[None, dict(frame=dict(duration=FRAME_MS, redraw=True),
                                 transition=dict(duration=0),
                                 fromcurrent=False, mode="immediate")],
            )],
        )]
    fig.update_layout(**layout)
    return fig


def _render(fig, animate):
    if not animate:
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        return
    html = pio.to_html(
        fig,
        include_plotlyjs="cdn",
        full_html=False,
        auto_play=True,
        config={"displayModeBar": False, "responsive": True},
        animation_opts=dict(frame=dict(duration=FRAME_MS, redraw=True),
                            transition=dict(duration=0)),
        default_width="100%",
        default_height=f"{CHART_H}px",
    )
    components.html(
        '<style>html,body{margin:0;background:transparent;}</style>' + html,
        height=CHART_H + 6,
        scrolling=False,
    )


def _chart(df, specs, animate, y_title=""):
    _render(_build_fig(df, specs, animate, y_title), animate)


# ── Halaman ──────────────────────────────────────────────────────────────────
def render_temporal():
    if not GMN_NODES:
        st.info("Belum ada node GMN yang terdaftar.")
        return

    page_header(
        title="Monitoring Temporal",
        subtitle="Tren time-series multi-parameter untuk dinamika hidrotermal musiman.",
        badge_text="● Data Simulasi",
        badge_tooltip=(
            "Deret waktu 365 hari dibangkitkan dari nilai dasar node, pola musiman, dan derau acak "
            "untuk validasi prototipe; bukan hasil pengukuran lapangan."
        ),
    )

    # ── Kontrol ──────────────────────────────────────────────────────────────
    with st.container(key="card_ctrl"):
        c1, c2, c3 = st.columns([5, 5, 2], gap="medium", vertical_alignment="bottom")
        with c1:
            node_ids = [n["id"] for n in GMN_NODES]
            names = {n["id"]: n["name"] for n in GMN_NODES}
            node_id = st.selectbox(
                "Stasiun / node GMN", node_ids,
                format_func=lambda i: f"{i} — {names[i]}", key="tmp_node",
            )
        with c2:
            st.caption("Resolusi waktu")
            gran = st.radio("Resolusi waktu", list(GRANULARITY.keys()), horizontal=True,
                            label_visibility="collapsed", key="tmp_gran")
        with c3:
            animate = st.toggle("Animasi", value=True, key="tmp_anim")

    node = next(n for n in GMN_NODES if n["id"] == node_id)

    df_raw = _simulate(node)
    freq = GRANULARITY[gran]
    df = df_raw if freq == "D" else df_raw.resample(freq, on="Date").mean().reset_index()

    # Mini bar KPI = rata-rata bulanan
    monthly = df_raw.resample("ME", on="Date").mean()

    # ── KPI ──────────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Node Terpilih", node_id, subtext=node["name"])
    with k2:
        kpi_card("Suhu Tanah 1.0 m", f"{df_raw['deep_soil_temp'].mean():.1f} °C",
                 subtext="Rata-rata periode", spark=monthly["deep_soil_temp"].round(3).tolist())
    with k3:
        kpi_card("Gas H₂S", f"{df_raw['h2s_gas'].mean():.1f} ppm",
                 subtext="Rata-rata periode", spark=monthly["h2s_gas"].round(3).tolist())
    with k4:
        kpi_card("Periode", f"{len(df_raw)} Hari",
                 subtext=f"Simulasi {df_raw['Date'].dt.year.iloc[0]}")

    st.write("")

    # ── Kartu grafik ─────────────────────────────────────────────────────────
    with st.container(key="card_series"):
        card_header(f"Dinamika Parameter · {node_id}", node["name"])

        # Pilihan kategori memakai radio (bukan st.tabs) agar hanya satu kategori
        # yang dirender dan animasinya terlihat saat kategori dibuka.
        cat = st.radio("Kategori", CATEGORIES, horizontal=True,
                       label_visibility="collapsed", key="tmp_cat")

        if cat == "Termal":
            _chart(df, [
                _spec("shallow_soil_temp", "#F97316"),
                _spec("deep_soil_temp", "#9A3412"),
            ], animate, y_title="Suhu (°C)")

        elif cat == "Lingkungan":
            a, b = st.columns(2, gap="medium")
            with a:
                _chart(df, [
                    _spec("air_temp", "#F59E0B"),
                    _spec("air_humidity", "#0EA5E9", axis="y2"),
                ], animate)
            with b:
                _chart(df, [_spec("soil_moisture", "#22C55E")], animate, y_title="Kelembapan (%)")

        elif cat == "Fluida & Gas":
            a, b = st.columns(2, gap="medium")
            with a:
                _chart(df, [
                    _spec("ph_level", "#8B5CF6"),
                    _spec("ec_meter", "#3B82F6", axis="y2"),
                ], animate)
            with b:
                _chart(df, [
                    _spec("h2s_gas", "#EC4899"),
                    _spec("co2_gas", "#64748B", axis="y2"),
                ], animate)

        else:  # Ternormalisasi
            cols = ["shallow_soil_temp", "deep_soil_temp", "soil_moisture", "ph_level", "h2s_gas"]
            colors = ["#F97316", "#9A3412", "#22C55E", "#8B5CF6", "#EC4899"]
            df_norm = df.copy()
            for c in cols:
                lo, hi = df_norm[c].min(), df_norm[c].max()
                df_norm[c] = (df_norm[c] - lo) / (hi - lo) if hi > lo else 0.0
            _chart(df_norm, [_spec(c, col) for c, col in zip(cols, colors)],
                   animate, y_title="Skala 0–1")

    # ── Catatan ──────────────────────────────────────────────────────────────
    with st.expander("Catatan data dan pengukuran", expanded=False):
        st.markdown(
            """
- **Data simulasi:** nilai dasar tiap parameter diambil dari node, lalu ditambah pola musiman dan derau acak. Animasi hanya efek tampilan, bukan aliran data langsung.
- **Suhu tanah 1.0 m:** baseline lebih stabil dan minim terpengaruh fluktuasi cuaca harian, sehingga cocok sebagai indikator transfer panas hidrotermal konduktif dari reservoir.
- **Dua sumbu:** parameter berbeda satuan (mis. pH dan EC) ditampilkan dengan sumbu kiri dan kanan agar bentuk kurvanya terbaca.
            """
        )