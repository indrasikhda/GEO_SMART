import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

from core.io import GMN_NODES
from core.maps import create_base_map


def render_monitoring():
    """
    GMN Monitoring View - GEO-SMART (Modern Minimalist Clean Layout)
    """

    # ── Custom CSS for Compact Pill Badges, Minimal Cards & Smaller Metrics ──
    st.markdown("""
        <style>
        /* ── Override khusus untuk mengecilkan ukuran Metric Card di halaman GMN ── */
        [data-testid="stMetricValue"] {
            font-size: 1.35rem !important;  /* Ukuran nilai metric diperkecil */
            font-weight: 800 !important;
            line-height: 1.2 !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.68rem !important;  /* Ukuran judul metric */
            font-weight: 700 !important;
        }
        [data-testid="stMetricDelta"] {
            font-size: 0.70rem !important;  /* Ukuran teks delta (sub-label) diperkecil */
            padding: 0.15rem 0.4rem !important;
            margin-top: 0.3rem !important;
        }

        /* ── CSS Bawaan GMN ── */
        .gmn-pill-proposed {
            background-color: #EFF6FF;
            color: #1D4ED8;
            padding: 3px 10px;
            border-radius: 9999px;
            font-size: 0.72rem;
            font-weight: 700;
            border: 1px solid #BFDBFE;
            display: inline-block;
        }
        .gmn-pill-online {
            background-color: #ECFDF5;
            color: #047857;
            padding: 3px 10px;
            border-radius: 9999px;
            font-size: 0.72rem;
            font-weight: 700;
            border: 1px solid #A7F3D0;
            display: inline-block;
        }
        .gmn-metric-label {
            font-size: 0.70rem !important;
            color: #64748B !important;
            font-weight: 600;
            margin-bottom: 2px;
        }
        .gmn-metric-val {
            font-size: 1.05rem !important;
            color: #0F172A !important;
            font-weight: 800;
        }
        </style>
    """, unsafe_allow_html=True)

    # ── TOP KPI ROW ─────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(label="GMN Nodes", value=len(GMN_NODES), delta="Proposed Network")
    with k2:
        st.metric(label="Node Status", value="Simulated", delta="Pre-deployment")
    with k3:
        st.metric(label="Telemetry Parameters", value="11 Channels", delta="Subsurface & Gas")
    with k4:
        st.metric(label="Data Pipeline", value="LoRa / 4G", delta="IoT Field-to-Cloud")

    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

    # ── MAIN SPLIT LAYOUT: NODE STATUS (LEFT) + MAP (RIGHT) ─────────────────
    col_nodes, col_map = st.columns([5, 7], gap="medium")

    # ------------------------------------------------------------------------
    # LEFT: NODE STATUS CARDS
    # ------------------------------------------------------------------------
    with col_nodes:
        st.markdown("### Node Status & Telemetry")

        for node in GMN_NODES:
            node_id = node.get("id", "GMN")
            node_name = node.get("name", "Monitoring Node")
            node_status = node.get("status", "Proposed Node")

            # Determine Pill Badge
            if "online" in node_status.lower():
                badge_html = '<span class="gmn-pill-online">● Online</span>'
            else:
                badge_html = '<span class="gmn-pill-proposed">● Proposed</span>'

            with st.container(border=True):
                # Node Title & Status Badge
                c_top_l, c_top_r = st.columns([3, 1])
                with c_top_l:
                    st.markdown(f"**{node_id}** · <span style='font-size:0.85rem; color:#475569;'>{node_name}</span>", unsafe_allow_html=True)
                with c_top_r:
                    st.markdown(f"<div style='text-align:right;'>{badge_html}</div>", unsafe_allow_html=True)

                st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

                # 4-Column Sensor Grid (Super Compact Metrics)
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.markdown('<div class="gmn-metric-label">Soil Temp (0.5m)</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="gmn-metric-val">{node.get("shallow_soil_temp", 68.4)} °C</div>', unsafe_allow_html=True)
                    st.markdown('<div class="gmn-metric-label" style="margin-top:6px;">Air Temp</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="gmn-metric-val">{node.get("air_temp", 29.6)} °C</div>', unsafe_allow_html=True)
                    st.markdown('<div class="gmn-metric-label" style="margin-top:6px;">Soil Moisture</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="gmn-metric-val">{node.get("soil_moisture", 42.5)} %</div>', unsafe_allow_html=True)
                
                with m2:
                    st.markdown('<div class="gmn-metric-label">Soil Temp (1.0m)</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="gmn-metric-val">{node.get("deep_soil_temp", 74.2)} °C</div>', unsafe_allow_html=True)
                    st.markdown('<div class="gmn-metric-label" style="margin-top:6px;">Air Humidity</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="gmn-metric-val">{node.get("air_humidity", 78.2)} %</div>', unsafe_allow_html=True)
                    st.markdown('<div class="gmn-metric-label" style="margin-top:6px;">Fluid pH</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="gmn-metric-val">{node.get("ph_level", 2.8)}</div>', unsafe_allow_html=True)

                with m3:
                    st.markdown('<div class="gmn-metric-label">EC Meter</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="gmn-metric-val">{node.get("ec_meter", 3800)} µS</div>', unsafe_allow_html=True)
                    st.markdown('<div class="gmn-metric-label" style="margin-top:6px;">H₂S Gas</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="gmn-metric-val">{node.get("h2s_gas", 14.2)} ppm</div>', unsafe_allow_html=True)
                    st.markdown('<div class="gmn-metric-label" style="margin-top:6px;">CO₂ Gas</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="gmn-metric-val">{node.get("co2_gas", 850)} ppm</div>', unsafe_allow_html=True)

                with m4:
                    st.markdown('<div class="gmn-metric-label">Battery</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="gmn-metric-val">{node.get("battery", 94)} %</div>', unsafe_allow_html=True)
                    st.markdown('<div class="gmn-metric-label" style="margin-top:6px;">Telemetry</div>', unsafe_allow_html=True)
                    st.markdown('<div class="gmn-metric-val" style="font-size:0.9rem !important;">LoRa / 4G</div>', unsafe_allow_html=True)
                    st.markdown('<div class="gmn-metric-label" style="margin-top:6px;">Interval</div>', unsafe_allow_html=True)
                    st.markdown('<div class="gmn-metric-val" style="font-size:0.9rem !important;">15 Min</div>', unsafe_allow_html=True)

                # Bottom Metadata (Coordinates & Timestamp)
                st.markdown("<hr style='margin: 10px 0 6px 0; border: none; border-top: 1px solid #F1F5F9;' />", unsafe_allow_html=True)
                f1, f2 = st.columns(2)
                with f1:
                    st.caption(f"📍 **GNSS:** {node.get('lat', '--')}, {node.get('lng', '--')}")
                with f2:
                    st.caption(f"🕒 **Update:** {node.get('last_update', 'Simulated Stream')}")

    # ------------------------------------------------------------------------
    # RIGHT: CLEAN NETWORK MAP
    # ------------------------------------------------------------------------
    with col_map:
        st.markdown("### Deployment Network Map")

        m = create_base_map(center=[1.30, 124.85], zoom=10)

        # Feature group for clean layer control
        fg_nodes = folium.FeatureGroup(name="Proposed GMN Nodes")

        for node in GMN_NODES:
            node_id = node.get("id", "GMN")
            node_name = node.get("name", "Monitoring Node")
            node_status = node.get("status", "Proposed")
            lat, lng = node.get("lat"), node.get("lng")

            if lat is None or lng is None:
                continue

            if "online" in node_status.lower():
                marker_color, fill_color = "#10B981", "#A7F3D0"
            else:
                marker_color, fill_color = "#2563EB", "#BFDBFE"

            popup_html = f"""
            <div style="font-family: sans-serif; font-size: 11px; width: 210px;">
                <b style="font-size: 13px; color: #0F172A;">{node_id}</b> — {node_name}<br><br>
                <b>Soil Temp (0.5m):</b> {node.get('shallow_soil_temp', 68.4)} °C<br>
                <b>Soil Temp (1.0m):</b> {node.get('deep_soil_temp', 74.2)} °C<br>
                <b>Soil Moisture:</b> {node.get('soil_moisture', 42.5)} %<br>
                <b>Fluid pH:</b> {node.get('ph_level', 2.8)} | <b>EC:</b> {node.get('ec_meter', 3800)} µS<br>
                <b>H₂S:</b> {node.get('h2s_gas', 14.2)} ppm | <b>CO₂:</b> {node.get('co2_gas', 850)} ppm
            </div>
            """

            folium.CircleMarker(
                location=[lat, lng],
                radius=8,
                color=marker_color,
                fill=True,
                fill_color=fill_color,
                fill_opacity=0.9,
                popup=folium.Popup(popup_html, max_width=240),
                tooltip=f"{node_id} ({node_name})"
            ).add_to(fg_nodes)

        fg_nodes.add_to(m)
        folium.LayerControl(collapsed=True).add_to(m)

        st_folium(m, width="100%", height=510, key="gmn_network_map")

    # ── CLEAN EXPANDABLE IOT ARCHITECTURE ──────────────────────────────────
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    with st.expander("IoT Architecture & 11-Parameter Hardware Specification", expanded=False):
        tab_sensors, tab_hw, tab_pipeline = st.tabs(["11-Parameter Suite", "Hardware Stack", "Data Pipeline"])

        with tab_sensors:
            sensor_data = {
                "No": list(range(1, 12)),
                "Parameter Measurement": [
                    "Temperatur tanah dangkal (0.5m)",
                    "Temperatur tanah lebih dalam (1.0m)",
                    "Temperatur udara",
                    "Kelembapan relatif udara",
                    "Kelembapan tanah",
                    "pH fluida geothermal",
                    "Electrical Conductivity (EC)",
                    "H₂S Gas Concentration",
                    "CO₂ Gas Concentration",
                    "Waktu pengukuran",
                    "Koordinat node"
                ],
                "Sensor Hardware": [
                    "PT100 RTD Probe + MAX31865",
                    "PT100 RTD Probe + MAX31865",
                    "Sensirion SHT31",
                    "Sensirion SHT31",
                    "DFRobot SEN0193 Capacitive Soil Moisture Sensor",
                    "DFRobot Gravity Analog pH Sensor V2 / SEN0161-V2",
                    "DFRobot Gravity Analog EC Meter K=1",
                    "Winsen MQ-136",
                    "Winsen MH-Z19B NDIR",
                    "DS3231 RTC",
                    "u-blox NEO-M8N GNSS"
                ]
            }
            st.dataframe(pd.DataFrame(sensor_data), use_container_width=True, hide_index=True)

        with tab_hw:
            hw_col1, hw_col2, hw_col3 = st.columns(3)
            with hw_col1:
                st.markdown("**Processing & Core**\n- ESP32-WROOM-32 Dual Core MCU\n- ADS1115 16-Bit ADC\n- MAX31865 RTD Amplifiers")
            with hw_col2:
                st.markdown("**Telemetry & Power**\n- SX1276/SX1262 LoRa Transceiver\n- SIM7600G-H 4G Cellular Module\n- 20W Solar Panel + LiFePO4 Pack")
            with hw_col3:
                st.markdown("**Field Enclosure**\n- IP67 Industrial ABS Box\n- SS316 Thermowell Armored Probes\n- IP68 PTFE Gas Vent Caps")

        with tab_pipeline:
            st.info("**Data Flow:** Probes (11 Parameters) ➔ ESP32 Edge MCU ➔ LoRaWAN / 4G Gateway ➔ Cloud Broker (MQTT/InfluxDB) ➔ GEO-SMART Dashboard")


if __name__ == "__main__":
    render_monitoring()