import streamlit as st
import pandas as pd
import plotly.express as px
import folium

from streamlit_folium import st_folium

from core.fahp import (
    calculate_fahp_weights,
    CRITERIA_LIST,
    get_default_pairwise_matrix,
)

from core.raster import get_raster_stats_and_overlay
from core.maps import create_base_map


# ============================================================
# LITERATURE SUBCRITERIA
# Based on the literature-informed framework
# ============================================================

SUBCRITERIA = {
    "manifestation": [
        ("0–2500 m", 0.486),
        ("2500–5000 m", 0.328),
        ("5000–10000 m", 0.130),
        (">10000 m", 0.056),
    ],

    "geology": [
        ("Indicator areas", 0.800),
        ("Other", 0.200),
    ],

    "alteration": [
        ("Indicator areas", 0.800),
        ("Other", 0.200),
    ],

    "lineament": [
        ("0–1000 m", 0.486),
        ("1000–2500 m", 0.328),
        ("2500–5000 m", 0.130),
        (">5000 m", 0.056),
    ],

    "lst": [
        ("45.1–55.04 °C", 0.486),
        ("40.1–45 °C", 0.328),
        ("30.1–40 °C", 0.130),
        ("−0.23–30 °C", 0.056),
    ],
}


# ============================================================
# HELPER
# ============================================================

def format_fuzzy(value):
    """
    Format a Triangular Fuzzy Number for dashboard display.
    """

    if isinstance(value, (tuple, list)) and len(value) == 3:
        return (
            f"({value[0]:.3g}, "
            f"{value[1]:.3g}, "
            f"{value[2]:.3g})"
        )

    return str(value)


# ============================================================
# MAIN VIEW
# ============================================================

def render_fahp_gpi():

    # ========================================================
    # INITIALIZE FAHP MATRIX
    # ========================================================

    if "fahp_matrix" not in st.session_state:
        st.session_state.fahp_matrix = (
            get_default_pairwise_matrix()
        )

    current_matrix = st.session_state.fahp_matrix

    # ========================================================
    # FAHP CALCULATION
    # ========================================================

    fahp_res = calculate_fahp_weights(
        current_matrix
    )

    weights = fahp_res["weights"]

    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        '<div class="data-card-header">'
        'FAHP Engine Status'
        '</div>',
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.metric(
            "Criteria",
            "5",
            "Current model",
        )

    with k2:
        st.metric(
            "Method",
            "Fuzzy-AHP",
            "Preliminary",
        )

    with k3:
        st.metric(
            "CR",
            f"{fahp_res['CR']:.3f}",
            (
                "Acceptable"
                if fahp_res["is_consistent"]
                else "Review"
            ),
        )

    with k4:
        st.metric(
            "Weight Sum",
            f"{sum(weights):.3f}",
            "Normalized",
        )

    with k5:
        st.metric(
            "Source",
            "Şener 2021",
            "Literature",
        )

    st.write("")

    # ========================================================
    # LITERATURE NOTICE
    # ========================================================

    st.info(
        "Preliminary criterion weights are "
        "literature-informed based on Şener & Şener (2021). "
        "The literature-derived framework is transferred "
        "as an initial reference for the Sulawesi Utara prototype. "
        "Local expert validation is required before "
        "field application."
    )

    # ========================================================
    # MATRIX + WEIGHTS
    # ========================================================

    col_matrix, col_weights = st.columns(
        [6, 6],
        gap="large",
    )

    # ========================================================
    # FUZZY PAIRWISE MATRIX
    # ========================================================

    with col_matrix:

        st.markdown(
            '<div class="data-card-header">'
            'Fuzzy Pairwise Comparison'
            '</div>',
            unsafe_allow_html=True,
        )

        criteria_names = [
            criterion["name"]
            for criterion in CRITERIA_LIST
        ]

        display_matrix = []

        for row in current_matrix:

            display_row = []

            for value in row:
                display_row.append(
                    format_fuzzy(value)
                )

            display_matrix.append(
                display_row
            )

        df_matrix = pd.DataFrame(
            display_matrix,
            index=criteria_names,
            columns=criteria_names,
        )

        st.dataframe(
            df_matrix,
            use_container_width=True,
            height=260,
        )

        st.caption(
            "Literature-informed fuzzy comparison matrix. "
            "Values are represented as Triangular Fuzzy "
            "Numbers (lower, modal, upper)."
        )

        if st.button(
            "Reset to Literature Matrix",
            use_container_width=True,
        ):

            st.session_state.fahp_matrix = (
                get_default_pairwise_matrix()
            )

            st.rerun()

        # ====================================================
        # FUZZY SCALE
        # ====================================================

        with st.expander(
            "Fuzzy Comparison Reference",
            expanded=False,
        ):

            st.markdown(
                """
                **Triangular Fuzzy Number (TFN)**

                A fuzzy comparison is represented as:

                **(lower, modal, upper)**

                Example:

                **(3, 4, 6)**

                represents a range of relative importance
                rather than a single crisp value.

                The current matrix is used as a
                literature-informed preliminary model.
                """
            )

    # ========================================================
    # CALCULATED WEIGHTS
    # ========================================================

    with col_weights:

        st.markdown(
            '<div class="data-card-header">'
            'Calculated Criterion Weights'
            '</div>',
            unsafe_allow_html=True,
        )

        df_weights = pd.DataFrame(
            {
                "Criterion": [
                    criterion["name"]
                    for criterion in CRITERIA_LIST
                ],
                "Weight": [
                    weight * 100
                    for weight in weights
                ],
            }
        )

        df_weights = df_weights.sort_values(
            "Weight",
            ascending=True,
        )

        fig = px.bar(
            df_weights,
            x="Weight",
            y="Criterion",
            orientation="h",
            text=df_weights["Weight"].apply(
                lambda x: f"{x:.1f}%"
            ),
            color="Weight",
            color_continuous_scale=[
                "#CFFAFE",
                "#0891B2",
                "#0E7490",
            ],
            height=300,
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            showlegend=False,
            margin=dict(
                l=0,
                r=60,
                t=10,
                b=10,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="Inter",
                size=11,
                color="#475569",
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor="#E2E8F0",
                title="",
                range=[
                    0,
                    max(df_weights["Weight"]) * 1.15,
                ],
            ),
            yaxis=dict(
                showgrid=False,
                title="",
            ),
            coloraxis_showscale=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        df_display = pd.DataFrame(
            {
                "Criterion": [
                    criterion["name"]
                    for criterion in CRITERIA_LIST
                ],
                "Weight": [
                    f"{weight * 100:.2f}%"
                    for weight in weights
                ],
                "Role": [
                    criterion["role"]
                    for criterion in CRITERIA_LIST
                ],
            }
        )

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            height=200,
        )

    # ========================================================
    # SUBCRITERIA
    # ========================================================

    st.write("")
    st.divider()

    st.markdown(
        '<div class="data-card-header">'
        'Literature-Based Subcriteria'
        '</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Subcriteria shown here represent the "
        "literature-informed preliminary framework."
    )

    sub_cols = st.columns(5)

    for index, criterion in enumerate(CRITERIA_LIST):

        criterion_id = criterion["id"]

        with sub_cols[index]:

            st.markdown(
                f"**{criterion['name']}**"
            )

            rows = []

            for label, sub_weight in SUBCRITERIA.get(
                criterion_id,
                [],
            ):

                rows.append(
                    {
                        "Subcriteria": label,
                        "Weight": f"{sub_weight:.3f}",
                    }
                )

            if rows:

                st.dataframe(
                    pd.DataFrame(rows),
                    use_container_width=True,
                    hide_index=True,
                    height=190,
                )

            else:

                st.caption(
                    "No subcriteria configured."
                )

    # ========================================================
    # GPI SECTION
    # ========================================================

    st.write("")
    st.divider()

    st.markdown(
        '<div class="data-card-header">'
        'Geothermal Prospectivity Index (GPI)'
        '</div>',
        unsafe_allow_html=True,
    )

    col_gpi_info, col_gpi_map = st.columns(
        [5, 7],
        gap="large",
    )

    # ========================================================
    # GPI STATUS
    # ========================================================

    with col_gpi_info:

        # IMPORTANT:
        # Use Streamlit native components here instead
        # of raw HTML to avoid displaying HTML as text.

        st.markdown("#### GPI Status")

        st.metric(
            label="Current Model Status",
            value="PRELIMINARY",
        )

        st.warning(
            "Incomplete evidence integration"
        )

        st.caption(
            "A final spatial GPI should only be generated "
            "after the required evidence layers have been "
            "standardized and integrated."
        )

        # ====================================================
        # FORMULA
        # ====================================================

        st.markdown("#### Weighted Overlay Formula")

        st.latex(
            r"""
            GPI(x,y) = \sum_i w_i S_i(x,y)
            """
        )

        st.markdown(
            """
            **wᵢ** = FAHP criterion weight

            **Sᵢ(x,y)** = standardized spatial evidence

            **Σ** = weighted combination of evidence layers
            """
        )

        # ====================================================
        # EVIDENCE STATUS
        # ====================================================

        st.markdown("#### Evidence Integration Status")

        evidence_status = pd.DataFrame(
            {
                "Evidence": [
                    "LST",
                    "NDVI",
                    "Manifestation",
                    "Geology / Lithology",
                    "Hydrothermal Alteration",
                    "Fault & Lineament",
                ],
                "Status": [
                    "CONNECTED",
                    "CONNECTED",
                    "CONNECTED",
                    "CONNECTED",
                    "PENDING",
                    "CONNECTED",
                ],
            }
        )

        st.dataframe(
            evidence_status,
            use_container_width=True,
            hide_index=True,
        )

        # ====================================================
        # TECHNICAL DETAILS
        # ====================================================

        with st.expander(
            "Technical Details",
            expanded=False,
        ):

            st.markdown(
                f"""
                **FAHP**

                - Method: Literature-informed Fuzzy-AHP
                - Criteria: 5
                - Source: Şener & Şener (2021)

                **Consistency Diagnostic**

                - λ max: {fahp_res["lambda_max"]:.4f}
                - CI: {fahp_res["CI"]:.4f}
                - CR: {fahp_res["CR"]:.4f}

                **GPI**

                The conceptual GPI follows a weighted
                spatial overlay:

                GPI(x,y) = Σ [wᵢ × Sᵢ(x,y)]

                A complete spatial GPI requires all required
                evidence layers to be available and
                standardized.

                **Current Status**

                Preliminary — Evidence Integration in Progress

                **Target Region**

                Sulawesi Utara, Indonesia
                """
            )

    # ========================================================
    # SPATIAL REFERENCE
    # ========================================================

    with col_gpi_map:

        st.markdown(
            "#### Spatial Evidence Reference"
        )

        m = create_base_map(
            center=[
                1.35,
                124.85,
            ],
            zoom=8,
        )

        # ====================================================
        # REAL LST OVERLAY
        # ====================================================

        lst_overlay = (
            get_raster_stats_and_overlay("lst")
        )

        if (
            lst_overlay.get("png_path")
            and lst_overlay.get("bounds")
        ):

            folium.raster_layers.ImageOverlay(
                image=lst_overlay["png_path"],
                bounds=lst_overlay["bounds"],
                opacity=0.65,
                name="LST Thermal",
            ).add_to(m)

        folium.LayerControl().add_to(m)

        st_folium(
            m,
            width="100%",
            height=420,
            key="gpi_reference_map",
        )

        if lst_overlay.get("min") is not None:
            st.markdown(f"""
                <div style="padding:0.5rem 0.75rem;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:6px;margin-top:0.4rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.2rem;">
                        <span style="font-size:0.72rem;font-weight:700;color:#0F172A;">🌡️ LST Thermal Reference</span>
                        <span style="font-size:0.68rem;font-weight:700;color:#DC2626;">Hotspot</span>
                    </div>
                    <div style="height:8px;border-radius:4px;background:linear-gradient(90deg, #0369A1 0%, #38BDF8 35%, #FEF08A 55%, #F59E0B 75%, #DC2626 90%, #7F1D1D 100%);"></div>
                    <div style="display:flex;justify-content:space-between;font-size:0.65rem;color:#64748B;font-weight:600;margin-top:0.2rem;">
                        <span>{lst_overlay['min']:.1f}°C (Cool)</span>
                        <span>Mean: {lst_overlay['mean']:.1f}°C</span>
                        <span style="color:#991B1B;">{lst_overlay['max']:.1f}°C (Thermal Peak)</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.caption(
            "LST overlay — real raster evidence. "
            "The map currently serves as spatial reference; "
            "full GPI spatial overlay remains preliminary "
            "until the required evidence layers are integrated."
        )