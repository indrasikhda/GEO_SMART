import streamlit as st
import folium
from streamlit_folium import st_folium
from core.maps import create_base_map
from core.io import MANIFESTATIONS, GMN_NODES

def render_overview():
    # Real-Time System Status - KPI Grid
    st.markdown('<div class="data-card-header">System Status</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Evidence Layers",
            value="8",
            delta="5 Active"
        )
    
    with col2:
        st.metric(
            label="AHP Criteria",
            value="5",
            delta="Calibrated"
        )
    
    with col3:
        st.metric(
            label="Priority Zones",
            value="12",
            delta="6 High"
        )
    
    with col4:
        st.metric(
            label="GMN Nodes",
            value="3",
            delta="Proposed"
        )
    
    with col5:
        st.metric(
            label="Data Status",
            value="62.5%",
            delta="Connected"
        )
    
    st.write("")
    
    # Main Content Grid - Map Dominant
    col_map, col_metrics = st.columns([7, 5], gap="large")
    
    with col_map:
        st.markdown('<div class="data-card-header">Study Area Overview</div>', unsafe_allow_html=True)
        
        # Manifestation locations - 5 documented thermal sites
        m = create_base_map(center=[1.30, 124.85], zoom=10)
        
        # Add manifestation markers
        for manifest in MANIFESTATIONS:
            folium.CircleMarker(
                location=[manifest["lat"], manifest["lng"]],
                radius=8,
                color="#DC2626",
                fill=True,
                fillColor="#FCA5A5",
                fillOpacity=0.7,
                popup=f"<b>{manifest['name']}</b><br>{manifest['type']}",
                tooltip=manifest["name"]
            ).add_to(m)
        
        # Add GMN nodes (proposed)
        for node in GMN_NODES:
            folium.CircleMarker(
                location=[node["lat"], node["lng"]],
                radius=6,
                color="#0891B2",
                fill=True,
                fillColor="#A5F3FC",
                fillOpacity=0.8,
                popup=f"<b>{node['id']}</b><br>{node['name']}",
                tooltip=f"{node['id']} (Proposed)"
            ).add_to(m)
        
        folium.LayerControl().add_to(m)
        st_folium(m, width="100%", height=480, key="overview_main_map")
        
        # Quick Legend
        st.markdown("""
            <div style="display:flex;gap:1.5rem;margin-top:0.75rem;font-size:0.8rem;">
                <div style="display:flex;align-items:center;gap:0.5rem;">
                    <div style="width:12px;height:12px;border-radius:50%;background:#DC2626;"></div>
                    <span class="status-badge badge-danger">Thermal Manifestation</span>
                </div>
                <div style="display:flex;align-items:center;gap:0.5rem;">
                    <div style="width:12px;height:12px;border-radius:50%;background:#0891B2;"></div>
                    <span class="status-badge badge-primary">GMN Node (Proposed)</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_metrics:
        # Exploration Priority Distribution
        st.markdown('<div class="data-card-header">Priority Distribution</div>', unsafe_allow_html=True)
        
        p1, p2, p3 = st.columns(3)
        with p1:
            st.metric(label="High", value="6", delta="≥0.75 GPI")
        with p2:
            st.metric(label="Moderate", value="5", delta="0.60-0.74")
        with p3:
            st.metric(label="Low", value="1", delta="<0.60")
        
        st.write("")
        
        # Evidence Layer Status
        st.markdown('<div class="data-card-header">Evidence Integration</div>', unsafe_allow_html=True)
        
        evidence_status = [
            ("LST Raster", "Connected", "success"),
            ("NDVI Raster", "Connected", "success"),
            ("Manifestations", "Connected", "success"),
            ("Geology / Lithology", "Connected", "success"),
            ("Fault & Lineament", "Connected", "success"),
            ("Lineament Density", "Pending", "neutral"),
            ("Alteration", "Pending", "neutral"),
            ("Seismicity", "Pending", "neutral"),
        ]
        
        for layer, status, badge_type in evidence_status:
            st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;padding:0.5rem;border-bottom:1px solid #E2E8F0;">
                    <span style="font-size:0.85rem;font-weight:500;color:#475569;">{layer}</span>
                    <span class="status-badge badge-{badge_type}">{status}</span>
                </div>
            """, unsafe_allow_html=True)
        
        st.write("")
        
        # Net Zero Impact - Compact
        st.markdown("""
            <div class="data-card" style="background:linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);border-color:#A7F3D0;">
                <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.75rem;">
                    <div style="width:36px;height:36px;background:#059669;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                        <span style="font-size:1.25rem;">⚡</span>
                    </div>
                    <div>
                        <div style="font-size:0.95rem;font-weight:800;color:#065F46;">Net Zero Contribution</div>
                        <div style="font-size:0.75rem;color:#047857;">Clean Energy Acceleration</div>
                    </div>
                </div>
                <div style="font-size:0.8rem;color:#065F46;line-height:1.5;">
                    Precision targeting reduces exploration carbon footprint and accelerates geothermal deployment for Indonesia's Net Zero 2060 target.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Methodology Note - Collapsible
        with st.expander("System Methodology", expanded=False):
            st.markdown("""
                **Workflow:** Remote Sensing → Evidence Integration → AHP Weighting → GPI Calculation → Priority Zoning → GMN Monitoring
                
                **Status:** Literature-informed prototype using real satellite data (LST, NDVI), documented thermal manifestations, and integrated regional GeoJSON geology & fault networks (Sulawesi Utara).
            """)

