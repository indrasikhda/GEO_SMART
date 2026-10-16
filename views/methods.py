import streamlit as st
import textwrap
from core.data import METHODS_STEPS
from ui.components import page_header, kpi_card, dark_highlight_card

def render_methods():
    # ── Header Halaman Ringkas (Anggaran Teks) ──────────────────────────────
    page_header(
        title="Metode & Alur Kerja",
        subtitle="Kerangka kerja pengambilan keputusan eksplorasi dari penginderaan jauh hingga pemantauan IoT.",
        badge_text="● 6 Tahapan Pipeline",
        badge_tooltip="Alur kerja terintegrasi dari data satelit hingga monitoring lapangan"
    )

    # ── Baris KPI Bento (Maksimal 4 kartu) ──────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Tahapan Pipeline", "6 Fase", subtext="Siklus pra-eksplorasi")
    with k2:
        kpi_card("Model Pembobotan", "Fuzzy-AHP", trend="Konsisten", trend_type="success")
    with k3:
        kpi_card("Indeks Prospek", "GPI", subtext="Σ(w_i × S_i) weighted overlay")
    with k4:
        kpi_card("Target Transisi", "Net Zero", trend="2060", trend_type="success")

    st.write("")

    # ── Bento Card: Visualisasi Pipeline 6 Tahap ────────────────────────────
    st.markdown(textwrap.dedent("""
<div class="bento-card">
<div class="bento-card-header">
<div>
<div class="bento-card-title">Alur Kerja Sistem Eksplorasi GEO-SMART</div>
<div class="bento-card-sub">Integrasi sekuensial modul data, multikriteria, dan pemantauan IoT</div>
</div>
</div>
<div style="display:flex;overflow-x:auto;gap:0.75rem;padding:0.75rem 0;">
<div style="flex:1;min-width:120px;text-align:center;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:0.85rem 0.5rem;">
<div style="width:32px;height:32px;margin:0 auto 0.4rem;background:#22C55E;color:#FFF;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.9rem;">1</div>
<div style="font-size:0.78rem;font-weight:700;color:#0F172A;">Penginderaan Jauh</div>
<div style="font-size:0.65rem;color:#64748B;">LST &amp; NDVI</div>
</div>
<div style="flex:1;min-width:120px;text-align:center;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:0.85rem 0.5rem;">
<div style="width:32px;height:32px;margin:0 auto 0.4rem;background:#22C55E;color:#FFF;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.9rem;">2</div>
<div style="font-size:0.78rem;font-weight:700;color:#0F172A;">Bukti Spasial</div>
<div style="font-size:0.65rem;color:#64748B;">Geologi &amp; Sesar</div>
</div>
<div style="flex:1;min-width:120px;text-align:center;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:0.85rem 0.5rem;">
<div style="width:32px;height:32px;margin:0 auto 0.4rem;background:#22C55E;color:#FFF;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.9rem;">3</div>
<div style="font-size:0.78rem;font-weight:700;color:#0F172A;">Fuzzy AHP</div>
<div style="font-size:0.65rem;color:#64748B;">Pembobotan</div>
</div>
<div style="flex:1;min-width:120px;text-align:center;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:0.85rem 0.5rem;">
<div style="width:32px;height:32px;margin:0 auto 0.4rem;background:#22C55E;color:#FFF;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.9rem;">4</div>
<div style="font-size:0.78rem;font-weight:700;color:#0F172A;">Kalkulasi GPI</div>
<div style="font-size:0.65rem;color:#64748B;">Indeks Prospek</div>
</div>
<div style="flex:1;min-width:120px;text-align:center;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:0.85rem 0.5rem;">
<div style="width:32px;height:32px;margin:0 auto 0.4rem;background:#22C55E;color:#FFF;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.9rem;">5</div>
<div style="font-size:0.78rem;font-weight:700;color:#0F172A;">Zona Prioritas</div>
<div style="font-size:0.65rem;color:#64748B;">Analisis Kendala</div>
</div>
<div style="flex:1;min-width:120px;text-align:center;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:0.85rem 0.5rem;">
<div style="width:32px;height:32px;margin:0 auto 0.4rem;background:#22C55E;color:#FFF;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.9rem;">6</div>
<div style="font-size:0.78rem;font-weight:700;color:#0F172A;">Monitoring GMN</div>
<div style="font-size:0.65rem;color:#64748B;">Telemetri IoT</div>
</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

    # ── Tahap Pengembangan & Dampak Net Zero (Grid 2 Kolom) ─────────────────
    col_dev, col_impact = st.columns([1, 1], gap="medium")

    with col_dev:
        st.markdown(textwrap.dedent("""
<div class="bento-card">
<div class="bento-card-header">
<div>
<div class="bento-card-title">Tahap Pengembangan Sistem</div>
<div class="bento-card-sub">Status prototipe vs rencana validasi lapangan</div>
</div>
</div>
<div style="padding:0.65rem 0.85rem;background:#F0FDF4;border:1px solid #BBF7D0;border-radius:10px;margin-bottom:0.6rem;">
<div style="font-size:0.78rem;font-weight:700;color:#15803D;margin-bottom:0.2rem;">Fase Saat Ini &bull; Prototipe Literatur</div>
<div style="font-size:0.72rem;color:#166534;line-height:1.5;">
Mengintegrasikan data satelit riil (Landsat 8/9 &amp; Sentinel-2) dengan bobot multikriteria Şener &amp; Şener (2021) untuk sistem panas bumi vulkanik.
</div>
</div>
<div style="padding:0.65rem 0.85rem;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;">
<div style="font-size:0.78rem;font-weight:700;color:#334155;margin-bottom:0.2rem;">Fase Selanjutnya &bull; Validasi Ahli &amp; Lapangan</div>
<div style="font-size:0.72rem;color:#64748B;line-height:1.5;">
Kalibrasi matriks FAHP oleh panel pakar geologi lokal, survei MT/geolistrik ground truth, dan pengeboran landaian suhu.
</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)

    with col_impact:
        dark_highlight_card(
            title="Akselerasi Transisi Bersih",
            main_stat="Net Zero 2060",
            sub_stat="Mitigasi Risiko Pra-Eksplorasi Panas Bumi",
            desc="Penentuan target zona prospek secara presisi menurunkan frekuensi sumur eksplorasi kering (dry holes), memperkecil jejak karbon proyek, dan mempercepat pemanfaatan energi beban dasar bersih 24/7 di Indonesia.",
            tag="DAMPAK ENERGI"
        )

    # ── Expander Detail Langkah Metodologi ──────────────────────────────────
    with st.expander("ℹ️ Detail Langkah Metodologi 11 Tahapan Lengkap", expanded=False):
        if METHODS_STEPS:
            for step in METHODS_STEPS:
                st.markdown(f"**{step.get('step', '')}. {step.get('title', '')}** — {step.get('desc', '')}")
        else:
            st.markdown("""
                1. **Penginderaan Jauh:** Akuisisi citra termal LST Landsat dan tutupan vegetasi NDVI Sentinel-2.
                2. **Integrasi Bukti:** Penggabungan geologi regional, sesar, dan inventaris manifestasi.
                3. **Matriks Pasangan:** Pembobotan kriteria terstandardisasi Fuzzy AHP.
                4. **Kalkulasi GPI:** Tumpang susun berbobot multi-kriteria spasial.
                5. **Zonasi Prioritas:** Peringkat zona prospektif dan filter kendala lingkungan.
                6. **Monitoring GMN:** Desain jaringan stasiun sensor telemetri 11-parameter.
            """)
