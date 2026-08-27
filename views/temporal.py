import streamlit as st
import plotly.express as px
import pandas as pd

def render_temporal():
    col_sel, _ = st.columns([4, 8])
    with col_sel:
        date_range = st.date_input(
            "Select Date Range",
            value=[pd.to_datetime("2025-01-01"), pd.to_datetime("2025-12-31")]
        )

    st.markdown("<div style='margin-bottom:1.25rem'></div>", unsafe_allow_html=True)

    dates = pd.date_range("2025-01-01", periods=12, freq="MS")
    df = pd.DataFrame({
        "Month": dates.strftime("%b %Y"),
        "LST Mean (°C)": [28.5, 28.7, 29.1, 29.4, 29.8, 30.2, 30.8, 31.2, 30.5, 29.9, 29.2, 28.8],
        "NDVI Mean": [0.82, 0.82, 0.81, 0.81, 0.80, 0.79, 0.78, 0.78, 0.79, 0.80, 0.81, 0.82],
        "GMN Temperature": [66.2, 66.8, 67.4, 68.0, 68.4, 69.1, 70.2, 71.0, 69.8, 68.6, 67.9, 67.1],
        "GMN pH": [3.32, 3.30, 3.28, 3.26, 3.25, 3.21, 3.18, 3.15, 3.20, 3.24, 3.27, 3.31],
    })

    c1, c2 = st.columns(2, gap="medium")
    for col, y_col, color, title in [
        (c1, "LST Mean (°C)", "#FF9500", "LST Trend (Landsat 8/9)"),
        (c2, "NDVI Mean", "#34C759", "NDVI Trend (Sentinel-2)"),
    ]:
        with col:
            fig = px.line(df, x="Month", y=y_col, title=title, color_discrete_sequence=[color])
            fig.update_traces(line_width=2.5)
            fig.update_layout(height=220, margin=dict(l=10, r=10, t=34, b=10),
                paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
                font=dict(family="Inter", size=10, color="#636366"),
                title_font=dict(size=13, color="#1C1C1E", family="Inter"),
                xaxis=dict(showgrid=False, title=""), yaxis=dict(showgrid=True, gridcolor="#F2F2F7", title=""))
            st.markdown("""<div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:14px;box-shadow:0 2px 10px rgba(0,0,0,0.02);margin-bottom:1rem;">""", unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2, gap="medium")
    for col, y_col, color, title in [
        (c3, "GMN Temperature", "#FF3B30", "GMN Core Temperature Trend"),
        (c4, "GMN pH", "#1C1C1E", "GMN pH Shift Trend"),
    ]:
        with col:
            fig = px.line(df, x="Month", y=y_col, title=title, color_discrete_sequence=[color])
            fig.update_traces(line_width=2.5)
            fig.update_layout(height=220, margin=dict(l=10, r=10, t=34, b=10),
                paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
                font=dict(family="Inter", size=10, color="#636366"),
                title_font=dict(size=13, color="#1C1C1E", family="Inter"),
                xaxis=dict(showgrid=False, title=""), yaxis=dict(showgrid=True, gridcolor="#F2F2F7", title=""))
            st.markdown("""<div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:14px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">""", unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
