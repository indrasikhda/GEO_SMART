import streamlit as st
import pandas as pd
import textwrap
from core.data import DATA_SOURCES_INVENTORY
from ui.components import page_header, kpi_card

def render_data_sources():
    # ── Header Halaman Ringkas (Anggaran Teks) ──────────────────────────────
    page_header(
        title="Sumber Data & Provenance",
        subtitle="Inventaris seluruh dataset spasial, resolusi, lembaga sumber, dan status verifikasi ilmiah.",
        badge_text="● Transparansi Ilmiah",
        badge_tooltip="Klasifikasi status data untuk memastikan integritas pra-eksplorasi"
    )

    df_raw = pd.DataFrame(DATA_SOURCES_INVENTORY)

    real_count = sum(1 for d in DATA_SOURCES_INVENTORY if d["Status"] == "REAL")
    lit_count = sum(1 for d in DATA_SOURCES_INVENTORY if "LITERATURE" in d["Status"] or d["Status"] == "CALCULATED")
    pending_count = sum(1 for d in DATA_SOURCES_INVENTORY if d["Status"] == "PENDING")
    sim_count = sum(1 for d in DATA_SOURCES_INVENTORY if d["Status"] in ["SIMULATED", "PROPOSED"])

    # ── Baris KPI Bento (Maksimal 4 kartu) ──────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Total Dataset", f"{len(DATA_SOURCES_INVENTORY)}", subtext="Basis data spasial")
    with k2:
        kpi_card("Data Riil", f"{real_count}", trend="Satelit & Lapangan", trend_type="success")
    with k3:
        kpi_card("Literatur / Kalkulasi", f"{lit_count}", subtext="Benchmark terverifikasi")
    with k4:
        kpi_card("Simulasi & Pending", f"{sim_count + pending_count}", subtext="Dalam pengembangan")

    st.write("")

    # ── Bento Card: Registry Dataset Berdasarkan Tipe ───────────────────────
    categories = {}
    for item in DATA_SOURCES_INVENTORY:
        cat = item.get("Type", "Lainnya")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    for category, items in categories.items():
        st.markdown(textwrap.dedent(f"""
<div class="bento-card">
<div class="bento-card-header">
<div>
<div class="bento-card-title">{category}</div>
<div class="bento-card-sub">{len(items)} dataset terdaftar dalam modul ini</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

        for item in items:
            status = item.get("Status", "PENDING")
            badge_bg = "#DCFCE7" if status == "REAL" else ("#EFF6FF" if "LITERATURE" in status or status == "CALCULATED" else "#F1F5F9")
            badge_color = "#15803D" if status == "REAL" else ("#1D4ED8" if "LITERATURE" in status or status == "CALCULATED" else "#64748B")

            st.markdown(textwrap.dedent(f"""
<div style="padding:0.65rem 0.85rem;margin-bottom:0.45rem;border:1px solid #E2E8F0;border-radius:10px;background:#FFFFFF;">
<div style="display:flex;justify-content:space-between;align-items:flex-start;">
<div>
<div style="font-size:0.84rem;font-weight:700;color:#0F172A;">{item['Data Source']}</div>
<div style="font-size:0.72rem;color:#64748B;margin-top:0.15rem;">{item['Role']}</div>
</div>
<span style="font-size:0.65rem;font-weight:700;padding:0.15rem 0.5rem;border-radius:9999px;background:{badge_bg};color:{badge_color};">{status}</span>
</div>
<div style="display:flex;gap:1.5rem;font-size:0.7rem;color:#64748B;padding-top:0.4rem;margin-top:0.4rem;border-top:1px solid #F1F5F9;">
<div><b>Layer:</b> {item.get('Layer', 'N/A')}</div>
<div><b>Sumber:</b> {item.get('Source', 'N/A')}</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Expander Unduh Tabel Data Lengkap ────────────────────────────────────
    with st.expander("ℹ️ Unduh Tabel Katalog Data Lengkap (CSV)", expanded=False):
        st.dataframe(df_raw, use_container_width=True, hide_index=True)
        csv = df_raw.to_csv(index=False)
        st.download_button(
            label="Unduh File CSV",
            data=csv,
            file_name="geosmart_data_inventory.csv",
            mime="text/csv",
            key="data_sources_download_csv"
        )