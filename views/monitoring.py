import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

from core.io import GMN_NODES, PRIORITY_ZONES
from core.data import DATA_SOURCES_INVENTORY
from core.maps import create_base_map
from ui.components import page_header, kpi_card, card_header, badge

# ════════════════════════════════════════════════════════════════════════════
# Halaman: Monitoring GMN
# Pola: header → 4 KPI → [kartu telemetri node 5 | kartu peta 7] → expander
# Catatan: nilai sensor di core/io.py bersifat simulasi dan node belum dipasang.
# ════════════════════════════════════════════════════════════════════════════

# (field di GMN_NODES, label, satuan)
PARAMS = [
    ("shallow_soil_temp", "Suhu tanah 0.5 m", "°C"),
    ("deep_soil_temp", "Suhu tanah 1.0 m", "°C"),
    ("air_temp", "Suhu udara", "°C"),
    ("air_humidity", "Kelembapan udara", "%"),
    ("soil_moisture", "Kelembapan tanah", "%"),
    ("ph_level", "pH fluida", ""),
    ("ec_meter", "EC", "µS/cm"),
    ("h2s_gas", "Gas H₂S", "ppm"),
    ("co2_gas", "Gas CO₂", "ppm"),
]

# 11 kanal sensor (spesifikasi hardware)
SENSOR_SPECS = [
    ("Temperatur tanah dangkal (0.5 m)", "PT100 RTD + MAX31865"),
    ("Temperatur tanah dalam (1.0 m)", "PT100 RTD + MAX31865"),
    ("Temperatur udara sekitar", "Sensirion SHT31"),
    ("Kelembapan relatif udara", "Sensirion SHT31"),
    ("Kelembapan tanah", "DFRobot SEN0193 Kapasitif"),
    ("pH fluida geotermal", "DFRobot SEN0161-V2 Analog"),
    ("Electrical Conductivity (EC)", "DFRobot EC Meter K=1"),
    ("Konsentrasi gas H₂S", "Winsen MQ-136"),
    ("Konsentrasi gas CO₂", "Winsen MH-Z19B NDIR"),
    ("RTC waktu pengukuran", "DS3231 High-Precision RTC"),
    ("Koordinat GNSS node", "u-blox NEO-M8N GNSS"),
]

STATUS_ID = {"SIMULATED": "Simulasi", "PROPOSED": "Usulan", "REAL": "Nyata"}
FIELD_STATUS_ID = {"Not deployed": "Belum dipasang"}
MAP_HEIGHT = 440


def _fmt(value) -> str:
    """Format nilai sensor; '—' bila tidak ada (tidak memakai nilai bawaan palsu)."""
    if value is None:
        return "—"
    try:
        return f"{float(value):g}"
    except (TypeError, ValueError):
        return str(value)


def _zone_for(node: dict):
    """Zona prioritas yang koordinatnya sama dengan node (jika ada)."""
    for z in PRIORITY_ZONES:
        if abs(z["lat"] - node.get("lat", 1e9)) < 1e-6 and abs(z["lng"] - node.get("lng", 1e9)) < 1e-6:
            return z
    return None


def _is_online(node: dict) -> bool:
    return "online" in str(node.get("status", "")).lower()


def _tiles_html(node: dict) -> str:
    tiles = ""
    for key, label, unit in PARAMS:
        unit_html = (f'<span style="font-size:0.7rem;font-weight:600;color:#64748B;'
                     f'margin-left:0.2rem;">{unit}</span>') if unit else ""
        tiles += (
            '<div style="background:#F8FAFC;border:1px solid #EEF2F0;border-radius:12px;'
            'padding:0.6rem 0.7rem;">'
            f'<div style="font-size:0.68rem;color:#64748B;font-weight:600;">{label}</div>'
            f'<div style="font-size:1.05rem;font-weight:800;color:#0F172A;line-height:1.3;">'
            f'{_fmt(node.get(key))}{unit_html}</div></div>'
        )
    return f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.5rem;">{tiles}</div>'


def render_monitoring():
    if not GMN_NODES:
        st.info("Belum ada node GMN yang terdaftar.")
        return

    src_status = {d["Data Source"]: d["Status"] for d in DATA_SOURCES_INVENTORY}
    iot_status = STATUS_ID.get(src_status.get("IoT Ground Telemetry", ""), "N/A")

    n_nodes = len(GMN_NODES)
    n_online = sum(1 for n in GMN_NODES if _is_online(n))
    n_proposed = n_nodes - n_online

    # ── Header ───────────────────────────────────────────────────────────────
    page_header(
        title="Monitoring GMN",
        subtitle="Telemetri sensor 11 kanal pada node pemantauan lapangan.",
        badge_text=f"● {n_nodes} Node Pemantauan",
        badge_tooltip="Node masih berstatus usulan; nilai sensor yang tampil adalah data simulasi.",
    )

    # ── KPI ──────────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Node Jaringan", str(n_nodes),
                 subtext=("Semua masih usulan" if n_online == 0
                          else f"{n_online} online · {n_proposed} usulan"))
    with k2:
        kpi_card("Status Telemetri", iot_status, trend="Pra-implementasi", trend_type="neutral")
    with k3:
        kpi_card("Kanal Sensor", f"{len(SENSOR_SPECS)} Kanal", subtext="Suhu, kelembapan, gas, pH")
    with k4:
        kpi_card("Protokol IoT", "LoRa / 4G", subtext="Interval 15 menit")

    st.write("")

    col_nodes, col_map = st.columns([5, 7], gap="medium")

    # ── Kartu telemetri: pilih node → semua parameter terukur ───────────────
    with col_nodes:
        with st.container(key="card_nodes"):
            card_header("Telemetri Stasiun", "Nilai simulasi; node belum dipasang di lapangan")

            ids = [n["id"] for n in GMN_NODES]
            sel_id = st.radio("Pilih node", ids, horizontal=True,
                              label_visibility="collapsed", key="gmn_selected")
            node = next(n for n in GMN_NODES if n["id"] == sel_id)

            status_badge = badge("Online", "success") if _is_online(node) else badge("Usulan", "neutral")
            purpose = node.get("purpose", "")
            purpose_html = (f'<div style="font-size:0.72rem;color:#64748B;margin-top:0.2rem;">{purpose}</div>'
                            if purpose else "")
            st.markdown(
                '<div>'
                '<div style="display:flex;justify-content:space-between;align-items:center;gap:0.5rem;">'
                f'<div style="font-size:0.9rem;font-weight:700;color:#0F172A;">'
                f'{node["id"]} · {node.get("name", "Node")}</div>{status_badge}</div>'
                f'{purpose_html}</div>',
                unsafe_allow_html=True,
            )

            st.markdown(_tiles_html(node), unsafe_allow_html=True)

            zone = _zone_for(node)
            zone_text = (f'{zone["zone"]} · GPI {zone["gpi"]:.2f}' if zone else "—")
            field_text = FIELD_STATUS_ID.get(node.get("last_update"), node.get("last_update") or "—")
            rows = [
                ("Koordinat", f'{node.get("lat", "—")}, {node.get("lng", "—")}'),
                ("Zona prioritas", zone_text),
                ("Status lapangan", field_text),
            ]
            st.markdown(
                '<div>' + "".join(
                    f'<div class="stat-row"><span class="l">{l}</span><span class="v">{v}</span></div>'
                    for l, v in rows
                ) + '</div>',
                unsafe_allow_html=True,
            )

    # ── Kartu peta ───────────────────────────────────────────────────────────
    with col_map:
        with st.container(key="card_map"):
            card_header("Peta Jaringan Stasiun", "Node terpilih ditandai lebih besar")

            m = create_base_map(center=[1.35, 124.85], zoom=8)
            fg_nodes = folium.FeatureGroup(name="Node GMN (usulan)")
            for n in GMN_NODES:
                lat, lng = n.get("lat"), n.get("lng")
                if lat is None or lng is None:
                    continue
                online = _is_online(n)
                is_sel = n["id"] == sel_id
                color = "#10B981" if online else "#2563EB"
                fill = "#A7F3D0" if online else "#BFDBFE"

                popup_html = (
                    '<div style="font-family:sans-serif;font-size:11px;width:200px;">'
                    f'<b style="font-size:13px;">{n["id"]}</b> — {n.get("name", "Node")}<br><br>'
                    f'<b>Suhu tanah 0.5 m:</b> {_fmt(n.get("shallow_soil_temp"))} °C<br>'
                    f'<b>Suhu tanah 1.0 m:</b> {_fmt(n.get("deep_soil_temp"))} °C<br>'
                    f'<b>H₂S:</b> {_fmt(n.get("h2s_gas"))} ppm · <b>CO₂:</b> {_fmt(n.get("co2_gas"))} ppm'
                    '</div>'
                )
                folium.CircleMarker(
                    location=[lat, lng],
                    radius=12 if is_sel else 8,
                    color=color,
                    weight=3 if is_sel else 1.5,
                    fill=True,
                    fill_color=color if is_sel else fill,
                    fill_opacity=0.95 if is_sel else 0.85,
                    popup=folium.Popup(popup_html, max_width=240),
                    tooltip=f'{n["id"]} · {n.get("name", "Node")}',
                ).add_to(fg_nodes)
            fg_nodes.add_to(m)
            folium.LayerControl(collapsed=True).add_to(m)

            st_folium(
                m,
                width="100%",
                height=MAP_HEIGHT,
                key=f"gmn_network_map_{sel_id}",
                returned_objects=[],
            )

            st.markdown(
                '<div style="display:flex;flex-wrap:wrap;gap:0.4rem 1.25rem;font-size:0.75rem;'
                'color:#475569;font-weight:600;">'
                '<span style="display:flex;align-items:center;gap:0.4rem;">'
                '<span style="width:12px;height:12px;border-radius:50%;background:#2563EB;"></span>'
                'Node terpilih</span>'
                '<span style="display:flex;align-items:center;gap:0.4rem;">'
                '<span style="width:10px;height:10px;border-radius:50%;background:#BFDBFE;'
                'border:1.5px solid #2563EB;"></span>Node usulan lain</span>'
                '</div>',
                unsafe_allow_html=True,
            )

    # ── Arsitektur & hardware ────────────────────────────────────────────────
    with st.expander("Arsitektur IoT & spesifikasi hardware", expanded=False):
        tab_sensors, tab_hw = st.tabs(["Spesifikasi 11 Sensor", "Hardware & Daya"])
        with tab_sensors:
            st.dataframe(
                pd.DataFrame({
                    "No": list(range(1, len(SENSOR_SPECS) + 1)),
                    "Parameter Pengukuran": [p for p, _ in SENSOR_SPECS],
                    "Modul Sensor": [s for _, s in SENSOR_SPECS],
                }),
                use_container_width=True,
                hide_index=True,
            )
        with tab_hw:
            st.markdown(
                """
- **Pemrosesan:** ESP32-WROOM-32 Dual Core MCU + ADS1115 16-Bit ADC.
- **Komunikasi & daya:** SX1262 LoRaWAN / SIM7600G-H 4G LTE · panel surya monocrystalline 20 W + baterai LiFePO4.
- **Enclosure:** kotak proteksi industri IP67 + kabel berarmor SS316 dengan thermowell.
                """
            )