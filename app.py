import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set page configuration - THIS MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="BrandGuardian AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_brand' not in st.session_state:
    st.session_state.current_brand = None

# Simple landing page
def show_landing_page():
    st.title("🛡️ BrandGuardian AI")
    st.write("### Complete Brand Protection Platform")
    
    # Features overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("📊 Sentiment Analysis")
        st.write("Real-time brand sentiment tracking across social media")
    with col2:
        st.subheader("🚨 Crisis Detection")
        st.write("Early warning system for brand threats")
    with col3:
        st.subheader("📈 Competitive Intelligence")
        st.write("Monitor competitors and market position")
    
    # Demo access
    with st.expander("🚀 Quick Start Demo"):
        st.write("Use these demo credentials to test the platform:")
        st.code("Brand ID: demo_brand\nPassword: demo123")
        
        if st.button("Auto-fill Demo Credentials"):
            st.session_state.authenticated = True
            st.session_state.current_brand = "demo_brand"
            st.rerun()

# Main dashboard (simplified)
def show_dashboard():
    st.title("📊 Brand Dashboard")
    st.write(f"Welcome, **{st.session_state.current_brand}**!")
    
    # Sample metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Brand Sentiment", "72%", "+4%")
    with col2:
        st.metric("Mentions", "1,247", "12%")
    with col3:
        st.metric("Engagement", "5.2%", "+1.2%")
    with col4:
        st.metric("Crisis Level", "Low", "-2%")
    
    # Sample data
    st.subheader("Recent Brand Mentions")
    sample_data = pd.DataFrame({
        'Platform': ['Twitter', 'Facebook', 'Instagram', 'Twitter', 'Facebook'],
        'Sentiment': [0.8, -0.3, 0.6, 0.9, -0.5],
        'Engagement': [245, 189, 567, 321, 98],
        'Time': [datetime.now() - timedelta(hours=h) for h in [1, 3, 5, 7, 9]]
    })
    st.dataframe(sample_data)
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.current_brand = None
        st.rerun()

# Main app logic
def main():
    if not st.session_state.authenticated:
        show_landing_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
