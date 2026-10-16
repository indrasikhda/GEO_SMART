import streamlit as st
import folium
from streamlit_folium import st_folium
from core.io import MANIFESTATIONS
from core.maps import create_base_map, add_geological_layers
from core.raster import get_raster_stats_and_overlay

EVIDENCE_LAYERS = [
    {
        "name": "Land Surface Temperature",
        "type": "Raster",
        "status": "Connected",
        "source": "Landsat 8/9 TIRS",
        "badge": "success"
    },
    {
        "name": "NDVI Vegetation Index",
        "type": "Raster",
        "status": "Connected",
        "source": "Sentinel-2 MSI",
        "badge": "success"
    },
    {
        "name": "Geothermal Manifestations",
        "type": "Point",
        "status": "Connected",
        "source": "Field Survey",
        "badge": "success"
    },
    {
        "name": "Geology / Lithology",
        "type": "Polygon",
        "status": "Connected",
        "source": "Regional Geological Map (1:100k)",
        "badge": "success"
    },
    {
        "name": "Fault & Lineament",
        "type": "Line",
        "status": "Connected",
        "source": "Structural Geology (1:100k)",
        "badge": "success"
    },
    {
        "name": "Lineament Density",
        "type": "Raster",
        "status": "Pending",
        "source": "DEM Analysis",
        "badge": "neutral"
    },
    {
        "name": "Hydrothermal Alteration",
        "type": "Polygon",
        "status": "Pending",
        "source": "ASTER/Sentinel-2",
        "badge": "neutral"
    },
    {
        "name": "Micro-Seismicity",
        "type": "Point",
        "status": "Pending",
        "source": "Seismic Network",
        "badge": "neutral"
    }
]

def render_evidence():
    # Evidence Status Summary
    st.markdown('<div class="data-card-header">Evidence Integration Status</div>', unsafe_allow_html=True)
    
    connected = sum(1 for layer in EVIDENCE_LAYERS if layer["status"] == "Connected")
    pending = len(EVIDENCE_LAYERS) - connected
    
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.metric(label="Total Layers", value=len(EVIDENCE_LAYERS), delta="Criteria")
    
    with k2:
        st.metric(label="Connected", value=connected, delta=f"{(connected/len(EVIDENCE_LAYERS)*100):.1f}%")
    
    with k3:
        st.metric(label="Pending", value=pending, delta="Integration")
    
    with k4:
        st.metric(label="Data Types", value="3", delta="Raster/Vector")
    
    st.write("")
    
    # Main Layout
    col_layers, col_map = st.columns([5, 7], gap="large")
    
    with col_layers:
        st.markdown('<div class="data-card-header">Layer Inventory</div>', unsafe_allow_html=True)
        
        # Layer selection checkboxes
        st.markdown('<div style="font-size:0.8rem;color:#64748B;margin-bottom:0.75rem;">Toggle layers for map display</div>', unsafe_allow_html=True)
        
        selected_layers = []
        for layer in EVIDENCE_LAYERS:
            is_available = layer["status"] == "Connected"
            col_check, col_info = st.columns([1, 11])
            
            with col_check:
                if is_available:
                    # Default: raster and manifestations checked, geological layers default unchecked to keep initial view light
                    default_checked = layer["name"] in ["Land Surface Temperature", "NDVI Vegetation Index", "Geothermal Manifestations"]
                    checked = st.checkbox("", value=default_checked, key=f"layer_{layer['name']}", label_visibility="collapsed")
                    if checked:
                        selected_layers.append(layer["name"])
                else:
                    st.markdown('<div style="padding:0.3rem;"></div>', unsafe_allow_html=True)
            
            with col_info:
                st.markdown(f"""
                    <div style="padding:0.5rem;margin-bottom:0.5rem;border:1px solid #E2E8F0;border-radius:6px;background:{'#F8FAFC' if not is_available else '#FFFFFF'};">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.25rem;">
                            <span style="font-size:0.8rem;font-weight:600;color:{'#94A3B8' if not is_available else '#0F172A'};">{layer['name']}</span>
                            <span class="status-badge badge-{layer['badge']}">{layer['status']}</span>
                        </div>
                        <div style="font-size:0.7rem;color:#64748B;">
                            Type: {layer['type']} | Source: {layer['source']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.write("")
        
        # Integration Progress
        st.markdown("""
            <div class="data-card">
                <div style="font-size:0.85rem;font-weight:700;color:#475569;margin-bottom:0.75rem;">Integration Progress</div>
                <div style="width:100%;height:8px;background:#E2E8F0;border-radius:4px;overflow:hidden;">
                    <div style="width:62.5%;height:100%;background:linear-gradient(90deg, #0891B2, #0E7490);"></div>
                </div>
                <div style="font-size:0.75rem;color:#64748B;margin-top:0.5rem;">
                    62.5% Complete (5 of 8 layers connected)
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Pending Layers Note
        with st.expander("Pending Layers Details", expanded=False):
            st.markdown("""
                **Pending Data Integration:**
                - Lineament Density: Automated DEM-derived kernel density analysis
                - Hydrothermal Alteration: ASTER mineral band ratio mapping
                - Micro-Seismicity: Regional BMKG seismic network catalog
                
                **Connected Datasets:**
                - Geology / Lithology: 15 Multi-district GeoJSON layers for Sulawesi Utara
                - Fault & Lineament: 10 Structural fault trace GeoJSON layers
                - Remote Sensing: Landsat 8/9 LST & Sentinel-2 NDVI GeoTIFF
                - Manifestations: Documented field thermal inventory
            """)
    
    with col_map:
        st.markdown('<div class="data-card-header">Spatial Overlay</div>', unsafe_allow_html=True)
        
        m = create_base_map(center=[1.35, 124.85], zoom=8, include_geology=False)
        
        # Add Geology / Lithology FeatureGroup
        show_lito = "Geology / Lithology" in selected_layers
        show_geostruk = "Fault & Lineament" in selected_layers
        add_geological_layers(m, show_lito=show_lito, show_geostruk=show_geostruk)
        
        # Add LST if selected
        lst_overlay = None
        if "Land Surface Temperature" in selected_layers:
            lst_overlay = get_raster_stats_and_overlay("lst")
            if lst_overlay.get("png_path") and lst_overlay.get("bounds"):
                folium.raster_layers.ImageOverlay(
                    image=lst_overlay["png_path"],
                    bounds=lst_overlay["bounds"],
                    opacity=0.65,
                    name="LST"
                ).add_to(m)
        
        # Add NDVI if selected
        ndvi_overlay = None
        if "NDVI Vegetation Index" in selected_layers:
            ndvi_overlay = get_raster_stats_and_overlay("ndvi")
            if ndvi_overlay.get("png_path") and ndvi_overlay.get("bounds"):
                folium.raster_layers.ImageOverlay(
                    image=ndvi_overlay["png_path"],
                    bounds=ndvi_overlay["bounds"],
                    opacity=0.65,
                    name="NDVI"
                ).add_to(m)
        
        # Add manifestations if selected
        if "Geothermal Manifestations" in selected_layers:
            for manifest in MANIFESTATIONS:
                name_val = manifest.get('name', 'Geothermal Point')
                type_val = manifest.get('type', 'Manifestation')
                temp_val = manifest.get('temp', '-')
                ph_val = manifest.get('ph_level', manifest.get('ph', '-'))
                folium.CircleMarker(
                    location=[manifest["lat"], manifest["lng"]],
                    radius=7,
                    color="#DC2626",
                    fill=True,
                    fillColor="#FCA5A5",
                    fillOpacity=0.8,
                    popup=f"<b>{name_val}</b><br>Type: {type_val}<br>Temp: {temp_val}°C | pH: {ph_val}",
                    tooltip=name_val
                ).add_to(m)
        
        folium.LayerControl().add_to(m)
        st_folium(m, width="100%", height=490, key="evidence_overlay_map")

        # ── DYNAMIC COLOR RAMP LEGENDS ──────────────────────────────────
        has_lst = "Land Surface Temperature" in selected_layers and lst_overlay
        has_ndvi = "NDVI Vegetation Index" in selected_layers and ndvi_overlay

        if has_lst or has_ndvi:
            leg_col1, leg_col2 = st.columns(2 if (has_lst and has_ndvi) else 1)
            
            if has_lst:
                target_col = leg_col1 if (has_lst and has_ndvi) else st
                with target_col:
                    st.markdown(f"""
                        <div style="padding:0.6rem 0.8rem;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:6px;margin-top:0.5rem;">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.25rem;">
                                <span style="font-size:0.75rem;font-weight:700;color:#0F172A;">🌡️ LST Thermal Gradient</span>
                                <span style="font-size:0.68rem;font-weight:700;color:#DC2626;">Hotspot</span>
                            </div>
                            <div style="height:10px;border-radius:5px;background:linear-gradient(90deg, #0369A1 0%, #38BDF8 35%, #FEF08A 55%, #F59E0B 75%, #DC2626 90%, #7F1D1D 100%);"></div>
                            <div style="display:flex;justify-content:space-between;font-size:0.68rem;color:#64748B;font-weight:600;margin-top:0.2rem;">
                                <span>{lst_overlay['min']:.1f}°C (Cool)</span>
                                <span>{lst_overlay['mean']:.1f}°C</span>
                                <span style="color:#991B1B;">{lst_overlay['max']:.1f}°C (Heat Anomaly)</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            if has_ndvi:
                target_col = leg_col2 if (has_lst and has_ndvi) else st
                with target_col:
                    st.markdown(f"""
                        <div style="padding:0.6rem 0.8rem;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:6px;margin-top:0.5rem;">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.25rem;">
                                <span style="font-size:0.75rem;font-weight:700;color:#0F172A;">🌿 NDVI Vegetation Index</span>
                                <span style="font-size:0.68rem;font-weight:700;color:#065F46;">Dense Veg</span>
                            </div>
                            <div style="height:10px;border-radius:5px;background:linear-gradient(90deg, #92400E 0%, #D97706 20%, #FACC15 40%, #4ADE80 65%, #16A34A 85%, #064E3B 100%);"></div>
                            <div style="display:flex;justify-content:space-between;font-size:0.68rem;color:#64748B;font-weight:600;margin-top:0.2rem;">
                                <span>{ndvi_overlay['min']:.2f} (Low/Bare)</span>
                                <span>{ndvi_overlay['mean']:.2f}</span>
                                <span style="color:#064E3B;">{ndvi_overlay['max']:.2f} (Dense Canopy)</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        
        st.caption("Combined multi-source evidence overlay for Sulawesi Utara geothermal prospectivity analysis")


