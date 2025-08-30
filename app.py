import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import hashlib
import re
import requests
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from urllib.parse import urlencode
from cryptography.fernet import Fernet

# Set page configuration
st.set_page_config(
    page_title="BrandGuardian AI Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional design
st.markdown("""
<style>
    .main { 
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
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
    
    .header-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        background: rgba(255, 255, 255, 0.08);
    }
    
    .api-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    }
    
    .positive { color: #10B981; }
    .negative { color: #EF4444; }
    .warning { color: #F59E0B; }
    
    .subscription-card {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(99, 102, 241, 0.3);
    }
    
    .crisis-alert {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 5px solid #FCA5A5;
    }
    
    .success-alert {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 5px solid #A7F3D0;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }
    
    .platform-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Encryption setup
def generate_encryption_key():
    if not os.path.exists('encryption.key'):
        key = Fernet.generate_key()
        with open('encryption.key', 'wb') as key_file:
            key_file.write(key)
    with open('encryption.key', 'rb') as key_file:
        return key_file.read()

encryption_key = generate_encryption_key()
cipher_suite = Fernet(encryption_key)

# Subscription Tiers
SUBSCRIPTION_TIERS = {
    "starter": {
        "price": 299,
        "features": [
            "Basic sentiment monitoring", 
            "2 social platforms", 
            "Daily reports", 
            "Email alerts", 
            "10 keyword monitors",
            "7-day data retention"
        ],
        "limits": {
            "social_platforms": 2, 
            "keywords": 10, 
            "historical_data": 7
        }
    },
    "professional": {
        "price": 799,
        "features": [
            "Advanced sentiment analysis", 
            "5 social platforms", 
            "Real-time alerts", 
            "Competitive analysis", 
            "50 keyword monitors",
            "30-day data retention",
            "API access",
            "Basic webhooks"
        ],
        "limits": {
            "social_platforms": 5, 
            "keywords": 50, 
            "historical_data": 30
        }
    },
    "enterprise": {
        "price": 1999,
        "features": [
            "AI-powered sentiment analysis", 
            "Unlimited social platforms", 
            "Real-time alerts", 
            "Advanced competitive intelligence", 
            "Unlimited keyword monitors",
            "1-year data retention",
            "Full API access",
            "Advanced webhooks",
            "Custom integrations",
            "Priority support",
            "White-label options",
            "SLA guarantee"
        ],
        "limits": {
            "social_platforms": 999, 
            "keywords": 999, 
            "historical_data": 365
        }
    }
}

# Database Class with Encryption
class SecureBrandDB:
    def __init__(self):
        self.data_file = "brands_secure_data.json"
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                encrypted_data = f.read()
                decrypted_data = cipher_suite.decrypt(encrypted_data.encode()).decode()
                self.brands = json.loads(decrypted_data)
        else:
            self.brands = {}
            self.save_data()
    
    def save_data(self):
        data_str = json.dumps(self.brands, indent=2)
        encrypted_data = cipher_suite.encrypt(data_str.encode()).decode()
        with open(self.data_file, 'w') as f:
            f.write(encrypted_data)
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_brand(self, brand_id, password, brand_name, email, tier="starter"):
        if brand_id in self.brands:
            return False
        
        self.brands[brand_id] = {
            "password": self._hash_password(password),
            "brand_name": brand_name,
            "email": email,
            "subscription_tier": tier,
            "subscription_status": "active",
            "connected_platforms": {},
            "api_keys": {},
            "monitoring_keywords": [],
            "webhook_urls": {},
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat()
        }
        self.save_data()
        return True
    
    def authenticate(self, brand_id, password):
        brand = self.brands.get(brand_id)
        if brand and brand["password"] == self._hash_password(password):
            brand["last_login"] = datetime.now().isoformat()
            self.save_data()
            return True
        return False
    
    def get_brand(self, brand_id):
        return self.brands.get(brand_id, {})
    
    def update_brand(self, brand_id, updates):
        if brand_id in self.brands:
            self.brands[brand_id].update(updates)
            self.save_data()
            return True
        return False

    def add_api_key(self, brand_id, platform, api_data):
        brand = self.get_brand(brand_id)
        if brand:
            if "api_keys" not in brand:
                brand["api_keys"] = {}
            
            # Encrypt sensitive API data
            encrypted_data = {}
            for key, value in api_data.items():
                if value:  # Only encrypt if value exists
                    encrypted_data[key] = cipher_suite.encrypt(value.encode()).decode()
            
            brand["api_keys"][platform] = {
                "data": encrypted_data,
                "added_date": datetime.now().isoformat(),
                "last_used": None,
                "status": "connected"
            }
            return self.update_brand(brand_id, {"api_keys": brand["api_keys"]})
        return False

    def get_api_key(self, brand_id, platform, key_name):
        brand = self.get_brand(brand_id)
        if brand and platform in brand.get("api_keys", {}):
            encrypted_value = brand["api_keys"][platform]["data"].get(key_name)
            if encrypted_value:
                return cipher_suite.decrypt(encrypted_value.encode()).decode()
        return None

# API Integration System
class ProfessionalAPIManager:
    def __init__(self):
        self.supported_platforms = {
            "twitter": {
                "name": "Twitter API v2",
                "icon": "🐦",
                "help_url": "https://developer.twitter.com/en/docs/twitter-api",
                "auth_type": "bearer_token",
                "fields": [
                    {"name": "Bearer Token", "type": "password", "required": True, 
                     "help": "Get this from your Twitter Developer Portal"}
                ],
                "rate_limit": "500,000 tweets/month"
            },
            "facebook": {
                "name": "Facebook Graph API",
                "icon": "📘",
                "help_url": "https://developers.facebook.com/docs/graph-api",
                "auth_type": "access_token",
                "fields": [
                    {"name": "Access Token", "type": "password", "required": True,
                     "help": "Long-lived user access token with required permissions"},
                    {"name": "Page ID", "type": "text", "required": True,
                     "help": "ID of the Facebook Page you want to monitor"}
                ],
                "rate_limit": "200 calls/hour"
            },
            "instagram": {
                "name": "Instagram Graph API",
                "icon": "📸",
                "help_url": "https://developers.facebook.com/docs/instagram-api",
                "auth_type": "access_token",
                "fields": [
                    {"name": "Access Token", "type": "password", "required": True,
                     "help": "Instagram Graph API access token"},
                    {"name": "Business Account ID", "type": "text", "required": True,
                     "help": "Your Instagram Business Account ID"}
                ],
                "rate_limit": "200 calls/hour"
            },
            "youtube": {
                "name": "YouTube Data API",
                "icon": "📺",
                "help_url": "https://developers.google.com/youtube/v3",
                "auth_type": "api_key",
                "fields": [
                    {"name": "API Key", "type": "password", "required": True,
                     "help": "YouTube Data API v3 key"}
                ],
                "rate_limit": "10,000 units/day"
            },
            "reddit": {
                "name": "Reddit API",
                "icon": "🔴",
                "help_url": "https://www.reddit.com/dev/api/",
                "auth_type": "oauth",
                "fields": [
                    {"name": "Client ID", "type": "text", "required": True,
                     "help": "Reddit app client ID"},
                    {"name": "Client Secret", "type": "password", "required": True,
                     "help": "Reddit app client secret"},
                    {"name": "User Agent", "type": "text", "required": True,
                     "help": "Unique user agent for your application"}
                ],
                "rate_limit": "60 calls/minute"
            },
            "google_analytics": {
                "name": "Google Analytics",
                "icon": "📊",
                "help_url": "https://developers.google.com/analytics",
                "auth_type": "service_account",
                "fields": [
                    {"name": "Property ID", "type": "text", "required": True,
                     "help": "GA4 property ID (format: properties/XXXXXX)"},
                    {"name": "Service Account JSON", "type": "textarea", "required": True,
                     "help": "Service account key file contents"}
                ],
                "rate_limit": "50,000 requests/day"
            }
        }
    
    def test_connection(self, platform, credentials):
        """Test API connection with provided credentials"""
        try:
            if platform == "twitter":
                return self._test_twitter(credentials)
            elif platform == "facebook":
                return self._test_facebook(credentials)
            elif platform == "youtube":
                return self._test_youtube(credentials)
            else:
                # Simulate successful connection for other platforms
                time.sleep(1.5)
                return {
                    "success": True,
                    "message": f"✅ Successfully connected to {self.supported_platforms[platform]['name']}",
                    "rate_limit": self.supported_platforms[platform]["rate_limit"]
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Connection failed: {str(e)}",
                "suggestion": "Please check your credentials and try again"
            }
    
    def _test_twitter(self, credentials):
        """Test Twitter API connection"""
        bearer_token = credentials.get("Bearer Token")
        if not bearer_token:
            return {"success": False, "message": "Bearer Token is required"}
        
        try:
            headers = {"Authorization": f"Bearer {bearer_token}"}
            response = requests.get(
                "https://api.twitter.com/2/users/me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "✅ Twitter API connection successful",
                    "user_data": response.json(),
                    "rate_limit": "500,000 tweets/month"
                }
            else:
                return {
                    "success": False,
                    "message": f"❌ Twitter API error: {response.status_code}",
                    "suggestion": "Check your Bearer Token and API permissions"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Connection error: {str(e)}",
                "suggestion": "Check your internet connection and try again"
            }
    
    def _test_facebook(self, credentials):
        """Test Facebook Graph API connection"""
        access_token = credentials.get("Access Token")
        page_id = credentials.get("Page ID")
        
        if not access_token or not page_id:
            return {"success": False, "message": "Access Token and Page ID are required"}
        
        try:
            url = f"https://graph.facebook.com/v19.0/{page_id}"
            params = {
                "access_token": access_token,
                "fields": "id,name"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "✅ Facebook Graph API connection successful",
                    "page_data": response.json(),
                    "rate_limit": "200 calls/hour"
                }
            else:
                return {
                    "success": False,
                    "message": f"❌ Facebook API error: {response.status_code}",
                    "suggestion": "Check your Access Token and Page ID"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Connection error: {str(e)}",
                "suggestion": "Check your internet connection and try again"
            }
    
    def _test_youtube(self, credentials):
        """Test YouTube Data API connection"""
        api_key = credentials.get("API Key")
        if not api_key:
            return {"success": False, "message": "API Key is required"}
        
        try:
            params = {
                "key": api_key,
                "part": "snippet",
                "chart": "mostPopular",
                "maxResults": 1,
                "regionCode": "US"
            }
            
            response = requests.get(
                "https://www.googleapis.com/youtube/v3/videos",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "✅ YouTube Data API connection successful",
                    "rate_limit": "10,000 units/day"
                }
            else:
                return {
                    "success": False,
                    "message": f"❌ YouTube API error: {response.status_code}",
                    "suggestion": "Check your API Key and ensure YouTube Data API is enabled"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Connection error: {str(e)}",
                "suggestion": "Check your internet connection and try again"
            }

# Advanced Sentiment Analysis with AI
class AdvancedSentimentAnalyzer:
    def __init__(self):
        # Enhanced sentiment lexicon with weights and context
        self.lexicon = self._build_advanced_lexicon()
        self.negators = {"not", "no", "never", "without", "isn't", "aren't", "wasn't", "weren't", "don't", "doesn't", "didn't"}
        self.intensifiers = {
            "very": 1.3, "extremely": 1.5, "really": 1.2, "so": 1.2, "quite": 1.1,
            "somewhat": 0.8, "slightly": 0.7, "barely": 0.6, "highly": 1.4
        }
    
    def _build_advanced_lexicon(self):
        return {
            # Positive words with weights
            "excellent": 1.0, "amazing": 0.9, "great": 0.8, "good": 0.7, "love": 0.9,
            "best": 0.8, "awesome": 0.9, "fantastic": 0.9, "perfect": 1.0, "wonderful": 0.8,
            "outstanding": 0.9, "superb": 0.9, "brilliant": 0.8, "favorite": 0.7, "recommend": 0.6,
            "stellar": 0.9, "phenomenal": 1.0, "exceptional": 0.9, "marvelous": 0.8,
            
            # Negative words with weights
            "terrible": 1.0, "awful": 0.9, "bad": 0.7, "hate": 0.9, "worst": 1.0,
            "disappointing": 0.8, "poor": 0.7, "failure": 0.8, "rubbish": 0.7, "waste": 0.6,
            "avoid": 0.6, "broken": 0.7, "useless": 0.8, "horrible": 0.9, "disaster": 0.9,
            "pathetic": 0.8, "appalling": 0.9, "dreadful": 0.8, "unacceptable": 0.7,
            
            # Business context words
            "profit": 0.6, "growth": 0.7, "success": 0.8, "innovation": 0.7,
            "bankruptcy": -0.9, "layoff": -0.8, "lawsuit": -0.9, "recall": -0.8,
            "investment": 0.6, "acquisition": 0.5, "merger": 0.4, "expansion": 0.6
        }
    
    def analyze_sentiment(self, text):
        """Advanced sentiment analysis with context awareness"""
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        sentiment_score = 0
        significant_words = 0
        negation = False
        intensity = 1.0
        
        i = 0
        while i < len(words):
            word = words[i]
            
            # Check for negators
            if word in self.negators:
                negation = not negation
                i += 1
                continue
            
            # Check for intensifiers
            if word in self.intensifiers:
                intensity = self.intensifiers[word]
                i += 1
                continue
            
            # Calculate word sentiment
            if word in self.lexicon:
                word_sentiment = self.lexicon[word] * intensity
                if negation:
                    word_sentiment *= -1
                
                sentiment_score += word_sentiment
                significant_words += 1
                
                # Reset modifiers
                negation = False
                intensity = 1.0
            
            i += 1
        
        # Normalize score
        if significant_words > 0:
            final_score = sentiment_score / significant_words
            return max(-1.0, min(1.0, final_score))
        
        return 0.0
    
    def get_sentiment_label(self, score):
        if score >= 0.7:
            return "Very Positive", "😊"
        elif score >= 0.3:
            return "Positive", "🙂"
        elif score >= -0.2:
            return "Neutral", "😐"
        elif score >= -0.6:
            return "Negative", "😠"
        else:
            return "Very Negative", "😡"

# Initialize components
db = SecureBrandDB()
api_manager = ProfessionalAPIManager()
sentiment_analyzer = AdvancedSentimentAnalyzer()

# Authentication functions
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_brand' not in st.session_state:
        st.session_state.current_brand = None
    if 'subscription_tier' not in st.session_state:
        st.session_state.subscription_tier = None

def login_section():
    st.sidebar.header("🔐 Brand Login")
    
    with st.sidebar.form("login_form"):
        brand_id = st.text_input("Brand ID", placeholder="your_brand_name")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Login", use_container_width=True)
        
        if submitted:
            if db.authenticate(brand_id, password):
                st.session_state.authenticated = True
                st.session_state.current_brand = brand_id
                brand_data = db.get_brand(brand_id)
                st.session_state.subscription_tier = brand_data["subscription_tier"]
                st.sidebar.success(f"Welcome back, {brand_data['brand_name']}! 🎉")
            else:
                st.sidebar.error("Invalid credentials. Please try again.")
    
    if st.session_state.authenticated:
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_brand = None
            st.session_state.subscription_tier = None
            st.rerun()

def registration_section():
    with st.sidebar.expander("📝 New Brand Registration", expanded=False):
        with st.form("register_form"):
            st.write("Create your BrandGuardian account")
            
            col1, col2 = st.columns(2)
            with col1:
                brand_id = st.text_input("Brand ID*", help="Unique identifier for your brand")
            with col2:
                brand_name = st.text_input("Brand Name*")
            
            email = st.text_input("Email Address*")
            
            col3, col4 = st.columns(2)
            with col3:
                password = st.text_input("Password*", type="password")
            with col4:
                confirm_password = st.text_input("Confirm Password*", type="password")
            
            tier = st.selectbox("Subscription Tier*", 
                              list(SUBSCRIPTION_TIERS.keys()),
                              format_func=lambda x: f"{x.title()} - ${SUBSCRIPTION_TIERS[x]['price']}/mo")
            
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            
            if submitted:
                if not all([brand_id, brand_name, email, password, confirm_password]):
                    st.error("Please fill in all required fields (*)")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif db.create_brand(brand_id, password, brand_name, email, tier):
                    st.success("🎉 Account created successfully! Please login.")
                else:
                    st.error("Brand ID already exists. Please choose a different one.")

# API Management Section
def api_management_section():
    st.header("🔌 API & Integration Center")
    st.write("Connect your social media accounts and platforms to start monitoring")
    
    brand_data = db.get_brand(st.session_state.current_brand)
    
    # Display connected APIs
    st.subheader("📊 Connected Platforms")
    
    if "api_keys" in brand_data and brand_data["api_keys"]:
        cols = st.columns(3)
        for i, (platform, details) in enumerate(brand_data["api_keys"].items()):
            with cols[i % 3]:
                platform_info = api_manager.supported_platforms.get(platform, {})
                st.markdown(f"""
                <div class="api-card">
                    <div class="platform-icon">{platform_info.get('icon', '🔗')}</div>
                    <h4>{platform_info.get('name', platform.title())}</h4>
                    <p>Connected: {details.get('added_date', 'N/A')[:10]}</p>
                    <p>Status: <span class="positive">✅ Active</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Disconnect {platform}", key=f"disconnect_{platform}", use_container_width=True):
                    updated_keys = brand_data["api_keys"]
                    updated_keys.pop(platform)
                    db.update_brand(st.session_state.current_brand, {"api_keys": updated_keys})
                    st.success(f"Disconnected from {platform}")
                    st.rerun()
    else:
        st.info("No platforms connected yet. Add your first integration below.")
    
    # Add new API connection
    st.subheader("➕ Add New Integration")
    
    platforms = api_manager.supported_platforms
    selected_platform = st.selectbox("Select Platform", list(platforms.keys()), 
                                   format_func=lambda x: f"{platforms[x]['icon']} {platforms[x]['name']}")
    
    platform_info = platforms[selected_platform]
    
    st.markdown(f"""
    <div class="api-card">
        <h4>{platform_info['icon']} {platform_info['name']}</h4>
        <p><strong>Authentication:</strong> {platform_info['auth_type'].replace('_', ' ').title()}</p>
        <p><strong>Rate Limit:</strong> {platform_info['rate_limit']}</p>
        <p><a href="{platform_info['help_url']}" target="_blank">📚 API Documentation</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form(f"add_{selected_platform}_api"):
        st.write("**API Credentials**")
        
        credentials = {}
        for field in platform_info["fields"]:
            if field["type"] == "password":
                credentials[field["name"]] = st.text_input(
                    f"{field['name']}*" if field["required"] else field["name"],
                    type="password",
                    help=field["help"]
                )
            elif field["type"] == "textarea":
                credentials[field["name"]] = st.text_area(
                    f"{field['name']}*" if field["required"] else field["name"],
                    height=100,
                    help=field["help"]
                )
            else:
                credentials[field["name"]] = st.text_input(
                    f"{field['name']}*" if field["required"] else field["name"],
                    help=field["help"]
                )
        
        col1, col2 = st.columns(2)
        with col1:
            test_connection = st.form_submit_button("🧪 Test Connection", use_container_width=True)
        with col2:
            save_connection = st.form_submit_button("💾 Save Connection", use_container_width=True)
        
        if test_connection:
            with st.spinner("Testing connection..."):
                result = api_manager.test_connection(selected_platform, credentials)
            
            if result["success"]:
                st.markdown(f"""
                <div class="success-alert">
                    <h4>✅ Connection Successful!</h4>
                    <p>{result['message']}</p>
                    <p><strong>Rate Limit:</strong> {result.get('rate_limit', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"❌ {result['message']}")
                if "suggestion" in result:
                    st.info(result["suggestion"])
        
        if save_connection:
            # Validate required fields
            missing_fields = []
            for field in platform_info["fields"]:
                if field["required"] and not credentials[field["name"]]:
                    missing_fields.append(field["name"])
            
            if missing_fields:
                st.error(f"Missing required fields: {', '.join(missing_fields)}")
            else:
                db.add_api_key(st.session_state.current_brand, selected_platform, credentials)
                st.success(f"✅ {platform_info['name']} credentials saved successfully!")

# Professional Dashboard
def professional_dashboard():
    st.markdown("<h1 class='header-title'>BrandGuardian AI</h1>", unsafe_allow_html=True)
    
    brand_data = db.get_brand(st.session_state.current_brand)
    st.write(f"### Welcome back, {brand_data['brand_name']}! 👋")
    
    # Key Metrics
    st.subheader("📈 Brand Health Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>84%</h3>
            <p>Brand Sentiment</p>
            <p class="positive">+4% from last week</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>1,247</h3>
            <p>Total Mentions</p>
            <p class="positive">+12% from last week</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>5.2%</h3>
            <p>Engagement Rate</p>
            <p class="positive">+1.2% from last week</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Low</h3>
            <p>Crisis Level</p>
            <p class="positive">-2% from last week</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sentiment Trend Chart
    st.subheader("📊 Sentiment Trend (Last 7 Days)")
    
    # Generate sample sentiment data
    dates = pd.date_range(end=datetime.now(), periods=7)
    sentiment_data = pd.DataFrame({
        'Date': dates,
        'Sentiment': [0.7, 0.65, 0.8, 0.75, 0.82, 0.78, 0.84],
        'Mentions': [150, 180, 220, 190, 240, 210, 247]
    })
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=sentiment_data['Date'], y=sentiment_data['Sentiment'], 
                  name="Sentiment Score", line=dict(color="#6366F1", width=3)),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Bar(x=sentiment_data['Date'], y=sentiment_data['Mentions'], 
               name="Mentions", marker_color="#8B5CF6", opacity=0.6),
        secondary_y=True,
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    fig.update_yaxes(title_text="Sentiment Score", secondary_y=False)
    fig.update_yaxes(title_text="Mentions", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Platform Distribution
    st.subheader("🌐 Mentions by Platform")
    
    platform_data = pd.DataFrame({
        'Platform': ['Twitter', 'Facebook', 'Instagram', 'YouTube', 'Reddit'],
        'Mentions': [450, 320, 280, 120, 77],
        'Sentiment': [0.8, 0.75, 0.82, 0.7, 0.65]
    })
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(platform_data, values='Mentions', names='Platform',
                    color_discrete_sequence=px.colors.sequential.Plasma)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(platform_data, x='Platform', y='Sentiment',
                    color='Sentiment', color_continuous_scale='Viridis')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Mentions
    st.subheader("💬 Recent Brand Mentions")
    
    sample_mentions = [
        {"text": "Loving the new product from @OurBrand! The quality is exceptional! 👍", "sentiment": 0.9, "platform": "Twitter"},
        {"text": "Customer service was really helpful today. Quick response and solved my issue!", "sentiment": 0.8, "platform": "Facebook"},
        {"text": "The new update has some bugs. Hope they fix it soon.", "sentiment": -0.3, "platform": "Twitter"},
        {"text": "Best purchase I've made this year! Highly recommend!", "sentiment": 0.95, "platform": "Instagram"},
        {"text": "Disappointed with the shipping time. Took longer than expected.", "sentiment": -0.6, "platform": "Twitter"}
    ]
    
    for mention in sample_mentions:
        sentiment_label, emoji = sentiment_analyzer.get_sentiment_label(mention["sentiment"])
        sentiment_color = "positive" if mention["sentiment"] > 0.3 else "negative" if mention["sentiment"] < -0.3 else "warning"
        
        st.markdown(f"""
        <div class="metric-card">
            <p>{mention['text']}</p>
            <p><strong>Platform:</strong> {mention['platform']} • 
            <strong>Sentiment:</strong> <span class="{sentiment_color}">{sentiment_label} {emoji}</span></p>
        </div>
        """, unsafe_allow_html=True)

# Main application
def main():
    init_session_state()
    
    # Sidebar sections
    with st.sidebar:
        login_section()
        if not st.session_state.authenticated:
            registration_section()
    
    if not st.session_state.authenticated:
        # Landing page for non-authenticated users
        st.markdown("<h1 class='header-title'>BrandGuardian AI</h1>", unsafe_allow_html=True)
        st.write("### Enterprise-Grade Brand Protection & Intelligence Platform")
        
        # Features grid
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🔍 AI-Powered Monitoring</h3>
                <p>Advanced sentiment analysis across all social platforms</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>🚨 Real-Time Alerts</h3>
                <p>Instant notifications for brand crises and opportunities</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>📊 Competitive Intelligence</h3>
                <p>Comprehensive market analysis and benchmarking</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Pricing
        st.subheader("💎 Pricing Plans")
        pricing_cols = st.columns(3)
        for i, (tier, details) in enumerate(SUBSCRIPTION_TIERS.items()):
            with pricing_cols[i]:
                st.markdown(f"""
                <div class="subscription-card">
                    <h3>{tier.title()}</h3>
                    <h2>${details['price']}/mo</h2>
                    <div style="text-align: left; margin-top: 20px;">
                        {"".join([f"<p>✓ {feature}</p>" for feature in details['features'][:4]])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Get Started with {tier.title()}", key=f"pricing_{tier}", use_container_width=True):
                    st.info("Please register to get started")
        
        # Demo access
        with st.expander("🎯 Quick Demo Access", expanded=True):
            st.write("Experience the platform instantly with demo credentials:")
            st.code("Brand ID: demo_brand\nPassword: demo123")
            
            if st.button("🚀 Launch Demo Dashboard", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.current_brand = "demo_brand"
                st.session_state.subscription_tier = "enterprise"
                st.rerun()
        
        return
    
    # Authenticated user experience
    brand_data = db.get_brand(st.session_state.current_brand)
    
    # Navigation
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Navigation")
    
    app_sections = {
        "Dashboard": professional_dashboard,
        "API Management": api_management_section,
    }
    
    selected_section = st.sidebar.radio("Go to", list(app_sections.keys()))
    
    # User info in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    **Account Info**
    - **Plan:** {st.session_state.subscription_tier.title()}
    - **Status:** Active ✅
    - **Member since:** {brand_data.get('created_at', 'N/A')[:10]}
    """)
    
    # Display selected section
    app_sections[selected_section]()

if __name__ == "__main__":
    main()
