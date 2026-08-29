import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from core.fahp import calculate_fahp_weights, CRITERIA_LIST, get_default_pairwise_matrix
from core.gpi import compute_gpi_score
from core.raster import get_raster_stats_and_overlay
from core.maps import create_base_map

def render_saaty_scale_table():
    """Render Saaty's 1-9 scale explanation"""
    st.markdown("""
        <div style="background:#F9F9FB;border-radius:12px;padding:14px;margin-bottom:14px;">
            <h4 style="font-size:0.85rem;font-weight:700;color:#1C1C1E;margin:0 0 8px 0;">📊 Saaty's Pairwise Comparison Scale</h4>
            <table style="width:100%;font-size:0.75rem;color:#636366;">
                <tr style="border-bottom:1px solid #E5E5EA;">
                    <td style="padding:4px 0;font-weight:600;">1</td>
                    <td style="padding:4px 0;">Equal importance</td>
                </tr>
                <tr style="border-bottom:1px solid #E5E5EA;">
                    <td style="padding:4px 0;font-weight:600;">3</td>
                    <td style="padding:4px 0;">Moderate importance of one over another</td>
                </tr>
                <tr style="border-bottom:1px solid #E5E5EA;">
                    <td style="padding:4px 0;font-weight:600;">5</td>
                    <td style="padding:4px 0;">Strong importance</td>
                </tr>
                <tr style="border-bottom:1px solid #E5E5EA;">
                    <td style="padding:4px 0;font-weight:600;">7</td>
                    <td style="padding:4px 0;">Very strong importance</td>
                </tr>
                <tr style="border-bottom:1px solid #E5E5EA;">
                    <td style="padding:4px 0;font-weight:600;">9</td>
                    <td style="padding:4px 0;">Extreme importance</td>
                </tr>
                <tr>
                    <td style="padding:4px 0;font-weight:600;">2,4,6,8</td>
                    <td style="padding:4px 0;">Intermediate values between adjacent scales</td>
                </tr>
            </table>
            <p style="font-size:0.7rem;color:#8E8E93;margin:8px 0 0 0;">
                <b>Note:</b> If criterion A has importance value X over criterion B, then B over A = 1/X
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_fahp_gpi():
    # Initialize session state
    if "fahp_matrix" not in st.session_state:
        st.session_state.fahp_matrix = get_default_pairwise_matrix()

    criteria_names = [c["name"] for c in CRITERIA_LIST]
    current_matrix = st.session_state.fahp_matrix
    fahp_res = calculate_fahp_weights(current_matrix)
    weights = fahp_res["weights"]

    # === PAGE HEADER ===
    st.markdown("""
        <div style="margin-bottom:1.5rem;">
            <h2 style="font-size:1.85rem;font-weight:800;color:#1C1C1E;margin:0 0 6px 0;">AHP Weighting & GPI</h2>
            <p style="font-size:0.9rem;color:#636366;margin:0;">
                Analytic Hierarchy Process for criteria weighting and Geothermal Prospectivity Index calculation
            </p>
        </div>
    """, unsafe_allow_html=True)

    # === WORKFLOW VISUAL ===
    st.markdown("""
        <div style="background:#F9F9FB;border-radius:16px;padding:18px;margin-bottom:1.5rem;">
            <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;justify-content:center;">
                <div style="text-align:center;">
                    <div style="background:#5E5CE6;color:#FFF;padding:10px 18px;border-radius:12px;font-size:0.8rem;font-weight:700;">
                        1. EXPERT INPUT
                    </div>
                    <div style="font-size:0.7rem;color:#8E8E93;margin-top:4px;">Pairwise Judgement</div>
                </div>
                <div style="font-size:1.2rem;color:#AEAEB2;">→</div>
                <div style="text-align:center;">
                    <div style="background:#007AFF;color:#FFF;padding:10px 18px;border-radius:12px;font-size:0.8rem;font-weight:700;">
                        2. AHP CALCULATION
                    </div>
                    <div style="font-size:0.7rem;color:#8E8E93;margin-top:4px;">Geometric Mean Method</div>
                </div>
                <div style="font-size:1.2rem;color:#AEAEB2;">→</div>
                <div style="text-align:center;">
                    <div style="background:#34C759;color:#FFF;padding:10px 18px;border-radius:12px;font-size:0.8rem;font-weight:700;">
                        3. CONSISTENCY CHECK
                    </div>
                    <div style="font-size:0.7rem;color:#8E8E93;margin-top:4px;">CR < 0.10</div>
                </div>
                <div style="font-size:1.2rem;color:#AEAEB2;">→</div>
                <div style="text-align:center;">
                    <div style="background:#1C1C1E;color:#FFF;padding:10px 18px;border-radius:12px;font-size:0.8rem;font-weight:700;">
                        4. CALCULATED WEIGHTS
                    </div>
                    <div style="font-size:0.7rem;color:#8E8E93;margin-top:4px;">System Output</div>
                </div>
                <div style="font-size:1.2rem;color:#AEAEB2;">→</div>
                <div style="text-align:center;">
                    <div style="background:#FF9500;color:#FFF;padding:10px 18px;border-radius:12px;font-size:0.8rem;font-weight:700;">
                        5. GPI
                    </div>
                    <div style="font-size:0.7rem;color:#8E8E93;margin-top:4px;">Σ(wᵢ × Sᵢ)</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # === KPI ROW ===
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">Criteria</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#F2F2F7;display:flex;align-items:center;justify-content:center;font-size:13px;">⚙️</div>
                </div>
                <div style="font-size:1.75rem;font-weight:800;color:#1C1C1E;">8</div>
                <span style="font-size:0.72rem;font-weight:600;color:#636366;">Geothermal prospectivity criteria</span>
            </div>
        """, unsafe_allow_html=True)

    with k2:
        c_cr = "#34C759" if fahp_res["is_consistent"] else "#FF3B30"
        st.markdown(f"""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">Consistency Ratio</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#F2F2F7;display:flex;align-items:center;justify-content:center;font-size:13px;">✓</div>
                </div>
                <div style="font-size:1.75rem;font-weight:800;color:{c_cr};">{fahp_res['CR']}</div>
                <span style="font-size:0.72rem;font-weight:600;color:{c_cr};">{fahp_res['status']}</span>
            </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">λ<sub>max</sub></span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#F2F2F7;display:flex;align-items:center;justify-content:center;font-size:13px;">λ</div>
                </div>
                <div style="font-size:1.75rem;font-weight:800;color:#1C1C1E;">{fahp_res['lambda_max']}</div>
                <span style="font-size:0.72rem;font-weight:600;color:#636366;">Principal eigenvalue</span>
            </div>
        """, unsafe_allow_html=True)

    with k4:
        connected_count = 3  # LST, NDVI, Manifestation
        total_count = 8
        st.markdown(f"""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <span style="font-size:0.85rem;font-weight:600;color:#636366;">Evidence Status</span>
                    <div style="width:26px;height:26px;border-radius:9999px;background:#FFF4E0;display:flex;align-items:center;justify-content:center;font-size:13px;">🗺️</div>
                </div>
                <div style="font-size:1.75rem;font-weight:800;color:#FF9500;">{connected_count}/{total_count}</div>
                <span style="font-size:0.72rem;font-weight:600;color:#636366;">Layers connected</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:1.5rem'></div>", unsafe_allow_html=True)

    # === STEP 1-2: EXPERT JUDGEMENT & PAIRWISE COMPARISON ===
    st.markdown("""
        <div style="background:#5E5CE6;color:#FFF;padding:8px 14px;border-radius:10px;display:inline-block;font-size:0.8rem;font-weight:700;margin-bottom:10px;">
            STEP 1-2: EXPERT JUDGEMENT — PAIRWISE COMPARISON <span style="background:#FFFFFF30;padding:2px 8px;border-radius:6px;margin-left:6px;">INPUT</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <p style="font-size:0.85rem;color:#636366;margin:0 0 16px 0;">
            Expert judgement provides the relative importance between geothermal prospectivity criteria using 
            <b>Saaty's 1-9 scale</b>. These pairwise assessments are the <b>INPUT</b> for the AHP calculation process.
        </p>
    """, unsafe_allow_html=True)

    col_saaty, col_matrix = st.columns([4, 8], gap="medium")
    
    with col_saaty:
        render_saaty_scale_table()
        
    with col_matrix:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 4px 0;">Pairwise Comparison Matrix</h3>
                <p style="font-size:0.75rem;color:#8E8E93;margin:0 0 14px 0;">
                    Matrix <b>A</b> — Edit cells to reflect expert judgement. Initial matrix: equal importance (all values = 1).
                </p>
        """, unsafe_allow_html=True)

        df_matrix = pd.DataFrame(current_matrix, index=criteria_names, columns=criteria_names)
        edited = st.data_editor(df_matrix, use_container_width=True, key="fahp_matrix_editor", height=320)

        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("🔄 Reset to Equal Importance", use_container_width=True):
                st.session_state.fahp_matrix = get_default_pairwise_matrix()
                st.rerun()
        with col_btn2:
            if st.button("⚡ Calculate AHP Weights", type="primary", use_container_width=True):
                st.session_state.fahp_matrix = edited.to_numpy(dtype=float).tolist()
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:1.5rem'></div>", unsafe_allow_html=True)

    # === STEP 3-4: CALCULATION & CONSISTENCY ===
    st.markdown("""
        <div style="background:#007AFF;color:#FFF;padding:8px 14px;border-radius:10px;display:inline-block;font-size:0.8rem;font-weight:700;margin-bottom:10px;">
            STEP 3-4: AHP CALCULATION & CONSISTENCY CHECK <span style="background:#FFFFFF30;padding:2px 8px;border-radius:6px;margin-left:6px;">PROCESS</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <p style="font-size:0.85rem;color:#636366;margin:0 0 16px 0;">
            System calculates normalized weights using <b>Row Geometric Mean Method</b> and checks consistency.
            <b>Consistency Ratio (CR)</b> measures the consistency of expert judgements. 
            CR &lt; 0.10 indicates acceptable consistency.
        </p>
    """, unsafe_allow_html=True)

    col_consistency, col_formula = st.columns([5, 7], gap="medium")
    
    with col_consistency:
        st.markdown(f"""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 12px 0;">Consistency Metrics</h3>
                <div style="margin-bottom:12px;">
                    <div style="font-size:0.75rem;color:#8E8E93;">Principal Eigenvalue (λ<sub>max</sub>)</div>
                    <div style="font-size:1.4rem;font-weight:800;color:#1C1C1E;">{fahp_res['lambda_max']}</div>
                </div>
                <div style="margin-bottom:12px;">
                    <div style="font-size:0.75rem;color:#8E8E93;">Consistency Index (CI)</div>
                    <div style="font-size:1.4rem;font-weight:800;color:#1C1C1E;">{fahp_res['CI']}</div>
                </div>
                <div style="margin-bottom:12px;">
                    <div style="font-size:0.75rem;color:#8E8E93;">Consistency Ratio (CR)</div>
                    <div style="font-size:1.4rem;font-weight:800;color:{'#34C759' if fahp_res['is_consistent'] else '#FF3B30'};">{fahp_res['CR']}</div>
                </div>
                <div style="background:{'#E8FAF0' if fahp_res['is_consistent'] else '#FFE5E5'};border-radius:10px;padding:10px;margin-top:12px;">
                    <div style="font-size:0.8rem;font-weight:700;color:{'#34C759' if fahp_res['is_consistent'] else '#FF3B30'};">
                        {'✓ Acceptable Consistency' if fahp_res['is_consistent'] else '⚠ Inconsistent Matrix'}
                    </div>
                    <div style="font-size:0.7rem;color:#636366;margin-top:4px;">
                        {f'CR = {fahp_res["CR"]} < 0.10' if fahp_res['is_consistent'] else f'CR = {fahp_res["CR"]} ≥ 0.10 — Please review pairwise comparisons'}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_formula:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 12px 0;">Calculation Methodology</h3>
                <div style="background:#F9F9FB;border-radius:10px;padding:12px;margin-bottom:10px;">
                    <div style="font-size:0.75rem;font-weight:700;color:#1C1C1E;margin-bottom:6px;">1. Row Geometric Mean</div>
                    <div style="font-family:monospace;font-size:0.8rem;color:#636366;">
                        w'ᵢ = (∏ⱼ aᵢⱼ)^(1/n)
                    </div>
                </div>
                <div style="background:#F9F9FB;border-radius:10px;padding:12px;margin-bottom:10px;">
                    <div style="font-size:0.75rem;font-weight:700;color:#1C1C1E;margin-bottom:6px;">2. Normalization</div>
                    <div style="font-family:monospace;font-size:0.8rem;color:#636366;">
                        wᵢ = w'ᵢ / Σw'ᵢ
                    </div>
                </div>
                <div style="background:#F9F9FB;border-radius:10px;padding:12px;margin-bottom:10px;">
                    <div style="font-size:0.75rem;font-weight:700;color:#1C1C1E;margin-bottom:6px;">3. Consistency Index</div>
                    <div style="font-family:monospace;font-size:0.8rem;color:#636366;">
                        CI = (λ<sub>max</sub> - n) / (n - 1)
                    </div>
                </div>
                <div style="background:#F9F9FB;border-radius:10px;padding:12px;">
                    <div style="font-size:0.75rem;font-weight:700;color:#1C1C1E;margin-bottom:6px;">4. Consistency Ratio</div>
                    <div style="font-family:monospace;font-size:0.8rem;color:#636366;">
                        CR = CI / RI
                    </div>
                    <div style="font-size:0.7rem;color:#8E8E93;margin-top:4px;">
                        where RI (Random Index) = 1.41 for n=8
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:1.5rem'></div>", unsafe_allow_html=True)

    # === STEP 5: CALCULATED WEIGHTS ===
    st.markdown("""
        <div style="background:#1C1C1E;color:#FFF;padding:8px 14px;border-radius:10px;display:inline-block;font-size:0.8rem;font-weight:700;margin-bottom:10px;">
            STEP 5: CALCULATED CRITERIA WEIGHTS <span style="background:#FFFFFF30;padding:2px 8px;border-radius:6px;margin-left:6px;">OUTPUT</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <p style="font-size:0.85rem;color:#636366;margin:0 0 16px 0;">
            Normalized weights are <b>CALCULATED OUTPUT</b> generated by the system from the pairwise comparison matrix.
            These weights represent the relative importance of each criterion for geothermal prospectivity assessment.
        </p>
    """, unsafe_allow_html=True)

    col_weights_table, col_weights_chart = st.columns([5, 7], gap="medium")

    with col_weights_table:
        statuses = ["⚪ Pending", "⚪ Pending", "🟢 Connected", "⚪ Pending", "🟢 Connected", "🟢 Connected", "⚪ Pending", "⚪ Pending"]
        df_weights = pd.DataFrame({
            "Criterion": criteria_names,
            "Weight": [f"{w*100:.2f}%" for w in weights],
            "Evidence Status": statuses
        })
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 4px 0;">Criteria Weights & Evidence</h3>
                <p style="font-size:0.75rem;color:#8E8E93;margin:0 0 12px 0;">Normalized weights (Σw = 1.0) and data integration status</p>
        """, unsafe_allow_html=True)
        st.dataframe(df_weights, use_container_width=True, hide_index=True, height=320)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_weights_chart:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 4px 0;">Weight Distribution</h3>
                <p style="font-size:0.75rem;color:#8E8E93;margin:0 0 10px 0;">Relative importance of prospectivity criteria</p>
        """, unsafe_allow_html=True)

        df_w = pd.DataFrame({
            "Criterion": criteria_names,
            "Weight (%)": [round(w * 100, 2) for w in weights]
        }).sort_values("Weight (%)", ascending=True)

        fig = px.bar(df_w, x="Weight (%)", y="Criterion", orientation="h",
                     text="Weight (%)", color_discrete_sequence=["#1C1C1E"])
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_layout(
            height=320, margin=dict(l=0, r=50, t=10, b=10),
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
            font=dict(family="Inter", size=10, color="#636366"),
            xaxis=dict(showgrid=True, gridcolor="#F2F2F7", title="", range=[0, max([w*100 for w in weights])*1.2]),
            yaxis=dict(showgrid=False, title="")
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:1.5rem'></div>", unsafe_allow_html=True)

    # === STEP 6: GPI ===
    st.markdown("""
        <div style="background:#FF9500;color:#FFF;padding:8px 14px;border-radius:10px;display:inline-block;font-size:0.8rem;font-weight:700;margin-bottom:10px;">
            STEP 6: GEOTHERMAL PROSPECTIVITY INDEX (GPI) <span style="background:#FFFFFF30;padding:2px 8px;border-radius:6px;margin-left:6px;">🟡 DEMO</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <p style="font-size:0.85rem;color:#636366;margin:0 0 16px 0;">
            GPI combines <b>calculated weights</b> with <b>standardized evidence layers</b> using weighted overlay.
            Current GPI demonstrates the calculation workflow. Full spatial GPI requires complete geological dataset integration.
        </p>
    """, unsafe_allow_html=True)

    col_gpi_info, col_gpi_map = st.columns([5, 7], gap="medium")

    with col_gpi_info:
        gpi_res = compute_gpi_score(weights)
        st.markdown(f"""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 12px 0;">GPI Calculation</h3>
                
                <div style="background:#FFF4E0;border-radius:10px;padding:12px;margin-bottom:14px;">
                    <div style="font-size:0.75rem;font-weight:700;color:#FF9500;margin-bottom:4px;">⚠️ DEMO OUTPUT</div>
                    <div style="font-size:0.7rem;color:#636366;">
                        Current GPI uses placeholder evidence scores for 5 pending geological layers.
                        Full spatial overlay pending complete dataset integration.
                    </div>
                </div>
                
                <div style="background:#F9F9FB;border-radius:10px;padding:14px;margin-bottom:14px;">
                    <div style="font-size:0.75rem;font-weight:700;color:#1C1C1E;margin-bottom:8px;">Formula:</div>
                    <div style="font-family:monospace;font-size:0.9rem;color:#1C1C1E;margin-bottom:10px;">
                        GPI(x,y) = Σ [wᵢ × Sᵢ(x,y)]
                    </div>
                    <div style="font-size:0.7rem;color:#636366;">
                        where:<br>
                        • wᵢ = AHP-calculated weight<br>
                        • Sᵢ(x,y) = standardized evidence score (0-1)<br>
                        • Σ = weighted sum across 8 criteria
                    </div>
                </div>
                
                <div style="background:#E8FAF0;border-radius:10px;padding:14px;">
                    <div style="font-size:0.75rem;color:#8E8E93;margin-bottom:4px;">Demo GPI Score</div>
                    <div style="font-size:2rem;font-weight:800;color:#34C759;">{gpi_res['gpi_score']}</div>
                    <div style="font-size:0.8rem;font-weight:700;color:#34C759;margin-top:4px;">{gpi_res['class']}</div>
                    <div style="font-size:0.7rem;color:#636366;margin-top:8px;">
                        <b>Evidence Contribution:</b><br>
                        • 3/8 layers connected (LST, NDVI, Manifestation)<br>
                        • 5/8 layers pending geological data
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_gpi_map:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:0 0 4px 0;">Prospectivity Map Preview</h3>
                <p style="font-size:0.75rem;color:#8E8E93;margin:0 0 12px 0;">LST overlay (one of 3 connected evidence layers)</p>
        """, unsafe_allow_html=True)
        
        m = create_base_map(center=[1.32, 124.84], zoom=10)
        lst_overlay = get_raster_stats_and_overlay("lst")
        if lst_overlay.get("png_path") and lst_overlay.get("bounds"):
            folium.raster_layers.ImageOverlay(
                image=lst_overlay["png_path"],
                bounds=lst_overlay["bounds"],
                opacity=0.7
            ).add_to(m)
        
        st_folium(m, width="100%", height=380, key="fahp_gpi_map")
        st.markdown("</div>", unsafe_allow_html=True)

