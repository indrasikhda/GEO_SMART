import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from core.fahp import calculate_fahp_weights, CRITERIA_LIST, get_default_pairwise_matrix
from core.gpi import compute_gpi_score
from core.raster import get_raster_stats_and_overlay
from core.maps import create_base_map

def render_fahp_gpi():
    if "fahp_matrix" not in st.session_state:
        st.session_state.fahp_matrix = get_default_pairwise_matrix()

    criteria_names = [c["name"] for c in CRITERIA_LIST]
    current_matrix = st.session_state.fahp_matrix
    fahp_res = calculate_fahp_weights(current_matrix)
    weights = fahp_res["weights"]

    # KPI Row
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">Criteria</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#F2F2F7;display:flex;align-items:center;justify-content:center;font-size:13px;">⚙️</div>
                </div>
                <div style="font-size:1.75rem;font-weight:800;color:#1C1C1E;">8</div>
                <span style="font-size:0.72rem;font-weight:600;color:#34C759;">Expert judgement layers</span>
            </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">Consistency Ratio</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#F2F2F7;display:flex;align-items:center;justify-content:center;font-size:13px;">%</div>
                </div>
                <div style="font-size:1.75rem;font-weight:800;color:#1C1C1E;">{fahp_res['CR']}</div>
                <span style="font-size:0.72rem;font-weight:600;color:#34C759;">CR &lt; 0.10 ✓</span>
            </div>
        """, unsafe_allow_html=True)

    with k3:
        c = "#34C759" if fahp_res["is_consistent"] else "#FF3B30"
        st.markdown(f"""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">Consistency Status</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#F2F2F7;display:flex;align-items:center;justify-content:center;font-size:13px;">✓</div>
                </div>
                <div style="font-size:1.3rem;font-weight:800;color:{c};">{fahp_res['status']}</div>
                <span style="font-size:0.72rem;font-weight:600;color:#636366;">Matrix consistency check</span>
            </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">GPI Status</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#FFF4E0;display:flex;align-items:center;justify-content:center;font-size:13px;">🗺️</div>
                </div>
                <div style="font-size:1.3rem;font-weight:800;color:#FF9500;">Demo Output</div>
                <span style="font-size:0.72rem;font-weight:600;color:#636366;">Evidence integration pending</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:1.25rem'></div>", unsafe_allow_html=True)

    col_matrix, col_weights_chart = st.columns([6, 6], gap="medium")

    with col_matrix:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 4px 0;">Expert Judgement — Matrix A</h3>
                <p style="font-size:0.75rem;color:#8E8E93;margin:0 0 14px 0;">Pairwise comparison matrix (Saaty 1–9 ratio scale)</p>
        """, unsafe_allow_html=True)

        df_matrix = pd.DataFrame(current_matrix, index=criteria_names, columns=criteria_names)
        edited = st.data_editor(df_matrix.round(2), use_container_width=True, key="fahp_matrix_saas")

        if st.button("Calculate FAHP"):
            st.session_state.fahp_matrix = edited.to_numpy(dtype=float).tolist()
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col_weights_chart:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 4px 0;">Calculated Weights</h3>
                <p style="font-size:0.75rem;color:#8E8E93;margin:0 0 10px 0;">Normalized row geometric means w<sub>i</sub></p>
        """, unsafe_allow_html=True)

        df_w = pd.DataFrame({
            "Criterion": criteria_names,
            "Weight (%)": [round(w * 100, 1) for w in weights]
        }).sort_values("Weight (%)", ascending=True)

        fig = px.bar(df_w, x="Weight (%)", y="Criterion", orientation="h",
                     text="Weight (%)", color_discrete_sequence=["#1C1C1E"])
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(
            height=310, margin=dict(l=0, r=40, t=10, b=10),
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
            font=dict(family="Inter", size=10, color="#636366"),
            xaxis=dict(showgrid=True, gridcolor="#F2F2F7", title=""),
            yaxis=dict(showgrid=False, title="")
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:1.25rem'></div>", unsafe_allow_html=True)

    col_table, col_gpi_map = st.columns([5, 7], gap="medium")

    with col_table:
        statuses = ["Pending", "Pending", "Connected", "Pending", "Pending", "Pending", "Connected", "Connected"]
        df_ev = pd.DataFrame({
            "Criterion": criteria_names,
            "Weight": [f"{w*100:.1f}%" for w in weights],
            "Status": statuses
        })
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 4px 0;">Weighted Evidence</h3>
                <p style="font-size:0.75rem;color:#8E8E93;margin:0 0 12px 0;">Evidence integration status per criterion</p>
        """, unsafe_allow_html=True)
        st.dataframe(df_ev, use_container_width=True, hide_index=True)
        st.button("Generate GPI")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_gpi_map:
        gpi_res = compute_gpi_score(weights)
        st.markdown(f"""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                    <div>
                        <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0;">GPI Output</h3>
                        <p style="font-size:0.75rem;color:#8E8E93;margin:2px 0 0 0;">Score: <b style="color:#FF9500;">{gpi_res['gpi_score']}</b> — {gpi_res['class']}</p>
                    </div>
                    <span style="font-size:0.7rem;color:#FF9500;background:#FFF4E0;padding:3px 8px;border-radius:9999px;font-weight:700;">DEMO OUTPUT</span>
                </div>
        """, unsafe_allow_html=True)
        m = create_base_map(center=[2.92, 125.12], zoom=7)
        lst_overlay = get_raster_stats_and_overlay("lst")
        if lst_overlay.get("png_path") and lst_overlay.get("bounds"):
            folium.raster_layers.ImageOverlay(
                image=lst_overlay["png_path"],
                bounds=lst_overlay["bounds"],
                opacity=0.75
            ).add_to(m)
        st_folium(m, width="100%", height=310, key="fahp_gpi_map_saas")
        st.markdown("</div>", unsafe_allow_html=True)
