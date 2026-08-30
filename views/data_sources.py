import streamlit as st
import pandas as pd
from core.data import DATA_SOURCES_INVENTORY

def render_data_sources():
    # Data Classification Summary
    st.markdown('<div class="data-card-header">Data Inventory</div>', unsafe_allow_html=True)
    
    df_raw = pd.DataFrame(DATA_SOURCES_INVENTORY)
    
    real_count = sum(1 for d in DATA_SOURCES_INVENTORY if d["Status"] == "REAL")
    lit_count = sum(1 for d in DATA_SOURCES_INVENTORY if "LITERATURE" in d["Status"] or d["Status"] == "CALCULATED")
    pending_count = sum(1 for d in DATA_SOURCES_INVENTORY if d["Status"] == "PENDING")
    sim_count = sum(1 for d in DATA_SOURCES_INVENTORY if d["Status"] in ["SIMULATED", "PROPOSED"])
    
    k1, k2, k3, k4, k5 = st.columns(5)
    
    with k1:
        st.metric(label="Total Datasets", value=len(DATA_SOURCES_INVENTORY), delta="Sources")
    
    with k2:
        st.metric(label="Real Data", value=real_count, delta="Connected")
    
    with k3:
        st.metric(label="Literature", value=lit_count, delta="Benchmarks")
    
    with k4:
        st.metric(label="Simulated", value=sim_count, delta="Demo")
    
    with k5:
        st.metric(label="Pending", value=pending_count, delta="Integration")
    
    st.write("")
    
    # Data Classification Info
    st.markdown("""
        <div class="data-card" style="background:#F0F9FF;border-color:#BFDBFE;">
            <div style="font-size:0.85rem;color:#1E3A8A;line-height:1.6;">
                <b>Data Provenance Classification:</b> All datasets classified by verified source to maintain scientific transparency 
                and eliminate ambiguous assumptions. Status labels indicate real measurements, literature benchmarks, calculations, or simulations.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Data Table with Status Badges
    st.markdown('<div class="data-card-header">Dataset Registry</div>', unsafe_allow_html=True)
    
    # Group by data type
    categories = {}
    for item in DATA_SOURCES_INVENTORY:
        cat = item.get("Type", "Other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    for category, items in categories.items():
        st.markdown(f"""
            <div style="font-size:0.9rem;font-weight:700;color:#0F172A;margin:1.5rem 0 0.75rem 0;padding-bottom:0.5rem;border-bottom:2px solid #E2E8F0;">
                {category}
            </div>
        """, unsafe_allow_html=True)
        
        for item in items:
            status_badge_map = {
                "REAL": "success",
                "LITERATURE-INFORMED": "info",
                "CALCULATED": "primary",
                "SIMULATED": "warning",
                "PROPOSED": "info",
                "PENDING": "neutral"
            }
            badge_type = status_badge_map.get(item["Status"], "neutral")
            
            st.markdown(f"""
                <div style="padding:0.75rem;margin-bottom:0.5rem;border:1px solid #E2E8F0;border-radius:6px;background:#FFFFFF;">
                    <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:0.5rem;">
                        <div>
                            <div style="font-size:0.85rem;font-weight:600;color:#0F172A;">{item['Data Source']}</div>
                            <div style="font-size:0.75rem;color:#64748B;margin-top:0.25rem;">{item['Role']}</div>
                        </div>
                        <span class="status-badge badge-{badge_type}">{item['Status']}</span>
                    </div>
                    <div style="display:flex;gap:1.5rem;font-size:0.7rem;color:#64748B;padding-top:0.5rem;border-top:1px solid #F1F5F9;">
                        <div><b>Layer:</b> {item.get('Layer', 'N/A')}</div>
                        <div><b>Source:</b> {item.get('Source', 'N/A')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.write("")
    
    # Status Legend
    st.markdown("""
        <div class="data-card">
            <div style="font-size:0.85rem;font-weight:700;color:#475569;margin-bottom:0.75rem;">Status Classification</div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.75rem;">
                <div>
                    <span class="status-badge badge-success">REAL</span>
                    <div style="font-size:0.7rem;color:#64748B;margin-top:0.25rem;">Verified field/satellite measurements</div>
                </div>
                <div>
                    <span class="status-badge badge-info">LITERATURE</span>
                    <div style="font-size:0.7rem;color:#64748B;margin-top:0.25rem;">Published benchmark values</div>
                </div>
                <div>
                    <span class="status-badge badge-primary">CALCULATED</span>
                    <div style="font-size:0.7rem;color:#64748B;margin-top:0.25rem;">System-derived results</div>
                </div>
                <div>
                    <span class="status-badge badge-warning">SIMULATED</span>
                    <div style="font-size:0.7rem;color:#64748B;margin-top:0.25rem;">Demonstration data</div>
                </div>
                <div>
                    <span class="status-badge badge-info">PROPOSED</span>
                    <div style="font-size:0.7rem;color:#64748B;margin-top:0.25rem;">Planned deployment</div>
                </div>
                <div>
                    <span class="status-badge badge-neutral">PENDING</span>
                    <div style="font-size:0.7rem;color:#64748B;margin-top:0.25rem;">Awaiting integration</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Downloadable Data Table
    with st.expander("Download Full Inventory", expanded=False):
        st.dataframe(df_raw, use_container_width=True, hide_index=True)
        
        # Convert to CSV for download
        csv = df_raw.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="geosmart_data_inventory.csv",
            mime="text/csv",
            key="data_sources_download_csv"
        )