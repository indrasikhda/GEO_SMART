import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import textwrap
from core.io import GMN_NODES
from core.maps import create_base_map
from ui.components import page_header, kpi_card

def render_monitoring():
    # ── Header Halaman Ringkas (Anggaran Teks) ──────────────────────────────
    page_header(
        title="Monitoring GMN",
        subtitle="Jaringan telemetri sensor 11-parameter dan pemantauan stasiun lapangan pra-eksplorasi.",
        badge_text="● 3 Node Pemantauan",
        badge_tooltip="Stasiun IoT terhubung secara simulasi stream"
    )

    # ── Baris KPI Bento (Maksimal 4 kartu) ──────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Node Jaringan", f"{len(GMN_NODES)}", subtext="Stasiun usulan lapangan")
    with k2:
        kpi_card("Status Telemetri", "Simulasi", trend="Pra-Implementasi", trend_type="neutral")
    with k3:
        kpi_card("Kanal Sensor", "11 Kanal", subtext="Suhu, kelembapan, gas, pH")
    with k4:
        kpi_card("Protokol IoT", "LoRa / 4G", subtext="Interval 15 menit")

    st.write("")

    # ── Layout Konten: Kartu Telemetri Node (5) + Peta Jaringan (7) ─────────
    col_nodes, col_map = st.columns([5, 7], gap="medium")

    with col_nodes:
        st.markdown(textwrap.dedent("""
<div class="bento-card">
<div class="bento-card-header">
<div>
<div class="bento-card-title">Telemetri Stasiun Sensor</div>
<div class="bento-card-sub">Data real-time parameter fisika &amp; kimia tanah</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

        for node in GMN_NODES:
            node_id = node.get("id", "GMN")
            node_name = node.get("name", "Monitoring Node")
            node_status = node.get("status", "Proposed Node")

            is_online = "online" in node_status.lower()
            badge_bg = "#DCFCE7" if is_online else "#EFF6FF"
            badge_color = "#15803D" if is_online else "#1D4ED8"
            badge_text = "ONLINE" if is_online else "USULAN"

            st.markdown(textwrap.dedent(f"""
<div style="padding:0.75rem;margin-bottom:0.6rem;border:1px solid #E2E8F0;border-radius:12px;background:#FFFFFF;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
<div>
<span style="font-size:0.9rem;font-weight:800;color:#0F172A;">{node_id}</span>
<span style="font-size:0.78rem;color:#64748B;margin-left:0.35rem;">{node_name}</span>
</div>
<span style="font-size:0.62rem;font-weight:700;padding:0.12rem 0.5rem;border-radius:9999px;background:{badge_bg};color:{badge_color};">{badge_text}</span>
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.4rem;font-size:0.72rem;background:#F8FAFC;padding:0.5rem;border-radius:8px;">
<div>
<div style="color:#64748B;font-size:0.62rem;font-weight:600;">Suhu 0.5m</div>
<div style="font-weight:800;color:#0F172A;">{node.get('shallow_soil_temp', 68.4)}°C</div>
</div>
<div>
<div style="color:#64748B;font-size:0.62rem;font-weight:600;">Suhu 1.0m</div>
<div style="font-weight:800;color:#0F172A;">{node.get('deep_soil_temp', 74.2)}°C</div>
</div>
<div>
<div style="color:#64748B;font-size:0.62rem;font-weight:600;">Gas H₂S</div>
<div style="font-weight:800;color:#0F172A;">{node.get('h2s_gas', 14.2)} ppm</div>
</div>
<div>
<div style="color:#64748B;font-size:0.62rem;font-weight:600;">Gas CO₂</div>
<div style="font-weight:800;color:#0F172A;">{node.get('co2_gas', 850)} ppm</div>
</div>
</div>
<div style="display:flex;justify-content:space-between;font-size:0.68rem;color:#64748B;margin-top:0.4rem;padding-top:0.35rem;border-top:1px solid #F1F5F9;">
<span>📍 {node.get('lat', '--')}, {node.get('lng', '--')}</span>
<span>Baterai: <b>{node.get('battery', 94)}%</b></span>
</div>
</div>
""").strip(), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col_map:
        st.markdown(textwrap.dedent("""
<div class="bento-card" style="padding-bottom:1rem;">
<div class="bento-card-header">
<div>
<div class="bento-card-title">Peta Jaringan Stasiun Pemantauan</div>
<div class="bento-card-sub">Sebaran spasial node telemetri lapangan di Sulawesi Utara</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

        m = create_base_map(center=[1.35, 124.85], zoom=8)

        fg_nodes = folium.FeatureGroup(name="Proposed GMN Nodes")
        for node in GMN_NODES:
            node_id = node.get("id", "GMN")
            node_name = node.get("name", "Monitoring Node")
            node_status = node.get("status", "Proposed")
            lat, lng = node.get("lat"), node.get("lng")

            if lat is None or lng is None:
                continue

            marker_color = "#10B981" if "online" in node_status.lower() else "#2563EB"
            fill_color = "#A7F3D0" if "online" in node_status.lower() else "#BFDBFE"

            popup_html = f"""
            <div style="font-family: sans-serif; font-size: 11px; width: 210px;">
                <b style="font-size: 13px; color: #0F172A;">{node_id}</b> — {node_name}<br><br>
                <b>Suhu Tanah (0.5m):</b> {node.get('shallow_soil_temp', 68.4)} °C<br>
                <b>Suhu Tanah (1.0m):</b> {node.get('deep_soil_temp', 74.2)} °C<br>
                <b>Gas H₂S:</b> {node.get('h2s_gas', 14.2)} ppm | <b>CO₂:</b> {node.get('co2_gas', 850)} ppm
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
        st_folium(m, width="100%", height=440, key="gmn_network_map")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Expander Spesifikasi Hardware 11 Parameter ──────────────────────────
    with st.expander("ℹ️ Arsitektur IoT & Spesifikasi Hardware 11-Parameter", expanded=False):
        tab_sensors, tab_hw = st.tabs(["Spesifikasi 11 Sensor", "Hardware & Daya"])
        with tab_sensors:
            sensor_data = {
                "No": list(range(1, 12)),
                "Parameter Pengukuran": [
                    "Temperatur tanah dangkal (0.5m)",
                    "Temperatur tanah dalam (1.0m)",
                    "Temperatur udara sekitar",
                    "Kelembapan relatif udara",
                    "Kelembapan tanah",
                    "pH fluida geotermal",
                    "Electrical Conductivity (EC)",
                    "Konsentrasi Gas H₂S",
                    "Konsentrasi Gas CO₂",
                    "RTC Waktu pengukuran",
                    "Koordinat GNSS node"
                ],
                "Modul Sensor": [
                    "PT100 RTD + MAX31865",
                    "PT100 RTD + MAX31865",
                    "Sensirion SHT31",
                    "Sensirion SHT31",
                    "DFRobot SEN0193 Kapasitif",
                    "DFRobot SEN0161-V2 Analog",
                    "DFRobot EC Meter K=1",
                    "Winsen MQ-136",
                    "Winsen MH-Z19B NDIR",
                    "DS3231 High-Precision RTC",
                    "u-blox NEO-M8N GNSS"
                ]
            }
            st.dataframe(pd.DataFrame(sensor_data), use_container_width=True, hide_index=True)

        with tab_hw:
            st.markdown("""
                - **Processing:** ESP32-WROOM-32 Dual Core MCU + ADS1115 16-Bit ADC.
                - **Komunikasi & Daya:** SX1262 LoRaWAN / SIM7600G-H 4G LTE &bull; 20W Monocrystalline Solar Panel + LiFePO4 Battery.
                - **Enclosure:** Kotak Proteksi Industri IP67 + SS316 Thermowell Armored Cable.
            """)