import streamlit as st
from core.data import METHODS_STEPS

def render_methods():
    st.markdown("<p style='font-size:0.9rem;color:#636366;margin-bottom:1.5rem;'>GEO-SMART scientific workflow methodology and processing pipeline.</p>", unsafe_allow_html=True)

    for i, item in enumerate(METHODS_STEPS):
        st.markdown(f"""
            <div style="background:#FFFFFF;border-radius:20px;border:1px solid #ECECEC;padding:20px 24px;margin-bottom:0.875rem;box-shadow:0 2px 10px rgba(0,0,0,0.02);display:flex;gap:18px;align-items:flex-start;">
                <div style="min-width:36px;height:36px;background:#F2F2F7;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800;color:#636366;">{i+1}</div>
                <div>
                    <span style="font-size:0.7rem;font-weight:700;text-transform:uppercase;color:#8E8E93;letter-spacing:0.05em;">{item['step']}</span>
                    <h3 style="font-size:1rem;font-weight:800;color:#1C1C1E;margin:4px 0 6px 0;">{item['title']}</h3>
                    <p style="font-size:0.85rem;color:#636366;margin:0;line-height:1.55;">{item['desc']}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
