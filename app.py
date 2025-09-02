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
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Set page config first
st.set_page_config(
    page_title="BrandGuardian AI Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Generate and display premium access key
def generate_premium_key():
    """Generate a secure premium access key"""
    key = secrets.token_urlsafe(16)
    premium_key = f"BG-PREMIUM-{key.upper()}"
    return premium_key

# Display the premium key in the console (for admin use)
premium_access_key = generate_premium_key()
print(f"PREMIUM ACCESS KEY: {premium_access_key}")

# Advanced CSS with enhanced black and gold theme and animations
st.markdown("""
<style>
    /* Base styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800;900&display=swap');
    
    .main {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #000000 100%);
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #000000 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    /* Animated particles background */
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
        background: radial-gradient(circle, rgba(255, 215, 0, 0.8) 0%, rgba(255, 215, 0, 0) 70%);
        border-radius: 50%;
        animation: float 20s infinite linear;
    }
    
    @keyframes float {
        0% { transform: translateY(0) translateX(0); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) translateX(100px); opacity: 0; }
    }
    
    /* Premium header styling */
    .premium-header {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        margin: 20px 0;
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 50%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 2px 10px rgba(255, 215, 0, 0.3);
        animation: goldGlow 3s ease-in-out infinite alternate;
        position: relative;
    }
    
    @keyframes goldGlow {
        from { 
            text-shadow: 0px 2px 10px rgba(255, 215, 0, 0.3);
            transform: scale(1);
        }
        to { 
            text-shadow: 0px 2px 20px rgba(255, 215, 0, 0.6);
            transform: scale(1.02);
        }
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
        font-size: 1.2rem;
        color: #FFD700;
        text-align: center;
        margin-bottom: 40px;
        animation: fadeIn 2s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Enhanced card styling */
    .metric-card {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        margin: 15px 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
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
        box-shadow: 0 15px 50px rgba(255, 215, 0, 0.3);
        border: 1px solid rgba(255, 215, 0, 0.5);
    }
    
    .search-analysis-card {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    
    .search-analysis-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 45px rgba(255, 215, 0, 0.3);
    }
    
    .search-result-card {
        background: rgba(0, 0, 0, 0.6);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #FFD700;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .search-result-card:hover {
        background: rgba(0, 0, 0, 0.8);
        transform: translateX(10px);
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.2);
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
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .threat-indicator:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }
    
    .threat-critical {
        background: linear-gradient(135deg, rgba(139, 0, 0, 0.5), rgba(139, 0, 0, 0.2));
        color: #FF0000;
        border: 1px solid rgba(255, 0, 0, 0.7);
    }
    
    .threat-high {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.3), rgba(255, 0, 0, 0.1));
        color: #FF0000;
        border: 1px solid rgba(255, 0, 0, 0.5);
    }
    
    .threat-medium {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.3), rgba(255, 165, 0, 0.1));
        color: #FFA500;
        border: 1px solid rgba(255, 165, 0, 0.5);
    }
    
    .threat-low {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.3), rgba(255, 215, 0, 0.1));
        color: #FFD700;
        border: 1px solid rgba(255, 215, 0, 0.5);
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
        color: #FF0000;
        font-weight: 700;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        border-radius: 15px;
        border: 1px solid rgba(255, 215, 0, 0.5);
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.5));
        color: #FFD700;
        font-weight: 700;
        padding: 12px 24px;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
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
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 215, 0, 0.1));
        border: 1px solid rgba(255, 215, 0, 0.8);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.3);
    }
    
    /* Enhanced tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(0, 0, 0, 0.7);
        border-radius: 15px 15px 0 0;
        padding: 14px 20px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-bottom: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 0, 0, 0.8);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 215, 0, 0.1));
        border: 1px solid rgba(255, 215, 0, 0.5);
        border-bottom: none;
        box-shadow: 0 -4px 15px rgba(255, 215, 0, 0.2);
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
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        color: white;
        transition: all 0.3s ease;
    }
    
    .stSelectbox [data-baseweb="select"]:hover, 
    .stTextInput [data-baseweb="input"]:hover, 
    .stTextArea [data-baseweb="textarea"]:hover,
    .stNumberInput [data-baseweb="input"]:hover,
    .stDateInput [data-baseweb="input"]:hover,
    .stTimeInput [data-baseweb="input"]:hover {
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid rgba(255, 215, 0, 0.5);
    }
    
    /* Custom spinner */
    .stSpinner > div {
        border: 4px solid rgba(0, 0, 0, 0.1);
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
        background: rgba(0, 0, 0, 0.7);
        border-radius: 12px;
        padding: 14px 18px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(0, 0, 0, 0.8);
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
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
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
        background: rgba(0, 0, 0, 0.7);
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
        background: rgba(0, 0, 0, 0.7);
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
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 40px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
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
                    radial-gradient(circle at 80% 20%, rgba(255, 165, 0, 0.1), transparent 50%),
                    radial-gradient(circle at 40% 80%, rgba(255, 140, 0, 0.1), transparent 50%);
        animation: bgMove 20s ease infinite;
    }
    
    @keyframes bgMove {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(20px, -20px) rotate(120deg); }
        66% { transform: translate(-20px, 20px) rotate(240deg); }
    }
    
    /* Premium access card */
    .premium-access-card {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 165, 0, 0.1));
        border: 2px solid rgba(255, 215, 0, 0.3);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.2);
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
    
    /* Enhanced AI visualization */
    .ai-visualization {
        background: rgba(0, 0, 0, 0.7);
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    /* AI pulse animation */
    .ai-pulse {
        position: relative;
        display: inline-block;
    }
    
    .ai-pulse::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: rgba(255, 215, 0, 0.3);
        animation: aiPulse 2s infinite;
    }
    
    @keyframes aiPulse {
        0% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.2); opacity: 0.3; }
        100% { transform: scale(1); opacity: 0.7; }
    }
    
    /* New Threat Analysis Animation */
    .threat-analysis-container {
        position: relative;
        width: 100%;
        height: 250px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 20px 0;
    }
    
    .radar-scanner {
        position: relative;
        width: 180px;
        height: 180px;
        margin-bottom: 20px;
    }
    
    .radar-background {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0.5) 70%, transparent 100%);
        border: 2px solid rgba(255, 215, 0, 0.3);
        overflow: hidden;
    }
    
    .radar-grid {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
    }
    
    .radar-grid::before,
    .radar-grid::after {
        content: '';
        position: absolute;
        background: rgba(255, 215, 0, 0.2);
    }
    
    .radar-grid::before {
        width: 2px;
        height: 100%;
        left: 50%;
        transform: translateX(-50%);
    }
    
    .radar-grid::after {
        width: 100%;
        height: 2px;
        top: 50%;
        transform: translateY(-50%);
    }
    
    .radar-sweep {
        position: absolute;
        width: 50%;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.8), transparent);
        top: 50%;
        left: 50%;
        transform-origin: left center;
        animation: radarSweep 3s linear infinite;
    }
    
    @keyframes radarSweep {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .radar-sweep::before {
        content: '';
        position: absolute;
        width: 10px;
        height: 10px;
        background: rgba(255, 215, 0, 0.8);
        border-radius: 50%;
        right: 0;
        top: -4px;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
    }
    
    .threat-dots {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
    }
    
    .threat-dot {
        position: absolute;
        width: 8px;
        height: 8px;
        background: rgba(255, 215, 0, 0.8);
        border-radius: 50%;
        opacity: 0;
        animation: threatPulse 2s infinite;
    }
    
    .threat-dot.active {
        opacity: 1;
    }
    
    @keyframes threatPulse {
        0% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.5); opacity: 1; }
        100% { transform: scale(1); opacity: 0.7; }
    }
    
    .analysis-status {
        font-size: 1.2rem;
        font-weight: 600;
        color: #FFD700;
        text-align: center;
        margin-bottom: 15px;
    }
    
    .progress-container {
        width: 80%;
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        width: 0%;
        background: linear-gradient(90deg, #FFD700, #FFA500);
        border-radius: 4px;
        transition: width 0.3s ease;
        animation: progressFill 3.5s ease-in-out forwards;
    }
    
    @keyframes progressFill {
        0% { width: 0%; }
        100% { width: 100%; }
    }
    
    .analysis-phases {
        display: flex;
        justify-content: space-between;
        width: 80%;
        margin-top: 15px;
    }
    
    .phase {
        display: flex;
        flex-direction: column;
        align-items: center;
        opacity: 0.5;
        transition: opacity 0.3s;
    }
    
    .phase.active {
        opacity: 1;
    }
    
    .phase-icon {
        font-size: 1.5rem;
        margin-bottom: 5px;
    }
    
    .phase-text {
        font-size: 0.8rem;
        color: #FFD700;
    }
    
    .phase:nth-child(1) {
        animation: phaseActivate 3.5s ease-in-out forwards;
    }
    
    .phase:nth-child(2) {
        animation: phaseActivate 3.5s ease-in-out 0.875s forwards;
    }
    
    .phase:nth-child(3) {
        animation: phaseActivate 3.5s ease-in-out 1.75s forwards;
    }
    
    .phase:nth-child(4) {
        animation: phaseActivate 3.5s ease-in-out 2.625s forwards;
    }
    
    @keyframes phaseActivate {
        0% { opacity: 0.5; }
        25% { opacity: 1; }
        100% { opacity: 1; }
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

# Add the new animation function
def show_threat_analysis_animation():
    """Display a radar scanning animation for threat analysis"""
    placeholder = st.empty()
    
    with placeholder.container():
        st.markdown("""
        <div class="threat-analysis-container">
            <div class="radar-scanner">
                <div class="radar-background"></div>
                <div class="radar-grid"></div>
                <div class="radar-sweep"></div>
                <div class="threat-dots">
                    <div class="threat-dot active" style="top: 30%; left: 40%; animation-delay: 0.5s;"></div>
                    <div class="threat-dot active" style="top: 60%; left: 70%; animation-delay: 1.0s;"></div>
                    <div class="threat-dot active" style="top: 20%; left: 60%; animation-delay: 1.5s;"></div>
                    <div class="threat-dot active" style="top: 70%; left: 30%; animation-delay: 2.0s;"></div>
                    <div class="threat-dot active" style="top: 50%; left: 80%; animation-delay: 2.5s;"></div>
                </div>
            </div>
            <div class="analysis-status">Scanning for threats...</div>
            <div class="progress-container">
                <div class="progress-bar"></div>
            </div>
            <div class="analysis-phases">
                <div class="phase">
                    <div class="phase-icon">🔍</div>
                    <div class="phase-text">Scanning</div>
                </div>
                <div class="phase">
                    <div class="phase-icon">🧠</div>
                    <div class="phase-text">Processing</div>
                </div>
                <div class="phase">
                    <div class="phase-icon">📊</div>
                    <div class="phase-text">Analyzing</div>
                </div>
                <div class="phase">
                    <div class="phase-icon">✅</div>
                    <div class="phase-text">Complete</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    return placeholder

# Enhanced Security Manager with Premium Access
class SecurityManager:
    def __init__(self):
        self.valid_access_keys = {
            "BG2024-PRO-ACCESS": "full",
            "BG-ADVANCED-ANALYSIS": "analysis",
            "BG-PREMIUM-2024": "premium",
            "BRAND-GUARDIAN-PRO": "pro",
            premium_access_key: "premium"  # Add the generated key
        }
        self.failed_attempts = {}
        self.lockout_time = timedelta(minutes=15)
        self.max_attempts = 5
        self.session_timeout = timedelta(minutes=30)
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
    
    def encrypt_data(self, data):
        """Encrypt sensitive data"""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher_suite.encrypt(data)
    
    def decrypt_data(self, encrypted_data):
        """Decrypt sensitive data"""
        return self.cipher_suite.decrypt(encrypted_data).decode()
    
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
        self.subscription_plans = {
            "basic": {
                "name": "Basic",
                "price": "$99/month",
                "features": [
                    "Basic threat monitoring",
                    "3 social platforms",
                    "100 API calls/day",
                    "Standard reports",
                    "Email support"
                ],
                "color": "#3B82F6"
            },
            "advanced": {
                "name": "Advanced",
                "price": "$299/month",
                "features": [
                    "All Basic features",
                    "5 social platforms",
                    "500 API calls/day",
                    "Advanced analytics",
                    "Priority support",
                    "Custom alerts"
                ],
                "color": "#8B5CF6"
            },
            "premium": {
                "name": "Premium",
                "price": "$599/month",
                "features": [
                    "All Advanced features",
                    "Unlimited platforms",
                    "Unlimited API calls",
                    "Real-time monitoring",
                    "Dedicated account manager",
                    "Custom integrations"
                ],
                "color": "#FFD700"
            }
        }
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
                        "password": self.hash_password("brandguardian2024"),
                        "access_level": "admin",
                        "company": "Default Company",
                        "email": "admin@example.com",
                        "user_id": str(uuid.uuid4()),
                        "created_at": datetime.now().isoformat(),
                        "last_login": None,
                        "failed_attempts": 0,
                        "last_failed_attempt": None,
                        "session_token": None,
                        "mfa_enabled": False,
                        "subscription": "premium"
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
    
    def register_user(self, username, password, company, email, access_level="client"):
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
            "company": company,
            "email": email,
            "user_id": str(uuid.uuid4()),
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "failed_attempts": 0,
            "last_failed_attempt": None,
            "session_token": None,
            "mfa_enabled": False,
            "subscription": "basic"  # Default subscription
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
            
            self.save_users()
            return True, "Authentication successful"
        else:
            # Increment failed attempts
            user_data['failed_attempts'] = user_data.get('failed_attempts', 0) + 1
            user_data['last_failed_attempt'] = datetime.now().isoformat()
            self.save_users()
            
            remaining_attempts = self.max_attempts - user_data['failed_attempts']
            if remaining_attempts <= 0:
                return False, "Account locked. Please try again in 15 minutes."
            else:
                return False, f"Invalid password. {remaining_attempts} attempts remaining."
    
    def update_user_subscription(self, username, subscription_plan):
        """Update a user's subscription plan"""
        if username in self.users and subscription_plan in self.subscription_plans:
            self.users[username]["subscription"] = subscription_plan
            self.users[username]["subscription_updated"] = datetime.now().isoformat()
            self.save_users()
            return True
        return False
    
    def get_user_subscription(self, username):
        """Get a user's subscription plan"""
        if username in self.users:
            return self.users[username].get("subscription", "basic")
        return "basic"
    
    def check_subscription_feature(self, username, feature):
        """Check if a user's subscription includes a specific feature"""
        subscription = self.get_user_subscription(username)
        
        # Define feature access by subscription level
        feature_access = {
            "basic": ["basic_monitoring", "standard_reports", "email_support"],
            "advanced": ["basic_monitoring", "standard_reports", "email_support", 
                         "advanced_analytics", "priority_support", "custom_alerts"],
            "premium": ["basic_monitoring", "standard_reports", "email_support",
                        "advanced_analytics", "priority_support", "custom_alerts",
                        "real_time_monitoring", "dedicated_manager", "custom_integrations"]
        }
        
        return feature in feature_access.get(subscription, [])

# Initialize enhanced authentication and API manager
auth_system = EnhancedAuthenticationSystem()

# Enhanced API Key Manager with User Isolation
class EnhancedAPIKeyManager:
    def __init__(self):
        self.encryptor = SecureEncryptor()
        self.api_keys_dir = "api_keys"
        os.makedirs(self.api_keys_dir, exist_ok=True)
        
        # Define supported platforms first
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
api_manager = EnhancedAPIKeyManager()

# Enhanced AI Analysis Engine
class AIAnalysisEngine:
    def __init__(self):
        self.threat_keywords = {
            'high': ['scam', 'fraud', 'lawsuit', 'bankruptcy', 'fake', 'illegal', 'sue', 'crime', 'phishing', 'counterfeit'],
            'medium': ['complaint', 'problem', 'issue', 'bad', 'terrible', 'awful', 'disappointed', 'poor', 'broken'],
            'low': ['review', 'feedback', 'comment', 'opinion', 'thought', 'experience', 'question', 'info']
        }
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        # Simulate sentiment analysis
        words = text.lower().split()
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'best']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'disappointing', 'poor', 'broken']
        
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        if positive_count > negative_count:
            return "positive", min(1.0, positive_count / len(words))
        elif negative_count > positive_count:
            return "negative", min(1.0, negative_count / len(words))
        else:
            return "neutral", 0.5
    
    def detect_threats(self, text, brand_name):
        """Detect threats in text"""
        text_lower = text.lower()
        brand_lower = brand_name.lower()
        
        # Check if brand is mentioned
        brand_mentioned = brand_lower in text_lower
        
        # Detect threat level
        threat_level = "low"
        found_keywords = []
        threat_score = 0.0
        
        for level, keywords in self.threat_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if level == "high":
                        threat_score += 0.3
                    elif level == "medium":
                        threat_score += 0.2
                    else:
                        threat_score += 0.1
                    found_keywords.append(keyword)
        
        # Determine threat level based on score
        if threat_score >= 0.3:
            threat_level = "high"
        elif threat_score >= 0.1:
            threat_level = "medium"
        
        # Generate analysis results
        results = {
            'text': text,
            'brand': brand_name,
            'brand_mentioned': brand_mentioned,
            'threat_level': threat_level,
            'threat_score': min(1.0, threat_score),
            'keywords_found': found_keywords,
            'timestamp': datetime.now().isoformat(),
            'sentiment': self.analyze_sentiment(text)
        }
        
        return results
    
    def generate_threat_report(self, analyses):
        """Generate comprehensive threat report"""
        # Count threat levels
        threat_counts = {
            'high': sum(1 for a in analyses if a['threat_level'] == 'high'),
            'medium': sum(1 for a in analyses if a['threat_level'] == 'medium'),
            'low': sum(1 for a in analyses if a['threat_level'] == 'low')
        }
        
        # Calculate average sentiment
        sentiment_scores = [a['sentiment'][1] for a in analyses]
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        # Generate recommendations
        recommendations = []
        
        if threat_counts['high'] > 0:
            recommendations.append("Immediate action required for high-level threats")
            recommendations.append("Activate crisis management protocol")
            recommendations.append("Notify legal team")
        
        if threat_counts['medium'] > 0:
            recommendations.append("Monitor medium-level threats closely")
            recommendations.append("Prepare response templates")
        
        if avg_sentiment < 0.3:
            recommendations.append("Address negative sentiment with PR campaign")
        
        if not recommendations:
            recommendations.append("Continue standard monitoring")
        
        # Create report
        report = {
            'total_analyses': len(analyses),
            'threat_counts': threat_counts,
            'average_sentiment': avg_sentiment,
            'recommendations': recommendations,
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def create_keyword_frequency(self, texts):
        """Create keyword frequency analysis"""
        # Combine all texts and count word frequencies
        all_text = ' '.join(texts).lower()
        words = re.findall(r'\b\w+\b', all_text)
        
        # Filter out common stop words
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'a', 'an'}
        
        word_counts = {}
        for word in words:
            if word not in stop_words and len(word) > 2:
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # Sort by frequency and return top 20
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        return dict(sorted_words)
    
    def create_threat_patterns(self, analyses):
        """Create threat pattern analysis"""
        patterns = {
            'high_threat_keywords': Counter(),
            'medium_threat_keywords': Counter(),
            'low_threat_keywords': Counter(),
            'platform_distribution': Counter(),
            'time_distribution': Counter()
        }
        
        for analysis in analyses:
            # Count keywords by threat level
            for keyword in analysis['keywords_found']:
                if analysis['threat_level'] == 'high':
                    patterns['high_threat_keywords'][keyword] += 1
                elif analysis['threat_level'] == 'medium':
                    patterns['medium_threat_keywords'][keyword] += 1
                else:
                    patterns['low_threat_keywords'][keyword] += 1
            
            # Simulate platform distribution
            platform = random.choice(['Twitter', 'Facebook', 'Instagram', 'Reddit', 'YouTube'])
            patterns['platform_distribution'][platform] += 1
            
            # Simulate time distribution
            hour = datetime.now().hour
            patterns['time_distribution'][f"{hour:02d}:00"] += 1
        
        return patterns

# Enhanced AI Analysis Engine Extensions
class EnhancedAIAnalysisEngine(AIAnalysisEngine):
    def __init__(self):
        super().__init__()
        # Extended threat categories
        self.extended_threat_keywords = {
            'critical': ['data breach', 'security flaw', 'vulnerability', 'exploit', 'hack', 'cyberattack'],
            'high': ['scam', 'fraud', 'lawsuit', 'bankruptcy', 'fake', 'illegal', 'sue', 'crime', 'phishing', 'counterfeit'],
            'medium': ['complaint', 'problem', 'issue', 'bad', 'terrible', 'awful', 'disappointed', 'poor', 'broken'],
            'low': ['review', 'feedback', 'comment', 'opinion', 'thought', 'experience', 'question', 'info'],
            'positive': ['excellent', 'amazing', 'love', 'best', 'perfect', 'outstanding', 'recommend']
        }
        
        # Brand-specific patterns
        self.brand_patterns = {
            'impersonation': ['fake', 'scam', 'not real', 'imposter', 'phishing'],
            'product_issues': ['defective', 'broken', 'malfunction', 'faulty', 'poor quality'],
            'service_complaints': ['rude', 'unhelpful', 'slow', 'delayed', 'cancelled'],
            'pricing_issues': ['overpriced', 'ripoff', 'expensive', 'not worth', 'waste of money'],
            'legal_concerns': ['lawsuit', 'sue', 'legal action', 'court', 'attorney']
        }
        
        # Contextual sentiment indicators
        self.contextual_sentiment = {
            'negation_words': ['not', 'no', 'never', 'none', 'nothing', 'nobody', 'nowhere', 'neither', 'nor'],
            'intensifiers': ['very', 'extremely', 'really', 'absolutely', 'completely', 'totally', 'utterly'],
            'diminishers': ['slightly', 'somewhat', 'a bit', 'little', 'barely', 'hardly']
        }
    
    def advanced_sentiment_analysis(self, text):
        """Enhanced sentiment analysis with contextual understanding"""
        # Basic sentiment analysis
        sentiment, score = self.analyze_sentiment(text)
        
        # Contextual analysis
        words = text.lower().split()
        negation_detected = any(word in self.contextual_sentiment['negation_words'] for word in words)
        intensifier_detected = any(word in self.contextual_sentiment['intensifiers'] for word in words)
        diminisher_detected = any(word in self.contextual_sentiment['diminishers'] for word in words)
        
        # Adjust score based on context
        if negation_detected:
            score = 1.0 - score  # Flip sentiment
            sentiment = 'negative' if sentiment == 'positive' else 'positive' if sentiment == 'negative' else 'neutral'
        
        if intensifier_detected:
            score = min(1.0, score * 1.3)  # Increase intensity
        
        if diminisher_detected:
            score = max(0.0, score * 0.7)  # Decrease intensity
        
        # Emotion detection
        emotions = self.detect_emotions(text)
        
        return {
            'sentiment': sentiment,
            'score': score,
            'confidence': min(1.0, abs(score - 0.5) * 2),
            'emotions': emotions,
            'contextual_factors': {
                'negation': negation_detected,
                'intensified': intensifier_detected,
                'diminished': diminisher_detected
            }
        }
    
    def detect_emotions(self, text):
        """Detect emotions in text"""
        emotion_keywords = {
            'anger': ['angry', 'furious', 'mad', 'irate', 'outraged', 'annoyed', 'frustrated'],
            'fear': ['afraid', 'scared', 'terrified', 'worried', 'anxious', 'nervous'],
            'joy': ['happy', 'excited', 'delighted', 'pleased', 'thrilled', 'ecstatic'],
            'sadness': ['sad', 'unhappy', 'depressed', 'disappointed', 'upset', 'miserable'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned'],
            'disgust': ['disgusted', 'revolted', 'sickened', 'repulsed', 'appalled']
        }
        
        text_lower = text.lower()
        detected_emotions = {}
        
        for emotion, keywords in emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                detected_emotions[emotion] = min(1.0, count / 2)  # Normalize to 0-1
        
        return detected_emotions
    
    def enhanced_threat_detection(self, text, brand_name):
        """Enhanced threat detection with pattern recognition"""
        text_lower = text.lower()
        brand_lower = brand_name.lower()
        
        # Basic threat detection
        basic_result = self.detect_threats(text, brand_name)
        
        # Extended threat level detection
        extended_threat_level = "low"
        extended_threat_score = 0.0
        extended_keywords = []
        
        for level, keywords in self.extended_threat_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if level == "critical":
                        extended_threat_score += 0.5
                    elif level == "high":
                        extended_threat_score += 0.3
                    elif level == "medium":
                        extended_threat_score += 0.2
                    elif level == "low":
                        extended_threat_score += 0.1
                    elif level == "positive":
                        extended_threat_score -= 0.1  # Positive keywords reduce threat
                    extended_keywords.append(keyword)
        
        # Brand pattern detection
        detected_patterns = {}
        for pattern, keywords in self.brand_patterns.items():
            pattern_count = sum(1 for keyword in keywords if keyword in text_lower)
            if pattern_count > 0:
                detected_patterns[pattern] = pattern_count
                # Adjust threat score based on pattern
                if pattern in ['impersonation', 'legal_concerns']:
                    extended_threat_score += 0.2
                elif pattern in ['product_issues', 'service_complaints']:
                    extended_threat_score += 0.15
                elif pattern == 'pricing_issues':
                    extended_threat_score += 0.1
        
        # Determine final threat level
        if extended_threat_score >= 0.5:
            extended_threat_level = "critical"
        elif extended_threat_score >= 0.3:
            extended_threat_level = "high"
        elif extended_threat_score >= 0.1:
            extended_threat_level = "medium"
        
        # Combine with basic analysis
        threat_level_priority = {"critical": 5, "high": 4, "medium": 3, "low": 2}
        final_threat_level = max(
            basic_result['threat_level'], 
            extended_threat_level, 
            key=lambda x: threat_level_priority[x]
        )
        
        # Advanced sentiment analysis
        sentiment_analysis = self.advanced_sentiment_analysis(text)
        
        # Generate enhanced results
        enhanced_result = {
            **basic_result,
            'extended_threat_level': extended_threat_level,
            'extended_threat_score': min(1.0, extended_threat_score),
            'extended_keywords': extended_keywords,
            'detected_patterns': detected_patterns,
            'final_threat_level': final_threat_level,
            'sentiment_analysis': sentiment_analysis,
            'risk_score': self.calculate_risk_score(extended_threat_score, sentiment_analysis['score']),
            'urgency_level': self.calculate_urgency(final_threat_level, detected_patterns),
            'recommended_actions': self.generate_action_recommendations(final_threat_level, detected_patterns)
        }
        
        return enhanced_result
    
    def calculate_risk_score(self, threat_score, sentiment_score):
        """Calculate overall risk score (0-1)"""
        # Risk is higher when threat is high and sentiment is negative
        sentiment_risk = 1.0 - sentiment_score if sentiment_score < 0.5 else 0
        combined_risk = (threat_score * 0.7) + (sentiment_risk * 0.3)
        return min(1.0, combined_risk)
    
    def calculate_urgency(self, threat_level, patterns):
        """Calculate urgency level (1-5)"""
        urgency_map = {
            "critical": 5,
            "high": 4,
            "medium": 3,
            "low": 2
        }
        
        base_urgency = urgency_map.get(threat_level, 1)
        
        # Increase urgency for certain patterns
        if any(pattern in patterns for pattern in ['impersonation', 'legal_concerns']):
            base_urgency = min(5, base_urgency + 1)
        
        return base_urgency
    
    def generate_action_recommendations(self, threat_level, patterns):
        """Generate specific action recommendations"""
        recommendations = []
        
        # Base recommendations by threat level
        if threat_level == "critical":
            recommendations.extend([
                "IMMEDIATE: Activate crisis response team",
                "IMMEDIATE: Legal team notification required",
                "IMMEDIATE: Prepare public statement",
                "HIGH: Monitor all channels 24/7",
                "HIGH: Executive team briefing"
            ])
        elif threat_level == "high":
            recommendations.extend([
                "HIGH: Escalate to senior management",
                "HIGH: Prepare response within 2 hours",
                "MEDIUM: Increase monitoring frequency",
                "MEDIUM: Customer service team alert"
            ])
        elif threat_level == "medium":
            recommendations.extend([
                "MEDIUM: Standard response protocol",
                "MEDIUM: Track for escalation",
                "LOW: Weekly review inclusion"
            ])
        
        # Pattern-specific recommendations
        if "impersonation" in patterns:
            recommendations.append("HIGH: Report impersonation to platform")
            recommendations.append("MEDIUM: Issue customer warning")
        
        if "legal_concerns" in patterns:
            recommendations.append("HIGH: Legal department consultation")
            recommendations.append("MEDIUM: Preserve all evidence")
        
        if "product_issues" in patterns:
            recommendations.append("MEDIUM: Product team notification")
            recommendations.append("LOW: Quality assurance review")
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def predict_threat_trend(self, historical_data):
        """Predict threat trends based on historical data"""
        if len(historical_data) < 3:
            return {"trend": "insufficient_data", "confidence": 0}
        
        # Simple trend analysis
        recent_threats = historical_data[-7:]  # Last 7 days
        older_threats = historical_data[-14:-7]  # Previous 7 days
        
        recent_avg = sum(recent_threats) / len(recent_threats)
        older_avg = sum(older_threats) / len(older_threats)
        
        change_percent = ((recent_avg - older_avg) / older_avg) * 100 if older_avg > 0 else 0
        
        if change_percent > 20:
            trend = "increasing"
            confidence = min(0.9, abs(change_percent) / 50)
        elif change_percent < -20:
            trend = "decreasing"
            confidence = min(0.9, abs(change_percent) / 50)
        else:
            trend = "stable"
            confidence = 0.7
        
        # Predict next week
        if trend == "increasing":
            predicted_next = recent_avg * (1 + (change_percent / 100))
        elif trend == "decreasing":
            predicted_next = recent_avg * (1 - (abs(change_percent) / 100))
        else:
            predicted_next = recent_avg
        
        return {
            "trend": trend,
            "confidence": confidence,
            "change_percent": change_percent,
            "current_average": recent_avg,
            "predicted_next_week": max(0, predicted_next)
        }

# Initialize AI analysis engines
ai_engine = AIAnalysisEngine()
enhanced_ai_engine = EnhancedAIAnalysisEngine()

# Enhanced Visualizations
class AdvancedVisualizations:
    def __init__(self):
        self.colors = {
            'primary': '#FFD700',
            'secondary': '#FFA500',
            'success': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444',
            'info': '#3B82F6',
            'dark': '#000000',
            'light': '#F3F4F6'
        }
    
    def create_radar_chart(self, data, labels, title):
        """Create a radar chart using plotly"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=data,
            theta=labels,
            fill='toself',
            name='Threat Level',
            line_color=self.colors['primary'],
            fillcolor=f'rgba(255, 215, 0, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(data) * 1.1]
                )),
            showlegend=False,
            title=title,
            title_x=0.5,
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_sentiment_timeline(self, dates, values, title):
        """Create an advanced sentiment timeline"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines+markers',
            name='Sentiment',
            line=dict(color=self.colors['primary'], width=3),
            marker=dict(size=8, color=self.colors['primary'])
        ))
        
        fig.update_layout(
            title=title,
            title_x=0.5,
            xaxis_title='Date',
            yaxis_title='Sentiment Score',
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        
        return fig
    
    def create_threat_distribution(self, data, title):
        """Create a donut chart for threat distribution"""
        labels = list(data.keys())
        values = list(data.values())
        colors = [self.colors['danger'], self.colors['warning'], self.colors['success']]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker_colors=colors,
            textinfo='label+percent',
            textposition='auto'
        )])
        
        fig.update_layout(
            title=title,
            title_x=0.5,
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_keyword_bar_chart(self, keyword_data, title):
        """Create a bar chart for keyword frequency"""
        fig = go.Figure(data=[go.Bar(
            x=list(keyword_data.keys()),
            y=list(keyword_data.values()),
            marker_color=self.colors['primary']
        )])
        
        fig.update_layout(
            title=title,
            title_x=0.5,
            xaxis_title='Keywords',
            yaxis_title='Frequency',
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        
        return fig
    
    def create_pattern_heatmap(self, pattern_data, title):
        """Create a heatmap for threat patterns"""
        # Convert pattern data to DataFrame format
        platforms = list(pattern_data['platform_distribution'].keys())
        threat_levels = ['high', 'medium', 'low']
        
        # Create matrix data
        z_data = []
        for level in threat_levels:
            row = []
            for platform in platforms:
                # Simulate data based on actual distribution
                if level == 'high':
                    value = pattern_data['high_threat_keywords'].total() * 0.3
                elif level == 'medium':
                    value = pattern_data['medium_threat_keywords'].total() * 0.5
                else:
                    value = pattern_data['low_threat_keywords'].total() * 0.2
                
                # Adjust by platform distribution
                platform_factor = pattern_data['platform_distribution'][platform] / sum(pattern_data['platform_distribution'].values())
                row.append(value * platform_factor)
            z_data.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=z_data,
            x=platforms,
            y=threat_levels,
            colorscale='YlOrRd',
            showscale=True
        ))
        
        fig.update_layout(
            title=title,
            title_x=0.5,
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig

# Enhanced Visualizations
class EnhancedVisualizations(AdvancedVisualizations):
    def __init__(self):
        super().__init__()
    
    def create_emotion_heatmap(self, emotion_data, title):
        """Create emotion heatmap"""
        emotions = list(emotion_data.keys())
        values = list(emotion_data.values())
        
        fig = go.Figure(data=go.Heatmap(
            z=[values],
            x=emotions,
            y=['Emotion Intensity'],
            colorscale='RdYlBu_r',
            showscale=True
        ))
        
        fig.update_layout(
            title=title,
            title_x=0.5,
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_risk_gauge(self, risk_score, title):
        """Create risk gauge chart"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=risk_score * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#FFD700"},
                'steps': [
                    {'range': [0, 30], 'color': "#10B981"},
                    {'range': [30, 70], 'color': "#F59E0B"},
                    {'range': [70, 100], 'color': "#EF4444"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_prediction_chart(self, historical_data, prediction, title):
        """Create trend prediction chart"""
        dates = pd.date_range(end=datetime.now(), periods=len(historical_data))
        future_dates = pd.date_range(start=datetime.now(), periods=8)[1:]  # Next 7 days
        
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=dates,
            y=historical_data,
            mode='lines+markers',
            name='Historical',
            line=dict(color=self.colors['primary'], width=3),
            marker=dict(size=8)
        ))
        
        # Prediction
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=[prediction['predicted_next_week']] * 7,
            mode='lines',
            name='Prediction',
            line=dict(color=self.colors['warning'], width=3, dash='dash')
        ))
        
        # Confidence interval
        confidence_upper = prediction['predicted_next_week'] * (1 + (1 - prediction['confidence']))
        confidence_lower = prediction['predicted_next_week'] * (1 - (1 - prediction['confidence']))
        
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=[confidence_upper] * 7,
            mode='lines',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=[confidence_lower] * 7,
            mode='lines',
            line=dict(width=0),
            fillcolor='rgba(245, 158, 11, 0.2)',
            fill='tonexty',
            name='Confidence Interval'
        ))
        
        fig.update_layout(
            title=title,
            title_x=0.5,
            xaxis_title='Date',
            yaxis_title='Threat Count',
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        
        return fig

# Initialize visualizations
viz = AdvancedVisualizations()
enhanced_viz = EnhancedVisualizations()

# User registration and management functions
def show_user_registration():
    st.subheader("👥 Client Registration")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username", help="Choose a username for the client")
            company = st.text_input("Company Name", help="Client's company name")
        
        with col2:
            password = st.text_input("Password", type="password", help="Set a secure password (min 8 chars, upper/lowercase, number, special char)")
            email = st.text_input("Email", help="Client's email address")
        
        submitted = st.form_submit_button("Register Client", use_container_width=True)
        
        if submitted:
            if all([username, password, company, email]):
                success, message = auth_system.register_user(username, password, company, email)
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                else:
                    st.error(f"❌ {message}")
            else:
                st.error("Please fill all fields")

def show_user_management():
    st.subheader("👥 User Management")
    
    # Check if user is admin
    if st.session_state.get('user_access_level') != 'admin':
        st.error("⛔ Administrator access required")
        st.info("Only administrators can access user management features.")
        return
    
    # Show existing users
    st.write("### Existing Users")
    users_data = []
    for username, user_info in auth_system.users.items():
        subscription = user_info.get("subscription", "basic")
        users_data.append({
            "Username": username,
            "Company": user_info.get("company", "N/A"),
            "Email": user_info.get("email", "N/A"),
            "Access Level": user_info.get("access_level", "client"),
            "Subscription": f"{auth_system.subscription_plans[subscription]['name']} ({subscription})",
            "Last Login": user_info.get("last_login", "Never"),
            "Created": user_info.get("created_at", "N/A")[:10] if user_info.get("created_at") else "N/A"
        })
    
    if users_data:
        st.dataframe(pd.DataFrame(users_data), use_container_width=True)
    else:
        st.info("No users registered yet")
    
    # Registration form
    show_user_registration()
    
    # Subscription management
    st.markdown("---")
    st.subheader("💳 Subscription Management")
    
    user_to_manage = st.selectbox("Select User to Update Subscription", list(auth_system.users.keys()))
    
    if user_to_manage:
        current_subscription = auth_system.get_user_subscription(user_to_manage)
        
        st.write(f"Current Subscription: **{auth_system.subscription_plans[current_subscription]['name']}**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background-color: {auth_system.subscription_plans['basic']['color']}20; 
                        border: 1px solid {auth_system.subscription_plans['basic']['color']}; 
                        border-radius: 10px; padding: 15px;">
                <h4>{auth_system.subscription_plans['basic']['name']}</h4>
                <p>{auth_system.subscription_plans['basic']['price']}</p>
                <ul>
                    {"".join([f"<li>{feature}</li>" for feature in auth_system.subscription_plans['basic']['features']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Set Basic", key=f"basic_{user_to_manage}"):
                auth_system.update_user_subscription(user_to_manage, "basic")
                st.success(f"Updated {user_to_manage} to Basic subscription")
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div style="background-color: {auth_system.subscription_plans['advanced']['color']}20; 
                        border: 1px solid {auth_system.subscription_plans['advanced']['color']}; 
                        border-radius: 10px; padding: 15px;">
                <h4>{auth_system.subscription_plans['advanced']['name']}</h4>
                <p>{auth_system.subscription_plans['advanced']['price']}</p>
                <ul>
                    {"".join([f"<li>{feature}</li>" for feature in auth_system.subscription_plans['advanced']['features']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Set Advanced", key=f"advanced_{user_to_manage}"):
                auth_system.update_user_subscription(user_to_manage, "advanced")
                st.success(f"Updated {user_to_manage} to Advanced subscription")
                st.rerun()
        
        with col3:
            st.markdown(f"""
            <div style="background-color: {auth_system.subscription_plans['premium']['color']}20; 
                        border: 1px solid {auth_system.subscription_plans['premium']['color']}; 
                        border-radius: 10px; padding: 15px;">
                <h4>{auth_system.subscription_plans['premium']['name']}</h4>
                <p>{auth_system.subscription_plans['premium']['price']}</p>
                <ul>
                    {"".join([f"<li>{feature}</li>" for feature in auth_system.subscription_plans['premium']['features']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Set Premium", key=f"premium_{user_to_manage}"):
                auth_system.update_user_subscription(user_to_manage, "premium")
                st.success(f"Updated {user_to_manage} to Premium subscription")
                st.rerun()
    
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
    
    with col2:
        if st.button("Delete User", use_container_width=True, type="secondary"):
            if user_to_manage and user_to_manage != st.session_state.username:
                if st.checkbox(f"Confirm deletion of {user_to_manage}"):
                    del auth_system.users[user_to_manage]
                    auth_system.save_users()
                    st.success(f"User {user_to_manage} deleted")
                    st.rerun()
            elif user_to_manage == st.session_state.username:
                st.error("You cannot delete your own account")

def show_login_form():
    """Display login form with enhanced design"""
    st.markdown("""
    <div class="login-bg"></div>
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style="font-size: 3rem; font-weight: 800; background: linear-gradient(90deg, #FFD700 0%, #FFA500 55%, #FFD700 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🔒 BrandGuardian AI</h1>
        <p style="font-size: 1.2rem; color: #FFD700;">Advanced Brand Protection & Threat Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two-column layout for login
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style='text-align: center;'>
            <div style="font-size: 6rem; margin-bottom: 20px;" class="security-shield">🛡️</div>
            <h3 style="color: #FFD700;">Secure Login</h3>
            <p style="color: #FFD700;">Access your brand protection dashboard</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            # Remember me checkbox
            remember_me = st.checkbox("Remember me")
            
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit:
                success, message = auth_system.authenticate(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_access_level = auth_system.users[username]["access_level"]
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
    """Threat monitoring dashboard"""
    st.subheader("🛡️ Real-time Threat Dashboard")
    
    # Create metrics with custom styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Active Threats</h3>
            <h1>18</h1>
            <p style="color: #FF0000;">+5 from yesterday</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Threat Level</h3>
            <h1>High</h1>
            <p style="color: #FF0000;">Elevated risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Response Time</h3>
            <h1>2.1s</h1>
            <p style="color: #FFD700;">-0.4s improvement</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Protected Assets</h3>
            <h1>24</h1>
            <p style="color: #FFD700;">Fully secured</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Threat timeline with advanced visualization
    st.subheader("📈 Threat Timeline (7 Days)")
    
    # Generate sample data with valid dates
    dates = pd.date_range(end=datetime.now(), periods=7)
    threats = [8, 12, 5, 18, 10, 7, 14]
    
    # Create an advanced chart
    fig = viz.create_sentiment_timeline(dates, threats, "Threat Activity Over Time")
    st.plotly_chart(fig, use_container_width=True)
    
    # Threat distribution
    st.subheader("🌡️ Threat Distribution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        threat_data = {'High': 8, 'Medium': 5, 'Low': 5}
        fig = viz.create_threat_distribution(threat_data, "Threat Severity Distribution")
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
                # Show the enhanced animation
                animation_placeholder = show_threat_analysis_animation()
                
                # Simulate analysis with the animation running
                time.sleep(3.5)  # Allow time for animation to complete
                
                # Clear the animation
                animation_placeholder.empty()
                
                # Perform the actual analysis
                results = search_analyzer.analyze_search(search_query, brand_name)
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

def show_trend_analysis():
    """Trend analysis functionality"""
    st.subheader("📈 Threat Trend Analysis")
    
    # Generate trend data with valid dates
    dates = pd.date_range(end=datetime.now(), periods=30)
    high_threats = np.random.poisson(5, 30)
    medium_threats = np.random.poisson(10, 30)
    low_threats = np.random.poisson(20, 30)
    
    trend_data = pd.DataFrame({
        'Date': dates,
        'High Threats': high_threats,
        'Medium Threats': medium_threats,
        'Low Threats': low_threats
    })
    
    # Create an advanced multi-line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=trend_data['Date'],
        y=trend_data['High Threats'],
        mode='lines+markers',
        name='High Threats',
        line=dict(color='#EF4444', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=trend_data['Date'],
        y=trend_data['Medium Threats'],
        mode='lines+markers',
        name='Medium Threats',
        line=dict(color='#F59E0B', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=trend_data['Date'],
        y=trend_data['Low Threats'],
        mode='lines+markers',
        name='Low Threats',
        line=dict(color='#10B981', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Threat Trends Over Time",
        title_x=0.5,
        xaxis_title='Date',
        yaxis_title='Number of Threats',
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Platform distribution with radar chart
    st.subheader("🌐 Threat Distribution by Platform")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        platforms = ['Twitter', 'Facebook', 'Reddit', 'Instagram', 'YouTube']
        threat_counts = [45, 32, 28, 19, 12]
        
        # Create radar chart
        fig = viz.create_radar_chart(
            np.array(threat_counts),
            platforms,
            "Threat Distribution Across Platforms"
        )
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
    
    # Sentiment analysis over time
    st.subheader("📊 Sentiment Analysis")
    
    sentiment_dates = pd.date_range(end=datetime.now(), periods=14)
    sentiment_values = np.sin(np.linspace(0, 4*np.pi, 14)) * 0.5 + 0.5
    
    sentiment_data = pd.DataFrame({
        'Date': sentiment_dates,
        'Sentiment Score': sentiment_values
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=sentiment_data['Date'],
        y=sentiment_data['Sentiment Score'],
        mode='lines+markers',
        name='Sentiment',
        line=dict(color='#FFD700', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(255, 215, 0, 0.2)'
    ))
    
    fig.update_layout(
        title="Sentiment Analysis Over Time",
        title_x=0.5,
        xaxis_title='Date',
        yaxis_title='Sentiment Score',
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
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
            type="password",
            placeholder="BG2024-PRO-ACCESS",
            help="Enter your premium access key"
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
        st.info("Use demo key: BG2024-PRO-ACCESS")
        if st.button("Use Demo Key"):
            st.session_state.advanced_access = True
            st.session_state.access_level = "full"
            st.success("Demo access granted!")
            st.balloons()
            st.rerun()
    
    # Premium access card
    st.markdown("""
    <div class="premium-access-card">
        <h3>🌟 Premium Access Features</h3>
        <p>Unlock the full potential of BrandGuardian AI with our premium features:</p>
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
        placeholder=f"Paste your {platform_info['field_name']} here...",
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
        self.ai_engine = ai_engine
    
    def simulate_monitoring_with_api(self, brand_name, sector):
        posts = []
        user_id = st.session_state.get('user_id')
        if not user_id:
            return posts
            
        connected_platforms = list(api_manager.load_api_keys(user_id).keys()) or ['twitter', 'facebook', 'instagram']
        
        for platform in connected_platforms:
            for _ in range(random.randint(3, 8)):
                content = self.generate_business_post(brand_name, sector)
                post = {
                    'platform': platform.capitalize(),
                    'content': content,
                    'author': f"user_{random.randint(1000, 9999)}",
                    'engagement': random.randint(50, 5000),
                    'api_connected': platform in api_manager.load_api_keys(user_id)
                }
                
                # Add AI analysis
                analysis = self.ai_engine.detect_threats(content, brand_name)
                post['threat_level'] = analysis['threat_level']
                post['sentiment'] = analysis['sentiment'][0]
                
                posts.append(post)
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

# Search Analysis System
class SearchAnalyzer:
    def __init__(self):
        self.threat_keywords = {
            'high': ['scam', 'fraud', 'lawsuit', 'bankruptcy', 'fake', 'illegal', 'sue', 'crime'],
            'medium': ['complaint', 'problem', 'issue', 'bad', 'terrible', 'awful', 'disappointed'],
            'low': ['review', 'feedback', 'comment', 'opinion', 'thought', 'experience']
        }
    
    def analyze_search(self, query, brand_name):
        """Analyze search query for threats"""
        query_lower = query.lower()
        brand_lower = brand_name.lower()
        
        # Detect threat level
        threat_level = "low"
        found_keywords = []
        
        for level, keywords in self.threat_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    threat_level = level
                    found_keywords.append(keyword)
        
        # Generate analysis results
        results = {
            'query': query,
            'brand': brand_name,
            'threat_level': threat_level,
            'keywords_found': found_keywords,
            'timestamp': datetime.now().isoformat(),
            'analysis': self.generate_analysis(threat_level, found_keywords),
            'recommendations': self.generate_recommendations(threat_level)
        }
        
        return results
    
    def generate_analysis(self, threat_level, keywords):
        """Generate analysis text based on threat level"""
        analyses = {
            'high': "🚨 High threat potential detected. Immediate attention required. Multiple negative keywords found indicating serious brand reputation risks.",
            'medium': "⚠️ Medium threat level. Potential brand reputation issues detected. Monitor closely and consider proactive engagement.",
            'low': "✅ Low threat level. General brand mentions detected. Standard monitoring recommended."
        }
        return analyses.get(threat_level, "Analysis completed.")
    
    def generate_recommendations(self, threat_level):
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

# Initialize search analyzer
search_analyzer = SearchAnalyzer()

# User AI Dashboard (for regular users)
def show_user_ai_dashboard():
    st.header("🤖 BrandGuardian AI Dashboard")
    
    # Get user's subscription
    username = st.session_state.get('username')
    subscription = auth_system.get_user_subscription(username)
    subscription_info = auth_system.subscription_plans[subscription]
    
    # Welcome message with subscription info
    brand_name = st.session_state.get('brand_name', 'Your Brand')
    st.success(f"Welcome to your brand protection dashboard, {brand_name}!")
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="background-color: {subscription_info['color']}20; 
                    border: 1px solid {subscription_info['color']}; 
                    border-radius: 20px; padding: 8px 16px; margin-right: 15px;">
            <span style="color: {subscription_info['color']}; font-weight: bold;">
                {subscription_info['name']} Subscription
            </span>
        </div>
        <div>
            <a href="#upgrade" style="color: #FFD700; text-decoration: none;">Upgrade Plan →</a>
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
            <p style="color: #FFD700;">+12 from last week</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Threat Level</h3>
            <h1>Low</h1>
            <p style="color: #FFD700;">Stable</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Response Rate</h3>
            <h1>92%</h1>
            <p style="color: #FFD700;">Excellent</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Create tabs based on subscription
    available_tabs = ["Search Analysis"]  # Available to all subscriptions
    
    if auth_system.check_subscription_feature(username, "advanced_analytics"):
        available_tabs.append("Social Monitoring")
        available_tabs.append("AI Insights")
    
    if auth_system.check_subscription_feature(username, "real_time_monitoring"):
        available_tabs.append("Enhanced AI Analysis")
        available_tabs.append("Predictive Analytics")
    
    # Create the tab navigation
    tabs = st.tabs([f"🔍 {tab}" for tab in available_tabs])
    
    # Display tab content
    for i, tab_name in enumerate(available_tabs):
        with tabs[i]:
            if tab_name == "Search Analysis":
                show_search_analysis()
            elif tab_name == "Social Monitoring":
                show_social_monitoring()
            elif tab_name == "AI Insights":
                show_ai_insights()
            elif tab_name == "Enhanced AI Analysis":
                show_enhanced_threat_analysis()
            elif tab_name == "Predictive Analytics":
                show_predictive_analytics()
    
    # Subscription upgrade section
    st.markdown("---")
    st.subheader("💳 Subscription Plans")
    
    col1, col2, col3 = st.columns(3)
    
    plans = ["basic", "advanced", "premium"]
    
    for i, plan in enumerate(plans):
        plan_info = auth_system.subscription_plans[plan]
        current_plan = subscription == plan
        
        with [col1, col2, col3][i]:
            st.markdown(f"""
            <div style="background-color: {plan_info['color']}20; 
                        border: 1px solid {plan_info['color']}; 
                        border-radius: 15px; padding: 20px; height: 100%;">
                <h3 style="text-align: center;">{plan_info['name']}</h3>
                <h4 style="text-align: center;">{plan_info['price']}</h4>
                <ul>
                    {"".join([f"<li>{feature}</li>" for feature in plan_info['features']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if current_plan:
                st.success("Current Plan")
            else:
                if st.button(f"Upgrade to {plan_info['name']}", key=f"upgrade_{plan}"):
                    st.info(f"Redirecting to payment for {plan_info['name']} plan...")
                    # In a real app, this would redirect to a payment processor

# Add new functions for subscription-specific features
def show_social_monitoring():
    """Social monitoring functionality - requires Advanced subscription"""
    st.header("Social Monitoring")
    
    # Get user's subscription
    username = st.session_state.get('username')
    
    if not auth_system.check_subscription_feature(username, "advanced_analytics"):
        st.warning("⚠️ This feature requires an Advanced or Premium subscription")
        st.info("Upgrade your plan to access social media monitoring features.")
        return
    
    brand_name = st.session_state.get('brand_name', 'Your Brand')
    posts = enhanced_monitor.simulate_monitoring_with_api(brand_name, st.session_state.sector)
    
    # Display posts with AI analysis
    for post in posts[:5]:
        threat_class = f"threat-{post['threat_level']}"
        sentiment_color = "#FF0000" if post['sentiment'] == 'negative' else "#FFD700" if post['sentiment'] == 'positive' else "#FFFFFF"
        
        with st.expander(f"{post['platform']} - {post['content'][:50]}..."):
            st.write(post['content'])
            st.caption(f"Engagement: {post['engagement']}")
            st.markdown(f"""
            <div style="display: flex; gap: 10px; margin-top: 10px;">
                <span class="{threat_class}">Threat: {post['threat_level'].upper()}</span>
                <span style="color: {sentiment_color}; font-weight: 600;">Sentiment: {post['sentiment'].upper()}</span>
            </div>
            """, unsafe_allow_html=True)

def show_ai_insights():
    """AI insights functionality - requires Advanced subscription"""
    st.header("🧠 AI-Powered Insights")
    
    # Get user's subscription
    username = st.session_state.get('username')
    
    if not auth_system.check_subscription_feature(username, "advanced_analytics"):
        st.warning("⚠️ This feature requires an Advanced or Premium subscription")
        st.info("Upgrade your plan to access AI-powered insights.")
        return
    
    brand_name = st.session_state.get('brand_name', 'Your Brand')
    
    # Generate sample analyses
    analyses = []
    for i in range(10):
        text = f"Sample text {i} about {brand_name} with {'high' if i < 3 else 'medium' if i < 6 else 'low'} threat level"
        analysis = ai_engine.detect_threats(text, brand_name)
        analyses.append(analysis)
    
    # Generate report
    report = ai_engine.generate_threat_report(analyses)
    
    # Display report
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="ai-visualization">
            <h4>📊 Threat Summary</h4>
            <p>Total Analyses: {}</p>
            <p>High Threats: {}</p>
            <p>Medium Threats: {}</p>
            <p>Low Threats: {}</p>
            <p>Average Sentiment: {:.2f}</p>
        </div>
        """.format(
            report['total_analyses'],
            report['threat_counts']['high'],
            report['threat_counts']['medium'],
            report['threat_counts']['low'],
            report['average_sentiment']
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="ai-visualization">
            <h4>✅ AI Recommendations</h4>
            {}
        </div>
        """.format(
            ''.join([f'<p>• {rec}</p>' for rec in report['recommendations']])
        ), unsafe_allow_html=True)
    
    # Keyword frequency analysis
    st.subheader("🔤 Keyword Frequency Analysis")
    
    texts = [a['text'] for a in analyses]
    keyword_freq = ai_engine.create_keyword_frequency(texts)
    
    # Create bar chart
    fig = viz.create_keyword_bar_chart(keyword_freq, "Top Keywords in Threat Analysis")
    st.plotly_chart(fig, use_container_width=True)
    
    # Threat patterns
    st.subheader("🔍 Threat Pattern Analysis")
    
    patterns = ai_engine.create_threat_patterns(analyses)
    
    # Create heatmap
    fig = viz.create_pattern_heatmap(patterns, "Threat Patterns by Platform and Level")
    st.plotly_chart(fig, use_container_width=True)
    
    # Pattern details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="ai-visualization">
            <h4>🎯 Top Threat Keywords</h4>
            {}
        </div>
        """.format(
            ''.join([f'<p>• {word}: {count}</p>' for word, count in list(patterns['high_threat_keywords'].most_common(5))])
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="ai-visualization">
            <h4>📱 Platform Distribution</h4>
            {}
        </div>
        """.format(
            ''.join([f'<p>• {platform}: {count}</p>' for platform, count in patterns['platform_distribution'].most_common()])
        ), unsafe_allow_html=True)

# Add enhanced threat analysis function
def show_enhanced_threat_analysis():
    """Show enhanced threat analysis with new features"""
    st.header("🧠 Enhanced AI Threat Analysis")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        text_to_analyze = st.text_area(
            "Enter text to analyze:",
            height=150,
            placeholder="Enter social media posts, reviews, comments, or any text related to your brand...",
            help="The AI will analyze this text for threats, sentiment, emotions, and patterns"
        )
        
        brand_name = st.text_input(
            "Brand Name:",
            value=st.session_state.get('brand_name', 'Your Brand'),
            help="Enter your brand name for accurate analysis"
        )
    
    with col2:
        st.markdown("""
        <div class="search-analysis-card">
            <h4>🔍 Analysis Features</h4>
            <p>• Advanced threat detection</p>
            <p>• Contextual sentiment</p>
            <p>• Emotion recognition</p>
            <p>• Pattern identification</p>
            <p>• Risk scoring</p>
            <p>• Action recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🚀 Analyze with Enhanced AI", use_container_width=True):
        if text_to_analyze and brand_name:
            # Show analysis animation
            with st.spinner("Performing enhanced AI analysis..."):
                # Perform enhanced analysis
                result = enhanced_ai_engine.enhanced_threat_detection(text_to_analyze, brand_name)
                st.session_state.enhanced_analysis_result = result
                
                # Show success message with key insights
                st.success(f"Analysis complete! Threat level: {result['final_threat_level'].upper()}")
        else:
            st.error("Please enter both text and brand name")
    
    # Display results if available
    if 'enhanced_analysis_result' in st.session_state:
        result = st.session_state.enhanced_analysis_result
        
        # Main results overview
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        # Key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            threat_class = f"threat-{result['final_threat_level']}"
            st.markdown(f"""
            <div class="metric-card">
                <h4>Threat Level</h4>
                <h2><span class="{threat_class}">{result['final_threat_level'].upper()}</span></h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            risk_color = "#EF4444" if result['risk_score'] > 0.7 else "#F59E0B" if result['risk_score'] > 0.4 else "#10B981"
            st.markdown(f"""
            <div class="metric-card">
                <h4>Risk Score</h4>
                <h2 style="color: {risk_color};">{result['risk_score']:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            urgency_color = "#EF4444" if result['urgency_level'] >= 4 else "#F59E0B" if result['urgency_level'] >= 3 else "#10B981"
            st.markdown(f"""
            <div class="metric-card">
                <h4>Urgency</h4>
                <h2 style="color: {urgency_color};">{result['urgency_level']}/5</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            sentiment_color = "#EF4444" if result['sentiment_analysis']['sentiment'] == 'negative' else "#10B981" if result['sentiment_analysis']['sentiment'] == 'positive' else "#F59E0B"
            st.markdown(f"""
            <div class="metric-card">
                <h4>Sentiment</h4>
                <h2 style="color: {sentiment_color};">{result['sentiment_analysis']['sentiment'].upper()}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed analysis tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 Detailed Analysis",
            "😢 Emotion Analysis",
            "🎯 Pattern Detection",
            "⚡ Recommended Actions"
        ])
        
        with tab1:
            st.subheader("Detailed Threat Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="search-analysis-card">
                    <h4>🔍 Threat Keywords Found</h4>
                    {}
                </div>
                """.format(
                    ', '.join(result['extended_keywords']) if result['extended_keywords'] else 'No significant threat keywords detected'
                ), unsafe_allow_html=True)
                
                st.markdown("""
                <div class="search-analysis-card">
                    <h4>📊 Sentiment Details</h4>
                    <p><strong>Primary Sentiment:</strong> {}</p>
                    <p><strong>Sentiment Score:</strong> {:.2f}</p>
                    <p><strong>Confidence:</strong> {:.2f}</p>
                    <p><strong>Negation Detected:</strong> {}</p>
                    <p><strong>Intensified:</strong> {}</p>
                </div>
                """.format(
                    result['sentiment_analysis']['sentiment'].title(),
                    result['sentiment_analysis']['score'],
                    result['sentiment_analysis']['confidence'],
                    "Yes" if result['sentiment_analysis']['contextual_factors']['negation'] else "No",
                    "Yes" if result['sentiment_analysis']['contextual_factors']['intensified'] else "No"
                ), unsafe_allow_html=True)
            
            with col2:
                # Risk gauge
                fig = enhanced_viz.create_risk_gauge(
                    result['risk_score'],
                    "Overall Risk Assessment"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("Emotion Analysis")
            
            if result['sentiment_analysis']['emotions']:
                # Emotion heatmap
                fig = enhanced_viz.create_emotion_heatmap(
                    result['sentiment_analysis']['emotions'],
                    "Detected Emotions"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Emotion details
                emotions = result['sentiment_analysis']['emotions']
                sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
                
                st.markdown("""
                <div class="search-analysis-card">
                    <h4>😊 Emotion Breakdown</h4>
                    {}
                </div>
                """.format(
                    ''.join([f'<p><strong>{emotion.title()}:</strong> {intensity:.2f}</p>' for emotion, intensity in sorted_emotions])
                ), unsafe_allow_html=True)
            else:
                st.info("No significant emotions detected in the text")
        
        with tab3:
            st.subheader("Pattern Detection")
            
            if result['detected_patterns']:
                st.markdown("""
                <div class="search-analysis-card">
                    <h4>🎯 Detected Patterns</h4>
                    {}
                </div>
                """.format(
                    ''.join([f'<p><strong>{pattern.replace("_", " ").title()}:</strong> {count} indicator(s)</p>' 
                            for pattern, count in result['detected_patterns'].items()])
                ), unsafe_allow_html=True)
                
                # Pattern visualization
                patterns = list(result['detected_patterns'].keys())
                counts = list(result['detected_patterns'].values())
                
                fig = go.Figure(data=[go.Bar(
                    x=[p.replace('_', ' ').title() for p in patterns],
                    y=counts,
                    marker_color='#FFD700'
                )])
                
                fig.update_layout(
                    title="Pattern Frequency",
                    title_x=0.5,
                    xaxis_title='Pattern Type',
                    yaxis_title='Frequency',
                    font=dict(color='white'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No specific patterns detected in the text")
        
        with tab4:
            st.subheader("Recommended Actions")
            
            st.markdown("""
            <div class="search-analysis-card">
                <h4>⚡ Priority Actions</h4>
                {}
            </div>
            """.format(
                ''.join([f'<p><strong>{action}</strong></p>' for action in result['recommended_actions']])
            ), unsafe_allow_html=True)
            
            # Action timeline
            if result['urgency_level'] >= 4:
                st.error("🚨 CRITICAL: Immediate action required within 1 hour")
            elif result['urgency_level'] >= 3:
                st.warning("⚠️ HIGH: Action required within 24 hours")
            else:
                st.info("ℹ️ STANDARD: Action required within 3-5 days")

# Add predictive analytics function
def show_predictive_analytics():
    """Show predictive analytics dashboard"""
    st.header("🔮 Predictive Analytics")
    
    # Generate sample historical data
    np.random.seed(42)
    historical_data = np.random.poisson(15, 30)  # 30 days of data
    
    # Perform trend prediction
    prediction = enhanced_ai_engine.predict_threat_trend(historical_data)
    
    # Display prediction
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create prediction chart
        fig = enhanced_viz.create_prediction_chart(
            historical_data,
            prediction,
            "Threat Trend Prediction"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="search-analysis-card">
            <h4>📈 Trend Analysis</h4>
            <p><strong>Current Trend:</strong> {}</p>
            <p><strong>Confidence:</strong> {:.1f}%</p>
            <p><strong>Change:</strong> {:.1f}%</p>
            <p><strong>Predicted Next Week:</strong> {:.1f} threats</p>
        </div>
        """.format(
            prediction['trend'].title(),
            prediction['confidence'] * 100,
            prediction['change_percent'],
            prediction['predicted_next_week']
        ), unsafe_allow_html=True)
        
        # Recommendations based on trend
        if prediction['trend'] == "increasing":
            st.error("""
            <div class="search-analysis-card">
                <h4>⚠️ Alert</h4>
                <p>Threats are increasing! Consider:</p>
                <p>• Increasing monitoring frequency</p>
                <p>• Preparing response templates</p>
                <p>• Alerting team members</p>
            </div>
            """, unsafe_allow_html=True)
        elif prediction['trend'] == "decreasing":
            st.success("""
            <div class="search-analysis-card">
                <h4>✅ Positive Trend</h4>
                <p>Threats are decreasing! Maintain:</p>
                <p>• Current monitoring levels</p>
                <p>• Response protocols</p>
                <p>• Team readiness</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("""
            <div class="search-analysis-card">
                <h4>ℹ️ Stable Trend</h4>
                <p>Threat levels are stable. Continue:</p>
                <p>• Standard monitoring</p>
                <p>• Regular reviews</p>
                <p>• Team training</p>
            </div>
            """, unsafe_allow_html=True)

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
    if "brand_name" not in st.session_state:
        st.session_state.brand_name = "Your Brand"
    
    # Set user subscription in session state
    username = st.session_state.get('username')
    if username and "user_subscription" not in st.session_state:
        st.session_state.user_subscription = auth_system.get_user_subscription(username)
    
    # Header
    st.markdown("""
    <h1 class="premium-header floating">BrandGuardian AI Pro</h1>
    <div style="text-align: center; margin-bottom: 20px;" class="accent-text">Advanced Business Intelligence & Digital Risk Protection</div>
    """, unsafe_allow_html=True)
    
    # Sidebar with user info and logout button
    with st.sidebar:
        # User info
        subscription_info = auth_system.subscription_plans[st.session_state.user_subscription]
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 3rem;">👤</div>
            <h3>{st.session_state.username}</h3>
            <p>{st.session_state.get('user_access_level', 'user').title()} Access</p>
            <p>{auth_system.users[st.session_state.username]['company']}</p>
            <div style="background-color: {subscription_info['color']}20; 
                        border: 1px solid {subscription_info['color']}; 
                        border-radius: 20px; padding: 8px 16px; margin-top: 10px; display: inline-block;">
                <span style="color: {subscription_info['color']}; font-weight: bold;">
                    {subscription_info['name']} Subscription
                </span>
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
        if st.session_state.user_subscription == "premium":
            st.success("✅ Premium Access")
            st.markdown('<span class="premium-badge">PREMIUM</span>', unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ {subscription_info['name']} Access")
        
        st.markdown("---")
        user_id = st.session_state.get('user_id')
        api_keys = api_manager.load_api_keys(user_id) if user_id else {}
        st.subheader("🔑 API Status")
        st.info(f"{len(api_keys)} platform(s) connected")
        
        # User management for admin only
        if st.session_state.get('user_access_level') == 'admin':
            st.markdown("---")
            if st.button("👥 User Management", use_container_width=True):
                st.session_state.show_user_management = True
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
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
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
            "📊 Executive Dashboard", 
            "🔍 Advanced Threat Analysis",
            "🧠 Enhanced AI Analysis",
            "🔮 Predictive Analytics",
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
            show_enhanced_threat_analysis()
        
        with tab4:
            show_predictive_analytics()
        
        with tab5:
            st.header("Social Monitoring")
            posts = enhanced_monitor.simulate_monitoring_with_api(brand_name, st.session_state.sector)
            for post in posts[:5]:
                with st.expander(f"{post['platform']} - {post['content'][:50]}..."):
                    st.write(post['content'])
                    st.caption(f"Engagement: {post['engagement']}")
        
        # Other tabs
        for tab, title in [(tab6, "Competitive Intelligence"), (tab7, "Influencer Network"), 
                          (tab8, "Crisis Prediction"), (tab9, "Brand Health")]:
            with tab:
                st.header(title)
                st.write(f"{title} content...")
        
        with tab10:
            show_api_key_management()
    else:
        # Regular user navigation
        show_user_ai_dashboard()

if __name__ == "__main__":
    main()
