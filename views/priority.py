import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from core.io import PRIORITY_ZONES
from core.maps import create_base_map

def render_priority():
    # Priority Distribution Summary
    st.markdown('<div class="data-card-header">Priority Zone Classification</div>', unsafe_allow_html=True)
    
    high = sum(1 for z in PRIORITY_ZONES if z['priority'] == 'High')
    moderate = sum(1 for z in PRIORITY_ZONES if z['priority'] == 'Moderate')
    low = sum(1 for z in PRIORITY_ZONES if z['priority'] == 'Low')
    
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.metric(label="Total Zones", value=len(PRIORITY_ZONES), delta="Candidates")
    
    with k2:
        st.metric(label="High Priority", value=high, delta="GPI ≥0.75")
    
    with k3:
        st.metric(label="Moderate", value=moderate, delta="GPI 0.60-0.74")
    
    with k4:
        st.metric(label="Low Priority", value=low, delta="GPI <0.60")
    
    st.write("")
    
    # Demo Data Notice
    st.markdown("""
        <div class="data-card" style="background:#FEF3C7;border-color:#FDE68A;">
            <div style="display:flex;align-items:center;gap:0.75rem;">
                <span class="status-badge badge-warning">DEMO DATA</span>
                <div style="font-size:0.85rem;color:#92400E;">
                    Priority zones demonstrate workflow. Full GPI raster generation requires complete geological dataset.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Main Layout
    col_table, col_map = st.columns([5, 7], gap="large")
    
    with col_table:
        st.markdown('<div class="data-card-header">Zone Ranking</div>', unsafe_allow_html=True)
        
        # Sort by GPI descending
        sorted_zones = sorted(PRIORITY_ZONES, key=lambda x: x['gpi'], reverse=True)
        
        for zone in sorted_zones:
            priority_colors = {
                'High': ('success', '#ECFDF5'),
                'Moderate': ('warning', '#FFFBEB'),
                'Low': ('neutral', '#F8FAFC')
            }
            badge_type, bg_color = priority_colors.get(zone['priority'], ('neutral', '#F8FAFC'))
            
            st.markdown(f"""
                <div style="padding:0.75rem;margin-bottom:0.5rem;border:1px solid #E2E8F0;border-radius:8px;background:{bg_color};">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                        <span style="font-size:0.9rem;font-weight:700;color:#0F172A;">{zone['zone']}</span>
                        <span class="status-badge badge-{badge_type}">{zone['priority']}</span>
                    </div>
                    <div style="display:flex;gap:1rem;font-size:0.75rem;color:#64748B;">
                        <div><b>GPI:</b> {zone['gpi']}</div>
                        <div><b>Area:</b> {zone['area']} km²</div>
                    </div>
                    {f'<div style="margin-top:0.5rem;font-size:0.7rem;color:#DC2626;">⚠ {zone["constraint"]}</div>' if zone.get('constraint') else ''}
                </div>
            """, unsafe_allow_html=True)
        
        st.write("")
        
        # Classification Criteria
        with st.expander("Classification Criteria", expanded=False):
            st.markdown("""
                **Priority Thresholds:**
                - **High:** GPI ≥ 0.75 + No major constraints
                - **Moderate:** GPI 0.60-0.74 OR constraints present
                - **Low:** GPI < 0.60
                
                **Constraint Types:**
                - Environmental reserves / protected areas
                - Urban buffer zones
                - Volcanic crater buffers
                - Infrastructure corridors
            """)
    
    with col_map:
        st.markdown('<div class="data-card-header">Spatial Distribution</div>', unsafe_allow_html=True)
        
        m = create_base_map(center=[1.30, 124.85], zoom=10)
        
        # Add zone markers
        priority_colors_map = {
            'High': '#059669',
            'Moderate': '#D97706',
            'Low': '#64748B'
        }
        
        for zone in PRIORITY_ZONES:
            color = priority_colors_map.get(zone['priority'], '#64748B')
            
            folium.CircleMarker(
                location=[zone['lat'], zone['lng']],
                radius=8,
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                popup=f"""
                    <b>{zone['zone']}</b><br>
                    Priority: {zone['priority']}<br>
                    GPI: {zone['gpi']}<br>
                    Area: {zone['area']} km²
                    {f"<br><span style='color:#DC2626;'>⚠ {zone['constraint']}</span>" if zone.get('constraint') else ''}
                """,
                tooltip=f"{zone['zone']} - {zone['priority']}"
            ).add_to(m)
        
        folium.LayerControl().add_to(m)
        st_folium(m, width="100%", height=600, key="priority_zones_map")
        
        # Legend
        st.markdown("""
            <div style="display:flex;gap:1.5rem;margin-top:0.75rem;font-size:0.8rem;">
                <div style="display:flex;align-items:center;gap:0.5rem;">
                    <div style="width:12px;height:12px;border-radius:50%;background:#059669;"></div>
                    <span class="status-badge badge-success">High Priority</span>
                </div>
                <div style="display:flex;align-items:center;gap:0.5rem;">
                    <div style="width:12px;height:12px;border-radius:50%;background:#D97706;"></div>
                    <span class="status-badge badge-warning">Moderate</span>
                </div>
                <div style="display:flex;align-items:center;gap:0.5rem;">
                    <div style="width:12px;height:12px;border-radius:50%;background:#64748B;"></div>
                    <span class="status-badge badge-neutral">Low Priority</span>
                </div>
            </div>
        """, unsafe_allow_html=True)