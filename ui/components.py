import html as _html

import streamlit as st

# ════════════════════════════════════════════════════════════════════════════
# GEO-SMART REUSABLE UI COMPONENTS — ui/components.py
# Clean Bento Design System inspired by AeuxGlobal reference
#
# Catatan: semua HTML dibuat dalam SATU baris tanpa indentasi. Di Markdown,
# baris yang menjorok >= 4 spasi dibaca sebagai blok kode dan merusak tampilan.
# ════════════════════════════════════════════════════════════════════════════


# ── Header halaman ───────────────────────────────────────────────────────────
def page_header(title: str, subtitle: str = "", badge_text: str = "",
                badge_tooltip: str = "", action_html: str = ""):
    """
    Header halaman ringkas TANPA kartu pembungkus:
    - Judul tebal di kiri + badge kecil bertooltip (opsional)
    - Subjudul maksimal 1 baris, warna redup
    - Aksi/filter utama di kanan (opsional)
    """
    badge_html = ""
    if badge_text:
        tip = _html.escape(badge_tooltip, quote=True)
        title_attr = f'title="{tip}"' if tip else ""
        badge_html = f'<span class="header-status-badge" {title_attr}>{badge_text}</span>'

    sub_html = f'<div class="clean-page-subtitle">{subtitle}</div>' if subtitle else ""
    action_col = f'<div class="header-action-col">{action_html}</div>' if action_html else ""

    st.markdown(
        '<div class="clean-page-header">'
        '<div class="header-title-col">'
        f'<div class="header-title-row"><h1 class="clean-page-title">{title}</h1>{badge_html}</div>'
        f'{sub_html}'
        '</div>'
        f'{action_col}'
        '</div>',
        unsafe_allow_html=True,
    )


# ── Mini bar chart (SVG inline) ──────────────────────────────────────────────
def spark_bars_svg(values, hi=None, muted: str = "#D5E3DB", width: int = 64, height: int = 32) -> str:
    """
    Mini bar chart tanpa sumbu.
    - values : list angka (mis. hasil np.histogram(...)[0].tolist())
    - hi     : indeks batang yang disorot hijau (default: batang tertinggi)
    - muted  : warna batang lain
    """
    if not values:
        return ""
    vmin, vmax = min(values), max(values)
    rng = (vmax - vmin) or 1
    n, gap = len(values), 3
    bw = (width - gap * (n - 1)) / n
    if hi is None:
        hi = list(values).index(vmax)
    bars = []
    for i, v in enumerate(values):
        h = 4 + (v - vmin) / rng * (height - 4)
        color = "#22C55E" if i == hi else muted
        bars.append(
            f'<rect x="{i * (bw + gap):.1f}" y="{height - h:.1f}" '
            f'width="{bw:.1f}" height="{h:.1f}" rx="2" fill="{color}"/>'
        )
    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        f'{"".join(bars)}</svg>'
    )


# ── KPI card ─────────────────────────────────────────────────────────────────
def kpi_card(label: str, value: str, subtext: str = "", trend: str = "",
             trend_type: str = "neutral", dark: bool = False,
             spark=None, spark_hi=None):
    """
    Bento KPI Card:
    - Label kecil di atas (huruf normal, redup)
    - Angka besar (tebal), mini bar opsional di kanan
    - Subteks / trend di bawah hanya bila membawa informasi baru
    """
    card_cls = "bento-kpi dark" if dark else "bento-kpi"
    trend_html = f'<span class="kpi-trend {trend_type}">{trend}</span>' if trend else ""
    subtext_html = f'<span class="kpi-subtext">{subtext}</span>' if subtext else ""
    muted = "#1E503F" if dark else "#D5E3DB"
    spark_html = (
        f'<div class="kpi-spark">{spark_bars_svg(spark, hi=spark_hi, muted=muted)}</div>'
        if spark else ""
    )
    st.markdown(
        f'<div class="{card_cls}">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-main"><div class="kpi-value">{value}</div>{spark_html}</div>'
        f'<div class="kpi-footer-row">{subtext_html}{trend_html}</div>'
        '</div>',
        unsafe_allow_html=True,
    )


# ── Kartu sorotan gelap ──────────────────────────────────────────────────────
_BOLT_SVG = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#22C55E" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
)


def dark_highlight_card(title: str, main_stat: str, sub_stat: str = "",
                        desc: str = "", tag: str = "PRIORITAS UTAMA"):
    """
    Kartu aksen gelap (seperti 'Climate Change Index' di referensi).
    Cocok untuk menyorot zona GPI tertinggi atau status kritis.
    """
    sub_html = f'<div class="dark-card-substat">{sub_stat}</div>' if sub_stat else ""
    desc_html = f'<div class="dark-card-desc">{desc}</div>' if desc else ""
    st.markdown(
        '<div class="bento-card-dark-highlight">'
        f'<div class="dark-card-top-row"><span class="dark-card-tag">{tag}</span>{_BOLT_SVG}</div>'
        f'<div class="dark-card-title">{title}</div>'
        f'<div class="dark-card-stat">{main_stat}</div>'
        f'{sub_html}{desc_html}'
        '</div>',
        unsafe_allow_html=True,
    )


# ── Komponen di dalam kartu (pakai bersama st.container(key="card_...")) ─────
def card_header(title: str, sub: str = "", right_html: str = ""):
    """Judul di dalam kartu. Panggil di dalam `with st.container(key="card_xxx"):`."""
    sub_html = f'<div class="card-head-sub">{sub}</div>' if sub else ""
    st.markdown(
        f'<div class="card-head"><div><div class="card-head-title">{title}</div>{sub_html}</div>'
        f'{right_html}</div>',
        unsafe_allow_html=True,
    )


def stat_row(label: str, value: str):
    """Satu baris statistik. Untuk banyak baris pakai stat_rows() agar garis pemisah benar."""
    st.markdown(
        f'<div class="stat-row"><span class="l">{label}</span><span class="v">{value}</span></div>',
        unsafe_allow_html=True,
    )


def stat_rows(items):
    """
    items: list of (label, value).
    Dirender dalam SATU blok supaya aturan :last-child (tanpa garis di baris terakhir) bekerja.
    """
    rows = "".join(
        f'<div class="stat-row"><span class="l">{l}</span><span class="v">{v}</span></div>'
        for l, v in items
    )
    st.markdown(f'<div>{rows}</div>', unsafe_allow_html=True)


# ── Helper inline (mengembalikan string HTML) ────────────────────────────────
def badge(text: str, style: str = "neutral") -> str:
    """Badge kecil inline. style: success | neutral."""
    return f'<span class="geo-badge {style}">{text}</span>'


def info_tooltip(term: str, definition: str) -> str:
    """Teks dengan ikon info bertooltip (hover)."""
    safe_def = _html.escape(definition, quote=True)
    return (
        f'<span class="geo-tooltip-wrap">{term}&nbsp;'
        f'<span class="geo-info-icon" title="{safe_def}">i</span></span>'
    )