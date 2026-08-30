import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

from core.io import GMN_NODES


def render_temporal():
    # ── PAGE HEADER BANNER ──────────────────────────────────────────────────
    st.title("Temporal Monitoring")
    st.caption("Multi-temporal analysis of satellite-derived indices and dynamic ground telemetry streams.")

    st.warning(
        "**SIMULATED TIME-SERIES** — Multi-temporal telemetry curves shown below represent simulated "
        "daily observation data for prototype demonstration. Physical deployment and continuous MQTT data "
        "streams are scheduled for future field validation."
    )

    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

    # ── DYNAMIC CONTROLS (NODE SELECTOR & GRANULARITY) ───────────────────────
    ctrl_c1, ctrl_c2 = st.columns([2, 2])

    with ctrl_c1:
        node_options = [f"{n['id']} — {n['name']}" for n in GMN_NODES]
        selected_node_str = st.selectbox(
            "Select Monitoring Node",
            options=node_options,
            index=0
        )
        selected_node_id = selected_node_str.split(" — ")[0]
        selected_node_data = next((n for n in GMN_NODES if n["id"] == selected_node_id), GMN_NODES[0])

    with ctrl_c2:
        granularity = st.radio(
            "Time Granularity / Resampling",
            options=["Daily", "Weekly Mean", "Monthly Mean"],
            horizontal=True,
            index=0
        )

    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

    # ── TOP MONITORING SUMMARY KPI CARDS ─────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(label="Selected Node", value=selected_node_id, delta=selected_node_data["name"])

    with k2:
        st.metric(label="Observation Period", value="365 Days", delta="2025 Full Cycle")

    with k3:
        st.metric(label="Active Parameters", value="11 Probes", delta="Subsurface & Gas")

    with k4:
        st.metric(label="Display Resolution", value=granularity, delta="Dynamic Resampling")

    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

    # ── DATASET GENERATION WITH NODE-SPECIFIC BASELINES ──────────────────────
    dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    
    # Adjust baseline values dynamically depending on selected node
    seed_map = {"GMN-01": 42, "GMN-02": 101, "GMN-03": 202}
    np.random.seed(seed_map.get(selected_node_id, 42))
    n = len(dates)

    base_shallow = selected_node_data.get("shallow_soil_temp", 68.4)
    base_deep = selected_node_data.get("deep_soil_temp", 74.2)
    base_ph = selected_node_data.get("ph_level", 2.8)
    base_ec = selected_node_data.get("ec_meter", 3800)
    base_h2s = selected_node_data.get("h2s_gas", 14.2)
    base_co2 = selected_node_data.get("co2_gas", 850)

    # Generate synthetic telemetry curves
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

    # Apply granularity resampling
    if granularity == "Weekly Mean":
        df = df_raw.resample("W", on="Date").mean().reset_index()
    elif granularity == "Monthly Mean":
        df = df_raw.resample("M", on="Date").mean().reset_index()
    else:
        df = df_raw.copy()

    # ── CATEGORIZED TABS LAYOUT ─────────────────────────────────────────────
    tab_thermal, tab_atmosphere, tab_geochem, tab_normalized = st.tabs([
        "Subsurface Thermal",
        "Environmental & Atmosphere",
        "Hydrothermal Fluid & Gas",
        "Normalized Comparison"
    ])

    plotly_layout_defaults = dict(
        height=320,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=11, color="#64748B"),
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", title=""),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        hovermode="x unified"
    )

    # ------------------------------------------------------------------------
    # TAB 1: SUBSURFACE THERMAL TRENDS
    # ------------------------------------------------------------------------
    with tab_thermal:
        st.markdown(f"### Subsurface Ground Temperature Dynamics ({selected_node_id})")
        st.caption("Comparison between Shallow (0.5m) PT100 probe and Deep (1.0m) PT100 probe measurements.")

        fig_thermal = px.line(
            df,
            x="Date",
            y=["Shallow Soil Temp (°C)", "Deep Soil Temp (°C)"],
            color_discrete_sequence=["#EF4444", "#991B1B"]
        )
        fig_thermal.update_layout(**plotly_layout_defaults)
        fig_thermal.update_layout(yaxis_title="Temperature (°C)")
        st.plotly_chart(fig_thermal, use_container_width=True)

        st.info(
            "**Geothermal Thermal Insight:** Deep soil temperatures (1.0m) exhibit higher baseline heat levels "
            "and are significantly less affected by diurnal air temperature fluctuations, making them ideal for "
            "identifying true hydrothermal upflow anomalies."
        )

    # ------------------------------------------------------------------------
    # TAB 2: ATMOSPHERIC & HYDROLOGIC TRENDS
    # ------------------------------------------------------------------------
    with tab_atmosphere:
        st.markdown("### Atmospheric Baseline & Soil Hydrology")

        col_a1, col_a2 = st.columns(2)

        with col_a1:
            st.markdown("##### Air Temperature & Humidity (Sensirion SHT31)")
            fig_air = px.line(
                df,
                x="Date",
                y=["Air Temp (°C)", "Air Humidity (%)"],
                color_discrete_sequence=["#F59E0B", "#06B6D4"]
            )
            fig_air.update_layout(**plotly_layout_defaults)
            st.plotly_chart(fig_air, use_container_width=True)

        with col_a2:
            st.markdown("##### Soil Moisture Content (DFRobot SEN0193)")
            fig_moisture = px.line(
                df,
                x="Date",
                y="Soil Moisture (%)",
                color_discrete_sequence=["#10B981"]
            )
            fig_moisture.update_layout(**plotly_layout_defaults)
            fig_moisture.update_layout(yaxis_title="Moisture (%)")
            st.plotly_chart(fig_moisture, use_container_width=True)

    # ------------------------------------------------------------------------
    # TAB 3: HYDROTHERMAL FLUID & GAS VOLATILES
    # ------------------------------------------------------------------------
    with tab_geochem:
        st.markdown(f"### Hydrothermal Fluid Properties & Degassing Stream ({selected_node_id})")

        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown("##### Fluid pH & Electrical Conductivity (EC)")
            fig_fluid = px.line(
                df,
                x="Date",
                y=["Fluid pH", "EC (µS/cm)"],
                color_discrete_sequence=["#8B5CF6", "#3B82F6"]
            )
            fig_fluid.update_layout(**plotly_layout_defaults)
            st.plotly_chart(fig_fluid, use_container_width=True)

        with col_g2:
            st.markdown("##### Volatiles Degassing (Winsen MQ-136 H₂S & MH-Z19B CO₂)")
            fig_gas = px.line(
                df,
                x="Date",
                y=["H₂S Gas (ppm)", "CO₂ Gas (ppm)"],
                color_discrete_sequence=["#EC4899", "#64748B"]
            )
            fig_gas.update_layout(**plotly_layout_defaults)
            st.plotly_chart(fig_gas, use_container_width=True)

    # ------------------------------------------------------------------------
    # TAB 4: NORMALIZED COMPARATIVE ANALYSIS
    # ------------------------------------------------------------------------
    with tab_normalized:
        st.markdown("### Multi-Parameter Normalized Cross-Correlation (0.0 to 1.0)")
        st.caption("Min-Max normalization allowing direct temporal correlation across different physical units.")

        param_cols = [
            "Shallow Soil Temp (°C)",
            "Deep Soil Temp (°C)",
            "Soil Moisture (%)",
            "Fluid pH",
            "H₂S Gas (ppm)"
        ]

        df_norm = df.copy()
        for col in param_cols:
            min_val = df_norm[col].min()
            max_val = df_norm[col].max()
            if max_val > min_val:
                df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)
            else:
                df_norm[col] = 0.0

        fig_norm = px.line(
            df_norm,
            x="Date",
            y=param_cols,
            height=380
        )
        fig_norm.update_layout(**plotly_layout_defaults)
        fig_norm.update_layout(
            height=380,
            yaxis_title="Normalized Scale (0–1)",
            legend=dict(orientation="h", y=1.15, title="")
        )
        st.plotly_chart(fig_norm, use_container_width=True)


if __name__ == "__main__":
    render_temporal()