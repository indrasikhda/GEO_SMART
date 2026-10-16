import streamlit as st
import textwrap

# ════════════════════════════════════════════════════════════════════════════
# GEO-SMART REUSABLE UI COMPONENTS — ui/components.py
# Clean Bento Design System inspired by AeuxGlobal reference
# ════════════════════════════════════════════════════════════════════════════


def page_header(title: str, subtitle: str = "", badge_text: str = "", badge_tooltip: str = "", action_html: str = ""):
    """
    Header halaman ringkas TANPA kartu putih pembungkus:
    - Judul tebal (24-26px) di kiri + opsional badge kecil bertooltip di sampingnya
    - Subjudul maksimal 1 baris (12-14px) warna redup di bawah judul
    - Aksi/filter utama di sisi kanan (opsional)
    """
    badge_html = ""
    if badge_text:
        title_attr = f'title="{badge_tooltip}"' if badge_tooltip else ""
        badge_html = f'<span class="header-status-badge" {title_attr}>{badge_text}</span>'

    action_col_html = f'<div class="header-action-col">{action_html}</div>' if action_html else ""
    sub_html = f'<div class="clean-page-subtitle">{subtitle}</div>' if subtitle else ""

    html = textwrap.dedent(f"""
<div class="clean-page-header">
<div class="header-title-col">
<div class="header-title-row">
<h1 class="clean-page-title">{title}</h1>
{badge_html}
</div>
{sub_html}
</div>
{action_col_html}
</div>
""").strip()

    st.markdown(html, unsafe_allow_html=True)


def kpi_card(label: str, value: str, subtext: str = "", trend: str = "", trend_type: str = "neutral", dark: bool = False):
    """
    Bento KPI Card:
    - Label kecil di atas (12px, abu/muted)
    - Angka besar di tengah (28-32px, tebal)
    - Subteks / mini trend di bawah (hanya jika membawa info baru, tanpa pill redundan)
    """
    card_cls = "bento-kpi dark" if dark else "bento-kpi"
    trend_html = ""
    if trend:
        trend_cls = f"kpi-trend {trend_type}"
        trend_html = f'<span class="{trend_cls}">{trend}</span>'
    
    subtext_html = f'<span class="kpi-subtext">{subtext}</span>' if subtext else ""
    
    html = textwrap.dedent(f"""
<div class="{card_cls}">
<div class="kpi-label">{label}</div>
<div class="kpi-value">{value}</div>
<div class="kpi-footer-row">
{subtext_html}
{trend_html}
</div>
</div>
""").strip()

    st.markdown(html, unsafe_allow_html=True)


def dark_highlight_card(title: str, main_stat: str, sub_stat: str = "", desc: str = "", tag: str = "PRIORITAS UTAMA"):
    """
    Kartu aksen gelap bento (seperti kartu AeuxGlobal 'Climate Change Index' & 'Let's join our community').
    Cocok untuk menyorot zona GPI tertinggi atau status kritis.
    """
    sub_html = f'<div class="dark-card-substat">{sub_stat}</div>' if sub_stat else ""
    desc_html = f'<div class="dark-card-desc">{desc}</div>' if desc else ""

    html = textwrap.dedent(f"""
<div class="bento-card-dark-highlight">
<div class="dark-card-top-row">
<span class="dark-card-tag">{tag}</span>
<span style="font-size:1.1rem;">⚡</span>
</div>
<div class="dark-card-title">{title}</div>
<div class="dark-card-stat">{main_stat}</div>
{sub_html}
{desc_html}
</div>
""").strip()

    st.markdown(html, unsafe_allow_html=True)


def badge(text: str, style: str = "neutral") -> str:
    """Kembalikan HTML badge kecil inline."""
    return f'<span class="geo-badge {style}">{text}</span>'


def info_tooltip(term: str, definition: str) -> str:
    """Inline tooltip text with info icon."""
    safe_def = definition.replace('"', '&quot;')
    return f'<span class="geo-tooltip-wrap">{term}&nbsp;<span class="geo-info-icon" title="{safe_def}">ℹ</span></span>'
