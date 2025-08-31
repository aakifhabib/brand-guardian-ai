import streamlit as st
import time
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from collections import Counter
import json
import os
import hashlib
import base64
import math
from cryptography.fernet import Fernet
import binascii
import uuid
import secrets
from PIL import Image
import io
import requests

# Fix for plotly import error
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    # Create dummy classes to prevent errors if plotly isn't installed
    class go:
        @staticmethod
        def Figure(*args, **kwargs):
            return None
    class px:
        @staticmethod
        def line(*args, **kwargs):
            return None
    def make_subplots(*args, **kwargs):
        return None

# Set page config first
st.set_page_config(
    page_title="Brand Guardian AI",  # Changed from "Virelo AI Pro"
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Generate and display premium access key
def generate_premium_key():
    """Generate a secure premium access key"""
    key = secrets.token_urlsafe(16)
    premium_key = f"BG-PREMIUM-{key.upper()}"  # Changed from "VR-PREMIUM-"
    return premium_key

# Display the premium key in the console (for admin use)
premium_access_key = generate_premium_key()
print(f"PREMIUM ACCESS KEY: {premium_access_key}")

# Subscription tiers and pricing
SUBSCRIPTION_TIERS = {
    "basic": {
        "name": "Basic",
        "price": "$29/month",
        "features": [
            "Basic brand monitoring",
            "5 social platforms",
            "100 mentions/month",
            "Email alerts",
            "Basic reports"
        ],
        "api_calls": 1000,
        "threat_keywords": 50,
        "ai_analysis": False,
        "privileges": ["basic_monitoring", "basic_reports"]
    },
    "advanced": {
        "name": "Advanced",
        "price": "$99/month",
        "features": [
            "Advanced brand monitoring",
            "10 social platforms",
            "1000 mentions/month",
            "Email & SMS alerts",
            "Advanced reports",
            "AI-powered analysis",
            "Competitor tracking"
        ],
        "api_calls": 10000,
        "threat_keywords": 200,
        "ai_analysis": True,
        "privileges": ["basic_monitoring", "basic_reports", "ai_analysis", "competitor_tracking"]
    },
    "premium": {
        "name": "Premium",
        "price": "$299/month",
        "features": [
            "Premium brand monitoring",
            "Unlimited platforms",
            "Unlimited mentions",
            "Multi-channel alerts",
            "Custom reports",
            "Advanced AI analysis",
            "Competitor tracking",
            "Crisis management",
            "Dedicated support",
            "API access"
        ],
        "api_calls": 100000,
        "threat_keywords": 1000,
        "ai_analysis": True,
        "privileges": ["basic_monitoring", "basic_reports", "ai_analysis", "competitor_tracking", "crisis_management", "api_access"]
    }
}

# Advanced CSS with Gold and Black theme
st.markdown("""
<style>
    /* Base styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #2d2d2d 100%);
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #2d2d2d 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    /* Animated gold particles background */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }
    
    .particle {
        position: absolute;
        background: radial-gradient(circle, rgba(255, 215, 0, 0.8), rgba(255, 215, 0, 0));
        border-radius: 50%;
        animation: float 20s infinite linear;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    
    @keyframes float {
        0% { transform: translateY(0) translateX(0) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) translateX(100px) rotate(360deg); opacity: 0; }
    }
    
    /* Premium header styling */
    .premium-header {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        margin: 20px 0;
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 50%, #FF8C00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 2px 10px rgba(255, 215, 0, 0.3);
        animation: goldGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes goldGlow {
        from { text-shadow: 0px 2px 10px rgba(255, 215, 0, 0.3); }
        to { text-shadow: 0px 2px 20px rgba(255, 215, 0, 0.6), 0px 0px 30px rgba(255, 215, 0, 0.4); }
    }
    
    .floating {
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .accent-text {
        font-size: 1.4rem;
        color: #FFD700;
        text-align: center;
        margin-bottom: 40px;
        animation: fadeIn 2s ease-in;
        font-weight: 500;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Enhanced card styling with gold theme */
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(20, 20, 20, 0.8));
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        margin: 15px 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 215, 0, 0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent, rgba(255, 215, 0, 0.1), transparent);
        transform: translateX(-100%);
        transition: transform 0.6s;
    }
    
    .metric-card:hover::before {
        transform: translateX(100%);
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 215, 0, 0.3);
        border: 1px solid rgba(255, 215, 0, 0.5);
    }
    
    .search-analysis-card {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(20, 20, 20, 0.8));
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 215, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .search-analysis-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 215, 0, 0.3);
    }
    
    .search-result-card {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.7), rgba(20, 20, 20, 0.7));
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #FFD700;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .search-result-card:hover {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(30, 30, 30, 0.8));
        transform: translateX(10px);
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
    }
    
    /* Subscription tier cards */
    .tier-card {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(20, 20, 20, 0.8));
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 10px;
        border: 2px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 215, 0, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .tier-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 215, 0, 0.3);
    }
    
    .tier-card.premium {
        border-color: rgba(255, 215, 0, 0.6);
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(30, 30, 30, 0.9));
        box-shadow: 0 10px 40px rgba(255, 215, 0, 0.3), inset 0 1px 0 rgba(255, 215, 0, 0.3);
    }
    
    .tier-card.premium::before {
        content: 'MOST POPULAR';
        position: absolute;
        top: 15px;
        right: -30px;
        background: linear-gradient(90deg, #FFD700, #FFA500);
        color: #000000;
        padding: 5px 40px;
        font-weight: 700;
        font-size: 12px;
        transform: rotate(45deg);
    }
    
    .tier-price {
        font-size: 2.5rem;
        font-weight: 800;
        color: #FFD700;
        margin: 10px 0;
        text-shadow: 0px 0px 10px rgba(255, 215, 0, 0.5);
    }
    
    .tier-features {
        list-style: none;
        padding: 0;
        margin: 20px 0;
    }
    
    .tier-features li {
        padding: 8px 0;
        padding-left: 25px;
        position: relative;
    }
    
    .tier-features li::before {
        content: '✓';
        position: absolute;
        left: 0;
        color: #FFD700;
        font-weight: bold;
    }
    
    /* Enhanced threat indicators */
    .threat-indicator {
        padding: 10px 16px;
        border-radius: 25px;
        font-size: 13px;
        font-weight: 700;
        margin: 8px;
        display: inline-block;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    
    .threat-indicator:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.7);
    }
    
    .threat-high {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.3), rgba(255, 0, 0, 0.1));
        color: #ff6b6b;
        border: 1px solid rgba(255, 0, 0, 0.5);
        animation: threatPulse 2s infinite;
    }
    
    .threat-medium {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.3), rgba(255, 165, 0, 0.1));
        color: #ffa726;
        border: 1px solid rgba(255, 165, 0, 0.5);
    }
    
    .threat-low {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.3), rgba(0, 255, 0, 0.1));
        color: #66bb6a;
        border: 1px solid rgba(0, 255, 0, 0.5);
    }
    
    @keyframes threatPulse {
        0% { box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5), 0 0 0 0 rgba(255, 0, 0, 0.7); }
        50% { box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5), 0 0 0 10px rgba(255, 0, 0, 0); }
        100% { box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5), 0 0 0 0 rgba(255, 0, 0, 0.7); }
    }
    
    /* Status indicators */
    .api-status-connected {
        color: #FFD700;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
    }
    
    .api-status-connected::before {
        content: '●';
        margin-right: 5px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .api-status-disconnected {
        color: #ff6b6b;
        font-weight: 700;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        border-radius: 15px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.7), rgba(30, 30, 30, 0.7));
        color: #FFD700;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 215, 0, 0.2);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(40, 40, 40, 0.8));
        border: 1px solid rgba(255, 215, 0, 0.5);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 215, 0, 0.3);
    }
    
    /* Enhanced tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.7), rgba(30, 30, 30, 0.7));
        border-radius: 15px 15px 0 0;
        padding: 14px 20px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-bottom: none;
        font-weight: 600;
        transition: all 0.3s ease;
        color: #FFD700;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(40, 40, 40, 0.8));
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(40, 40, 40, 0.8));
        border: 1px solid rgba(255, 215, 0, 0.5);
        border-bottom: none;
        box-shadow: 0 -4px 15px rgba(255, 215, 0, 0.3);
    }
    
    /* Custom metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFD700;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    /* Enhanced input styling */
    .stSelectbox [data-baseweb="select"], 
    .stTextInput [data-baseweb="input"], 
    .stTextArea [data-baseweb="textarea"],
    .stNumberInput [data-baseweb="input"],
    .stDateInput [data-baseweb="input"],
    .stTimeInput [data-baseweb="input"] {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.7), rgba(30, 30, 30, 0.7));
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        color: #FFD700;
        transition: all 0.3s ease;
    }
    
    .stSelectbox [data-baseweb="select"]:hover, 
    .stTextInput [data-baseweb="input"]:hover, 
    .stTextArea [data-baseweb="textarea"]:hover,
    .stNumberInput [data-baseweb="input"]:hover,
    .stDateInput [data-baseweb="input"]:hover,
    .stTimeInput [data-baseweb="input"]:hover {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(40, 40, 40, 0.8));
        border: 1px solid rgba(255, 215, 0, 0.5);
    }
    
    /* Custom spinner */
    .stSpinner > div {
        border: 4px solid rgba(255, 215, 0, 0.1);
        border-radius: 50%;
        border-top: 4px solid #FFD700;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Custom expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.7), rgba(30, 30, 30, 0.7));
        border-radius: 12px;
        padding: 14px 18px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(40, 40, 40, 0.8));
    }
    
    /* Custom dataframes */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    /* Custom success/error boxes */
    .stAlert {
        border-radius: 15px;
        padding: 16px 20px;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
    }
    
    /* Custom sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #000000 0%, #1a1a1a 100%);
        border-right: 1px solid rgba(255, 215, 0, 0.2);
    }
    
    /* Custom chart elements */
    .stChart {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
    }
    
    /* Custom progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 50%, #FF8C00 100%);
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
    }
    
    /* Custom radio buttons */
    .stRadio [role="radiogroup"] {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.7), rgba(30, 30, 30, 0.7));
        padding: 18px;
        border-radius: 15px;
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    
    /* Custom slider */
    .stSlider [role="slider"] {
        background: linear-gradient(90deg, #FFD700, #FFA500);
        border-radius: 10px;
        height: 8px;
    }
    
    /* Custom checkbox */
    .stCheckbox [data-baseweb="checkbox"] {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.7), rgba(30, 30, 30, 0.7));
        border-radius: 8px;
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    
    /* Premium badge */
    .premium-badge {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #000000;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        margin-left: 10px;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200px; }
        100% { background-position: calc(200px + 100%); }
    }
    
    /* Security shield animation */
    .security-shield {
        display: inline-block;
        animation: shieldPulse 2s infinite;
    }
    
    @keyframes shieldPulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Login form enhancements */
    .login-container {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(20, 20, 20, 0.8));
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 40px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7);
        max-width: 500px;
        margin: 0 auto;
    }
    
    /* Animated background for login */
    .login-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: radial-gradient(circle at 20% 50%, rgba(255, 215, 0, 0.1), transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(255, 215, 0, 0.1), transparent 50%),
                    radial-gradient(circle at 40% 80%, rgba(255, 215, 0, 0.1), transparent 50%);
        animation: bgMove 20s ease infinite;
    }
    
    @keyframes bgMove {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(20px, -20px) rotate(120deg); }
        66% { transform: translate(-20px, 20px) rotate(240deg); }
    }
    
    /* Premium access card */
    .premium-access-card {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(20, 20, 20, 0.8));
        border: 2px solid rgba(255, 215, 0, 0.3);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.7);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .premium-access-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 215, 0, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Threat radar animation */
    .threat-radar {
        position: relative;
        width: 200px;
        height: 200px;
        margin: 0 auto;
    }
    
    .radar-circle {
        position: absolute;
        border: 2px solid rgba(255, 215, 0, 0.3);
        border-radius: 50%;
        animation: radarPulse 2s infinite;
    }
    
    @keyframes radarPulse {
        0% { transform: scale(0.8); opacity: 1; }
        100% { transform: scale(1.2); opacity: 0; }
    }
    
    /* User profile card */
    .user-profile-card {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.7), rgba(20, 20, 20, 0.7));
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        text-align: center;
        margin-bottom: 20px;
    }
    
    .user-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        margin: 0 auto 15px;
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
    }
    
    /* Activity log */
    .activity-log {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.5), rgba(20, 20, 20, 0.5));
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #FFD700;
    }
    
    .activity-time {
        color: #FFD700;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* Admin panel */
    .admin-panel {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.7), rgba(20, 20, 20, 0.7));
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin: 20px 0;
    }
    
    .admin-stat {
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        background: rgba(255, 215, 0, 0.1);
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .admin-stat:hover {
        background: rgba(255, 215, 0, 0.2);
        transform: translateY(-5px);
    }
    
    .admin-stat-value {
        font-size: 2rem;
        font-weight: 800;
        color: #FFD700;
    }
    
    .admin-stat-label {
        color: #ffffff;
        font-weight: 600;
    }
    
    /* AI Analysis Card */
    .ai-analysis-card {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.7), rgba(20, 20, 20, 0.7));
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    .ai-analysis-header {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .ai-icon {
        font-size: 2rem;
        margin-right: 10px;
        animation: aiPulse 2s infinite;
    }
    
    @keyframes aiPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .ai-confidence {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-left: 10px;
    }
    
    .confidence-high {
        background: rgba(0, 255, 0, 0.2);
        color: #66bb6a;
    }
    
    .confidence-medium {
        background: rgba(255, 165, 0, 0.2);
        color: #ffa726;
    }
    
    .confidence-low {
        background: rgba(255, 0, 0, 0.2);
        color: #ff6b6b;
    }
    
    /* AI Insights */
    .ai-insight {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.5), rgba(20, 20, 20, 0.5));
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #FFD700;
    }
    
    .ai-insight-title {
        color: #FFD700;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    /* Subscription status */
    .subscription-status {
        display: inline-flex;
        align-items: center;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        margin: 5px 0;
    }
    
    .status-basic {
        background: rgba(156, 39, 176, 0.2);
        color: #ce93d8;
    }
    
    .status-advanced {
        background: rgba(3, 169, 244, 0.2);
        color: #4fc3f7;
    }
    
    .status-premium {
        background: rgba(255, 215, 0, 0.2);
        color: #FFD700;
    }
    
    /* Privilege management */
    .privilege-card {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.6), rgba(20, 20, 20, 0.6));
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(255, 215, 0, 0.2);
    }
    
    .privilege-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .privilege-title {
        color: #FFD700;
        font-weight: 600;
    }
    
    .privilege-toggle {
        position: relative;
        display: inline-block;
        width: 50px;
        height: 24px;
    }
    
    .privilege-toggle input {
        opacity: 0;
        width: 0;
        height: 0;
    }
    
    .privilege-slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(255, 255, 255, 0.1);
        transition: .4s;
        border-radius: 24px;
    }
    
    .privilege-slider:before {
        position: absolute;
        content: "";
        height: 16px;
        width: 16px;
        left: 4px;
        bottom: 4px;
        background-color: white;
        transition: .4s;
        border-radius: 50%;
    }
    
    input:checked + .privilege-slider {
        background-color: #FFD700;
    }
    
    input:checked + .privilege-slider:before {
        transform: translateX(26px);
    }
    
    /* Enhanced threat animation */
    .threat-animation {
        position: relative;
        height: 200px;
        margin: 20px 0;
        border-radius: 15px;
        overflow: hidden;
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.5), rgba(20, 20, 20, 0.5));
        border: 1px solid rgba(255, 215, 0, 0.2);
    }
    
    .threat-wave {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E%3Cpath d='M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z' opacity='.25' fill='%23FFD700'%3E%3C/path%3E%3Cpath d='M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9-9.42,98.6-31.56,31.77-25.39,62.32-62,103.63-73,40.44-10.79,81.35-10.85,119.13,1.55,37.08,11.72,70.09,31.24,100.34,52.08,58.2,103.33,111.27,165.33,112.53C877.19,374.14,944.58,381.42,1012.67,367.3c36.15-7.1,72.09-21.69,104.45-40.59,36.19-19.15,69-44.14,98.85-72.54,30.46-29.3,60.74-58.49,91.69-87.53C1176.23,136.43,1200,82.54,1200,32.13V0Z' opacity='.5' fill='%23FFD700'%3E%3C/path%3E%3Cpath d='M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z' fill='%23FFD700'%3E%3C/path%3E%3C/svg%3E");
        background-size: 1200px 120px;
        animation: wave 10s linear infinite;
    }
    
    @keyframes wave {
        0% { background-position-x: 0; }
        100% { background-position-x: 1200px; }
    }
    
    .threat-pulse {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255, 215, 0, 0.8), rgba(255, 215, 0, 0));
        animation: threatPulseExpand 3s infinite;
    }
    
    @keyframes threatPulseExpand {
        0% { width: 100px; height: 100px; opacity: 0.8; }
        100% { width: 300px; height: 300px; opacity: 0; }
    }
    
    /* Enhanced chart container */
    .chart-container {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.6), rgba(20, 20, 20, 0.6));
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid rgba(255, 215, 0, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# Add animated particles to the background
def add_particles():
    st.markdown("""
    <div class="particles">
        <div class="particle" style="width: 10px; height: 10px; left: 10%; animation-duration: 20s;"></div>
        <div class="particle" style="width: 15px; height: 15px; left: 20%; animation-duration: 25s;"></div>
        <div class="particle" style="width: 8px; height: 8px; left: 30%; animation-duration: 30s;"></div>
        <div class="particle" style="width: 12px; height: 12px; left: 40%; animation-duration: 22s;"></div>
        <div class="particle" style="width: 18px; height: 18px; left: 50%; animation-duration: 28s;"></div>
        <div class="particle" style="width: 7px; height: 7px; left: 60%; animation-duration: 32s;"></div>
        <div class="particle" style="width: 14px; height: 14px; left: 70%; animation-duration: 24s;"></div>
        <div class="particle" style="width: 9px; height: 9px; left: 80%; animation-duration: 26s;"></div>
        <div class="particle" style="width: 16px; height: 16px; left: 90%; animation-duration: 29s;"></div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced AI Analysis System
class AIAnalysisSystem:
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 500
        
    def analyze_threat(self, query, brand_name, subscription_tier):
        """Analyze threat using AI based on subscription tier"""
        if subscription_tier not in SUBSCRIPTION_TIERS:
            subscription_tier = "basic"
        
        tier_info = SUBSCRIPTION_TIERS[subscription_tier]
        
        # Basic analysis for all tiers
        basic_analysis = self._basic_threat_analysis(query, brand_name)
        
        # Enhanced analysis for advanced and premium tiers
        if tier_info["ai_analysis"]:
            enhanced_analysis = self._enhanced_threat_analysis(query, brand_name)
            ai_insights = self._generate_ai_insights(query, brand_name, subscription_tier)
            return {
                **basic_analysis,
                **enhanced_analysis,
                "ai_insights": ai_insights,
                "subscription_tier": subscription_tier
            }
        else:
            return {
                **basic_analysis,
                "subscription_tier": subscription_tier
            }
    
    def _basic_threat_analysis(self, query, brand_name):
        """Basic threat analysis for all tiers"""
        query_lower = query.lower()
        brand_lower = brand_name.lower()
        
        # Detect threat level
        threat_level = "low"
        found_keywords = []
        
        threat_keywords = {
            'high': ['scam', 'fraud', 'lawsuit', 'bankruptcy', 'fake', 'illegal', 'sue', 'crime'],
            'medium': ['complaint', 'problem', 'issue', 'bad', 'terrible', 'awful', 'disappointed'],
            'low': ['review', 'feedback', 'comment', 'opinion', 'thought', 'experience']
        }
        
        for level, keywords in threat_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    threat_level = level
                    found_keywords.append(keyword)
        
        return {
            'query': query,
            'brand': brand_name,
            'threat_level': threat_level,
            'keywords_found': found_keywords,
            'timestamp': datetime.now().isoformat(),
            'analysis': self._generate_analysis(threat_level, found_keywords),
            'recommendations': self._generate_recommendations(threat_level)
        }
    
    def _enhanced_threat_analysis(self, query, brand_name):
        """Enhanced threat analysis for advanced and premium tiers"""
        # Simulate enhanced analysis
        sentiment_score = random.uniform(0, 1)
        urgency_score = random.uniform(0, 1)
        impact_score = random.uniform(0, 1)
        
        return {
            'sentiment_score': sentiment_score,
            'urgency_score': urgency_score,
            'impact_score': impact_score,
            'risk_assessment': self._assess_risk(sentiment_score, urgency_score, impact_score),
            'predicted_trend': self._predict_trend(query, brand_name)
        }
    
    def _generate_ai_insights(self, query, brand_name, subscription_tier):
        """Generate AI-powered insights"""
        insights = []
        
        # Contextual understanding
        insights.append({
            "type": "context",
            "title": "Contextual Analysis",
            "content": f"AI has identified that the query relates to {brand_name} in the context of potential brand reputation risks.",
            "confidence": random.uniform(0.7, 0.95)
        })
        
        # Pattern recognition
        insights.append({
            "type": "pattern",
            "title": "Pattern Recognition",
            "content": "Similar threat patterns have been detected in 3 other brands in your industry this month.",
            "confidence": random.uniform(0.6, 0.85)
        })
        
        # Predictive analysis (premium only)
        if subscription_tier == "premium":
            insights.append({
                "type": "predictive",
                "title": "Predictive Analysis",
                "content": "Based on current trends, AI predicts a 15% increase in similar mentions over the next 7 days.",
                "confidence": random.uniform(0.75, 0.9)
            })
        
        return insights
    
    def _assess_risk(self, sentiment_score, urgency_score, impact_score):
        """Assess overall risk based on scores"""
        overall_score = (sentiment_score + urgency_score + impact_score) / 3
        
        if overall_score > 0.7:
            return "High Risk"
        elif overall_score > 0.4:
            return "Medium Risk"
        else:
            return "Low Risk"
    
    def _predict_trend(self, query, brand_name):
        """Predict trend based on query"""
        trends = ["Increasing", "Stable", "Decreasing"]
        weights = [0.3, 0.4, 0.3]
        return random.choices(trends, weights=weights)[0]
    
    def _generate_analysis(self, threat_level, keywords):
        """Generate analysis text based on threat level"""
        analyses = {
            'high': "🚨 High threat potential detected. Immediate attention required. Multiple negative keywords found indicating serious brand reputation risks.",
            'medium': "⚠️ Medium threat level. Potential brand reputation issues detected. Monitor closely and consider proactive engagement.",
            'low': "✅ Low threat level. General brand mentions detected. Standard monitoring recommended."
        }
        return analyses.get(threat_level, "Analysis completed.")
    
    def _generate_recommendations(self, threat_level):
        """Generate recommendations based on threat level"""
        recommendations = {
            'high': [
                "Immediate crisis management protocol activation",
                "Legal team notification",
                "Press statement preparation",
                "Social media monitoring escalation",
                "Executive team alert"
            ],
            'medium': [
                "Enhanced monitoring of mentioned platforms",
                "Customer service team notification",
                "Response template preparation",
                "Competitive analysis update",
                "Weekly review scheduling"
            ],
            'low': [
                "Continue standard monitoring",
                "Track sentiment trends",
                "Update brand health metrics",
                "Monthly review scheduling"
            ]
        }
        return recommendations.get(threat_level, [])

# Initialize AI analysis system
ai_system = AIAnalysisSystem()

# Enhanced Security Manager with Premium Access
class SecurityManager:
    def __init__(self):
        self.valid_access_keys = {
            "BG2024-PRO-ACCESS": "full",  # Changed from "VR2024-PRO-ACCESS"
            "BG-ADVANCED-ANALYSIS": "analysis",  # Changed from "VR-ADVANCED-ANALYSIS"
            "BG-PREMIUM-2024": "premium",  # Changed from "VR-PREMIUM-2024"
            "BRANDGUARDIAN-PRO": "pro",  # Changed from "VIRELO-PRO"
            premium_access_key: "premium"  # Add the generated key
        }
        self.failed_attempts = {}
        self.lockout_time = timedelta(minutes=15)
        self.max_attempts = 5
        self.session_timeout = timedelta(minutes=30)
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.activity_log = []
    
    def encrypt_data(self, data):
        """Encrypt sensitive data"""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher_suite.encrypt(data)
    
    def decrypt_data(self, encrypted_data):
        """Decrypt sensitive data"""
        return self.cipher_suite.decrypt(encrypted_data).decode()
    
    def log_activity(self, user_id, action, details):
        """Log user activity"""
        self.activity_log.append({
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'action': action,
            'details': details
        })
    
    def validate_access_key(self, access_key):
        """Validate the provided access key with enhanced security"""
        # Check if user is temporarily locked out
        user_ip = self.get_user_ip()
        if user_ip in self.failed_attempts:
            last_attempt, attempts = self.failed_attempts[user_ip]
            if attempts >= self.max_attempts and datetime.now() - last_attempt < self.lockout_time:
                return {
                    "valid": False,
                    "access_level": "none",
                    "message": "❌ Too many failed attempts. Please try again in 15 minutes."
                }
        
        access_key = access_key.strip().upper()
        
        # Check if key exists
        if access_key in self.valid_access_keys:
            # Reset failed attempts on success
            if user_ip in self.failed_attempts:
                del self.failed_attempts[user_ip]
                
            return {
                "valid": True,
                "access_level": self.valid_access_keys[access_key],
                "message": "✅ Access granted to Advanced Threat Analysis"
            }
        else:
            # Track failed attempts
            if user_ip not in self.failed_attempts:
                self.failed_attempts[user_ip] = (datetime.now(), 1)
            else:
                last_attempt, attempts = self.failed_attempts[user_ip]
                self.failed_attempts[user_ip] = (datetime.now(), attempts + 1)
                
            remaining_attempts = self.max_attempts - self.failed_attempts[user_ip][1]
            if remaining_attempts <= 0:
                return {
                    "valid": False,
                    "access_level": "none",
                    "message": "❌ Too many failed attempts. Please try again in 15 minutes."
                }
                
            return {
                "valid": False,
                "access_level": "none",
                "message": f"❌ Invalid access key. {remaining_attempts} attempts remaining."
            }
    
    def check_access(self):
        """Check if user has access to advanced features"""
        if 'advanced_access' not in st.session_state:
            st.session_state.advanced_access = False
        if 'access_level' not in st.session_state:
            st.session_state.access_level = "none"
        
        # Check session timeout
        if 'login_time' in st.session_state:
            login_time = datetime.fromisoformat(st.session_state.login_time)
            if datetime.now() - login_time > self.session_timeout:
                # Session expired
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                return False
        
        return st.session_state.advanced_access
    
    def get_user_ip(self):
        """Get user IP address for security tracking"""
        try:
            # This is a simplified approach - in production, use proper IP detection
            return str(hash(str(st.session_state.get('user_id', 'anonymous'))))
        except:
            return "unknown"
    
    def generate_secure_token(self):
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)
    
    def get_activity_log(self, user_id=None):
        """Get activity log, optionally filtered by user"""
        if user_id:
            return [log for log in self.activity_log if log['user_id'] == user_id]
        return self.activity_log

# Initialize security manager
security_manager = SecurityManager()

# Enhanced Secure Encryption with Fernet
class SecureEncryptor:
    def __init__(self):
        # Get encryption key from environment variable
        encryption_key = os.environ.get("ENCRYPTION_KEY")
        
        if not encryption_key:
            # For demo purposes only - in production, this should always come from environment
            # Generate a key if none exists (for demo only)
            if 'demo_key' not in st.session_state:
                key = Fernet.generate_key()
                st.session_state.demo_key = key.decode()
            encryption_key = st.session_state.demo_key
        else:
            # Ensure the key is in the correct format
            if not encryption_key.startswith("fernet:"):
                encryption_key = f"fernet:{encryption_key}"
        
        # Use the key for Fernet
        try:
            if encryption_key.startswith("fernet:"):
                key = encryption_key[7:].encode()
            else:
                key = encryption_key.encode()
                
            self.cipher_suite = Fernet(key)
        except Exception as e:
            st.error(f"Encryption setup error: {e}")
            # Fallback to basic encoding if encryption fails
            self.cipher_suite = None
    
    def encrypt(self, text):
        """Encrypt text using Fernet encryption"""
        if self.cipher_suite:
            try:
                encrypted = self.cipher_suite.encrypt(text.encode())
                return f"enc_fernet_{base64.b64encode(encrypted).decode()}"
            except Exception as e:
                st.error(f"Encryption error: {e}")
                # Fallback to basic encoding
                return f"enc_base64_{base64.b64encode(text.encode()).decode()}"
        else:
            # Fallback to basic encoding
            return f"enc_base64_{base64.b64encode(text.encode()).decode()}"
    
    def decrypt(self, text):
        """Decrypt text using Fernet encryption"""
        if text.startswith("enc_fernet_"):
            if self.cipher_suite:
                try:
                    encrypted = base64.b64decode(text[11:])
                    decrypted = self.cipher_suite.decrypt(encrypted)
                    return decrypted.decode()
                except Exception as e:
                    st.error(f"Decryption error: {e}")
                    return text
            else:
                return text
        elif text.startswith("enc_base64_"):
            try:
                decoded = base64.b64decode(text[11:]).decode()
                return decoded
            except:
                return text
        else:
            return text

# Enhanced Authentication System with Multi-User Support
class EnhancedAuthenticationSystem:
    def __init__(self):
        self.users_file = "users.json"
        self.failed_attempts = {}
        self.lockout_time = timedelta(minutes=15)
        self.max_attempts = 5
        self.session_timeout = timedelta(minutes=30)
        self.load_users()
        
    def load_users(self):
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            else:
                # Default admin user - should be changed after first login
                self.users = {
                    "admin": {
                        "password": self.hash_password("brandguardian2024"),  # Changed default password
                        "access_level": "admin",
                        "subscription_tier": "premium",  # Admin gets premium for free
                        "company": "Brand Guardian AI",  # Changed company name
                        "email": "admin@brandguardian.com",  # Changed email
                        "user_id": str(uuid.uuid4()),
                        "created_at": datetime.now().isoformat(),
                        "last_login": None,
                        "failed_attempts": 0,
                        "last_failed_attempt": None,
                        "session_token": None,
                        "mfa_enabled": False,
                        "profile": {
                            "avatar": "👤",
                            "bio": "System Administrator",
                            "preferences": {
                                "theme": "dark",
                                "notifications": True,
                                "language": "en"
                            }
                        },
                        "privileges": SUBSCRIPTION_TIERS["premium"]["privileges"]  # Admin gets all privileges
                    }
                }
                self.save_users()
        except:
            self.users = {}
    
    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    
    def register_user(self, username, password, company, email, access_level="client", subscription_tier="basic"):
        """Register a new client user"""
        if username in self.users:
            return False, "Username already exists"
        
        # Password strength validation
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r"[0-9]", password):
            return False, "Password must contain at least one number"
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"
        
        self.users[username] = {
            "password": self.hash_password(password),
            "access_level": access_level,
            "subscription_tier": subscription_tier,
            "company": company,
            "email": email,
            "user_id": str(uuid.uuid4()),
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "failed_attempts": 0,
            "last_failed_attempt": None,
            "session_token": None,
            "mfa_enabled": False,
            "profile": {
                "avatar": "👤",
                "bio": f"User at {company}",
                "preferences": {
                    "theme": "dark",
                    "notifications": True,
                    "language": "en"
                }
            },
            "privileges": SUBSCRIPTION_TIERS[subscription_tier]["privileges"]  # Set privileges based on subscription
        }
        self.save_users()
        return True, "User registered successfully"
    
    def authenticate(self, username, password):
        """Authenticate a user with enhanced security"""
        if username not in self.users:
            return False, "User not found"
        
        # Check if account is locked
        user_data = self.users[username]
        if user_data.get('failed_attempts', 0) >= self.max_attempts:
            last_attempt = user_data.get('last_failed_attempt')
            if last_attempt and (datetime.now() - datetime.fromisoformat(last_attempt)) < self.lockout_time:
                return False, "Account locked. Please try again in 15 minutes."
            else:
                # Reset failed attempts after lockout period
                user_data['failed_attempts'] = 0
        
        if self.verify_password(user_data["password"], password):
            # Reset failed attempts on successful login
            user_data['failed_attempts'] = 0
            user_data['last_login'] = datetime.now().isoformat()
            
            # Generate session token
            session_token = security_manager.generate_secure_token()
            user_data['session_token'] = session_token
            
            # Log activity
            security_manager.log_activity(user_data['user_id'], "login", f"User {username} logged in")
            
            self.save_users()
            return True, "Authentication successful"
        else:
            # Increment failed attempts
            user_data['failed_attempts'] = user_data.get('failed_attempts', 0) + 1
            user_data['last_failed_attempt'] = datetime.now().isoformat()
            
            # Log failed attempt
            security_manager.log_activity(user_data['user_id'], "failed_login", f"Failed login attempt for {username}")
            
            self.save_users()
            
            remaining_attempts = self.max_attempts - user_data['failed_attempts']
            if remaining_attempts <= 0:
                return False, "Account locked. Please try again in 15 minutes."
            else:
                return False, f"Invalid password. {remaining_attempts} attempts remaining."
    
    def update_user_subscription(self, username, subscription_tier):
        """Update user subscription tier"""
        if username in self.users:
            self.users[username]['subscription_tier'] = subscription_tier
            # Update privileges based on new subscription tier
            self.users[username]['privileges'] = SUBSCRIPTION_TIERS[subscription_tier]["privileges"]
            self.save_users()
            security_manager.log_activity(self.users[username]['user_id'], "subscription_update", f"Subscription updated to {subscription_tier}")
            return True
        return False
    
    def get_user_subscription(self, username):
        """Get user subscription tier"""
        if username in self.users:
            return self.users[username].get('subscription_tier', 'basic')
        return 'basic'
    
    def update_user_privileges(self, username, privileges):
        """Update user privileges"""
        if username in self.users:
            self.users[username]['privileges'] = privileges
            self.save_users()
            security_manager.log_activity(self.users[username]['user_id'], "privileges_update", f"Privileges updated for {username}")
            return True
        return False
    
    def get_user_privileges(self, username):
        """Get user privileges"""
        if username in self.users:
            return self.users[username].get('privileges', [])
        return []
    
    def update_user_profile(self, username, profile_data):
        """Update user profile information"""
        if username in self.users:
            self.users[username]['profile'].update(profile_data)
            self.save_users()
            security_manager.log_activity(self.users[username]['user_id'], "profile_update", f"Profile updated for {username}")
            return True
        return False
    
    def get_user_profile(self, username):
        """Get user profile information"""
        if username in self.users:
            return self.users[username].get('profile', {})
        return {}

# Enhanced API Key Manager with User Isolation
class EnhancedAPIKeyManager:
    def __init__(self):
        self.encryptor = SecureEncryptor()
        self.api_keys_dir = "api_keys"
        os.makedirs(self.api_keys_dir, exist_ok=True)
        
        # Add the supported_platforms attribute that was missing
        self.supported_platforms = {
            "twitter": {
                "name": "Twitter API v2",
                "icon": "🐦",
                "help_url": "https://developer.twitter.com/",
                "field_name": "Bearer Token",
                "field_help": "Enter your Twitter Bearer Token from developer portal",
                "rate_limit": "500,000 tweets/month"
            },
            "facebook": {
                "name": "Facebook Graph API",
                "icon": "📘",
                "help_url": "https://developers.facebook.com/",
                "field_name": "Access Token",
                "field_help": "Enter your Facebook Access Token with pages permissions",
                "rate_limit": "200 calls/hour"
            },
            "instagram": {
                "name": "Instagram Graph API",
                "icon": "📸",
                "help_url": "https://developers.facebook.com/docs/instagram-api",
                "field_name": "Access Token",
                "field_help": "Enter your Instagram Access Token for business account",
                "rate_limit": "200 calls/hour"
            },
            "google": {
                "name": "Google APIs",
                "icon": "🔍",
                "help_url": "https://console.cloud.google.com/",
                "field_name": "API Key",
                "field_help": "Enter your Google Cloud API Key",
                "rate_limit": "10,000 requests/day"
            },
            "youtube": {
                "name": "YouTube Data API",
                "icon": "📺",
                "help_url": "https://developers.google.com/youtube",
                "field_name": "API Key",
                "field_help": "Enter your YouTube Data API key",
                "rate_limit": "10,000 units/day"
            },
            "reddit": {
                "name": "Reddit API",
                "icon": "🔴",
                "help_url": "https://www.reddit.com/dev/api/",
                "field_name": "API Key",
                "field_help": "Enter your Reddit API key",
                "rate_limit": "60 calls/minute"
            },
            "tiktok": {
                "name": "TikTok Business API",
                "icon": "🎵",
                "help_url": "https://developers.tiktok.com/",
                "field_name": "Access Token",
                "field_help": "Enter your TikTok Business API access token",
                "rate_limit": "1,000 calls/day"
            },
            "openai": {
                "name": "OpenAI API",
                "icon": "🤖",
                "help_url": "https://platform.openai.com/",
                "field_name": "API Key",
                "field_help": "Enter your OpenAI API key for AI analysis",
                "rate_limit": "3,500 requests/day"
            },
            "google_analytics": {
                "name": "Google Analytics",
                "icon": "📊",
                "help_url": "https://analytics.google.com/",
                "field_name": "Property ID",
                "field_help": "Enter your GA4 Property ID (format: properties/XXXXXX)",
                "rate_limit": "50,000 requests/day"
            },
            "linkedin": {
                "name": "LinkedIn Marketing API",
                "icon": "💼",
                "help_url": "https://developer.linkedin.com/",
                "field_name": "Access Token",
                "field_help": "Enter your LinkedIn Marketing API access token",
                "rate_limit": "100 calls/day"
            }
        }
        
    def get_user_file(self, user_id):
        """Get the API key file for a specific user"""
        return os.path.join(self.api_keys_dir, f"{user_id}_keys.json")
    
    def load_api_keys(self, user_id):
        """Load API keys for a specific user"""
        user_file = self.get_user_file(user_id)
        try:
            if os.path.exists(user_file):
                with open(user_file, 'r') as f:
                    return json.load(f)
            else:
                return {}
        except:
            return {}
    
    def save_api_keys(self, user_id, api_keys):
        """Save API keys for a specific user"""
        user_file = self.get_user_file(user_id)
        with open(user_file, 'w') as f:
            json.dump(api_keys, f, indent=2)
    
    def get_api_key(self, user_id, platform):
        """Get API key for a specific user and platform"""
        api_keys = self.load_api_keys(user_id)
        if platform in api_keys:
            return self.encryptor.decrypt(api_keys[platform])
        return None
    
    def save_api_key(self, user_id, platform, api_key):
        """Save API key for a specific user and platform"""
        api_keys = self.load_api_keys(user_id)
        if api_key:
            api_keys[platform] = self.encryptor.encrypt(api_key)
            self.save_api_keys(user_id, api_keys)
            return True
        return False
    
    def delete_api_key(self, user_id, platform):
        """Delete API key for a specific user and platform"""
        api_keys = self.load_api_keys(user_id)
        if platform in api_keys:
            del api_keys[platform]
            self.save_api_keys(user_id, api_keys)
            return True
        return False
    
    def test_connection(self, platform, api_key):
        try:
            time.sleep(1)
            success_rate = 0.9
            
            if random.random() < success_rate:
                return {
                    "success": True,
                    "message": f"✅ Successfully connected to {self.supported_platforms[platform]['name']}",
                    "platform": platform,
                    "rate_limit": self.supported_platforms[platform]['rate_limit']
                }
            else:
                return {
                    "success": False,
                    "message": f"❌ Failed to connect to {self.supported_platforms[platform]['name']}",
                    "suggestion": "Please check your API key and try again."
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Connection error: {str(e)}"
            }

# Initialize enhanced authentication and API manager
auth_system = EnhancedAuthenticationSystem()
api_manager = EnhancedAPIKeyManager()

# Advanced Data Visualization with Plotly
class AdvancedVisualizations:
    def __init__(self):
        self.colors = {
            'primary': '#FFD700',
            'secondary': '#FFA500',
            'success': '#66bb6a',
            'warning': '#ffa726',
            'danger': '#ff6b6b',
            'info': '#29b6f6',
            'dark': '#000000',
            'light': '#FFD700'
        }
    
    def create_threat_radar_chart(self, data, labels, title):
        """Create an enhanced radar chart using Plotly"""
        if not PLOTLY_AVAILABLE:
            st.error("Plotly is not installed. Charts cannot be displayed.")
            return None
            
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=data,
            theta=labels,
            fill='toself',
            name='Threat Level',
            line_color=self.colors['primary'],
            fillcolor=f'rgba(255, 215, 0, 0.3)',
            marker=dict(
                size=8,
                color=self.colors['primary'],
                symbol='circle'
            )
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(data) * 1.1]
                )
            ),
            title=title,
            title_font=dict(size=18, color=self.colors['primary']),
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='white')
        )
        
        return fig
    
    def create_sentiment_timeline(self, dates, values, title):
        """Create an enhanced sentiment timeline using Plotly"""
        if not PLOTLY_AVAILABLE:
            st.error("Plotly is not installed. Charts cannot be displayed.")
            return None
            
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines+markers',
            name='Sentiment Score',
            line=dict(
                color=self.colors['primary'],
                width=3
            ),
            marker=dict(
                size=8,
                color=self.colors['primary'],
                symbol='circle'
            )
        ))
        
        # Add a trend line
        z = np.polyfit(range(len(dates)), values, 1)
        p = np.poly1d(z)
        trend_line = p(range(len(dates)))
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=trend_line,
            mode='lines',
            name='Trend',
            line=dict(
                color=self.colors['secondary'],
                width=2,
                dash='dash'
            )
        ))
        
        fig.update_layout(
            title=title,
            title_font=dict(size=18, color=self.colors['primary']),
            xaxis_title='Date',
            yaxis_title='Sentiment Score',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='white'),
            xaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',
                tickfont=dict(color='white')
            ),
            yaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',
                tickfont=dict(color='white')
            )
        )
        
        return fig
    
    def create_threat_distribution(self, data, title):
        """Create an enhanced donut chart for threat distribution using Plotly"""
        if not PLOTLY_AVAILABLE:
            st.error("Plotly is not installed. Charts cannot be displayed.")
            return None
            
        labels = list(data.keys())
        values = list(data.values())
        colors = [self.colors['danger'], self.colors['warning'], self.colors['success']]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.7,
            marker_colors=colors,
            textinfo='label+percent',
            textfont=dict(color='white', size=12),
            hoverinfo='label+value+percent'
        )])
        
        fig.update_layout(
            title=title,
            title_font=dict(size=18, color=self.colors['primary']),
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='white'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=0.1,
                xanchor="center",
                x=0.5
            )
        )
        
        return fig
    
    def create_threat_heatmap(self, data, title):
        """Create a threat heatmap using Plotly"""
        if not PLOTLY_AVAILABLE:
            st.error("Plotly is not installed. Charts cannot be displayed.")
            return None
            
        fig = go.Figure(data=go.Heatmap(
            z=data,
            colorscale='YlOrRd',
            showscale=True
        ))
        
        fig.update_layout(
            title=title,
            title_font=dict(size=18, color=self.colors['primary']),
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='white'),
            xaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',
                tickfont=dict(color='white')
            ),
            yaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',
                tickfont=dict(color='white')
            )
        )
        
        return fig
    
    def create_threat_gauge(self, value, title, min_val=0, max_val=100):
        """Create a threat gauge using Plotly"""
        if not PLOTLY_AVAILABLE:
            st.error("Plotly is not installed. Charts cannot be displayed.")
            return None
            
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, max_val]},
                'bar': {'color': self.colors['primary']},
                'steps': [
                    {'range': [0, max_val * 0.33], 'color': self.colors['success']},
                    {'range': [max_val * 0.33, max_val * 0.66], 'color': self.colors['warning']},
                    {'range': [max_val * 0.66, max_val], 'color': self.colors['danger']}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_val * 0.8
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='white')
        )
        
        return fig

# Initialize visualizations
viz = AdvancedVisualizations()

# User registration and management functions
def show_user_registration():
    st.subheader("👥 Client Registration")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username", help="Choose a username for the client")
            company = st.text_input("Company Name", help="Client's company name")
            subscription_tier = st.selectbox("Subscription Tier", ["basic", "advanced", "premium"], 
                                         format_func=lambda x: f"{x.title()} - {SUBSCRIPTION_TIERS[x]['price']}")
        
        with col2:
            password = st.text_input("Password", type="password", help="Set a secure password (min 8 chars, upper/lowercase, number, special char)")
            email = st.text_input("Email", help="Client's email address")
        
        submitted = st.form_submit_button("Register Client", use_container_width=True)
        
        if submitted:
            if all([username, password, company, email]):
                success, message = auth_system.register_user(username, password, company, email, "client", subscription_tier)
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                else:
                    st.error(f"❌ {message}")
            else:
                st.error("Please fill all fields")

def show_subscription_plans():
    """Display subscription plans"""
    st.subheader("💳 Subscription Plans")
    
    col1, col2, col3 = st.columns(3)
    
    tiers = ["basic", "advanced", "premium"]
    
    for i, tier in enumerate(tiers):
        tier_info = SUBSCRIPTION_TIERS[tier]
        
        with [col1, col2, col3][i]:
            st.markdown(f"""
            <div class="tier-card {'premium' if tier == 'premium' else ''}">
                <h3>{tier_info['name']}</h3>
                <div class="tier-price">{tier_info['price']}</div>
                <ul class="tier-features">
                    {''.join([f'<li>{feature}</li>' for feature in tier_info['features']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Choose {tier_info['name']}", key=f"choose_{tier}"):
                # In a real application, this would process payment
                st.success(f"Redirecting to {tier_info['name']} plan checkout...")

def show_user_management():
    st.subheader("👥 User Management")
    
    # Check if user is admin
    if st.session_state.get('user_access_level') != 'admin':
        st.error("⛔ Administrator access required")
        st.info("Only administrators can access user management features.")
        return
    
    # Admin statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="admin-stat">
            <div class="admin-stat-value">{}</div>
            <div class="admin-stat-label">Total Users</div>
        </div>
        """.format(len(auth_system.users)), unsafe_allow_html=True)
    
    with col2:
        active_users = sum(1 for user in auth_system.users.values() if user.get('last_login'))
        st.markdown("""
        <div class="admin-stat">
            <div class="admin-stat-value">{}</div>
            <div class="admin-stat-label">Active Users</div>
        </div>
        """.format(active_users), unsafe_allow_html=True)
    
    with col3:
        premium_users = sum(1 for user in auth_system.users.values() if user.get('subscription_tier') == 'premium')
        st.markdown("""
        <div class="admin-stat">
            <div class="admin-stat-value">{}</div>
            <div class="admin-stat-label">Premium Users</div>
        </div>
        """.format(premium_users), unsafe_allow_html=True)
    
    with col4:
        failed_logins = len([log for log in security_manager.activity_log if log['action'] == 'failed_login'])
        st.markdown("""
        <div class="admin-stat">
            <div class="admin-stat-value">{}</div>
            <div class="admin-stat-label">Failed Logins</div>
        </div>
        """.format(failed_logins), unsafe_allow_html=True)
    
    # Show existing users
    st.write("### Existing Users")
    users_data = []
    for username, user_info in auth_system.users.items():
        users_data.append({
            "Username": username,
            "Company": user_info.get("company", "N/A"),
            "Email": user_info.get("email", "N/A"),
            "Access Level": user_info.get("access_level", "client"),
            "Subscription": user_info.get("subscription_tier", "basic").title(),
            "Last Login": user_info.get("last_login", "Never"),
            "Created": user_info.get("created_at", "N/A")[:10] if user_info.get("created_at") else "N/A",
            "Status": "Active" if user_info.get('failed_attempts', 0) < 5 else "Locked"
        })
    
    if users_data:
        st.dataframe(pd.DataFrame(users_data), use_container_width=True)
    else:
        st.info("No users registered yet")
    
    # User subscription management
    st.markdown("---")
    st.subheader("💳 User Subscription Management")
    
    user_to_manage = st.selectbox("Select User", list(auth_system.users.keys()))
    
    if user_to_manage:
        current_subscription = auth_system.get_user_subscription(user_to_manage)
        new_subscription = st.selectbox(
            "New Subscription Tier",
            ["basic", "advanced", "premium"],
            index=["basic", "advanced", "premium"].index(current_subscription)
        )
        
        if st.button("Update Subscription", use_container_width=True):
            if new_subscription != current_subscription:
                auth_system.update_user_subscription(user_to_manage, new_subscription)
                st.success(f"✅ Subscription updated to {new_subscription.title()}")
                st.rerun()
            else:
                st.info("No changes made")
    
    # User privilege management
    st.markdown("---")
    st.subheader("🔑 User Privilege Management")
    
    user_to_manage = st.selectbox("Select User for Privilege Management", list(auth_system.users.keys()))
    
    if user_to_manage:
        current_privileges = auth_system.get_user_privileges(user_to_manage)
        
        st.write(f"### Current Privileges for {user_to_manage}")
        
        # Create privilege toggles
        all_privileges = [
            "basic_monitoring", "basic_reports", "ai_analysis", 
            "competitor_tracking", "crisis_management", "api_access"
        ]
        
        new_privileges = []
        
        for privilege in all_privileges:
            is_enabled = privilege in current_privileges
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{privilege.replace('_', ' ').title()}**")
            
            with col2:
                # Custom toggle switch
                toggle_key = f"toggle_{user_to_manage}_{privilege}"
                toggle_value = st.checkbox(
                    "", 
                    value=is_enabled,
                    key=toggle_key
                )
                
                if toggle_value:
                    new_privileges.append(privilege)
        
        if st.button("Update Privileges", use_container_width=True):
            if new_privileges != current_privileges:
                auth_system.update_user_privileges(user_to_manage, new_privileges)
                st.success(f"✅ Privileges updated for {user_to_manage}")
                st.rerun()
            else:
                st.info("No changes made")
    
    # Registration form
    st.markdown("---")
    show_user_registration()
    
    # User actions (delete, reset password)
    st.markdown("---")
    st.subheader("User Actions")
    
    user_to_manage = st.selectbox("Select User for Actions", list(auth_system.users.keys()))
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Reset Password", use_container_width=True):
            if user_to_manage:
                # In a real application, you would send a password reset email
                st.info(f"Password reset initiated for {user_to_manage}. An email has been sent with instructions.")
                security_manager.log_activity(auth_system.users[user_to_manage]['user_id'], "password_reset", f"Password reset for {user_to_manage}")
    
    with col2:
        if st.button("Delete User", use_container_width=True, type="secondary"):
            if user_to_manage and user_to_manage != st.session_state.username:
                if st.checkbox(f"Confirm deletion of {user_to_manage}"):
                    del auth_system.users[user_to_manage]
                    auth_system.save_users()
                    security_manager.log_activity(auth_system.users[user_to_manage]['user_id'], "user_deleted", f"User {user_to_manage} deleted")
                    st.success(f"User {user_to_manage} deleted")
                    st.rerun()
            elif user_to_manage == st.session_state.username:
                st.error("You cannot delete your own account")
    
    # Activity log
    st.markdown("---")
    st.subheader("📋 Recent Activity Log")
    
    activity_logs = security_manager.get_activity_log()[-10:]  # Get last 10 activities
    for log in reversed(activity_logs):
        st.markdown(f"""
        <div class="activity-log">
            <div class="activity-time">{datetime.fromisoformat(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}</div>
            <div><strong>Action:</strong> {log['action']}</div>
            <div><strong>User ID:</strong> {log['user_id']}</div>
            <div><strong>Details:</strong> {log['details']}</div>
        </div>
        """, unsafe_allow_html=True)

def show_login_form():
    """Display login form with enhanced design"""
    st.markdown("""
    <div class="login-bg"></div>
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style="font-size: 3rem; font-weight: 800; background: linear-gradient(90deg, #FFD700 0%, #FFA500 55%, #FF8C00 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🔒 Brand Guardian AI</h1>
        <p style="font-size: 1.2rem; color: #FFD700;">Advanced Brand Protection & Threat Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two-column layout for login
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style='text-align: center;'>
            <div style="font-size: 6rem; margin-bottom: 20px;" class="security-shield">🛡️</div>
            <h3 style="color: white;">Secure Login</h3>
            <p style="color: #FFD700;">Access your brand protection dashboard</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("👤 Username")
            password = st.text_input("🔒 Password", type="password")
            
            # Remember me checkbox
            remember_me = st.checkbox("Remember me")
            
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit:
                success, message = auth_system.authenticate(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_access_level = auth_system.users[username]["access_level"]
                    st.session_state.subscription_tier = auth_system.users[username]["subscription_tier"]
                    st.session_state.user_id = auth_system.users[username]["user_id"]
                    st.session_state.login_time = datetime.now().isoformat()
                    st.session_state.remember_me = remember_me
                    
                    st.success("✅ Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    # Security information
    with st.expander("🔒 Security Information"):
        st.markdown("""
        - All credentials are encrypted using military-grade encryption
        - Multi-factor authentication ready
        - Session timeout after 30 minutes of inactivity
        - All login attempts are logged and monitored
        - Regular security audits conducted
        """)
    
    # Forgot password link
    st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <a href='#' style='color: #FFD700; text-decoration: none;'>Forgot your password?</a>
    </div>
    """, unsafe_allow_html=True)

# Advanced Threat Analysis Functionality
def show_advanced_threat_analysis():
    if not security_manager.check_access():
        show_access_required()
        return
    
    st.header("🔍 Advanced Threat Analysis")
    st.success("✅ Premium Access Granted - Advanced Features Unlocked")
    
    # Tab system for advanced analysis
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Threat Dashboard",
        "🔍 Search Analysis",
        "📈 Trend Analysis", 
        "⚡ Quick Actions"
    ])
    
    with tab1:
        show_threat_dashboard()
    
    with tab2:
        show_search_analysis()
    
    with tab3:
        show_trend_analysis()
    
    with tab4:
        show_quick_actions()

def show_threat_dashboard():
    """Threat monitoring dashboard with enhanced animations"""
    st.subheader("🛡️ Real-time Threat Dashboard")
    
    # Enhanced threat animation
    st.markdown("""
    <div class="threat-animation">
        <div class="threat-wave"></div>
        <div class="threat-pulse"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create metrics with custom styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Active Threats</h3>
            <h1>18</h1>
            <p style="color: #ff6b6b;">+5 from yesterday</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Threat Level</h3>
            <h1>High</h1>
            <p style="color: #ff6b6b;">Elevated risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Response Time</h3>
            <h1>2.1s</h1>
            <p style="color: #66bb6a;">-0.4s improvement</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Protected Assets</h3>
            <h1>24</h1>
            <p style="color: #66bb6a;">Fully secured</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Threat timeline with enhanced visualization
    st.subheader("📈 Threat Timeline (7 Days)")
    
    # Generate sample data with valid dates
    dates = pd.date_range(end=datetime.now(), periods=7)
    threats = [8, 12, 5, 18, 10, 7, 14]
    
    # Create an enhanced chart
    fig = viz.create_sentiment_timeline(dates, threats, "Threat Activity Over Time")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Threat distribution with enhanced visualization
    st.subheader("🌡️ Threat Distribution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        threat_data = {'High': 8, 'Medium': 5, 'Low': 5}
        fig = viz.create_threat_distribution(threat_data, "Threat Severity Distribution")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="search-analysis-card">
            <h4>📊 Threat Insights</h4>
            <p><span class="threat-high">High</span>: 8 threats detected</p>
            <p><span class="threat-medium">Medium</span>: 5 threats detected</p>
            <p><span class="threat-low">Low</span>: 5 threats detected</p>
            <p>Most active platform: Twitter</p>
            <p>Peak time: 14:00-16:00</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Threat gauge visualization
    st.subheader("🎯 Threat Intensity Gauge")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig = viz.create_threat_gauge(75, "Overall Threat Level")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = viz.create_threat_gauge(60, "Response Urgency")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        fig = viz.create_threat_gauge(85, "Impact Assessment")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent threats table
    st.subheader("🚨 Recent Threat Alerts")
    
    threat_alerts = []
    for i in range(8):
        threat_alerts.append({
            'Time': (datetime.now() - timedelta(hours=i)).strftime("%H:%M"),
            'Platform': random.choice(['Twitter', 'Facebook', 'Reddit', 'Instagram']),
            'Type': random.choice(['Impersonation', 'Negative Review', 'Fake Account', 'Copyright']),
            'Severity': random.choice(['High', 'Medium', 'Low']),
            'Status': random.choice(['Active', 'Resolved', 'Monitoring'])
        })
    
    alert_df = pd.DataFrame(threat_alerts)
    st.dataframe(
        alert_df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Time": st.column_config.TextColumn("Time", width="small"),
            "Platform": st.column_config.TextColumn("Platform", width="small"),
            "Type": st.column_config.TextColumn("Type", width="medium"),
            "Severity": st.column_config.TextColumn("Severity", width="small"),
            "Status": st.column_config.TextColumn("Status", width="small")
        }
    )

def show_search_analysis():
    """Search analysis functionality"""
    st.subheader("🔍 Advanced Search Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_area(
            "Enter search query or keywords to analyze:",
            height=100,
            placeholder="Example: 'Your Brand scam complaints customer service issues'",
            help="Enter keywords, phrases, or full sentences to analyze for brand threats"
        )
        
        # Get the brand name from session state or use a default
        brand_name = st.session_state.get('brand_name', 'Your Brand')
        
        if st.button("🚀 Analyze Threats", use_container_width=True):
            if search_query and brand_name:
                with st.spinner("🔍 Analyzing threats..."):
                    time.sleep(2)
                    # Get user subscription tier
                    subscription_tier = st.session_state.get('subscription_tier', 'basic')
                    results = ai_system.analyze_threat(search_query, brand_name, subscription_tier)
                    st.session_state.search_results = results
                    st.success("Analysis complete!")
            else:
                st.error("Please enter both search query and brand name")
    
    with col2:
        st.markdown("""
        <div class="search-analysis-card">
            <h4>🎯 Search Analysis Tips</h4>
            <p>• Use specific keywords</p>
            <p>• Include brand names</p>
            <p>• Add negative modifiers</p>
            <p>• Use quotation marks for phrases</p>
            <p>• Include platform names</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="search-analysis-card">
            <h4>📊 Threat Levels</h4>
            <p><span class="threat-high">High</span> - Immediate action needed</p>
            <p><span class="threat-medium">Medium</span> - Monitor closely</p>
            <p><span class="threat-low">Low</span> - Standard monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display results if available
    if 'search_results' in st.session_state:
        results = st.session_state.search_results
        
        st.markdown("---")
        st.subheader("📋 Analysis Results")
        
        # Subscription tier indicator
        subscription_tier = results.get('subscription_tier', 'basic')
        st.markdown(f"""
        <div class="subscription-status status-{subscription_tier}">
            {subscription_tier.title()} Plan
        </div>
        """, unsafe_allow_html=True)
        
        # Threat level indicator
        threat_class = f"threat-{results['threat_level']}"
        st.markdown(f"""
        <div class="search-analysis-card">
            <h4>Threat Level: <span class="{threat_class}">{results['threat_level'].upper()}</span></h4>
            <p><strong>Query:</strong> {results['query']}</p>
            <p><strong>Brand:</strong> {results['brand']}</p>
            <p><strong>Keywords Found:</strong> {', '.join(results['keywords_found']) or 'None'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Analysis and recommendations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="search-analysis-card">
                <h4>📝 Analysis</h4>
                <p>{results['analysis']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="search-analysis-card">
                <h4>✅ Recommendations</h4>
                {''.join([f'<p>• {rec}</p>' for rec in results['recommendations']])}
            </div>
            """, unsafe_allow_html=True)
        
        # AI Analysis (for advanced and premium tiers)
        if 'ai_insights' in results:
            st.subheader("🤖 AI-Powered Analysis")
            
            for insight in results['ai_insights']:
                confidence_class = f"confidence-{('high' if insight['confidence'] > 0.7 else 'medium' if insight['confidence'] > 0.5 else 'low')}"
                
                st.markdown(f"""
                <div class="ai-analysis-card">
                    <div class="ai-analysis-header">
                        <span class="ai-icon">🤖</span>
                        <h4>{insight['title']}</h4>
                        <span class="ai-confidence {confidence_class}">{int(insight['confidence'] * 100)}% confidence</span>
                    </div>
                    <p>{insight['content']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Enhanced metrics (for advanced and premium tiers)
        if 'sentiment_score' in results:
            st.subheader("📊 Enhanced Metrics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Sentiment Score", f"{results['sentiment_score']:.2f}", 
                         delta="Neutral" if 0.4 <= results['sentiment_score'] <= 0.6 else 
                              ("Positive" if results['sentiment_score'] > 0.6 else "Negative"))
            
            with col2:
                st.metric("Urgency Score", f"{results['urgency_score']:.2f}",
                         delta="High" if results['urgency_score'] > 0.7 else "Medium" if results['urgency_score'] > 0.4 else "Low")
            
            with col3:
                st.metric("Impact Score", f"{results['impact_score']:.2f}",
                         delta="High" if results['impact_score'] > 0.7 else "Medium" if results['impact_score'] > 0.4 else "Low")
            
            st.markdown(f"""
            <div class="search-analysis-card">
                <h4>🎯 Risk Assessment</h4>
                <p><strong>Overall Risk:</strong> {results['risk_assessment']}</p>
                <p><strong>Predicted Trend:</strong> {results['predicted_trend']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Similar threat examples
        st.subheader("🔍 Similar Threat Patterns")
        similar_threats = generate_similar_threats(results)
        for threat in similar_threats:
            st.markdown(f"""
            <div class="search-result-card">
                <p><strong>{threat['platform']}</strong> - {threat['content']}</p>
                <p>Severity: <span class="threat-{threat['severity']}">{threat['severity']}</span></p>
            </div>
            """, unsafe_allow_html=True)

def generate_similar_threats(results):
    """Generate similar threat examples"""
    threats = []
    for i in range(3):
        threats.append({
            'platform': random.choice(['Twitter', 'Reddit', 'Facebook', 'Instagram']),
            'content': f"Similar {results['threat_level']} threat pattern detected",
            'severity': results['threat_level'],
            'date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
        })
    return threats

def show_trend_analysis():
    """Trend analysis functionality with enhanced graphs"""
    st.subheader("📈 Threat Trend Analysis")
    
    # Generate trend data with valid dates
    dates = pd.date_range(end=datetime.now(), periods=30)
    high_threats = np.random.poisson(5, 30)
    medium_threats = np.random.poisson(10, 30)
    low_threats = np.random.poisson(20, 30)
    
    # Create enhanced multi-line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates, y=high_threats,
        mode='lines+markers',
        name='High Threats',
        line=dict(color='#ff6b6b', width=3),
        marker=dict(size=6, color='#ff6b6b')
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=medium_threats,
        mode='lines+markers',
        name='Medium Threats',
        line=dict(color='#ffa726', width=3),
        marker=dict(size=6, color='#ffa726')
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=low_threats,
        mode='lines+markers',
        name='Low Threats',
        line=dict(color='#66bb6a', width=3),
        marker=dict(size=6, color='#66bb6a')
    ))
    
    fig.update_layout(
        title='Threat Trends Over Time',
        title_font=dict(size=18, color='#FFD700'),
        xaxis_title='Date',
        yaxis_title='Number of Threats',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='white')
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.1,
            xanchor="center",
            x=0.5
        )
    )
    
    if PLOTLY_AVAILABLE:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Plotly is not installed. Charts cannot be displayed.")
    
    # Platform distribution with enhanced radar chart
    st.subheader("🌐 Threat Distribution by Platform")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        platforms = ['Twitter', 'Facebook', 'Reddit', 'Instagram', 'YouTube']
        threat_counts = [45, 32, 28, 19, 12]
        
        # Create radar chart
        fig = viz.create_threat_radar_chart(
            np.array(threat_counts),
            platforms,
            "Threat Distribution Across Platforms"
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="search-analysis-card">
            <h4>📊 Platform Insights</h4>
            <p>Twitter: 45 threats (42%)</p>
            <p>Facebook: 32 threats (30%)</p>
            <p>Reddit: 28 threats (26%)</p>
            <p>Instagram: 19 threats (18%)</p>
            <p>YouTube: 12 threats (11%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sentiment analysis over time with enhanced visualization
    st.subheader("📊 Sentiment Analysis")
    
    sentiment_dates = pd.date_range(end=datetime.now(), periods=14)
    sentiment_values = np.sin(np.linspace(0, 4*np.pi, 14)) * 0.5 + 0.5
    
    fig = go.Figure()
    
    # Add area chart for sentiment
    fig.add_trace(go.Scatter(
        x=sentiment_dates,
        y=sentiment_values,
        fill='tozeroy',
        fillcolor='rgba(255, 215, 0, 0.3)',
        line=dict(color='#FFD700', width=3),
        name='Sentiment Score'
    ))
    
    # Add threshold lines
    fig.add_hline(y=0.7, line_dash="dash", line_color="rgba(255, 0, 0, 0.5)", annotation_text="Positive Threshold")
    fig.add_hline(y=0.3, line_dash="dash", line_color="rgba(255, 165, 0, 0.5)", annotation_text="Negative Threshold")
    
    fig.update_layout(
        title='Sentiment Analysis Over Time',
        title_font=dict(size=18, color='#FFD700'),
        xaxis_title='Date',
        yaxis_title='Sentiment Score',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='white'),
            range=[0, 1]
        )
    )
    
    if PLOTLY_AVAILABLE:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Plotly is not installed. Charts cannot be displayed.")
    
    # Threat heatmap
    st.subheader("🔥 Threat Heatmap by Hour and Day")
    
    # Generate sample heatmap data
    hours = list(range(24))
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # Create random data for the heatmap
    heatmap_data = np.random.rand(7, 24) * 100
    
    fig = viz.create_threat_heatmap(heatmap_data, "Threat Intensity Heatmap")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

def show_quick_actions():
    """Quick action buttons"""
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Scan All Platforms", use_container_width=True):
            st.success("Platform scan initiated!")
            time.sleep(1)
            st.info("Scanning Twitter, Facebook, Instagram, Reddit...")
    
    with col2:
        if st.button("📊 Generate Report", use_container_width=True):
            st.success("Threat report generation started!")
            time.sleep(1)
            st.info("Compiling data from last 7 days...")
    
    with col3:
        if st.button("🚨 Crisis Protocol", use_container_width=True):
            st.error("Crisis protocol activated!")
            time.sleep(1)
            st.warning("Alerting team members...")

def show_access_required():
    st.header("🔒 Advanced Threat Analysis")
    st.warning("🚫 Premium Access Required")
    
    st.write("""
    ### Unlock Advanced Threat Analysis Features
    
    To access our premium threat detection capabilities, please enter your access key below.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        access_key = st.text_input(
            "Enter Access Key:",
            type="password"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🔓 Unlock Features", use_container_width=True):
            if access_key:
                result = security_manager.validate_access_key(access_key)
                if result["valid"]:
                    st.session_state.advanced_access = True
                    st.session_state.access_level = result["access_level"]
                    st.success(result["message"])
                    st.balloons()
                    st.rerun()
                else:
                    st.error(result["message"])
            else:
                st.error("Please enter an access key")
    
    with st.expander("🆓 Demo Access"):
        st.info("Use demo key: BG2024-PRO-ACCESS")  # Changed from "VR2024-PRO-ACCESS"
        if st.button("Use Demo Key"):
            st.session_state.advanced_access = True
            st.session_state.access_level = "full"
            st.success("Demo access granted!")
            st.balloons()
            st.rerun()
    
    # Show subscription plans
    show_subscription_plans()
    
    # Premium access card
    st.markdown("""
    <div class="premium-access-card">
        <h3>🌟 Premium Access Features</h3>
        <p>Unlock the full potential of Brand Guardian AI with our premium features:</p>
        <ul style="text-align: left; display: inline-block;">
            <li>Advanced threat detection algorithms</li>
            <li>Real-time monitoring across all platforms</li>
            <li>AI-powered sentiment analysis</li>
            <li>Customizable threat alerts</li>
            <li>Detailed threat intelligence reports</li>
            <li>Priority customer support</li>
        </ul>
        <p>Contact your administrator to get your premium access key.</p>
    </div>
    """, unsafe_allow_html=True)

# API Management Tab
def show_api_key_management():
    st.header("🔑 API Key Management Center")
    
    # Get current user's ID
    user_id = st.session_state.get('user_id')
    if not user_id:
        st.error("User not authenticated")
        return
    
    # Get user subscription tier
    subscription_tier = st.session_state.get('subscription_tier', 'basic')
    tier_info = SUBSCRIPTION_TIERS[subscription_tier]
    
    # Display subscription info
    st.markdown(f"""
    <div class="subscription-status status-{subscription_tier}">
        Current Plan: {tier_info['name']} - {tier_info['price']}
    </div>
    """, unsafe_allow_html=True)
    
    # Display current connections
    st.subheader("🌐 Connected Platforms")
    
    api_keys = api_manager.load_api_keys(user_id)
    if api_keys:
        cols = st.columns(3)
        for i, (platform, encrypted_key) in enumerate(api_keys.items()):
            if platform in api_manager.supported_platforms:
                platform_info = api_manager.supported_platforms[platform]
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="search-analysis-card">
                        <div style="font-size: 2rem; margin-bottom: 10px;">{platform_info['icon']}</div>
                        <h4>{platform_info['name']}</h4>
                        <p>Status: <span class="api-status-connected">✅ Connected</span></p>
                        <p>Rate Limit: {platform_info['rate_limit']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Disconnect {platform}", key=f"disconnect_{platform}", use_container_width=True):
                        if api_manager.delete_api_key(user_id, platform):
                            st.success(f"Disconnected from {platform_info['name']}")
                            st.rerun()
    else:
        st.info("🌟 Connect your first platform to get started!")
    
    # Add new connection
    st.subheader("🚀 Connect New Platform")
    
    platforms = api_manager.supported_platforms
    selected_platform = st.selectbox("Select Platform", list(platforms.keys()), 
                                   format_func=lambda x: f"{platforms[x]['icon']} {platforms[x]['name']}")
    
    platform_info = platforms[selected_platform]
    
    st.markdown(f"""
    <div class="search-analysis-card">
        <h4>{platform_info['icon']} {platform_info['name']}</h4>
        <p><strong>Rate Limit:</strong> {platform_info['rate_limit']}</p>
        <p><strong>Documentation:</strong> <a href="{platform_info['help_url']}" target="_blank">Get API Key →</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    api_key = st.text_input(
        f"{platform_info['field_name']}*",
        type="password",
        help=platform_info['field_help']
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧪 Test Connection", use_container_width=True):
            if api_key:
                with st.spinner("Testing..."):
                    result = api_manager.test_connection(selected_platform, api_key)
                if result["success"]:
                    st.success(result["message"])
                    st.info(f"Rate Limit: {result['rate_limit']}")
                else:
                    st.error(result["message"])
            else:
                st.error("Please enter API key")
    
    with col2:
        if st.button("💾 Save Connection", use_container_width=True):
            if api_key:
                if api_manager.save_api_key(user_id, selected_platform, api_key):
                    st.success("✅ Connection saved!")
                    st.balloons()
                else:
                    st.error("❌ Save failed")
            else:
                st.error("Please enter API key")
    
    with col3:
        if st.button("🔄 Clear", use_container_width=True):
            st.rerun()
    
    # Platform status
    st.subheader("📊 Platform Status")
    status_data = []
    for platform, info in api_manager.supported_platforms.items():
        status_data.append({
            "Platform": f"{info['icon']} {info['name']}",
            "Status": "✅ Connected" if platform in api_keys else "❌ Disconnected",
            "Rate Limit": info['rate_limit']
        })
    
    status_df = pd.DataFrame(status_data)
    st.dataframe(status_df, use_container_width=True, hide_index=True)

# Enhanced monitoring class
class EnhancedSocialMediaMonitor:
    def __init__(self):
        self.api_manager = api_manager
    
    def simulate_monitoring_with_api(self, brand_name, sector, subscription_tier):
        posts = []
        user_id = st.session_state.get('user_id')
        if not user_id:
            return posts
            
        tier_info = SUBSCRIPTION_TIERS[subscription_tier]
        max_platforms = 5 if subscription_tier == "basic" else 10 if subscription_tier == "advanced" else 20
        max_posts = 3 if subscription_tier == "basic" else 8 if subscription_tier == "advanced" else 15
        
        connected_platforms = list(api_manager.load_api_keys(user_id).keys()) or ['twitter', 'facebook', 'instagram']
        connected_platforms = connected_platforms[:max_platforms]
        
        for platform in connected_platforms:
            for _ in range(random.randint(1, max_posts)):
                posts.append({
                    'platform': platform.capitalize(),
                    'content': self.generate_business_post(brand_name, sector),
                    'author': f"user_{random.randint(1000, 9999)}",
                    'engagement': random.randint(50, 5000),
                    'api_connected': platform in api_manager.load_api_keys(user_id),
                    'ai_analyzed': tier_info['ai_analysis']
                })
        return posts
    
    def generate_business_post(self, brand_name, sector):
        templates = {
            'technology': [f"{brand_name} new feature launch", f"{brand_name} customer support issues"],
            'finance': [f"{brand_name} stock performance", f"{brand_name} financial results"],
            'retail': [f"{brand_name} product quality", f"{brand_name} store experience"]
        }
        return random.choice(templates.get(sector, templates['technology']))

# Initialize
enhanced_monitor = EnhancedSocialMediaMonitor()

# User AI Dashboard (for regular users)
def show_user_ai_dashboard():
    st.header("🤖 Brand Guardian AI Dashboard")
    
    # Welcome message with user's brand name
    brand_name = st.session_state.get('brand_name', 'Your Brand')
    st.success(f"Welcome to your brand protection dashboard, {brand_name}!")
    
    # Get user subscription tier
    subscription_tier = st.session_state.get('subscription_tier', 'basic')
    tier_info = SUBSCRIPTION_TIERS[subscription_tier]
    
    # User profile section
    user_profile = auth_system.get_user_profile(st.session_state.username)
    
    st.markdown(f"""
    <div class="user-profile-card">
        <div class="user-avatar">{user_profile.get('avatar', '👤')}</div>
        <h3>{st.session_state.username}</h3>
        <p>{user_profile.get('bio', 'Brand Protection Specialist')}</p>
        <p><strong>Company:</strong> {auth_system.users[st.session_state.username]['company']}</p>
        <div class="subscription-status status-{subscription_tier}">
            {tier_info['name']} Plan - {tier_info['price']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Brand Mentions</h3>
            <h1>142</h1>
            <p style="color: #66bb6a;">+12 from last week</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Threat Level</h3>
            <h1>Low</h1>
            <p style="color: #66bb6a;">Stable</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Response Rate</h3>
            <h1>92%</h1>
            <p style="color: #66bb6a;">Excellent</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main AI functionality for users
    st.subheader("🔍 Brand Threat Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Search Analysis", "Social Monitoring", "Reports"])
    
    with tab1:
        show_search_analysis()
    
    with tab2:
        st.header("Social Monitoring")
        posts = enhanced_monitor.simulate_monitoring_with_api(brand_name, st.session_state.sector, subscription_tier)
        for post in posts[:5]:
            with st.expander(f"{post['platform']} - {post['content'][:50]}..."):
                st.write(post['content'])
                st.caption(f"Engagement: {post['engagement']}")
                if post.get('ai_analyzed'):
                    st.markdown('<span class="ai-confidence confidence-high">AI Analyzed</span>', unsafe_allow_html=True)
    
    with tab3:
        st.header("📊 Brand Reports")
        st.info("Your brand reports will be generated here")
        
        if st.button("Generate Weekly Report", use_container_width=True):
            with st.spinner("Generating report..."):
                time.sleep(2)
                st.success("Report generated successfully!")
                
                # Sample report data
                report_data = {
                    "Period": "Last 7 days",
                    "Total Mentions": "142",
                    "Positive Sentiment": "68%",
                    "Negative Sentiment": "12%",
                    "Neutral Sentiment": "20%",
                    "Top Platforms": "Twitter, Instagram, Facebook",
                    "Recommendations": "Continue current strategy, focus on customer engagement"
                }
                
                for key, value in report_data.items():
                    st.write(f"**{key}:** {value}")

def main():
    # Add animated particles
    add_particles()
    
    # Check authentication first
    if not st.session_state.get('authenticated', False):
        show_login_form()
        return
    
    # Initialize session state
    if "sector" not in st.session_state:
        st.session_state.sector = "technology"
    if "advanced_access" not in st.session_state:
        st.session_state.advanced_access = False
    if "brand_name" not in st.session_state:
        st.session_state.brand_name = "Your Brand"
    
    # Header
    st.markdown("""
    <h1 class="premium-header floating">Brand Guardian AI</h1>
    <div style="text-align: center; margin-bottom: 20px;" class="accent-text">Advanced Brand Protection & Threat Intelligence Platform</div>
    """, unsafe_allow_html=True)
    
    # Sidebar with user info and logout button
    with st.sidebar:
        # User profile card
        user_profile = auth_system.get_user_profile(st.session_state.username)
        subscription_tier = st.session_state.get('subscription_tier', 'basic')
        tier_info = SUBSCRIPTION_TIERS[subscription_tier]
        
        st.markdown(f"""
        <div class="user-profile-card">
            <div class="user-avatar">{user_profile.get('avatar', '👤')}</div>
            <h3>{st.session_state.username}</h3>
            <p>{user_profile.get('bio', 'Brand Protection Specialist')}</p>
            <p><strong>Company:</strong> {auth_system.users[st.session_state.username]['company']}</p>
            <div class="subscription-status status-{subscription_tier}">
                {tier_info['name']} Plan
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.header("Business Configuration")
        brand_name = st.text_input("Brand Name", st.session_state.brand_name)
        st.session_state.brand_name = brand_name
        
        sector = st.selectbox("Business Sector", ["technology", "finance", "retail"])
        st.session_state.sector = sector
        
        st.markdown("---")
        st.subheader("🔐 Access Status")
        if st.session_state.advanced_access:
            st.success("✅ Premium Access")
            st.markdown('<span class="premium-badge">PREMIUM</span>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Basic Access")
        
        st.markdown("---")
        user_id = st.session_state.get('user_id')
        api_keys = api_manager.load_api_keys(user_id) if user_id else {}
        st.subheader("🔑 API Status")
        st.info(f"{len(api_keys)} platform(s) connected")
        
        # User activity log
        st.subheader("📋 Recent Activity")
        user_activity = security_manager.get_activity_log(user_id)[-5:]  # Last 5 activities
        for activity in reversed(user_activity):
            st.markdown(f"""
            <div style="font-size: 0.8rem; margin-bottom: 5px;">
                <span style="color: #FFD700;">{datetime.fromisoformat(activity['timestamp']).strftime('%H:%M')}</span> - {activity['action']}
            </div>
            """, unsafe_allow_html=True)
        
        # User management for admin only
        if st.session_state.get('user_access_level') == 'admin':
            st.markdown("---")
            if st.button("👥 User Management", use_container_width=True):
                st.session_state.show_user_management = True
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            security_manager.log_activity(user_id, "logout", f"User {st.session_state.username} logged out")
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Show user management if admin clicked the button
    if st.session_state.get('show_user_management', False):
        show_user_management()
        if st.button("Back to Dashboard", use_container_width=True):
            st.session_state.show_user_management = False
            st.rerun()
        return
    
    # Different navigation based on user role
    if st.session_state.get('user_access_level') == 'admin':
        # Admin navigation
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📊 Executive Dashboard", 
            "🔍 Advanced Threat Analysis",
            "📱 Social Monitoring",
            "🥊 Competitive Intelligence",
            "🌟 Influencer Network",
            "🛡️ Crisis Prediction",
            "❤️ Brand Health",
            "🔑 API Management"
        ])
        
        with tab1:
            st.header("Executive Dashboard")
            st.write("Overview dashboard content...")
        
        with tab2:
            show_advanced_threat_analysis()
        
        with tab3:
            st.header("Social Monitoring")
            posts = enhanced_monitor.simulate_monitoring_with_api(brand_name, st.session_state.sector, "premium")
            for post in posts[:5]:
                with st.expander(f"{post['platform']} - {post['content'][:50]}..."):
                    st.write(post['content'])
                    st.caption(f"Engagement: {post['engagement']}")
        
        # Other tabs
        for tab, title in [(tab4, "Competitive Intelligence"), (tab5, "Influencer Network"), 
                          (tab6, "Crisis Prediction"), (tab7, "Brand Health")]:
            with tab:
                st.header(title)
                st.write(f"{title} content...")
        
        with tab8:
            show_api_key_management()
    else:
        # Regular user navigation
        show_user_ai_dashboard()

if __name__ == "__main__":
    main()
