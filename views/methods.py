import html

import streamlit as st

from core.data import METHODS_STEPS
from core.fahp import calculate_fahp_weights
from ui.components import page_header, kpi_card, card_header, dark_highlight_card

# ════════════════════════════════════════════════════════════════════════════
# Halaman: Metode & Alur Kerja
# Alur diambil dari METHODS_STEPS (core/data.py) sehingga jumlah tahap selalu cocok.
# Pola: header → 4 KPI → kartu alur → [tahap pengembangan | dampak] → expander
# ════════════════════════════════════════════════════════════════════════════

# Judul singkat berbahasa Indonesia, urut sama dengan METHODS_STEPS
STEP_SHORT = [
    "Penginderaan Jauh",
    "Bukti Multi-Sumber",
    "Pembobotan FAHP",
    "Standardisasi 0–1",
    "Overlay & GPI",
    "Zona Prioritas",
    "Node GMN",
    "Telemetri IoT",
    "Analisis Temporal",
    "Validasi Pakar",
    "Kontribusi Net Zero",
]

# status → (label Indonesia, nada warna)
STATUS_INFO = {
    "REAL DATA": ("Data nyata", "green"),
    "REAL / PENDING INTEGRATION": ("Sebagian terintegrasi", "green"),
    "LITERATURE-INFORMED": ("Berbasis literatur", "blue"),
    "METHODOLOGICAL FRAMEWORK": ("Kerangka metode", "blue"),
    "PRELIMINARY CALCULATION": ("Hitungan awal", "blue"),
    "PRELIMINARY TARGETING": ("Penargetan awal", "blue"),
    "PROPOSED": ("Usulan", "amber"),
    "SIMULATED TELEMETRY": ("Telemetri simulasi", "amber"),
    "DEMONSTRATION / FUTURE DATA": ("Demonstrasi", "amber"),
    "FUTURE VALIDATION": ("Validasi mendatang", "slate"),
    "STRATEGIC IMPACT": ("Dampak strategis", "slate"),
}
# nada → (latar badge, teks badge, warna angka)
TONES = {
    "green": ("#DCFCE7", "#15803D", "#22C55E"),
    "blue": ("#EFF6FF", "#1D4ED8", "#3B82F6"),
    "amber": ("#FEF3C7", "#B45309", "#F59E0B"),
    "slate": ("#F1F5F9", "#64748B", "#94A3B8"),
}
TONE_LEGEND = [
    ("green", "Data nyata"),
    ("blue", "Model berbasis literatur / hitungan awal"),
    ("amber", "Usulan / simulasi"),
    ("slate", "Tahap mendatang"),
]


def _e(value) -> str:
    return html.escape(str(value), quote=True)


def _tiles_html(steps) -> str:
    use_short = len(steps) == len(STEP_SHORT)
    tiles = ""
    for i, st_ in enumerate(steps):
        title = STEP_SHORT[i] if use_short else st_.get("title", st_.get("step", f"Tahap {i + 1}"))
        raw_status = st_.get("status", "")
        label, tone = STATUS_INFO.get(raw_status, (raw_status.title(), "slate"))
        bg, fg, solid = TONES[tone]
        tiles += (
            '<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:14px;padding:0.8rem 0.75rem;">'
            '<div style="display:flex;align-items:center;gap:0.5rem;">'
            f'<div style="width:26px;height:26px;border-radius:8px;background:{solid};color:#FFFFFF;'
            'display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.8rem;'
            f'flex-shrink:0;">{i + 1}</div>'
            f'<div style="font-size:0.8rem;font-weight:700;color:#0F172A;line-height:1.25;">{_e(title)}</div>'
            '</div>'
            f'<div style="margin-top:0.55rem;"><span title="{_e(raw_status)}" style="font-size:0.62rem;'
            f'font-weight:700;padding:0.12rem 0.5rem;border-radius:9999px;background:{bg};color:{fg};">'
            f'{_e(label)}</span></div></div>'
        )
    legend = "".join(
        f'<span style="display:flex;align-items:center;gap:0.4rem;">'
        f'<span style="width:10px;height:10px;border-radius:3px;background:{TONES[t][2]};"></span>{txt}</span>'
        for t, txt in TONE_LEGEND
    )
    return (
        f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.75rem;">{tiles}</div>'
        '<div style="display:flex;flex-wrap:wrap;gap:0.4rem 1.25rem;font-size:0.72rem;'
        f'color:#475569;font-weight:600;margin-top:0.75rem;">{legend}</div>'
    )


def render_methods():
    steps = METHODS_STEPS or []
    fahp = calculate_fahp_weights()

    # ── Header ───────────────────────────────────────────────────────────────
    page_header(
        title="Metode & Alur Kerja",
        subtitle="Alur keputusan eksplorasi dari data satelit hingga pemantauan lapangan.",
        badge_text=f"● {len(steps)} Tahapan",
        badge_tooltip="Alur terintegrasi: penginderaan jauh, bukti spasial, FAHP, GPI, zona prioritas, GMN, hingga validasi.",
    )

    # ── KPI ──────────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Tahapan Alur", str(len(steps)), subtext="Dari data satelit ke keputusan")
    with k2:
        kpi_card("Model Pembobotan", "Fuzzy AHP", subtext=f"CR {fahp['CR']:.3f}",
                 trend="Konsisten" if fahp["is_consistent"] else "Perlu review",
                 trend_type="success" if fahp["is_consistent"] else "warning")
    with k3:
        kpi_card("Indeks Prospek", "GPI", subtext="Σ(wᵢ × Sᵢ) weighted overlay")
    with k4:
        kpi_card("Target Transisi", "Net Zero", trend="2060", trend_type="success")

    st.write("")

    # ── Kartu alur kerja (dari METHODS_STEPS) ────────────────────────────────
    with st.container(key="card_pipeline"):
        card_header("Alur Kerja GEO-SMART", f"{len(steps)} tahapan beserta status tiap tahap")
        if steps:
            st.markdown(_tiles_html(steps), unsafe_allow_html=True)
        else:
            st.caption("Definisi tahapan belum tersedia.")

    st.write("")

    col_dev, col_impact = st.columns(2, gap="medium")

    with col_dev:
        with st.container(key="card_phase"):
            card_header("Tahap Pengembangan", "Prototipe saat ini dan rencana validasi")
            st.markdown(
                '<div style="padding:0.7rem 0.85rem;background:#F0FDF4;border:1px solid #BBF7D0;'
                'border-radius:12px;margin-bottom:0.6rem;">'
                '<div style="font-size:0.8rem;font-weight:700;color:#15803D;margin-bottom:0.2rem;">'
                'Saat ini · Prototipe berbasis literatur</div>'
                '<div style="font-size:0.74rem;color:#166534;line-height:1.5;">'
                'Data satelit nyata (Landsat 8/9 dan Sentinel-2) dipadukan dengan bobot '
                'Şener &amp; Şener (2021).</div></div>'
                '<div style="padding:0.7rem 0.85rem;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;">'
                '<div style="font-size:0.8rem;font-weight:700;color:#334155;margin-bottom:0.2rem;">'
                'Berikutnya · Validasi pakar dan lapangan</div>'
                '<div style="font-size:0.74rem;color:#64748B;line-height:1.5;">'
                'Penilaian pakar geologi lokal (Delphi/AHP) dan verifikasi lapangan '
                '(mis. survei MT/geolistrik dan landaian suhu).</div></div>',
                unsafe_allow_html=True,
            )

    with col_impact:
        dark_highlight_card(
            title="Kontribusi transisi bersih",
            main_stat="Net Zero",
            sub_stat="Target nasional 2060",
            desc=("Dirancang untuk memperbaiki penargetan spasial, mengurangi aktivitas eksplorasi "
                  "yang tidak perlu, dan mendukung pemantauan berkelanjutan."),
            tag="DAMPAK ENERGI",
        )

    # ── Detail seluruh tahapan ───────────────────────────────────────────────
    with st.expander(f"Detail {len(steps)} tahapan metodologi", expanded=False):
        if steps:
            for s in steps:
                label = STATUS_INFO.get(s.get("status", ""), (s.get("status", ""), "slate"))[0]
                st.markdown(
                    f"**{s.get('step', '')}** · {s.get('title', '')} — {s.get('desc', '')} "
                    f"*({label})*"
                )
        else:
            st.markdown("Definisi tahapan belum tersedia di `core/data.py`.")