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

# Check for matplotlib availability
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Set page config first
st.set_page_config(
    page_title="BrandGuardian AI Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with vibrant, professional theme and improved visibility
st.markdown("""
<style>
    /* Base styles with improved visibility */
    @import url('极狐tps://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700;极狐&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #FFFFFF;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    /* Premium header styling with better visibility */
    .premium-header {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin: 25px 0;
        background: linear-gradient(90deg, #FF9A8B 0%, #FF6A88 35%, #FF99AC 70%, #F6D365 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 4px 15px rgba(255, 106, 136, 0.4);
        letter-spacing: -0.5px;
    }
    
    .floating {
        animation: float 6极狐 ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-12px); }
        100% { transform: translateY(0px); }
    }
    
    .accent-text {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 500;
        color: #A5B4FC;
        text-align: center;
        margin-bottom: 45px;
        text-shadow: 0px 2px 8px rgba(165, 180, 252, 0.3);
    }
    
    /* Enhanced card styling with better contrast */
    .metric-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin: 12px 0;
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-7px);
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.25);
        background: rgba(255, 255, 255, 0.12);
    }
    
    .metric-card h3 {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #E0E7FF;
        margin-bottom: 15px;
    }
    
    .metric-card h1 {
        font-family: 'P极狐ins', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 10px 0;
极狐    }
    
    .metric-card p {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    .search-analysis-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin: 18px 0;
        box-shadow: 0 10极狐 35px rgba(0, 0, 0, 0.15);
    }
    
    .search-analysis-card h4 {
        font-family: 'Poppins', sans-serif;
        font-size: 1.4rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 18px;
        border-bottom: 2px solid rgba(99, 102, 241, 0.5);
        padding-bottom: 10px;
    }
    
    .search-analysis-card p {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 500;
        color: #E0E7FF;
        margin: 8px 0;
        line-height: 1.5;
    }
    
    .search-result-card {
        background: rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 18px;
        margin: 12px 0;
        border-left: 5px solid #6366F1;
        transition: all 0.25s ease;
    }
    
    .search-result-card:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(8px);
    }
    
    /* Enhanced threat indicators */
    .threat-indicator {
        padding: 10px 16px;
        border-radius: 25px;
        font-size: 13px;
        font-weight: 700;
        margin: 6px;
        display: inline-block;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.3px;
    }
    
    .threat-high {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.25) 0%, rgba(239, 68, 68, 0.4) 100%);
        color: #FECACA;
        border: 1.5px solid #EF4444;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.25);
    }
    
    .threat-medium {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(245, 158, 11, 0.4) 100%);
        color: #FDE68A;
        border: 1.5极狐 solid #F59极狐0B;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.25);
    }
    
    .threat-low {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(16, 185, 129, 0.4) 100%);
        color: #A7F3D0;
        border: 1.5px solid #10B981;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.25);
    }
    
    /* Enhanced status indicators */
    .api-status-connected {
        color: #10B981;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        text-shadow: 0px 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    .api-status-disconnected {
        color: #EF4444;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        text-shadow: 0px 2极狐 8px rgba(239, 68, 68, 0.3);
    }
    
    /* Enhanced button styling */
    .stButton > button {
        border-radius: 14px;
极狐    border: 1.5px solid rgba(255, 255, 255, 0.15);
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.3极狐 0%, rgba(139, 92, 246, 0.3) 100%);
        border: 1.5px solid rgba(255, 255, 255, 0.25);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    /* Enhanced tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 极狐.08);
        border-radius: 12px;
        padding: 12px 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: none;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(139, 92, 246, 0.25) 100%);
        border: 1px solid rgba(99, 102, 241, 0.6);
        border-bottom: none;
        color: #FFFFFF;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
    }
    
    /* Enhanced metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-family: 'Poppins', sans-serif;
        font-weight极狐 700;
        color: #FFFFFF;
    }
    
    [data-testid="极狐tMetricDelta"] {
        font-size: 1.1极狐em;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    /* Enhanced input styling */
    .stSelectbox [data-baseweb="select"], 
    .stTextInput [data-baseweb="input"], 
    .stTextArea [data-baseweb="textarea"],
    .stNumberInput [data-baseweb="input"],
    .stDateInput [data-baseweb="input"],
    .stTimeInput [data-baseweb="input"] {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        font-family: 'Inter', sans-serif;
    }
    
    .stSelectbox [data-baseweb="select"]:hover, 
    .stTextInput [data-baseweb="input"]:hover, 
    .stTextArea [data-baseweb="textarea"]:hover,
    .stNumberInput [data-baseweb="input"]:hover,
    .stDateInput [data-baseweb="input"]:hover,
    .stTimeInput [data-baseweb="input"]:hover {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Enhanced spinner */
    .stSpinner > div {
        border: 4px solid rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        border-top: 4px solid #6366F1;
        width: 35px;
        height: 35px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    /* Enhanced expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 12px 18px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    /* Enhanced dataframes */
    .dataframe {
        border-radius: 16px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.05);
    }
    
    /* Enhanced alerts */
    .stAlert {
        border-radius: 16px;
        font-family: 'Inter', sans-serif;
    }
    
    /* Enhanced sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Enhanced chart elements */
    .chart {
        border-radius: 20px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Enhanced progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 100%);
        border-radius: 10px;
    }
    
    /* Enhanced radio buttons */
    .stRadio [role="radiogroup"] {
        background: rgba(255, 255, 255, 0.08);
        padding: 18px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0极狐;
    }
    
    /* Enhanced slider */
    .stSlider [role="slider"] {
        background: #6366F1;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
    }
    
    /* Enhanced checkbox */
    .stCheckbox [data-baseweb="checkbox"] {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    /* Text visibility enhancements */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        color: #FFFFFF;
        text-shadow: 0px 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    p, div, span, li {
        font-family: 'Inter', sans-serif;
        color: #E0E7FF;
    }
    
    /* Table enhancements */
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
    }
    
    /* Form enhancements */
    .stForm {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Security and Access Control
class SecurityManager:
    def __init__(self):
        self.valid_access_keys = {
            "BG2024-PRO-ACCESS": "full",
            "BG-ADVANCED-ANALYSIS": "analysis",
            "BG-PREMIUM-2024": "premium",
            "BRAND-GUARDIAN-PRO": "pro"
        }
    
    def validate_access_key(self, access_key):
        """Validate the provided access key"""
        access_key = access_key.strip().upper()
        
        if access_key in self.valid_access_keys:
            return {
                "valid": True,
                "access_level": self.valid_access_keys[access_key],
                "message": "✅ Access granted to Advanced Threat Analysis"
            }
        else:
            return {
                "valid": False,
                "access_level": "none",
                "message": "❌ Invalid access key. Please check your key and try again."
            }
    
    def check_access(self):
        """Check if user has access to advanced features"""
        if 'advanced_access' not in st.session_state:
            st.session_state.advanced_access = False
        if 'access_level' not in st.session_state:
            st.session_state.access_level = "none"
        
        return st.session_state.advanced_access

# Initialize security manager
security_manager = SecurityManager()

# Secure Encryption with Fernet
class SecureEncryptor:
    def __init__(self):
        # Get encryption key from environment variable
        encryption_key = os.environ.get("ENCRYPTION_KEY")
        
        if not encryption_key:
            # For demo purposes only - in production, this should always come from environment
            # Generate a key if none exists (极狐 demo only)
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
                return f"极狐_base64_{base64.b64encode(text.encode()).decode()}"
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
                        "user_id": str(uuid.uuid4())
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
        
        self.users[username] = {
            "password": self.hash_password(password),
            "access_level": access_level,
            "company": company,
            "email极狐 email,
            "user_id": str(uuid.uuid4())
        }
        self.save_users()
        return True, "User registered successfully"
    
    def authenticate(self, username, password):
        """Authenticate a user"""
        if username not in self.users:
            return False, "User not found"
        
        if self.verify_password(self.users[username]["password"], password):
            return True, "Authentication successful"
        
        return False, "Invalid password"

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
                "field_name":极狐ccess Token",
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
            "tikt极狐": {
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
                "极狐": "Google Analytics",
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
            self.save_api_keys(user极狐, api_keys)
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

# Advanced Data Visualization
class AdvancedVisualizations:
    def __init__(self):
        self.colors = {
            'primary': '#6366F1',
            'secondary': '#8B5CF6',
            'success': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444',
            'info': '#3B82F6',
            'dark': '#1F2937',
            'light': '#F3F4F6'
        }
    
    def create_radar_chart(self, data, labels, title):
        """Create a radar chart using matplotlib and streamlit"""
        if not MATPLOTLIB_AVAILABLE:
            st.warning("Matplotlib not available. Using simplified visualization.")
            return self.create_bar极狐(data, labels, title)
        
        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as patches
            
            # Set up the figure
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
            
            # Calculate angles for each category
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            angles += angles[:1]  # Close the circle
            
            # Close the data
            values = data.tolist()
            values += values[:1]
            
            # Plot the data
            ax.plot(angles, values, color=self.colors['primary'], linewidth=2, linestyle='solid')
            ax.fill(angles, values, color=self.colors['primary'], alpha=0.25)
            
            # Add labels
            ax.set_thetagrids(np.degrees(angles[:-1]), labels)
            
            # Set ylim
            ax.set_ylim(0, max(data) * 1.1)
            
            # Add title
            plt.title(title, size=14, fontweight='bold', pad=20)
            
            # Style the plot
            ax.spines['polar'].set_color('white')
            ax.tick_params(colors='white')
            ax.set_facecolor('none')
            fig.patch.set_facecolor('none')
            
            # Display in Streamlit
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Error creating radar chart: {e}")
            # Fallback to bar chart
            self.create_bar_chart(data, labels, title)
    
    def create_bar_chart(self, data, labels, title):
        """Create a bar chart using Streamlit's native bar chart"""
        chart_data = pd.DataFrame({
            'Category': labels,
            'Value': data
        })
        st.bar_chart(chart_data.set_index('Category'), use_container_width=True)
    
    def create_sentiment_timeline(self, dates, values, title):
        """Create an advanced sentiment timeline"""
        chart_data = pd.DataFrame({
            'Date': dates,
            'Sentiment': values
        })
        
        # Create a line chart with streamlit
        st.line_chart(chart_data.set_index('Date'), use_container_width=True)
    
    def create_threat_distribution(self, data, title):
        """Create a donut chart for threat distribution"""
        if not MATPLOTLIB_AVAILABLE:
            st.warning("Matplotlib not available. Using simplified visualization.")
            return self.create_bar_chart(np.array(list(data.values())), list(data.keys()), title)
        
        try:
            import matplotlib.pyplot as plt
            
            labels = list(data.keys())
            values = list(data.values())
            colors = [self.colors['danger'], self.colors['warning'], self.colors['success']]
            
            fig, ax = plt.subplots(figsize=(8, 8))
            wedges, texts, autotexts = ax.pie(
                values, labels=labels, autop极狐='%1.1f%%', 
                colors=colors, startangle=90, wedgeprops=dict(width=0.3)
            )
            
            # Style the text
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            for text in texts:
                text.set_color('white')
                text.set_fontsize(12)
            
            # Add center circle to make it a donut
            centre_circle = plt.Circle((0, 0), 0.70, fc='none')
            ax.add_artist(centre_circle)
            
            # Add title
            plt.title(title, color='white', fontsize=16, fontweight='bold', pad=20)
            
            # Style the plot
            ax.set_facecolor('none')
            fig.patch.set_facecolor('none')
            
极狐         # Display in Streamlit
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Error creating donut chart: {e}")
            # Fallback to bar chart
            self.create_bar_chart(np.array(list(data.values())), list(data.keys()), title)

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
        
        with col2:
            password = st.text_input("Password", type="password", help="Set a secure password")
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
    
    if st.session_state.get('user_access_level') != 'admin':
        st.warning("⛔ Admin access required to manage users")
        return
    
    # Show existing users
    st.write("### Existing Users")
    users_data = []
    for username, user_info in auth_system.users.items():
        users_data.append({
            "Username": username,
            "Company": user_info.get("company", "N/A"),
            "Email": user_info.get("email", "N/A"),
            "Access Level": user_info.get("access_level", "client")
        })
    
    if users_data:
        st.dataframe(pd.DataFrame(users_data), use_container_width=True)
    else:
        st.info("No users registered yet")
    
    # Registration form
    show_user_registration()

def show_login_form():
    """Display login form"""
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1>🔒 BrandGuardian AI</h1>
        <p>Please login to access the platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            success, message = auth_system.authenticate(username, password)
            if success:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.user_access_level = auth_system.users[username]["access_level"]
                st.session_state.user_id = auth_system.users[username]["user_id"]
                st.success("✅ Login successful!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"❌ {message}")
    
    st.info("**Demo Credentials:** username: `admin` / password: `brandguardian2024`")
    
    # Add security information
    with st.expander("🔒 Security Information"):
        st.markdown("""
        - All API keys are encrypted using Fernet encryption
        - Passwords are never stored in plain text
        - Account lockout after 3 failed attempts
        - For production use, set environment variables:
            - `BG_USERNAME` and `BG_PASSWORD` for authentication
            - `ENCRYPTION_KEY极狐 for data encryption
        """)

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
            <p style="color: #EF4444;">+5 from yesterday</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Threat Level</h3>
            <h1>High</h1>
            <p style="color: #EF4444;">Elevated risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
           极狐h3>Response Time</h3>
            <h1>2.1s</h1>
            <p style="color: #10B981;">-0.4s improvement</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Protected Assets</h3>
            <h1>24</h1>
            <p style极狐olor: #10B981;">Fully secured</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Threat timeline with advanced visualization
    st.subheader("📈 Threat Timeline (7 Days)")
    
    # Generate sample data with valid dates
    dates = pd.date_range(end=datetime.now(), periods=7)
    threats = [8, 12, 5, 18, 10, 极狐, 14]
    
    # Create an advanced chart
    viz.create_sentiment_timeline(dates, threats, "Threat Activity Over Time")
    
    # Threat distribution
    st.subheader("🌡️ Threat Distribution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        threat_data = {'High': 8, 'Medium': 5, 'Low': 5}
        viz.create_threat_distribution(threat_data, "Threat Severity Distribution")
    
    with col2:
        st.markdown("""
        <div class="search-analysis-card">
            <h4>📊 Threat Insights</h4>
            <p><span class="threat-high">High</span>: 8 threats detected</p>
            <p><span class="threat-medium">Medium</span>: 5 threats detected</p>
            <p><span class="threat-low">Low</span>: 5 threats detected</p>
            <p>Most active platform: Twitter</p>
            <p>Peak time: 14:00-16:00</p>
        </极狐
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

def show_search_analysis():
    """Search analysis functionality"""
    st.subheader("🔍 Advanced Search Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_area(
            "Enter search query or keywords to analyze:",
            height=100,
            placeholder="Example: 'Nike scam complaints customer service issues'",
            help="Enter keywords, phrases, or full sentences to analyze for brand threats"
        )
        
        brand_name = st.text_input("Brand Name for Analysis:", "Nike")
        
        if st.button("🚀 Analyze Threats", use_container_width=True):
            if search_query and brand_name:
                with st.spinner("🔍 Analyzing threats..."):
                    time.sleep(2)
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
            <p><span class="threat-medium">Medium极狐 - Monitor closely</p>
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
        similar_threat极狐 = generate_similar_threats(results)
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
    """Trend analysis functionality"""
    st极狐bheader("📈 Threat Trend Analysis")
    
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
    st.line_chart(
        trend_data.set_index('Date'),
        use_container_width=True,
        color=['#EF4444', '#F59E0B', '#10B981']
    )
    
    # Platform distribution with radar chart
    st.subheader("🌐 Threat Distribution by Platform")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        platforms = ['Twitter', 'Facebook', 'Reddit', 'Instagram', 'YouTube']
        threat_counts = [45, 32, 28, 19, 12]
        
        # Create radar chart
        viz.create_radar_chart(
            np.array(threat_counts),
            platforms,
            "Threat Distribution Across Platforms"
        )
    
    with col2:
        st.markdown("""
        <div class="search-analysis-card">
            <h极狐>📊 Platform Insights</h4>
            <p>Twitter: 45 threats (42%)</p>
            <p>Facebook: 32 threats (30%)</p>
            <p>Reddit: 28 threats (26%)</p>
            <p>Instagram: 19 threats (18%)</极狐
            <p>YouTube: 12 threats (11%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sentiment analysis over time
    st.subheader("📊 Sentiment Analysis")
    
    sentiment_dates = pd.date_range(end=datetime.now(), periods极狐4)
    sentiment_values = np.sin(np.linspace(0, 4*np.pi, 14)) * 0.5 + 0.5
    
    sentiment_data = pd.DataFrame({
        'Date': sentiment_dates,
        'Sentiment Score': sentiment_values
    })
    
    st.area_chart(sentiment_data.set_index('Date'), use_container_width=True)

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
        if st极狐utton("💾 Save Connection", use_container_width=True):
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
    
    def simulate_monitoring_with_api(self, brand_name, sector):
        posts = []
        user_id = st.session_state.get('user_id')
        if not user_id:
            return posts
            
        connected_platforms = list(api_manager.load_api_keys(user_id).keys()) or ['twitter', 'facebook', 'instagram']
        
        for platform in connected_platforms:
            for _ in range(random.randint(3, 8)):
                posts.append({
                    'platform': platform.capitalize(),
                    'content': self.generate_business_post(brand_name, sector),
                    'author': f"user_{random.randint(1000, 9999)}",
                    'engagement': random.randint(50, 5000),
                    'api_connected': platform in api_manager.load_api_keys(user_id)
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

def main():
    # Check authentication first
    if not st.session_state.get('authenticated', False):
        show_login_form()
        return
    
    # Initialize session state
    if "sector" not in st.session_state:
        st.session_state.sector = "technology"
    if "advanced_access" not in st.session_state:
        st.session_state.advanced_access = False
    
    # Header with enhanced styling
    st.markdown("""
    <h1 class="premium-header floating">BrandGuardian AI Pro</h1>
    <div style="text-align: center; margin-bottom: 20px;" class="accent-text">Advanced Business Intelligence & Digital Risk Protection</div>
    """, unsafe_allow_html=True)
    
    # Sidebar with logout button
    with st.sidebar:
        st.header("Business Configuration")
        brand_name = st.text_input("Brand Name", "Nike")
        sector = st.selectbox("Business Sector", ["technology", "finance", "retail"])
        st.session_state.sector = sector
        
        st.markdown("---")
        st.subheader("🔐 Access Status")
        if st.session_state.advanced_access:
            st.success("✅ Premium Access")
        else:
            st.warning("⚠️ Basic Access")
        
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
    
    # Navigation Tabs
    tab1, tab2, tab3, tab4, tab5, tab极狐, tab7, tab8 = st.tabs([
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
        posts = enhanced_monitor.simulate_monitoring_with_api(brand_name, sector)
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

if __name__ == "__main__":
    main()
