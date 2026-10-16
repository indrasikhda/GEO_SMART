import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import textwrap
from core.io import GMN_NODES
from ui.components import page_header, kpi_card

def render_temporal():
    # ── Header Halaman Ringkas (Anggaran Teks) ──────────────────────────────
    page_header(
        title="Monitoring Temporal",
        subtitle="Analisis tren time-series multi-parameter untuk deteksi dinamika hidrotermal musiman.",
        badge_text="● Data Simulasi",
        badge_tooltip="Simulasi time-series 365 hari untuk validasi prototipe sebelum penyebaran stasiun fisik"
    )

    # ── Kontrol Pilihan Node & Granularitas Waktu (Bento Control Card) ──────
    with st.container(border=True):
        ctrl_c1, ctrl_c2 = st.columns([1, 1])
        with ctrl_c1:
            node_options = [f"{n['id']} — {n['name']}" for n in GMN_NODES]
            selected_node_str = st.selectbox(
                "Pilih Stasiun / Node GMN",
                options=node_options,
                index=0
            )
            selected_node_id = selected_node_str.split(" — ")[0]
            selected_node_data = next((n for n in GMN_NODES if n["id"] == selected_node_id), GMN_NODES[0])

        with ctrl_c2:
            granularity = st.radio(
                "Granularitas Waktu / Resampling",
                options=["Daily", "Weekly Mean", "Monthly Mean"],
                horizontal=True,
                index=0
            )

    # ── Baris KPI Bento (Maksimal 4 kartu) ──────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Node Terpilih", selected_node_id, subtext=selected_node_data["name"])
    with k2:
        kpi_card("Periode Observasi", "365 Hari", subtext="Siklus 2025")
    with k3:
        kpi_card("Parameter Aktif", "11 Kanal", subtext="Subsurface & Gas")
    with k4:
        kpi_card("Resolusi Waktu", granularity, trend="Dinamis", trend_type="neutral")

    st.write("")

    # ── Pembuatan Dataset Time-Series Berdasarkan Baseline Node ──────────────
    dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    seed_map = {"GMN-01": 42, "GMN-02": 101, "GMN-03": 202}
    np.random.seed(seed_map.get(selected_node_id, 42))
    n = len(dates)

    base_shallow = selected_node_data.get("shallow_soil_temp", 68.4)
    base_deep = selected_node_data.get("deep_soil_temp", 74.2)
    base_ph = selected_node_data.get("ph_level", 2.8)
    base_ec = selected_node_data.get("ec_meter", 3800)
    base_h2s = selected_node_data.get("h2s_gas", 14.2)
    base_co2 = selected_node_data.get("co2_gas", 850)

    shallow_soil_temp = base_shallow + 4.0 * np.sin(np.linspace(0, 2 * np.pi, n)) + np.random.normal(0, 1.0, n)
    deep_soil_temp = base_deep + 2.5 * np.sin(np.linspace(0, 2 * np.pi, n)) + np.random.normal(0, 0.6, n)
    air_temp = 28.5 + 2.5 * np.sin(np.linspace(0, 2 * np.pi, n) + np.pi / 4) + np.random.normal(0, 0.7, n)
    air_humidity = 78.0 + 8.0 * np.sin(np.linspace(0, 2 * np.pi, n) + np.pi / 2) + np.random.normal(0, 1.8, n)
    soil_moisture = 42.0 + 7.0 * np.sin(np.linspace(0, 2 * np.pi, n) + np.pi / 3) + np.random.normal(0, 2.0, n)
    ph_level = base_ph + 0.2 * np.cos(np.linspace(0, 2 * np.pi, n)) + np.random.normal(0, 0.04, n)
    ec_meter = base_ec + 250 * np.sin(np.linspace(0, 2 * np.pi, n)) + np.random.normal(0, 40, n)
    h2s_gas = base_h2s + 2.0 * np.sin(np.linspace(0, 4 * np.pi, n)) + np.random.normal(0, 0.5, n)
    co2_gas = base_co2 + 100 * np.cos(np.linspace(0, 3 * np.pi, n)) + np.random.normal(0, 20, n)

    df_raw = pd.DataFrame({
        "Date": dates,
        "Shallow Soil Temp (°C)": shallow_soil_temp,
        "Deep Soil Temp (°C)": deep_soil_temp,
        "Air Temp (°C)": air_temp,
        "Air Humidity (%)": air_humidity,
        "Soil Moisture (%)": soil_moisture,
        "Fluid pH": ph_level,
        "EC (µS/cm)": ec_meter,
        "H₂S Gas (ppm)": h2s_gas,
        "CO₂ Gas (ppm)": co2_gas
    })

    if granularity == "Weekly Mean":
        df = df_raw.resample("W", on="Date").mean().reset_index()
    elif granularity == "Monthly Mean":
        df = df_raw.resample("ME", on="Date").mean().reset_index()
    else:
        df = df_raw.copy()

    # ── Tabs Kategori Tren Sensor di dalam Bento Card ────────────────────────
    st.markdown(textwrap.dedent(f"""
<div class="bento-card">
<div class="bento-card-header">
<div>
<div class="bento-card-title">Kurva Dinamika Parameter &bull; {selected_node_id} ({selected_node_data['name']})</div>
<div class="bento-card-sub">Visualisasi time-series parameter termal, lingkungan, dan geokimia</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

    tab_thermal, tab_atmosphere, tab_geochem, tab_normalized = st.tabs([
        "Termal Subsurface",
        "Lingkungan & Udara",
        "Fluida Geotermal & Gas",
        "Perbandingan Ternormalisasi"
    ])

    plotly_layout = dict(
        height=300,
        margin=dict(l=10, r=10, t=25, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=10, color="#64748B"),
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", title=""),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        hovermode="x unified"
    )

    with tab_thermal:
        fig_thermal = px.line(
            df,
            x="Date",
            y=["Shallow Soil Temp (°C)", "Deep Soil Temp (°C)"],
            color_discrete_sequence=["#EF4444", "#991B1B"]
        )
        fig_thermal.update_layout(**plotly_layout)
        fig_thermal.update_layout(yaxis_title="Suhu (°C)")
        st.plotly_chart(fig_thermal, use_container_width=True)

    with tab_atmosphere:
        c1, c2 = st.columns(2)
        with c1:
            fig_air = px.line(df, x="Date", y=["Air Temp (°C)", "Air Humidity (%)"], color_discrete_sequence=["#F59E0B", "#06B6D4"])
            fig_air.update_layout(**plotly_layout)
            st.plotly_chart(fig_air, use_container_width=True)
        with c2:
            fig_moist = px.line(df, x="Date", y="Soil Moisture (%)", color_discrete_sequence=["#10B981"])
            fig_moist.update_layout(**plotly_layout)
            fig_moist.update_layout(yaxis_title="Kelembapan (%)")
            st.plotly_chart(fig_moist, use_container_width=True)

    with tab_geochem:
        cg1, cg2 = st.columns(2)
        with cg1:
            fig_fluid = px.line(df, x="Date", y=["Fluid pH", "EC (µS/cm)"], color_discrete_sequence=["#8B5CF6", "#3B82F6"])
            fig_fluid.update_layout(**plotly_layout)
            st.plotly_chart(fig_fluid, use_container_width=True)
        with cg2:
            fig_gas = px.line(df, x="Date", y=["H₂S Gas (ppm)", "CO₂ Gas (ppm)"], color_discrete_sequence=["#EC4899", "#64748B"])
            fig_gas.update_layout(**plotly_layout)
            st.plotly_chart(fig_gas, use_container_width=True)

    with tab_normalized:
        param_cols = ["Shallow Soil Temp (°C)", "Deep Soil Temp (°C)", "Soil Moisture (%)", "Fluid pH", "H₂S Gas (ppm)"]
        df_norm = df.copy()
        for col in param_cols:
            min_v = df_norm[col].min()
            max_v = df_norm[col].max()
            df_norm[col] = (df_norm[col] - min_v) / (max_v - min_v) if max_v > min_v else 0.0

        fig_norm = px.line(df_norm, x="Date", y=param_cols, height=320)
        fig_norm.update_layout(**plotly_layout)
        fig_norm.update_layout(height=320, yaxis_title="Skala Ternormalisasi (0–1)", legend=dict(orientation="h", y=1.12, title=""))
        st.plotly_chart(fig_norm, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Expander Catatan Metodologi Sensor ───────────────────────────────────
    with st.expander("ℹ️ Karakteristik Pengukuran Subsurface Tanah", expanded=False):
        st.markdown("""
            **Wawasan Termal:** Suhu tanah pada kedalaman 1.0m memiliki baseline yang lebih stabil dan sangat minim terpengaruh oleh fluktuasi cuaca harian permukaan. Karakteristik ini menjadikannya indikator andal dalam mendeteksi transfer panas hidrotermal konduktif dari reservoir bawah permukaan.
        """)