import streamlit as st
from core.data import METHODS_STEPS

def render_methods():
    # Workflow Pipeline Visualization
    st.markdown('<div class="data-card-header">Decision Pipeline</div>', unsafe_allow_html=True)
    
    # Workflow steps as horizontal flow
    st.markdown("""
        <div style="display:flex;overflow-x:auto;gap:1rem;padding:1.5rem 0;margin-bottom:2rem;">
            <div style="min-width:140px;text-align:center;">
                <div style="width:48px;height:48px;margin:0 auto 0.5rem;background:#0891B2;border-radius:10px;display:flex;align-items:center;justify-content:center;">
                    <span style="font-size:1.25rem;color:#FFF;">1</span>
                </div>
                <div style="font-size:0.8rem;font-weight:700;color:#0F172A;">Remote Sensing</div>
                <div style="font-size:0.7rem;color:#64748B;">LST + NDVI</div>
            </div>
            <div style="display:flex;align-items:center;color:#CBD5E1;font-size:1.5rem;">→</div>
            <div style="min-width:140px;text-align:center;">
                <div style="width:48px;height:48px;margin:0 auto 0.5rem;background:#0891B2;border-radius:10px;display:flex;align-items:center;justify-content:center;">
                    <span style="font-size:1.25rem;color:#FFF;">2</span>
                </div>
                <div style="font-size:0.8rem;font-weight:700;color:#0F172A;">Evidence Layers</div>
                <div style="font-size:0.7rem;color:#64748B;">Multi-Source</div>
            </div>
            <div style="display:flex;align-items:center;color:#CBD5E1;font-size:1.5rem;">→</div>
            <div style="min-width:140px;text-align:center;">
                <div style="width:48px;height:48px;margin:0 auto 0.5rem;background:#0891B2;border-radius:10px;display:flex;align-items:center;justify-content:center;">
                    <span style="font-size:1.25rem;color:#FFF;">3</span>
                </div>
                <div style="font-size:0.8rem;font-weight:700;color:#0F172A;">AHP Weighting</div>
                <div style="font-size:0.7rem;color:#64748B;">Criteria Priority</div>
            </div>
            <div style="display:flex;align-items:center;color:#CBD5E1;font-size:1.5rem;">→</div>
            <div style="min-width:140px;text-align:center;">
                <div style="width:48px;height:48px;margin:0 auto 0.5rem;background:#0891B2;border-radius:10px;display:flex;align-items:center;justify-content:center;">
                    <span style="font-size:1.25rem;color:#FFF;">4</span>
                </div>
                <div style="font-size:0.8rem;font-weight:700;color:#0F172A;">GPI Calculation</div>
                <div style="font-size:0.7rem;color:#64748B;">Weighted Overlay</div>
            </div>
            <div style="display:flex;align-items:center;color:#CBD5E1;font-size:1.5rem;">→</div>
            <div style="min-width:140px;text-align:center;">
                <div style="width:48px;height:48px;margin:0 auto 0.5rem;background:#0891B2;border-radius:10px;display:flex;align-items:center;justify-content:center;">
                    <span style="font-size:1.25rem;color:#FFF;">5</span>
                </div>
                <div style="font-size:0.8rem;font-weight:700;color:#0F172A;">Priority Zones</div>
                <div style="font-size:0.7rem;color:#64748B;">Target Areas</div>
            </div>
            <div style="display:flex;align-items:center;color:#CBD5E1;font-size:1.5rem;">→</div>
            <div style="min-width:140px;text-align:center;">
                <div style="width:48px;height:48px;margin:0 auto 0.5rem;background:#0891B2;border-radius:10px;display:flex;align-items:center;justify-content:center;">
                    <span style="font-size:1.25rem;color:#FFF;">6</span>
                </div>
                <div style="font-size:0.8rem;font-weight:700;color:#0F172A;">GMN Monitoring</div>
                <div style="font-size:0.7rem;color:#64748B;">Field Network</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Development Stage Comparison
    col_stage1, col_stage2 = st.columns(2, gap="large")
    
    with col_stage1:
        st.markdown("""
            <div class="data-card">
                <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1rem;">
                    <span class="status-badge badge-warning">CURRENT</span>
                    <div style="font-size:1rem;font-weight:800;color:#0F172A;">Prototype Stage</div>
                </div>
                <div style="font-size:0.85rem;color:#475569;line-height:1.6;">
                    Literature-informed baseline using published benchmarks (Şener & Şener, 2021) for volcanic geothermal systems. 
                    Real satellite data integrated. Geological layers pending.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_stage2:
        st.markdown("""
            <div class="data-card">
                <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1rem;">
                    <span class="status-badge badge-info">PLANNED</span>
                    <div style="font-size:1rem;font-weight:800;color:#0F172A;">Field Validation</div>
                </div>
                <div style="font-size:0.85rem;color:#475569;line-height:1.6;">
                    Expert consensus panels to calibrate pairwise matrices, refine scoring functions, and validate 
                    targets through ground truth surveys and drilling verification.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    # Net Zero Impact
    st.markdown("""
        <div class="data-card" style="background:linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);border-color:#A7F3D0;">
            <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1rem;">
                <div style="width:40px;height:40px;background:#059669;border-radius:10px;display:flex;align-items:center;justify-content:center;">
                    <span style="font-size:1.5rem;">⚡</span>
                </div>
                <div>
                    <div style="font-size:1.1rem;font-weight:800;color:#065F46;">Net Zero Contribution</div>
                    <div style="font-size:0.75rem;color:#047857;">Clean Energy Acceleration Pathway</div>
                </div>
            </div>
            <div style="font-size:0.85rem;color:#065F46;line-height:1.7;">
                <b>Precision Targeting</b> → Lower Exploration Risk → Reduced Non-Productive Drilling → 
                <b>Minimized Surface Footprint</b> → Accelerated Clean Geothermal Deployment → 
                <b>Indonesia Net Zero 2060</b>
            </div>
            <div style="margin-top:1rem;padding-top:1rem;border-top:1px solid #A7F3D0;font-size:0.8rem;color:#047857;">
                Geothermal provides 24/7 firm zero-carbon baseload energy. By reducing blind exploration wells, 
                GEO-SMART directly lowers project lifecycle carbon emissions.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Detailed Methodology - Collapsed by default
    with st.expander("Detailed Methodology Steps", expanded=False):
        if METHODS_STEPS:
            for step in METHODS_STEPS:
                st.markdown(f"""
                    **{step.get('step', '')}. {step.get('title', '')}**
                    
                    {step.get('desc', '')}
                """)
                if step != METHODS_STEPS[-1]:
                    st.write("")
        else:
            st.markdown("""
                1. **Remote Sensing** - LST and NDVI raster acquisition from Landsat/Sentinel
                2. **Evidence Integration** - Multi-source spatial layer compilation
                3. **Expert Judgement** - Pairwise comparison matrix input
                4. **AHP Calculation** - Row geometric mean weighting
                5. **Evidence Standardization** - 0-1 normalization
                6. **GPI Calculation** - Weighted overlay Σ(wi × Si)
                7. **Priority Zoning** - GPI + constraints analysis
                8. **GMN Design** - Monitoring network placement
                9. **IoT Architecture** - Sensor and telemetry design
                10. **Temporal Monitoring** - Time series analysis
                11. **Decision Support** - Sustainable development guidance
            """)
    
    # Disclaimer
    st.markdown("""
        <div style="margin-top:2rem;padding:1rem;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;font-size:0.8rem;color:#64748B;">
            <b style="color:#475569;">System Note:</b> GEO-SMART is a decision-support system. Outputs support exploration prioritization 
            and do not replace geological, geophysical, geochemical, environmental, or field validation requirements.
        </div>
    """, unsafe_allow_html=True)
