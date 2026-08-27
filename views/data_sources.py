import streamlit as st
from core.data import DATA_SOURCES_INVENTORY

STATUS_COLORS = {
    "Available":  {"dot": "#34C759", "bg": "#E8FAF0", "text": "#1B7A3E"},
    "Pending":    {"dot": "#FF9500", "bg": "#FFF4E0", "text": "#944E00"},
    "Simulated":  {"dot": "#007AFF", "bg": "#E3F0FF", "text": "#0051A8"},
}

def render_data_sources():
    st.markdown("<p style='font-size:0.9rem;color:#636366;margin-bottom:1.5rem;'>Inventory of satellite rasters, geological GIS layers, and IoT telemetry streams.</p>", unsafe_allow_html=True)

    for item in DATA_SOURCES_INVENTORY:
        sc = STATUS_COLORS.get(item["Status"], STATUS_COLORS["Pending"])
        st.markdown(f"""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:16px 22px;margin-bottom:0.75rem;box-shadow:0 2px 10px rgba(0,0,0,0.02);display:flex;align-items:center;justify-content:space-between;gap:16px;">
                <div style="display:flex;align-items:center;gap:14px;flex:1;">
                    <div style="width:36px;height:36px;background:#F2F2F7;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;">📄</div>
                    <div>
                        <span style="font-size:0.9rem;font-weight:700;color:#1C1C1E;">{item['Data Source']}</span>
                        <span style="font-size:0.75rem;color:#8E8E93;display:block;margin-top:2px;">{item['Role']}</span>
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:12px;flex-shrink:0;">
                    <code style="font-size:0.75rem;color:#636366;background:#F2F2F7;padding:3px 8px;border-radius:6px;">{item['Layer']}</code>
                    <span style="font-size:0.72rem;font-weight:700;color:{sc['text']};background:{sc['bg']};padding:4px 10px;border-radius:9999px;white-space:nowrap;">
                        ● {item['Status']}
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
