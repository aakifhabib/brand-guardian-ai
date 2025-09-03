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
from typing import Dict, List, Tuple, Optional, Any
import logging
from functools import lru_cache
import sqlite3
import threading
from streamlit.components.v1 import html

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config first
st.set_page_config(
    page_title="BrandGuardian AI Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database setup
def init_db():
    """Initialize the SQLite database for storing user data and settings"""
    conn = sqlite3.connect('brandguardian.db')
    c = conn.cursor()
    
    # Create tables if they don't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        company TEXT,
        email TEXT,
        access_level TEXT DEFAULT 'client',
        subscription TEXT DEFAULT 'basic',
        created_at TEXT,
        last_login TEXT,
        failed_attempts INTEGER DEFAULT 0,
        last_failed_attempt TEXT,
        session_token TEXT,
        mfa_enabled INTEGER DEFAULT 0
    )
    ''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        platform TEXT NOT NULL,
        encrypted_key TEXT NOT NULL,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS threat_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        brand_name TEXT,
        threat_level TEXT,
        platform TEXT,
        content TEXT,
        sentiment TEXT,
        timestamp TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Generate and display premium access key
def generate_premium_key():
    """Generate a secure premium access key"""
    key = secrets.token_urlsafe(16)
    premium_key = f"BG-PREMIUM-{key.upper()}"
    return premium_key

# Display the premium key in the console (for admin use)
premium_access_key = generate_premium_key()
print(f"PREMIUM ACCESS KEY: {premium_access_key}")

# Black and Gold UI Theme
st.markdown("""
<style>
    /* Import elegant fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Raleway:wght@200;300;400;500;600;700;800;900&family=Montserrat:wght@300;400;500;600;700;800;900&family=Cinzel:wght@400;500;600;700;800;900&display=swap');
    
    /* Base styles with elegant black background */
    .main {
        background: 
            radial-gradient(ellipse at top, #0a0a0a 0%, #000000 50%, #000000 100%),
            linear-gradient(135deg, #000000 0%, #0a0a0a 25%, #000000 50%, #0a0a0a 75%, #000000 100%);
        background-size: 400% 400%, 100% 100%;
        animation: subtleShift 30s ease infinite;
        color: #FFFFFF;
        font-family: 'Montserrat', sans-serif;
        overflow-x: hidden;
        position: relative;
    }
    
    @keyframes subtleShift {
        0% { background-position: 0% 50%, 0% 50%; }
        50% { background-position: 100% 50%, 100% 50%; }
        100% { background-position: 0% 50%, 0% 50%; }
    }
    
    .stApp {
        background: 
            radial-gradient(ellipse at top, #0a0a0a 0%, #000000 50%, #000000 100%),
            linear-gradient(135deg, #000000 0%, #0a0a0a 25%, #000000 50%, #0a0a0a 75%, #000000 100%);
        background-size: 400% 400%, 100% 100%;
        animation: subtleShift 30s ease infinite;
    }
    
    /* Gold particles for elegance */
    .gold-particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
        pointer-events: none;
    }
    
    .gold-particle {
        position: absolute;
        width: 3px;
        height: 3px;
        background: radial-gradient(circle, rgba(255, 215, 0, 0.9) 0%, rgba(212, 175, 55, 0.7) 50%, transparent 100%);
        border-radius: 50%;
        box-shadow: 
            0 0 10px rgba(255, 215, 0, 0.8),
            0 0 20px rgba(212, 175, 55, 0.6);
        animation: goldFloat 25s infinite linear;
    }
    
    @keyframes goldFloat {
        0% { 
            transform: translateY(100vh) translateX(0) scale(0);
            opacity: 0;
        }
        10% {
            opacity: 1;
            transform: translateY(90vh) translateX(10px) scale(1);
        }
        90% {
            opacity: 1;
            transform: translateY(10vh) translateX(-10px) scale(1);
        }
        100% { 
            transform: translateY(0) translateX(0) scale(0);
            opacity: 0;
        }
    }
    
    /* Elegant gold pattern overlay */
    .gold-pattern {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(90deg, transparent 98%, rgba(255, 215, 0, 0.1) 100%),
            linear-gradient(0deg, transparent 98%, rgba(212, 175, 55, 0.1) 100%);
        background-size: 50px 50px;
        z-index: -1;
        opacity: 0.4;
        animation: patternPulse 15s ease-in-out infinite;
    }
    
    @keyframes patternPulse {
        0%, 100% { opacity: 0.2; }
        50% { opacity: 0.5; }
    }
    
    /* Enhanced BrandGuardian logo - Gold Shield */
    .brandguardian-logo {
        display: inline-block;
        position: relative;
        font-size: 8rem;
        animation: goldShield 4s infinite ease-in-out;
        filter: 
            drop-shadow(0 0 30px rgba(255, 215, 0, 0.8))
            drop-shadow(0 0 60px rgba(212, 175, 55, 0.6));
    }
    
    .brandguardian-logo::before {
        content: '';
        position: absolute;
        top: -20%;
        left: -20%;
        width: 140%;
        height: 140%;
        background: conic-gradient(
            from 0deg,
            transparent,
            rgba(255, 215, 0, 0.3),
            rgba(212, 175, 55, 0.3),
            transparent
        );
        border-radius: 50%;
        animation: goldRotation 8s linear infinite;
        z-index: -1;
    }
    
    .brandguardian-logo::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 120%;
        height: 120%;
        background: radial-gradient(
            circle,
            rgba(255, 215, 0, 0.4) 0%,
            rgba(212, 175, 55, 0.2) 40%,
            transparent 70%
        );
        transform: translate(-50%, -50%);
        border-radius: 50%;
        animation: goldPulse 3s ease-in-out infinite;
        z-index: -2;
    }
    
    @keyframes goldShield {
        0%, 100% { 
            transform: scale(1) rotate(0deg) translateY(0);
            filter: 
                drop-shadow(0 0 30px rgba(255, 215, 0, 0.8))
                drop-shadow(0 0 60px rgba(212, 175, 55, 0.6));
        }
        25% { 
            transform: scale(1.1) rotate(-5deg) translateY(-10px);
            filter: 
                drop-shadow(0 0 40px rgba(255, 215, 0, 0.9))
                drop-shadow(0 0 80px rgba(212, 175, 55, 0.7));
        }
        50% { 
            transform: scale(1) rotate(0deg) translateY(0);
            filter: 
                drop-shadow(0 0 50px rgba(212, 175, 55, 0.8))
                drop-shadow(0 0 100px rgba(255, 215, 0, 0.6));
        }
        75% { 
            transform: scale(1.1) rotate(5deg) translateY(-10px);
            filter: 
                drop-shadow(0 0 40px rgba(255, 215, 0, 0.9))
                drop-shadow(0 0 80px rgba(212, 175, 55, 0.7));
        }
    }
    
    @keyframes goldRotation {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes goldPulse {
        0%, 100% { 
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.6;
        }
        50% { 
            transform: translate(-50%, -50%) scale(1.3);
            opacity: 0.9;
        }
    }
    
    /* Premium header with gold effects */
    .premium-header {
        font-family: 'Cinzel', serif;
        font-size: 5rem;
        font-weight: 900;
        text-align: center;
        margin: 20px 0;
        background: 
            linear-gradient(90deg, #D4AF37 0%, #FFD700 25%, #D4AF37 50%, #FFD700 75%, #D4AF37 100%);
        background-size: 200% 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 
            0px 0px 30px rgba(255, 215, 0, 0.5),
            0px 0px 60px rgba(212, 175, 55, 0.3);
        animation: 
            goldGlow 3s ease-in-out infinite alternate,
            gradientShift 4s linear infinite;
        position: relative;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    @keyframes goldGlow {
        from { 
            text-shadow: 
                0px 0px 30px rgba(255, 215, 0, 0.5),
                0px 0px 60px rgba(212, 175, 55, 0.3);
            transform: scale(1);
        }
        to { 
            text-shadow: 
                0px 0px 50px rgba(212, 175, 55, 0.8),
                0px 0px 100px rgba(255, 215, 0, 0.5);
            transform: scale(1.02);
        }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    .floating {
        animation: goldFloat 6s ease-in-out infinite;
    }
    
    @keyframes goldFloat {
        0% { transform: translateY(0px) rotateX(0deg); }
        25% { transform: translateY(-15px) rotateX(5deg); }
        50% { transform: translateY(-10px) rotateX(0deg); }
        75% { transform: translateY(-15px) rotateX(-5deg); }
        100% { transform: translateY(0px) rotateX(0deg); }
    }
    
    .accent-text {
        font-size: 1.6rem;
        color: #FFD700;
        text-align: center;
        margin-bottom: 40px;
        animation: fadeIn 2s ease-in;
        font-family: 'Raleway', sans-serif;
        font-weight: 400;
        letter-spacing: 2px;
        text-transform: uppercase;
        position: relative;
    }
    
    .accent-text::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 2px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        animation: scanLine 3s linear infinite;
    }
    
    @keyframes scanLine {
        0% { transform: translateX(-100%) translateX(-50%); }
        100% { transform: translateX(100%) translateX(-50%); }
    }
    
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(30px) scale(0.9);
            filter: blur(10px);
        }
        to { 
            opacity: 1; 
            transform: translateY(0) scale(1);
            filter: blur(0);
        }
    }
    
    /* Elegant card styling with gold effects */
    .metric-card {
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.9) 0%, rgba(10, 10, 10, 0.8) 100%),
            linear-gradient(45deg, rgba(255, 215, 0, 0.05) 0%, transparent 100%);
        backdrop-filter: blur(20px);
        padding: 30px;
        border-radius: 25px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        margin: 20px 0;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.8),
            inset 0 0 30px rgba(255, 215, 0, 0.1);
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
        perspective: 1000px;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 215, 0, 0.2), 
            rgba(212, 175, 55, 0.2),
            transparent
        );
        transform: skewX(-25deg);
        transition: left 0.75s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-12px) rotateX(5deg);
        box-shadow: 
            0 30px 80px rgba(255, 215, 0, 0.3),
            inset 0 0 40px rgba(212, 175, 55, 0.2);
        border: 1px solid rgba(212, 175, 55, 0.5);
    }
    
    .metric-card h3 {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        color: #FFD700;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-card h1 {
        font-family: 'Cinzel', serif;
        font-size: 3rem;
        margin: 10px 0;
        background: linear-gradient(90deg, #FFD700, #D4AF37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .search-analysis-card {
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.9) 0%, rgba(10, 10, 10, 0.8) 100%),
            linear-gradient(45deg, rgba(255, 215, 0, 0.05) 0%, transparent 100%);
        backdrop-filter: blur(20px);
        padding: 30px;
        border-radius: 25px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        margin: 25px 0;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.8),
            inset 0 0 30px rgba(255, 215, 0, 0.1);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .search-analysis-card:hover {
        transform: translateY(-8px) rotateX(3deg);
        box-shadow: 
            0 25px 70px rgba(212, 175, 55, 0.4),
            inset 0 0 40px rgba(255, 215, 0, 0.2);
    }
    
    .search-result-card {
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.8) 0%, rgba(10, 10, 10, 0.7) 100%);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border-left: 5px solid #FFD700;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .search-result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, 
            transparent 30%, 
            rgba(255, 215, 0, 0.1) 50%, 
            transparent 70%
        );
        transform: translateX(-100%);
        transition: transform 0.6s;
    }
    
    .search-result-card:hover::before {
        transform: translateX(100%);
    }
    
    .search-result-card:hover {
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.95) 0%, rgba(10, 10, 10, 0.9) 100%);
        transform: translateX(15px) rotateY(5deg);
        box-shadow: 
            0 15px 40px rgba(255, 215, 0, 0.4),
            inset 0 0 30px rgba(212, 175, 55, 0.2);
    }
    
    /* Elegant threat indicators with gold effects */
    .threat-indicator {
        padding: 12px 20px;
        border-radius: 30px;
        font-size: 14px;
        font-weight: 700;
        margin: 10px;
        display: inline-block;
        letter-spacing: 1px;
        box-shadow: 
            0 8px 25px rgba(0, 0, 0, 0.6),
            inset 0 0 15px rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        font-family: 'Montserrat', sans-serif;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }
    
    .threat-indicator::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .threat-indicator:hover::before {
        left: 100%;
    }
    
    .threat-indicator:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 
            0 12px 35px rgba(0, 0, 0, 0.8),
            inset 0 0 25px rgba(255, 255, 255, 0.2);
    }
    
    .threat-high {
        background: 
            linear-gradient(135deg, rgba(212, 175, 55, 0.3) 0%, rgba(255, 215, 0, 0.1) 100%),
            linear-gradient(45deg, rgba(212, 175, 55, 0.2) 0%, transparent 100%);
        color: #FFD700;
        border: 2px solid rgba(212, 175, 55, 0.5);
        animation: threatPulse 2s ease-in-out infinite;
    }
    
    .threat-medium {
        background: 
            linear-gradient(135deg, rgba(184, 134, 11, 0.3) 0%, rgba(218, 165, 32, 0.1) 100%),
            linear-gradient(45deg, rgba(184, 134, 11, 0.2) 0%, transparent 100%);
        color: #D4AF37;
        border: 2px solid rgba(184, 134, 11, 0.5);
    }
    
    .threat-low {
        background: 
            linear-gradient(135deg, rgba(255, 215, 0, 0.3) 0%, rgba(255, 223, 0, 0.1) 100%),
            linear-gradient(45deg, rgba(255, 215, 0, 0.2) 0%, transparent 100%);
        color: #FFD700;
        border: 2px solid rgba(255, 215, 0, 0.5);
    }
    
    @keyframes threatPulse {
        0%, 100% { 
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.6),
                inset 0 0 15px rgba(255, 255, 255, 0.1);
        }
        50% { 
            box-shadow: 
                0 8px 25px rgba(212, 175, 55, 0.6),
                inset 0 0 25px rgba(255, 215, 0, 0.3);
        }
    }
    
    /* Status indicators with gold effects */
    .api-status-connected {
        color: #FFD700;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        font-family: 'Raleway', sans-serif;
    }
    
    .api-status-connected::before {
        content: '●';
        margin-right: 8px;
        animation: goldPulse 2s ease-in-out infinite;
        font-size: 1.2em;
    }
    
    .api-status-disconnected {
        color: #D4AF37;
        font-weight: 700;
        font-family: 'Raleway', sans-serif;
    }
    
    /* Enhanced button styling with gold effects */
    .stButton > button {
        border-radius: 20px;
        border: 2px solid rgba(255, 215, 0, 0.5);
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.9) 0%, rgba(10, 10, 10, 0.8) 100%),
            linear-gradient(45deg, rgba(255, 215, 0, 0.1) 0%, transparent 100%);
        color: #FFD700;
        font-weight: 700;
        padding: 15px 30px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 8px 25px rgba(0, 0, 0, 0.7),
            inset 0 0 20px rgba(255, 215, 0, 0.1);
        font-family: 'Montserrat', sans-serif;
        letter-spacing: 1px;
        text-transform: uppercase;
        transform-style: preserve-3d;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 215, 0, 0.3), 
            rgba(212, 175, 55, 0.3),
            transparent
        );
        transition: left 0.6s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        background: 
            linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(212, 175, 55, 0.1) 100%),
            linear-gradient(45deg, rgba(212, 175, 55, 0.2) 0%, transparent 100%);
        border: 2px solid rgba(212, 175, 55, 0.8);
        transform: translateY(-5px) rotateX(5deg);
        box-shadow: 
            0 15px 40px rgba(255, 215, 0, 0.5),
            inset 0 0 30px rgba(212, 175, 55, 0.2);
    }
    
    /* Enhanced tab styling with gold effects */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        margin-bottom: 25px;
        background: rgba(20, 20, 20, 0.3);
        padding: 10px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.8) 0%, rgba(10, 10, 10, 0.7) 100%),
            linear-gradient(45deg, rgba(255, 215, 0, 0.05) 0%, transparent 100%);
        border-radius: 15px 15px 0 0;
        padding: 18px 25px;
        border: 2px solid rgba(255, 215, 0, 0.3);
        border-bottom: none;
        font-weight: 700;
        transition: all 0.4s ease;
        font-family: 'Montserrat', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, 
            transparent 30%, 
            rgba(255, 215, 0, 0.1) 50%, 
            transparent 70%
        );
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .stTabs [data-baseweb="tab"]:hover::before {
        opacity: 1;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.9) 0%, rgba(10, 10, 10, 0.8) 100%),
            linear-gradient(45deg, rgba(255, 215, 0, 0.1) 0%, transparent 100%);
        transform: translateY(-3px);
    }
    
    .stTabs [aria-selected="true"] {
        background: 
            linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(212, 175, 55, 0.1) 100%),
            linear-gradient(45deg, rgba(212, 175, 55, 0.2) 0%, transparent 100%);
        border: 2px solid rgba(255, 215, 0, 0.5);
        border-bottom: none;
        box-shadow: 
            0 -8px 25px rgba(255, 215, 0, 0.4),
            inset 0 0 20px rgba(212, 175, 55, 0.2);
        transform: translateY(-5px);
    }
    
    /* Custom metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 800;
        color: #FFD700;
        font-family: 'Cinzel', serif;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1.2rem;
        font-weight: 600;
        font-family: 'Raleway', sans-serif;
    }
    
    /* Enhanced input styling with gold effects */
    .stSelectbox [data-baseweb="select"], 
    .stTextInput [data-baseweb="input"], 
    .stTextArea [data-baseweb="textarea"],
    .stNumberInput [data-baseweb="input"],
    .stDateInput [data-baseweb="input"],
    .stTimeInput [data-baseweb="input"] {
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.8) 0%, rgba(10, 10, 10, 0.7) 100%),
            linear-gradient(45deg, rgba(255, 215, 0, 0.05) 0%, transparent 100%);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 2px solid rgba(255, 215, 0, 0.3);
        color: white;
        transition: all 0.4s ease;
        font-family: 'Raleway', sans-serif;
        padding: 12px 20px;
    }
    
    .stSelectbox [data-baseweb="select"]:hover, 
    .stTextInput [data-baseweb="input"]:hover, 
    .stTextArea [data-baseweb="textarea"]:hover,
    .stNumberInput [data-baseweb="input"]:hover,
    .stDateInput [data-baseweb="input"]:hover,
    .stTimeInput [data-baseweb="input"]:hover {
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.9) 0%, rgba(10, 10, 10, 0.8) 100%),
            linear-gradient(45deg, rgba(212, 175, 55, 0.1) 0%, transparent 100%);
        border: 2px solid rgba(212, 175, 55, 0.5);
        transform: translateY(-2px);
    }
    
    /* Custom spinner with gold effect */
    .stSpinner > div {
        border: 4px solid rgba(0, 0, 0, 0.1);
        border-radius: 50%;
        border-top: 4px solid #FFD700;
        width: 50px;
        height: 50px;
        animation: goldSpin 1s linear infinite;
        margin: 0 auto;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }
    
    @keyframes goldSpin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Custom expander with gold effects */
    .streamlit-expanderHeader {
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.8) 0%, rgba(10, 10, 10, 0.7) 100%),
            linear-gradient(45deg, rgba(255, 215, 0, 0.05) 0%, transparent 100%);
        border-radius: 20px;
        padding: 20px 25px;
        border: 2px solid rgba(255, 215, 0, 0.3);
        font-weight: 700;
        transition: all 0.4s ease;
        font-family: 'Montserrat', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }
    
    .streamlit-expanderHeader::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, 
            transparent 30%, 
            rgba(255, 215, 0, 0.1) 50%, 
            transparent 70%
        );
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .streamlit-expanderHeader:hover::before {
        opacity: 1;
    }
    
    .streamlit-expanderHeader:hover {
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.9) 0%, rgba(10, 10, 10, 0.8) 100%),
            linear-gradient(45deg, rgba(255, 215, 0, 0.1) 0%, transparent 100%);
        transform: translateY(-3px);
        border: 2px solid rgba(212, 175, 55, 0.5);
    }
    
    /* Custom dataframes */
    .dataframe {
        border-radius: 25px;
        overflow: hidden;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.8),
            inset 0 0 30px rgba(255, 215, 0, 0.1);
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.9) 0%, rgba(10, 10, 10, 0.8) 100%);
    }
    
    /* Custom success/error boxes */
    .stAlert {
        border-radius: 25px;
        padding: 20px 25px;
        font-weight: 700;
        box-shadow: 
            0 15px 45px rgba(0, 0, 0, 0.7),
            inset 0 0 25px rgba(255, 255, 255, 0.1);
        font-family: 'Raleway', sans-serif;
        letter-spacing: 1px;
    }
    
    /* Custom sidebar */
    .css-1d391kg {
        background: 
            linear-gradient(180deg, #0a0a0a 0%, #000000 100%),
            linear-gradient(135deg, rgba(255, 215, 0, 0.05) 0%, transparent 100%);
        border-right: 2px solid rgba(255, 215, 0, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Custom chart elements */
    .stChart {
        border-radius: 25px;
        overflow: hidden;
        box-shadow: 
            0 25px 70px rgba(0, 0, 0, 0.8),
            inset 0 0 40px rgba(255, 215, 0, 0.1);
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.9) 0%, rgba(10, 10, 10, 0.8) 100%);
    }
    
    /* Custom progress bars */
    .stProgress > div > div > div {
        background: 
            linear-gradient(90deg, #FFD700, #D4AF37, #B8860B);
        background-size: 200% 100%;
        border-radius: 15px;
        box-shadow: 
            0 8px 25px rgba(255, 215, 0, 0.6),
            inset 0 0 20px rgba(255, 255, 255, 0.2);
        animation: progressFlow 3s linear infinite;
    }
    
    @keyframes progressFlow {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    /* Custom radio buttons */
    .stRadio [role="radiogroup"] {
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.8) 0%, rgba(10, 10, 10, 0.7) 100%),
            linear-gradient(45deg, rgba(255, 215, 0, 0.05) 0%, transparent 100%);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid rgba(255, 215, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Custom slider */
    .stSlider [role="slider"] {
        background: 
            linear-gradient(90deg, #FFD700, #D4AF37, #B8860B);
        background-size: 200% 100%;
        border-radius: 15px;
        height: 12px;
        animation: sliderFlow 4s linear infinite;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
    }
    
    @keyframes sliderFlow {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    /* Custom checkbox */
    .stCheckbox [data-baseweb="checkbox"] {
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.8) 0%, rgba(10, 10, 10, 0.7) 100%),
            linear-gradient(45deg, rgba(255, 215, 0, 0.05) 0%, transparent 100%);
        border-radius: 15px;
        border: 2px solid rgba(255, 215, 0, 0.3);
        padding: 15px;
    }
    
    /* Premium badge with gold effects */
    .premium-badge {
        background: 
            linear-gradient(135deg, #FFD700, #D4AF37, #B8860B);
        background-size: 200% 100%;
        color: #000000;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 13px;
        font-weight: 800;
        display: inline-block;
        margin-left: 15px;
        box-shadow: 
            0 8px 25px rgba(255, 215, 0, 0.6),
            inset 0 0 20px rgba(255, 255, 255, 0.3);
        animation: 
            shimmer 2s infinite,
            badgeFlow 4s linear infinite;
        font-family: 'Montserrat', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    @keyframes shimmer {
        0% { background-position: -200px; }
        100% { background-position: calc(200px + 100%); }
    }
    
    @keyframes badgeFlow {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    /* Security shield animation */
    .security-shield {
        display: inline-block;
        animation: shieldGold 3s infinite;
    }
    
    @keyframes shieldGold {
        0%, 100% { 
            transform: scale(1) rotate(0deg);
            filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.8));
        }
        25% { 
            transform: scale(1.2) rotate(-10deg);
            filter: drop-shadow(0 0 40px rgba(212, 175, 55, 0.9));
        }
        50% { 
            transform: scale(1) rotate(0deg);
            filter: drop-shadow(0 0 60px rgba(255, 215, 0, 0.8));
        }
        75% { 
            transform: scale(1.2) rotate(10deg);
            filter: drop-shadow(0 0 40px rgba(212, 175, 55, 0.9));
        }
    }
    
    /* Login form enhancements */
    .login-container {
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.95) 0%, rgba(10, 10, 10, 0.9) 100%),
            linear-gradient(45deg, rgba(255, 215, 0, 0.1) 0%, transparent 100%);
        backdrop-filter: blur(25px);
        border-radius: 30px;
        padding: 50px;
        border: 2px solid rgba(255, 215, 0, 0.3);
        box-shadow: 
            0 30px 80px rgba(0, 0, 0, 0.9),
            inset 0 0 40px rgba(255, 215, 0, 0.1);
        max-width: 600px;
        margin: 0 auto;
        position: relative;
        overflow: hidden;
    }
    
    .login-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, 
            rgba(255, 215, 0, 0.1) 0%, 
            rgba(212, 175, 55, 0.1) 50%, 
            transparent 70%
        );
        animation: loginRotate 20s linear infinite;
    }
    
    @keyframes loginRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Animated background for login */
    .login-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: 
            radial-gradient(circle at 20% 50%, rgba(255, 215, 0, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(212, 175, 55, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(184, 134, 11, 0.15) 0%, transparent 50%);
        animation: bgGoldMove 25s ease infinite;
    }
    
    @keyframes bgGoldMove {
        0%, 100% { 
            transform: translate(0, 0) rotate(0deg) scale(1);
            filter: hue-rotate(0deg);
        }
        33% { 
            transform: translate(30px, -30px) rotate(120deg) scale(1.1);
            filter: hue-rotate(30deg);
        }
        66% { 
            transform: translate(-30px, 30px) rotate(240deg) scale(0.9);
            filter: hue-rotate(60deg);
        }
    }
    
    /* Premium access card */
    .premium-access-card {
        background: 
            linear-gradient(135deg, rgba(255, 215, 0, 0.15) 0%, rgba(212, 175, 55, 0.15) 100%),
            linear-gradient(45deg, rgba(184, 134, 11, 0.1) 0%, transparent 100%);
        border: 3px solid rgba(255, 215, 0, 0.4);
        border-radius: 30px;
        padding: 40px;
        margin: 30px 0;
        box-shadow: 
            0 25px 70px rgba(255, 215, 0, 0.3),
            inset 0 0 50px rgba(212, 175, 55, 0.2);
        text-align: center;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
    }
    
    .premium-access-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, 
            rgba(255, 215, 0, 0.2) 0%, 
            rgba(212, 175, 55, 0.2) 50%, 
            transparent 70%
        );
        animation: premiumRotate 25s linear infinite;
    }
    
    @keyframes premiumRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Threat radar animation */
    .threat-radar {
        position: relative;
        width: 250px;
        height: 250px;
        margin: 0 auto;
    }
    
    .radar-circle {
        position: absolute;
        border: 3px solid rgba(255, 215, 0, 0.4);
        border-radius: 50%;
        animation: radarGoldPulse 2.5s infinite;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
    }
    
    @keyframes radarGoldPulse {
        0% { 
            transform: scale(0.7); 
            opacity: 1;
            border-color: rgba(255, 215, 0, 0.8);
        }
        50% { 
            transform: scale(1.3); 
            opacity: 0.5;
            border-color: rgba(212, 175, 55, 0.8);
        }
        100% { 
            transform: scale(0.7); 
            opacity: 1;
            border-color: rgba(184, 134, 11, 0.8);
        }
    }
    
    /* Enhanced AI visualization */
    .ai-visualization {
        background: 
            linear-gradient(135deg, rgba(20, 20, 20, 0.9) 0%, rgba(10, 10, 10, 0.8) 100%),
            linear-gradient(45deg, rgba(255, 215, 0, 0.1) 0%, transparent 100%);
        border-radius: 30px;
        padding: 30px;
        margin: 30px 0;
        border: 2px solid rgba(255, 215, 0, 0.3);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.8),
            inset 0 0 40px rgba(212, 175, 55, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .ai-visualization::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            linear-gradient(45deg, 
                transparent 30%, 
                rgba(255, 215, 0, 0.05) 50%, 
                transparent 70%
            ),
            linear-gradient(-45deg, 
                transparent 30%, 
                rgba(212, 175, 55, 0.05) 50%, 
                transparent 70%
            );
        animation: aiScan 8s linear infinite;
    }
    
    @keyframes aiScan {
        0% { transform: translateX(-100%) translateY(-100%); }
        100% { transform: translateX(100%) translateY(100%); }
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
        background: radial-gradient(circle, 
            rgba(255, 215, 0, 0.4) 0%, 
            rgba(212, 175, 55, 0.2) 50%, 
            transparent 70%
        );
        animation: aiGoldPulse 3s infinite;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
    }
    
    @keyframes aiGoldPulse {
        0% { 
            transform: scale(1); 
            opacity: 0.7;
        }
        25% { 
            transform: scale(1.4); 
            opacity: 0.4;
        }
        50% { 
            transform: scale(1); 
            opacity: 0.7;
        }
        75% { 
            transform: scale(1.2); 
            opacity: 0.5;
        }
        100% { 
            transform: scale(1); 
            opacity: 0.7;
        }
    }
    
    /* New Threat Analysis Animation */
    .threat-analysis-container {
        position: relative;
        width: 100%;
        height: 300px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 30px 0;
    }
    
    .radar-scanner {
        position: relative;
        width: 220px;
        height: 220px;
        margin-bottom: 30px;
    }
    
    .radar-background {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: 
            radial-gradient(circle, 
                rgba(20, 20, 20, 0.95) 0%, 
                rgba(10, 10, 10, 0.8) 70%, 
                transparent 100%
            );
        border: 3px solid rgba(255, 215, 0, 0.4);
        overflow: hidden;
        box-shadow: 
            0 0 40px rgba(255, 215, 0, 0.5),
            inset 0 0 30px rgba(212, 175, 55, 0.3);
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
        background: rgba(255, 215, 0, 0.3);
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.6);
    }
    
    .radar-grid::before {
        width: 3px;
        height: 100%;
        left: 50%;
        transform: translateX(-50%);
    }
    
    .radar-grid::after {
        width: 100%;
        height: 3px;
        top: 50%;
        transform: translateY(-50%);
    }
    
    .radar-sweep {
        position: absolute;
        width: 60%;
        height: 4px;
        background: 
            linear-gradient(90deg, 
                transparent, 
                rgba(255, 215, 0, 0.9), 
                rgba(212, 175, 55, 0.9),
                transparent
            );
        top: 50%;
        left: 50%;
        transform-origin: left center;
        animation: radarGoldSweep 4s linear infinite;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
    }
    
    @keyframes radarGoldSweep {
        0% { 
            transform: rotate(0deg);
            background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.9), transparent);
        }
        33% { 
            transform: rotate(120deg);
            background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.9), transparent);
        }
        66% { 
            transform: rotate(240deg);
            background: linear-gradient(90deg, transparent, rgba(184, 134, 11, 0.9), transparent);
        }
        100% { 
            transform: rotate(360deg);
            background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.9), transparent);
        }
    }
    
    .radar-sweep::before {
        content: '';
        position: absolute;
        width: 15px;
        height: 15px;
        background: radial-gradient(circle, 
            rgba(255, 215, 0, 1) 0%, 
            rgba(212, 175, 55, 1) 50%, 
            rgba(184, 134, 11, 1) 100%
        );
        border-radius: 50%;
        right: 0;
        top: -6px;
        box-shadow: 
            0 0 20px rgba(255, 215, 0, 1),
            0 0 40px rgba(212, 175, 55, 0.8),
            0 0 60px rgba(184, 134, 11, 0.6);
        animation: sweepPulse 1s ease-in-out infinite;
    }
    
    @keyframes sweepPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.5); }
    }
    
    .threat-dots {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
    }
    
    .threat-dot {
        position: absolute;
        width: 12px;
        height: 12px;
        background: radial-gradient(circle, 
            rgba(255, 215, 0, 1) 0%, 
            rgba(212, 175, 55, 1) 50%, 
            rgba(184, 134, 11, 1) 100%
        );
        border-radius: 50%;
        opacity: 0;
        animation: threatGoldPulse 2.5s infinite;
        box-shadow: 
            0 0 15px rgba(255, 215, 0, 0.8),
            0 0 30px rgba(212, 175, 55, 0.6);
    }
    
    .threat-dot.active {
        opacity: 1;
    }
    
    @keyframes threatGoldPulse {
        0% { 
            transform: scale(1); 
            opacity: 0.7;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.8);
        }
        25% { 
            transform: scale(1.8); 
            opacity: 1;
            box-shadow: 0 0 25px rgba(212, 175, 55, 1);
        }
        50% { 
            transform: scale(1); 
            opacity: 0.7;
            box-shadow: 0 0 15px rgba(184, 134, 11, 0.8);
        }
        75% { 
            transform: scale(1.4); 
            opacity: 0.9;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.9);
        }
        100% { 
            transform: scale(1); 
            opacity: 0.7;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.8);
        }
    }
    
    .analysis-status {
        font-size: 1.5rem;
        font-weight: 700;
        color: #FFD700;
        text-align: center;
        margin-bottom: 20px;
        font-family: 'Cinzel', serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
    }
    
    .progress-container {
        width: 80%;
        height: 12px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.5);
    }
    
    .progress-bar {
        height: 100%;
        width: 0%;
        background: 
            linear-gradient(90deg, #FFD700, #D4AF37, #B8860B);
        background-size: 200% 100%;
        border-radius: 8px;
        transition: width 0.4s ease;
        animation: 
            progressFill 4s ease-in-out forwards,
            progressGoldFlow 2s linear infinite;
        box-shadow: 
            0 0 20px rgba(255, 215, 0, 0.6),
            inset 0 0 15px rgba(255, 255, 255, 0.3);
    }
    
    @keyframes progressFill {
        0% { width: 0%; }
        100% { width: 100%; }
    }
    
    @keyframes progressGoldFlow {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    .analysis-phases {
        display: flex;
        justify-content: space-between;
        width: 80%;
        margin-top: 20px;
    }
    
    .phase {
        display: flex;
        flex-direction: column;
        align-items: center;
        opacity: 0.4;
        transition: all 0.4s ease;
        transform: translateY(10px);
    }
    
    .phase.active {
        opacity: 1;
        transform: translateY(0);
    }
    
    .phase-icon {
        font-size: 2rem;
        margin-bottom: 10px;
        filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.6));
    }
    
    .phase-text {
        font-size: 0.9rem;
        color: #FFD700;
        font-family: 'Montserrat', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-align: center;
    }
    
    .phase:nth-child(1) {
        animation: phaseGoldActivate 4s ease-in-out forwards;
    }
    
    .phase:nth-child(2) {
        animation: phaseGoldActivate 4s ease-in-out 1s forwards;
    }
    
    .phase:nth-child(3) {
        animation: phaseGoldActivate 4s ease-in-out 2s forwards;
    }
    
    .phase:nth-child(4) {
        animation: phaseGoldActivate 4s ease-in-out 3s forwards;
    }
    
    @keyframes phaseGoldActivate {
        0% { 
            opacity: 0.4; 
            transform: translateY(10px) scale(0.9);
        }
        25% { 
            opacity: 1; 
            transform: translateY(-5px) scale(1.1);
        }
        50% { 
            opacity: 1; 
            transform: translateY(0) scale(1);
        }
        100% { 
            opacity: 1; 
            transform: translateY(0) scale(1);
        }
    }
</style>
""", unsafe_allow_html=True)

# Add gold particles to the background
def add_gold_particles():
    st.markdown("""
    <div class="gold-particles">
        <div class="gold-particle" style="left: 5%; animation-duration: 22s; animation-delay: 0s;"></div>
        <div class="gold-particle" style="left: 15%; animation-duration: 28s; animation-delay: 1s;"></div>
        <div class="gold-particle" style="left: 25%; animation-duration: 25s; animation-delay: 2s;"></div>
        <div class="gold-particle" style="left: 35%; animation-duration: 30s; animation-delay: 0.5s;"></div>
        <div class="gold-particle" style="left: 45%; animation-duration: 24s; animation-delay: 1.5s;"></div>
        <div class="gold-particle" style="left: 55%; animation-duration: 32s; animation-delay: 2.5s;"></div>
        <div class="gold-particle" style="left: 65%; animation-duration: 26s; animation-delay: 3s;"></div>
        <div class="gold-particle" style="left: 75%; animation-duration: 29s; animation-delay: 0.8s;"></div>
        <div class="gold-particle" style="left: 85%; animation-duration: 31s; animation-delay: 1.8s;"></div>
        <div class="gold-particle" style="left: 95%; animation-duration: 27s; animation-delay: 2.2s;"></div>
    </div>
    <div class="gold-pattern"></div>
    """, unsafe_allow_html=True)

# Add the new animation function
def show_threat_analysis_animation():
    """Display a gold radar scanning animation for threat analysis"""
    placeholder = st.empty()
    
    with placeholder.container():
        st.markdown("""
        <div class="threat-analysis-container">
            <div class="radar-scanner">
                <div class="radar-background"></div>
                <div class="radar-grid"></div>
                <div class="radar-sweep"></div>
                <div class="threat-dots">
                    <div class="threat-dot active" style="top: 25%; left: 35%; animation-delay: 0.5s;"></div>
                    <div class="threat-dot active" style="top: 65%; left: 75%; animation-delay: 1.2s;"></div>
                    <div class="threat-dot active" style="top: 15%; left: 55%; animation-delay: 1.8s;"></div>
                    <div class="threat-dot active" style="top: 75%; left: 25%; animation-delay: 2.4s;"></div>
                    <div class="threat-dot active" style="top: 45%; left: 85%; animation-delay: 3.0s;"></div>
                </div>
            </div>
            <div class="analysis-status">Gold Threat Scan</div>
            <div class="progress-container">
                <div class="progress-bar"></div>
            </div>
            <div class="analysis-phases">
                <div class="phase">
                    <div class="phase-icon">🔍</div>
                    <div class="phase-text">Gold Scan</div>
                </div>
                <div class="phase">
                    <div class="phase-icon">🧠</div>
                    <div class="phase-text">Neural Process</div>
                </div>
                <div class="phase">
                    <div class="phase-icon">📊</div>
                    <div class="phase-text">AI Analysis</div>
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
                "color": "#D4AF37"
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
                "color": "#FFD700"
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
                "color": "#B8860B"
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

# Initialize AI analysis engine
ai_engine = AIAnalysisEngine()

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
    
    def generate_analysis(self, threat_level, found_keywords):
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

# Advanced Data Visualization
class AdvancedVisualizations:
    def __init__(self):
        self.colors = {
            'primary': '#FFD700',
            'secondary': '#D4AF37',
            'success': '#B8860B',
            'warning': '#FFD700',
            'danger': '#D4AF37',
            'info': '#B8860B',
            'dark': '#0a0a0a',
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

# Initialize visualizations
viz = AdvancedVisualizations()

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
        <div class="brandguardian-logo">🛡️</div>
        <h1 style="font-size: 4rem; font-weight: 800; background: linear-gradient(90deg, #FFD700 0%, #D4AF37 50%, #B8860B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">BrandGuardian AI</h1>
        <p style="font-size: 1.4rem; color: #FFD700; font-family: 'Raleway', sans-serif;">GOLD STANDARD THREAT INTELLIGENCE</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two-column layout for login
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style='text-align: center;'>
            <div style="font-size: 7rem; margin-bottom: 30px;" class="security-shield">🔒</div>
            <h3 style="color: #FFD700; font-family: 'Cinzel', serif;">GOLD SECURE LOGIN</h3>
            <p style="color: #FFD700; font-family: 'Raleway', sans-serif;">ACCESS YOUR PREMIUM DASHBOARD</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            # Remember me checkbox
            remember_me = st.checkbox("Remember me")
            
            submit = st.form_submit_button("🚀 GOLD ACCESS", use_container_width=True)
            
            if submit:
                success, message = auth_system.authenticate(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_access_level = auth_system.users[username]["access_level"]
                    st.session_state.user_id = auth_system.users[username]["user_id"]
                    st.session_state.login_time = datetime.now().isoformat()
                    st.session_state.remember_me = remember_me
                    
                    st.success("✅ Gold Authentication Successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    # Security information
    with st.expander("🔒 GOLD SECURITY PROTOCOLS"):
        st.markdown("""
        - Military-grade gold encryption
        - Premium network authentication
        - Real-time threat detection
        - Biometric verification ready
        - Zero-trust architecture
        - Automated security audits
        """)
    
    # Forgot password link
    st.markdown("""
    <div style='text-align: center; margin-top: 30px;'>
        <a href='#' style='color: #FFD700; text-decoration: none; font-family: 'Raleway', sans-serif;'>FORGOT GOLD KEY?</a>
    </div>
    """, unsafe_allow_html=True)

# Advanced Threat Analysis Functionality
def show_advanced_threat_analysis():
    if not security_manager.check_access():
        show_access_required()
        return
    
    st.header("🔍 GOLD THREAT ANALYSIS")
    st.success("✅ GOLD ACCESS GRANTED - PREMIUM FEATURES UNLOCKED")
    
    # Tab system for advanced analysis
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 GOLD DASHBOARD",
        "🔍 PREMIUM SCAN",
        "📈 PREDICTIVE ANALYTICS", 
        "⚡ GOLD ACTIONS"
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
    st.subheader("🛡️ GOLD THREAT MATRIX")
    
    # Create metrics with custom styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>GOLD THREATS</h3>
            <h1>∞</h1>
            <p style="color: #FFD700;">PREMIUM DETECTION ACTIVE</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>THREAT LEVEL</h3>
            <h1>GOLD</h1>
            <p style="color: #FFD700;">PREMIUM ANALYSIS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>RESPONSE TIME</h3>
            <h1>0.00s</h1>
            <p style="color: #FFD700;">INSTANTANEOUS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>PROTECTED ASSETS</h3>
            <h1>∞</h1>
            <p style="color: #FFD700;">GOLD ENCRYPTION</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Threat timeline with advanced visualization
    st.subheader("📈 GOLD THREAT TIMELINE")
    
    # Generate sample data with valid dates
    dates = pd.date_range(end=datetime.now(), periods=7)
    threats = [8, 12, 5, 18, 10, 7, 14]
    
    # Create an advanced chart
    fig = viz.create_sentiment_timeline(dates, threats, "Gold Threat Activity Over Time")
    st.plotly_chart(fig, use_container_width=True)
    
    # Threat distribution
    st.subheader("🌡️ GOLD THREAT DISTRIBUTION")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        threat_data = {'High': 8, 'Medium': 5, 'Low': 5}
        fig = viz.create_threat_distribution(threat_data, "Gold Threat Severity Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="search-analysis-card">
            <h4>🧠 PREMIUM INSIGHTS</h4>
            <p><span class="threat-high">High</span>: 8 gold threats</p>
            <p><span class="threat-medium">Medium</span>: 5 premium threats</p>
            <p><span class="threat-low">Low</span>: 5 standard threats</p>
            <p>Primary platform: Twitter</p>
            <p>Peak frequency: 14:00-16:00</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent threats table
    st.subheader("🚨 GOLD THREAT ALERTS")
    
    threat_alerts = []
    for i in range(8):
        threat_alerts.append({
            'Time': (datetime.now() - timedelta(hours=i)).strftime("%H:%M"),
            'Platform': random.choice(['Twitter', 'Facebook', 'Reddit', 'Instagram']),
            'Type': random.choice(['Gold Impersonation', 'Premium Negative', 'Luxury Fake', 'Exclusive Copyright']),
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
            'content': f"Similar gold {results['threat_level']} threat pattern detected",
            'severity': results['threat_level'],
            'date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
        })
    return threats

def show_search_analysis():
    """Search analysis functionality"""
    st.subheader("🔍 PREMIUM NEURAL SEARCH")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_area(
            "Enter premium search query or neural keywords:",
            height=100,
            placeholder="Example: 'Your Brand gold scam neural complaints customer service luxury issues'",
            help="Enter gold keywords, neural phrases, or full premium sentences to analyze for brand threats"
        )
        
        # Get the brand name from session state or use a default
        brand_name = st.session_state.get('brand_name', 'Your Brand')
        
        if st.button("🚀 INITIATE GOLD SCAN", use_container_width=True):
            if search_query and brand_name:
                # Show the enhanced animation
                animation_placeholder = show_threat_analysis_animation()
                
                # Simulate analysis with the animation running
                time.sleep(4)  # Allow time for animation to complete
                
                # Clear the animation
                animation_placeholder.empty()
                
                # Perform the actual analysis
                results = search_analyzer.analyze_search(search_query, brand_name)
                st.session_state.search_results = results
                st.success("Gold Analysis Complete!")
            else:
                st.error("Please enter both gold query and brand name")
    
    with col2:
        st.markdown("""
        <div class="search-analysis-card">
            <h4>🎯 PREMIUM SCAN TIPS</h4>
            <p>• Use gold-specific keywords</p>
            <p>• Include premium brand names</p>
            <p>• Add luxury modifiers</p>
            <p>• Use premium quotation marks</p>
            <p>• Include gold platform names</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="search-analysis-card">
            <h4>📊 GOLD THREAT LEVELS</h4>
            <p><span class="threat-high">High</span> - Gold action needed</p>
            <p><span class="threat-medium">Medium</span> - Premium monitoring</p>
            <p><span class="threat-low">Low</span> - Standard scanning</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display results if available
    if 'search_results' in st.session_state:
        results = st.session_state.search_results
        
        st.markdown("---")
        st.subheader("📋 GOLD ANALYSIS RESULTS")
        
        # Threat level indicator
        threat_class = f"threat-{results['threat_level']}"
        st.markdown(f"""
        <div class="search-analysis-card">
            <h4>Gold Threat Level: <span class="{threat_class}">{results['threat_level'].upper()}</span></h4>
            <p><strong>Gold Query:</strong> {results['query']}</p>
            <p><strong>Premium Brand:</strong> {results['brand']}</p>
            <p><strong>Luxury Keywords Found:</strong> {', '.join(results['keywords_found']) or 'None'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Analysis and recommendations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="search-analysis-card">
                <h4>🧠 GOLD ANALYSIS</h4>
                <p>{results['analysis']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="search-analysis-card">
                <h4>✅ GOLD RECOMMENDATIONS</h4>
                {''.join([f'<p>• {rec}</p>' for rec in results['recommendations']])}
            </div>
            """, unsafe_allow_html=True)
        
        # Similar threat examples
        st.subheader("🔍 GOLD THREAT PATTERNS")
        similar_threats = generate_similar_threats(results)
        for threat in similar_threats:
            st.markdown(f"""
            <div class="search-result-card">
                <p><strong>{threat['platform']}</strong> - {threat['content']}</p>
                <p>Gold Severity: <span class="threat-{threat['severity']}">{threat['severity']}</span></p>
            </div>
            """, unsafe_allow_html=True)

def show_trend_analysis():
    """Trend analysis functionality"""
    st.subheader("📈 PREMIUM PREDICTIVE ANALYTICS")
    
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
        name='Gold High Threats',
        line=dict(color='#D4AF37', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=trend_data['Date'],
        y=trend_data['Medium Threats'],
        mode='lines+markers',
        name='Premium Medium Threats',
        line=dict(color='#FFD700', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=trend_data['Date'],
        y=trend_data['Low Threats'],
        mode='lines+markers',
        name='Standard Low Threats',
        line=dict(color='#B8860B', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Gold Threat Trends Over Time",
        title_x=0.5,
        xaxis_title='Date',
        yaxis_title='Number of Gold Threats',
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Platform distribution with radar chart
    st.subheader("🌐 PREMIUM DISTRIBUTION")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        platforms = ['Twitter', 'Facebook', 'Reddit', 'Instagram', 'YouTube']
        threat_counts = [45, 32, 28, 19, 12]
        
        # Create radar chart
        fig = viz.create_radar_chart(
            np.array(threat_counts),
            platforms,
            "Gold Threat Distribution Across Premium Platforms"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="search-analysis-card">
            <h4>🧠 LUXURY INSIGHTS</h4>
            <p>Twitter: 45 gold threats (42%)</p>
            <p>Facebook: 32 premium threats (30%)</p>
            <p>Reddit: 28 luxury threats (26%)</p>
            <p>Instagram: 19 standard threats (18%)</p>
            <p>YouTube: 12 basic threats (11%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sentiment analysis over time
    st.subheader("📊 GOLD SENTIMENT ANALYSIS")
    
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
        name='Gold Sentiment',
        line=dict(color='#FFD700', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(255, 215, 0, 0.2)'
    ))
    
    fig.update_layout(
        title="Gold Sentiment Analysis Over Time",
        title_x=0.5,
        xaxis_title='Date',
        yaxis_title='Gold Sentiment Score',
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_quick_actions():
    """Quick action buttons"""
    st.subheader("⚡ GOLD ACTION PROTOCOLS")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 PREMIUM SCAN", use_container_width=True):
            st.success("Gold Platform Scan Initiated!")
            time.sleep(1)
            st.info("Scanning Gold Twitter, Premium Facebook, Luxury Instagram, Standard Reddit...")
    
    with col2:
        if st.button("📊 GENERATE GOLD REPORT", use_container_width=True):
            st.success("Gold Threat Report Generation Started!")
            time.sleep(1)
            st.info("Compiling Gold Data from Last 7 Premium Periods...")
    
    with col3:
        if st.button("🚨 GOLD CRISIS PROTOCOL", use_container_width=True):
            st.error("Gold Crisis Protocol Activated!")
            time.sleep(1)
            st.warning("Alerting Premium Team Members...")

def show_access_required():
    st.header("🔒 GOLD THREAT ANALYSIS")
    st.warning("🚫 GOLD ACCESS REQUIRED")
    
    st.write("""
    ### Unlock Gold Threat Analysis Features
    
    To access our gold neural threat detection capabilities, please enter your gold access key below.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        access_key = st.text_input(
            "Enter Gold Access Key:",
            type="password",
            placeholder="BG2024-PRO-ACCESS",
            help="Enter your gold premium access key"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🔓 UNLOCK GOLD FEATURES", use_container_width=True):
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
                st.error("Please enter a gold access key")
    
    with st.expander("🆓 GOLD DEMO ACCESS"):
        st.info("Use gold demo key: BG2024-PRO-ACCESS")
        if st.button("Use Gold Demo Key"):
            st.session_state.advanced_access = True
            st.session_state.access_level = "full"
            st.success("Gold Demo Access Granted!")
            st.balloons()
            st.rerun()
    
    # Premium access card
    st.markdown("""
    <div class="premium-access-card">
        <h3>🌟 GOLD ACCESS FEATURES</h3>
        <p>Unlock the full gold potential of BrandGuardian AI with our premium features:</p>
        <ul style="text-align: left; display: inline-block;">
            <li>Gold threat detection algorithms</li>
            <li>Premium real-time monitoring across all platforms</li>
            <li>AI-powered gold sentiment analysis</li>
            <li>Gold customizable threat alerts</li>
            <li>Luxury threat intelligence reports</li>
            <li>Premium priority customer support</li>
        </ul>
        <p>Contact your gold administrator to get your premium access key.</p>
    </div>
    """, unsafe_allow_html=True)

# API Management Tab
def show_api_key_management():
    st.header("🔑 GOLD API MANAGEMENT CENTER")
    
    # Get current user's ID
    user_id = st.session_state.get('user_id')
    if not user_id:
        st.error("Gold User not authenticated")
        return
    
    # Display current connections
    st.subheader("🌐 PREMIUM CONNECTED PLATFORMS")
    
    api_keys = api_manager.load_api_keys(user_id)
    if api_keys:
        cols = st.columns(3)
        for i, (platform, encrypted_key) in enumerate(api_keys.items()):
            if platform in api_manager.supported_platforms:
                platform_info = api_manager.supported_platforms[platform]
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="search-analysis-card">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">{platform_info['icon']}</div>
                        <h4>{platform_info['name']}</h4>
                        <p>Gold Status: <span class="api-status-connected">✅ CONNECTED</span></p>
                        <p>Premium Rate Limit: {platform_info['rate_limit']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Gold Disconnect {platform}", key=f"disconnect_{platform}", use_container_width=True):
                        if api_manager.delete_api_key(user_id, platform):
                            st.success(f"Gold Disconnected from {platform_info['name']}")
                            st.rerun()
    else:
        st.info("🌟 Connect your first gold platform to get started!")
    
    # Add new connection
    st.subheader("🚀 CONNECT NEW GOLD PLATFORM")
    
    platforms = api_manager.supported_platforms
    selected_platform = st.selectbox("Select Gold Platform", list(platforms.keys()), 
                                   format_func=lambda x: f"{platforms[x]['icon']} {platforms[x]['name']}")
    
    platform_info = platforms[selected_platform]
    
    st.markdown(f"""
    <div class="search-analysis-card">
        <h4>{platform_info['icon']} {platform_info['name']}</h4>
        <p><strong>Gold Rate Limit:</strong> {platform_info['rate_limit']}</p>
        <p><strong>Premium Documentation:</strong> <a href="{platform_info['help_url']}" target="_blank">Get Gold API Key →</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    api_key = st.text_input(
        f"{platform_info['field_name']}*",
        type="password",
        placeholder=f"Paste your gold {platform_info['field_name']} here...",
        help=platform_info['field_help']
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧠 GOLD TEST CONNECTION", use_container_width=True):
            if api_key:
                with st.spinner("Gold Testing..."):
                    result = api_manager.test_connection(selected_platform, api_key)
                if result["success"]:
                    st.success(result["message"])
                    st.info(f"Gold Rate Limit: {result['rate_limit']}")
                else:
                    st.error(result["message"])
            else:
                st.error("Please enter gold API key")
    
    with col2:
        if st.button("💾 GOLD SAVE CONNECTION", use_container_width=True):
            if api_key:
                if api_manager.save_api_key(user_id, selected_platform, api_key):
                    st.success("✅ Gold Connection Saved!")
                    st.balloons()
                else:
                    st.error("❌ Gold Save Failed")
            else:
                st.error("Please enter gold API key")
    
    with col3:
        if st.button("🔄 GOLD CLEAR", use_container_width=True):
            st.rerun()
    
    # Platform status
    st.subheader("📊 GOLD PLATFORM STATUS")
    status_data = []
    for platform, info in api_manager.supported_platforms.items():
        status_data.append({
            "Gold Platform": f"{info['icon']} {info['name']}",
            "Status": "✅ GOLD CONNECTED" if platform in api_keys else "❌ GOLD DISCONNECTED",
            "Premium Rate Limit": info['rate_limit']
        })
    
    status_df = pd.DataFrame(status_data)
    st.dataframe(status_df, use_container_width=True, hide_index=True)

# User AI Dashboard (for regular users)
def show_user_ai_dashboard():
    st.header("🤖 PREMIUM BRANDGUIAN AI DASHBOARD")
    
    # Get user's subscription
    username = st.session_state.get('username')
    subscription = auth_system.get_user_subscription(username)
    subscription_info = auth_system.subscription_plans[subscription]
    
    # Welcome message with subscription info
    brand_name = st.session_state.get('brand_name', 'Your Brand')
    st.success(f"Welcome to your gold brand protection dashboard, {brand_name}!")
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
            <a href="#upgrade" style="color: #FFD700; text-decoration: none; font-family: 'Raleway', sans-serif;">Upgrade Gold Plan →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>PREMIUM MENTIONS</h3>
            <h1>∞</h1>
            <p style="color: #FFD700;">LUXURY GROWTH DETECTED</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>THREAT LEVEL</h3>
            <h1>GOLD</h1>
            <p style="color: #FFD700;">PREMIUM STABILITY</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>RESPONSE RATE</h3>
            <h1>100%</h1>
            <p style="color: #FFD700;">GOLD EFFICIENCY</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Create tabs based on subscription
    available_tabs = ["Premium Search Analysis"]  # Available to all subscriptions
    
    if auth_system.check_subscription_feature(username, "advanced_analytics"):
        available_tabs.append("Gold Social Monitoring")
        available_tabs.append("Premium AI Insights")
    
    if auth_system.check_subscription_feature(username, "real_time_monitoring"):
        available_tabs.append("Gold Advanced Threat Analysis")
    
    # Create the tab navigation
    tabs = st.tabs([f"🔍 {tab}" for tab in available_tabs])
    
    # Display tab content
    for i, tab_name in enumerate(available_tabs):
        with tabs[i]:
            if tab_name == "Premium Search Analysis":
                show_search_analysis()
            elif tab_name == "Gold Social Monitoring":
                show_social_monitoring()
            elif tab_name == "Premium AI Insights":
                show_ai_insights()
            elif tab_name == "Gold Advanced Threat Analysis":
                show_advanced_threat_analysis()
    
    # Subscription upgrade section
    st.markdown("---")
    st.subheader("💳 GOLD SUBSCRIPTION PLANS")
    
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
                st.success("Current Gold Plan")
            else:
                if st.button(f"Upgrade to {plan_info['name']}", key=f"upgrade_{plan}"):
                    st.info(f"Redirecting to gold payment for {plan_info['name']} plan...")
                    # In a real app, this would redirect to a payment processor

# Add new functions for subscription-specific features
def show_social_monitoring():
    """Social monitoring functionality - requires Advanced subscription"""
    st.header("PREMIUM SOCIAL MONITORING")
    
    # Get user's subscription
    username = st.session_state.get('username')
    
    if not auth_system.check_subscription_feature(username, "advanced_analytics"):
        st.warning("⚠️ This feature requires a Gold Advanced or Premium subscription")
        st.info("Upgrade your gold plan to access social media monitoring features.")
        return
    
    brand_name = st.session_state.get('brand_name', 'Your Brand')
    posts = enhanced_monitor.simulate_monitoring_with_api(brand_name, st.session_state.sector)
    
    # Display posts with AI analysis
    for post in posts[:5]:
        threat_class = f"threat-{post['threat_level']}"
        sentiment_color = "#D4AF37" if post['sentiment'] == 'negative' else "#FFD700" if post['sentiment'] == 'positive' else "#FFFFFF"
        
        with st.expander(f"{post['platform']} - {post['content'][:50]}..."):
            st.write(post['content'])
            st.caption(f"Premium Engagement: {post['engagement']}")
            st.markdown(f"""
            <div style="display: flex; gap: 10px; margin-top: 10px;">
                <span class="{threat_class}">Gold Threat: {post['threat_level'].upper()}</span>
                <span style="color: {sentiment_color}; font-weight: 600;">Premium Sentiment: {post['sentiment'].upper()}</span>
            </div>
            """, unsafe_allow_html=True)

def show_ai_insights():
    """AI insights functionality - requires Advanced subscription"""
    st.header("🧠 PREMIUM AI-POWERED INSIGHTS")
    
    # Get user's subscription
    username = st.session_state.get('username')
    
    if not auth_system.check_subscription_feature(username, "advanced_analytics"):
        st.warning("⚠️ This feature requires a Gold Advanced or Premium subscription")
        st.info("Upgrade your gold plan to access AI-powered insights.")
        return
    
    brand_name = st.session_state.get('brand_name', 'Your Brand')
    
    # Generate sample analyses
    analyses = []
    for i in range(10):
        text = f"Gold sample text {i} about {brand_name} with {'high' if i < 3 else 'medium' if i < 6 else 'low'} gold threat level"
        analysis = ai_engine.detect_threats(text, brand_name)
        analyses.append(analysis)
    
    # Generate report
    report = ai_engine.generate_threat_report(analyses)
    
    # Display report
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="ai-visualization">
            <h4>🧠 GOLD THREAT SUMMARY</h4>
            <p>Premium Total Analyses: {}</p>
            <p>Gold High Threats: {}</p>
            <p>Premium Medium Threats: {}</p>
            <p>Standard Low Threats: {}</p>
            <p>Gold Average Sentiment: {:.2f}</p>
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
            <h4>✅ PREMIUM AI RECOMMENDATIONS</h4>
            {}
        </div>
        """.format(
            ''.join([f'<p>• {rec}</p>' for rec in report['recommendations']])
        ), unsafe_allow_html=True)
    
    # Keyword frequency analysis
    st.subheader("🔤 GOLD KEYWORD FREQUENCY ANALYSIS")
    
    texts = [a['text'] for a in analyses]
    keyword_freq = ai_engine.create_keyword_frequency(texts)
    
    # Create bar chart
    fig = viz.create_keyword_bar_chart(keyword_freq, "Gold Top Keywords in Threat Analysis")
    st.plotly_chart(fig, use_container_width=True)
    
    # Threat patterns
    st.subheader("🔍 GOLD THREAT PATTERN ANALYSIS")
    
    patterns = ai_engine.create_threat_patterns(analyses)
    
    # Create heatmap
    fig = viz.create_pattern_heatmap(patterns, "Gold Threat Patterns by Platform and Level")
    st.plotly_chart(fig, use_container_width=True)
    
    # Pattern details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="ai-visualization">
            <h4>🎯 PREMIUM TOP THREAT KEYWORDS</h4>
            {}
        </div>
        """.format(
            ''.join([f'<p>• {word}: {count}</p>' for word, count in list(patterns['high_threat_keywords'].most_common(5))])
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="ai-visualization">
            <h4>📱 GOLD PLATFORM DISTRIBUTION</h4>
            {}
        </div>
        """.format(
            ''.join([f'<p>• {platform}: {count}</p>' for platform, count in patterns['platform_distribution'].most_common()])
        ), unsafe_allow_html=True)

def main():
    # Add gold particles background
    add_gold_particles()
    
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
    
    # Header with shield logo
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <div class="brandguardian-logo">🛡️</div>
        <h1 class="premium-header floating">BrandGuardian AI Pro</h1>
        <div style="text-align: center; margin-top: 15px;" class="accent-text">Premium Business Intelligence & Digital Risk Protection</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with user info and logout button
    with st.sidebar:
        # User info
        subscription_info = auth_system.subscription_plans[st.session_state.user_subscription]
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 25px;">
            <div style="font-size: 3.5rem;">👤</div>
            <h3>{st.session_state.username}</h3>
            <p>{st.session_state.get('user_access_level', 'user').title()} Access</p>
            <p>{auth_system.users[st.session_state.username]['company']}</p>
            <div style="background-color: {subscription_info['color']}20; 
                        border: 1px solid {subscription_info['color']}; 
                        border-radius: 20px; padding: 8px 16px; margin-top: 12px; display: inline-block;">
                <span style="color: {subscription_info['color']}; font-weight: bold;">
                    {subscription_info['name']} Subscription
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.header("Gold Business Configuration")
        brand_name = st.text_input("Gold Brand Name", st.session_state.brand_name)
        st.session_state.brand_name = brand_name
        
        sector = st.selectbox("Gold Business Sector", ["technology", "finance", "retail"])
        st.session_state.sector = sector
        
        st.markdown("---")
        st.subheader("🔐 GOLD ACCESS STATUS")
        if st.session_state.user_subscription == "premium":
            st.success("✅ GOLD PREMIUM ACCESS")
            st.markdown('<span class="premium-badge">GOLD PREMIUM</span>', unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ {subscription_info['name']} ACCESS")
        
        st.markdown("---")
        user_id = st.session_state.get('user_id')
        api_keys = api_manager.load_api_keys(user_id) if user_id else {}
        st.subheader("🔑 GOLD API STATUS")
        st.info(f"{len(api_keys)} gold platform(s) connected")
        
        # User management for admin only
        if st.session_state.get('user_access_level') == 'admin':
            st.markdown("---")
            if st.button("👥 GOLD USER MANAGEMENT", use_container_width=True):
                st.session_state.show_user_management = True
        
        st.markdown("---")
        if st.button("🚪 GOLD LOGOUT", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Show user management if admin clicked the button
    if st.session_state.get('show_user_management', False):
        show_user_management()
        if st.button("Back to Gold Dashboard", use_container_width=True):
            st.session_state.show_user_management = False
            st.rerun()
        return
    
    # Different navigation based on user role
    if st.session_state.get('user_access_level') == 'admin':
        # Admin navigation
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📊 PREMIUM EXECUTIVE DASHBOARD", 
            "🔍 GOLD THREAT ANALYSIS",
            "📱 PREMIUM SOCIAL MONITORING",
            "🥊 GOLD COMPETITIVE INTELLIGENCE",
            "🌟 LUXURY INFLUENCER NETWORK",
            "🛡️ GOLD CRISIS PREDICTION",
            "❤️ PREMIUM BRAND HEALTH",
            "🔑 GOLD API MANAGEMENT"
        ])
        
        with tab1:
            st.header("Gold Executive Dashboard")
            st.write("Gold overview dashboard content...")
        
        with tab2:
            show_advanced_threat_analysis()
        
        with tab3:
            st.header("Gold Social Monitoring")
            posts = enhanced_monitor.simulate_monitoring_with_api(brand_name, st.session_state.sector)
            for post in posts[:5]:
                with st.expander(f"{post['platform']} - {post['content'][:50]}..."):
                    st.write(post['content'])
                    st.caption(f"Premium Engagement: {post['engagement']}")
        
        # Other tabs
        for tab, title in [(tab4, "Gold Competitive Intelligence"), (tab5, "Luxury Influencer Network"), 
                          (tab6, "Gold Crisis Prediction"), (tab7, "Premium Brand Health")]:
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
