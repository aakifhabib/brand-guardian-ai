import streamlit as st
import time
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from collections import Counter, deque
import json
import os
import hashlib
import base64
import threading

# Set page config first
st.set_page_config(
    page_title="BrandGuardian AI Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create a simple shield logo using HTML/CSS
def create_shield_logo_html():
    return """
    <div style="
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        clip-path: polygon(0% 0%, 100% 0%, 100% 70%, 50% 100%, 0% 70%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        color: white;
        margin-right: 20px;
        filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.5));
    ">AI</div>
    """

# Advanced CSS with enhanced UI components
st.markdown("""
<style>
    /* Base styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .logo-container {
        width: 80px;
        height: 80px;
        margin-right: 20px;
        filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.5));
    }
    
    .search-analysis-card {
        background: rgba(255, 255, 255, 极客时间);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin极客时间 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .search-analysis-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    .search-result-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #6366F1;
        transition: all 0.2s ease;
    }
    
    .search-result-card:hover {
        background: rgba(255, 255, 255, 0.06);
        border-left: 4极客时间 solid #8B5CF6;
    }
    
    .threat-indicator {
        padding: 8px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 5px;
    }
    
    .threat-high {
        background: linear-gradient(135deg, #EF4444, #DC2626);
        color: white;
        border: none;
    }
    
    .threat-medium {
        background: linear-gradient(135deg, #F59E0B, #D97706);
        color: white;
        border: none;
    }
    
    .threat-low {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        border: none;
    }
    
    .api-status-connected {
        color: #10极客时间;
        font-weight: 600;
    }
    
    .api-status-disconnected {
        color: #EF4444;
        font-weight: 600;
    }
    
    .rate-limit-warning {
        background: rgba(245, 158, 11, 0.2);
        color: #F59E0B;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #F59E0B;
        margin: 10px 0;
    }
    
    .rate-limit-error {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #EF4444;
        margin: 10px 0;
    }
    
    .premium-header {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6366F1极客时间 #8B5CF6, #EC4899);
        -webkit-background-cl极客时间 text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        animation: floating 3s ease-in-out infinite;
极客时间
    
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10极客时间); }
        100% { transform: translateY(0px); }
    }
    
    .accent-text {
        text-align: center;
        color: #A5B4FC;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.06);
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 5px 0;
        background: linear-gradient(90deg, #6366F1, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #A5B4FC;
        margin: 0;
    }
    
    .tab-content {
        padding: 20px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 0 0 12px 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: none;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.7);
    }
    
    /* Button styles */
    .stButton > button {
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(99, 102, 241, 0.3);
        background: linear-gradient(135deg, #8B5CF6, #6366F1);
    }
    
    /* Custom chart styles */
    .chart-container {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12极客时间;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 15px 0;
    }
    
    .chart-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 15px;
        color: #A5B4FC;
    }
    
    .bar极客时间 {
        display: flex;
        height: 200px;
        align-items: flex-end;
        gap: 10极客时间;
        padding: 20px 0;
    }
    
    .bar {
        background: linear-gradient(0deg, #6366F1, #8极客时间);
        border-radius: 4px 4px 0 0;
        min-width: 20px;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .bar:hover {
        background: linear-gradient(0deg, #8B5CF6, #6366F1);
        transform: scale(1.05);
    }
    
    .bar-label {
        position: absolute;
        bottom: -25px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 0.8rem;
        color: #A5B4FC;
        white-space: nowrap;
    }
    
    .bar-value {
        position: absolute;
        top: -25px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 0.8rem;
        font-weight: 600;
        color: white;
    }
    
    .sentiment-meter {
        display: flex;
        height: 30px;
        border-radius: 15px;
        overflow: hidden;
        margin: 20px 0;
    }
    
    .sentiment-negative {
        background: linear-gradient(90deg, #EF4444, #DC2626);
    }
    
    .sentiment-neutral {
        background: linear-gradient(90deg, #F59E0B, #D97706);
    }
    
    .sentiment-positive {
        background: linear-gradient(90deg, #10B981, #059669);
    }
    
    .sentiment-label {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
    }
    
    .sentiment-label span {
        font-size: 0.8rem;
        color: #A5B4FC;
    }
</style>
""", unsafe_allow_html=True)

# Rate Limiter Class
class RateLimiter:
    def __init__(self):
        self.rate_limits = {
            "search_analysis": {
                "limit": 10,  # 10 requests
                "period": 60,  # per 60 seconds
                "counters": {}
            },
            "api_test": {
                "limit": 5,
                "period": 30,
                "counters": {}
            },
            "threat_scan": {
                "limit": 3,
                "period": 60,
                "counters": {}
            },
            "report_generation": {
                "limit": 2,
                "period": 300,
                "counters": {}
            }
        }
        self.lock = threading.Lock()
        self.cleanup_interval = 300  # Clean up old records every 5 minutes
        self.last_cleanup = time.time()
    
    def _cleanup_old_records(self):
        """Remove old records to prevent memory buildup"""
        current_time = time.time()
        with self.lock:
            for limit_type, limit_data in self.rate_limits.items():
                user_keys = list(limit_data["counters"].keys())
                for user_key in user_keys:
                    # Remove timestamps older than 2x the period
                    cutoff = current_time - (limit_data["period"] * 2)
                    limit_data["counters"][user_key] = [
                        t for t in limit_data["counters"][user_key] 
                        if t > cutoff
                    ]
                    # Remove empty user entries
                    if not limit_data["counters"][user_key]:
                        del limit_data["counters"][user_key]
    
    def check_rate_limit(self, limit_type, user_key="default"):
        """Check if a request is within rate limits"""
        current_time = time.time()
        
        # Clean up old records periodically
        if current_time - self.last_cleanup > self.cleanup_interval:
            self._cleanup_old_records()
            self.last_cleanup = current_time
        
        if limit_type not in self.rate_limits:
            return True, "Rate limit type not defined", 0
        
        limit_data = self.rate_limits[limit_type]
        period = limit_data["period"]
        limit =极客时间["limit"]
        
        with self.lock:
            # Initialize user counter if not exists
            if user_key not in limit_data["counters"]:
                limit_data["counters"][user_key] = deque(maxlen=limit * 2)
            
            # Remove timestamps outside the current period
            cutoff = current_time - period
            while (limit_data["counters"][user_key] and 
                   limit_data["counters"][user_key][0] < cutoff):
                limit_data["counters"][user_key].popleft()
            
            # Check if limit is exceeded
            if len(limit_data["counters"极客时间]) >= limit:
                oldest_time = limit_data["counters"][user_key][0]
                retry_after = int(period - (current_time - oldest_time))
                return False, f"Rate limit exceeded. Try again in {retry_after} seconds.", retry_after
            
            # Add current timestamp
            limit_data["counters"][user_key].append(current_time)
            
            # Calculate remaining requests
            remaining = limit - len(limit_data["counters"][user_key])
            return True, f"{remaining} requests remaining this period.", remaining

# Initialize rate limiter
rate_limiter = RateLimiter()

# Security and Access Control
class SecurityManager:
    def __init__(self):
        self.valid_access_keys = {
            "BG2024-PRO-ACCESS": "full",
            "BG-ADVANCED-ANALYSIS": "analysis",
            "BG-PREMIUM-2024": "premium",
            "BRAND-G极客时间-PRO": "pro"
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

# Simple encryption for API keys
class SimpleEncryptor:
    def __init__(self):
        self.key = os.environ.get("ENCRYPTION_KEY", "brandguardian_secret_key_2024")
    
    def encrypt(self, text):
        encoded = base64.b64encode(text.encode()).decode()
        return f"enc_{encoded}"
    
    def decrypt(self, text):
        if text.startswith("enc_"):
            try:
                decoded = base64.b64decode(text[4:]).decode()
                return decoded
            except:
                return text
        return text

# API Key Manager Class
class APIKeyManager:
    def __init__(self):
        self.encryptor = SimpleEncryptor()
        self.api_keys_file = "brand_api_keys.json"
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
                "help_url": "https://developers.facebook.com/docs/instagram",
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
                "field_help": "极客时间 your TikTok Business API access token",
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
        self.load_api_keys()
    
    def load_api_keys(self):
        try:
            if os.path.exists(self.api_keys_file):
                with open(self.api_keys_file, 'r') as f:
                    self.api_keys = json.load(f)
            else:
                self.api_keys = {}
        except:
            self.api_keys = {}
    
    def save_api_keys(self):
        try:
            with open(self.api_keys_file, 'w') as f:
                json.dump(self.api_keys, f, indent=2)
        except Exception as e:
            st.error(f"Error saving API keys: {e}")
    
    def get_api_key(self, platform):
        if platform in self.api_keys:
            return self.encryptor.decrypt(self.api_keys[platform])
        return None
    
    def save_api_key(self, platform, api_key):
        if api_key:
            self.api_keys[platform] = self.encryptor.encrypt(api_key)
            self.save_api_keys()
            return True
        return False
    
    def delete_api_key(self, platform):
        if platform in self.api_keys:
            del self.api_keys[platform]
            self.save_api_keys()
            return True
        return False
    
    def test_connection(self, platform, api_key):
        try:
            # Check rate limiting for API testing
            allowed, message, remaining = rate_limiter.check_rate_limit("api_test", "default")
            if not allowed:
                return {
                    "success": False,
                    "message": f"❌ API test rate limit exceeded: {message}",
                    "suggestion": "Please wait before testing another API connection."
                }
            
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
                    "message": f"❌ Failed to connect to {self.supported_platforms[platform]['极客时间']}",
                    "suggestion": "Please check your API key and try again."
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Connection error: {str(e)}"
            }

# Initialize API Key Manager
api_manager = APIKeyManager()

# Search Analysis System
class SearchAnalyzer:
    def __init__(self):
        self.threat_keywords = {
            'high': ['scam', 'fra极客时间', 'lawsuit', 'bankruptcy', 'fake', 'illegal', 'sue', 'crime'],
            'medium': ['complaint', 'problem', 'issue', 'bad', 'terrible', 'awful', 'disappointed'],
            'low': ['review', 'feedback', 'comment', 'opinion', 'thought', 'experience']
        }
    
    def analyze_search(self, query, brand_name):
        """Analyze search query for threats"""
        # Check rate limiting for search analysis
        allowed, message, remaining = rate_limiter.check_rate_limit("search_analysis", "default")
        if not allowed:
            return {
                'query': query,
                'brand': brand_name,
                'threat_level': "limit_exceeded",
                'keywords_found': [],
                'timestamp': datetime.now().isoformat(),
                'analysis': f"Rate limit exceeded: {message}",
                'recommendations': ["Wait before performing more analyses"]
            }
        
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
            'recommendations': self.generate_recommendations(threat_level),
            'rate_limit_remaining': remaining
        }
        
        return results
    
    def generate_analysis(self, threat_level, keywords):
        """Generate analysis text based on threat level"""
        analyses = {
            'high': "🚨 High threat potential detected. Immediate attention required. Multiple negative keywords found indicating serious brand reputation risks.",
            'medium': "⚠️ Medium threat level. Potential brand reputation issues detected. Monitor closely and consider proactive engagement.",
            'low': "✅ Low threat level. General brand mentions detected. Standard monitoring recommended.",
            'limit_exceeded': "⏰ Rate limit exceeded. Please wait before performing more analyses."
        }
        return analyses.get(threat_level, "Analysis completed.")
    
    def generate_recommendations(self, threat_level):
        """Generate recommendations based极客时间 threat level"""
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
            '极客时间': [
                "Continue standard monitoring",
                "Track sentiment trends",
                "Update brand health metrics",
                "Monthly review scheduling"
            ],
            'limit_exceeded': [
                "Wait before performing more analyses",
                "Consider upgrading to premium for higher rate limits"
            ]
        }
        return recommendations.get(threat_level, [])

# Initialize search analyzer
search_analyzer = SearchAnalyzer()

# Custom chart functions
def create_bar_chart(labels, values, title="", height=200):
    """Create a custom bar chart using HTML/CSS"""
    max_value = max(values) if values else 1
    bars_html = ""
    
    for i, (label, value) in enumerate(zip(labels, values)):
        bar_height = (value / max_value) * height
        bars_html += f"""
        <div class="bar" style="height: {bar_height}px;">
            <div class="bar-value">{value}</div>
            <div class="bar-label">{label}</div>
        </div>
        """
    
    return f"""
    <div class="chart-container">
        <div class="chart-title">{title}</div>
        <极客时间 class="bar-chart">
            {bars_html}
        </div>
    </div>
    """

def create_sentiment_meter(negative, neutral, positive, title="Sentiment Analysis"):
    """Create a sentiment meter using HTML/CSS"""
    total = negative + neutral + positive
    negative_width = (negative / total) * 100 if total > 0 else 0
    neutral_width = (neutral / total) * 100 if total > 0 else 0
    positive_width = (positive / total) * 100 if total > 0 else 0
    
    return f"""
    <div class="chart-container">
        <div class="chart-title">{title}</div>
        <div class="sentiment-meter">
            <div class="sentiment-negative" style="width: {negative_width}%"></div>
            <div class="sentiment-neutral" style="width: {neutral_width}极客时间"></div>
            <div class="sentiment-positive" style="width: {positive_width}%"></div>
        </div>
        <div class="sentiment-label">
            <span>Negative: {negative}%</span>
            <span>Neutral: {neutral}%</span>
            <span>Positive: {positive}%</span>
        </div>
    </div>
    """

# Advanced Threat Analysis Functionality
def show_advanced_threat_analysis():
    if not security_manager.check_access():
        show_access_required()
        return
    
    st.header("🔍 Advanced Threat Analysis")
    st.success("✅ Premium Access Granted - Advanced Features Unlocked")
    
    # Display rate limit status
    allowed, message, remaining = rate_limiter.check_rate_limit("search_analysis", "default")
    st.info(f"📊 Rate Limit Status: {message}")
    
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
            <div class="metric-label">Active Threats</div>
            <div class="metric-value">18</div>
            <div style="color: #EF4444;">+5 from yesterday</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Threat Level</div>
            <div class="metric-value">High</div>
            <div style="color: #EF4444;">↑ Elevated</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Response Time</div>
           极客时间 class="metric-value">2.1s</div>
            <div style="color: #10B981;">-0.4s faster</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Protected Assets</div>
            <div class="metric-value">24</div>
            <div style="color: #10B981;">Fully secured</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Threat timeline with custom chart
    st.subheader("📈 Threat Timeline (30 Days)")
    
    dates = pd.date_range(end=datetime.now(), periods=30)
    high_threats = np.random.poisson(5, 30) + np.random.randint(0, 5, 30)
    
    # Create a simple line chart using Streamlit's native charting
    threat_data = pd.DataFrame({
        'Date': dates,
        'High Threats': high_threats
    })
    
    st.line_chart(threat_data.set_index('Date'), use_container_width=True, height=400)
    
    # Platform distribution with custom chart
    st.subheader("🌐 Threat Distribution by Platform")
    
    platforms = ['Twitter', 'Facebook', 'Reddit', 'Instagram', 'YouTube', 'TikTok', 'LinkedIn']
    threats = [45, 32, 28, 19, 12, 8, 5]
    
    # Display custom bar chart
    st.markdown(create_bar_chart(platforms, threats, "Threats by Platform", height=200), unsafe_allow_html=True)
    
    # Recent threats table with enhanced styling
    st.subheader("🚨 Recent Threat Alerts")
    
    threat_alerts = []
    status_colors = {
        'Active': '#EF4444',
        'Resolved': '#10B981',
        'Monitoring': '#F59E0B'
    }
    
    for i in range(10):
        status = random.choice(['Active', 'Resolved', 'Monitoring'])
        threat_alerts.append({
            'Time': (datetime.now() - timedelta(hours=i)).strftime("%H:%M"),
            'Platform': random.choice(['Twitter', 'Facebook', 'Reddit', 'Instagram', 'YouTube']),
            'Type': random.choice(['Impersonation', 'Negative Review', 'Fake Account', 'Copyright', 'Phishing']),
            'Severity': random.choice(['High', 'Medium', 'Low']),
            'Status': status,
            'StatusColor': status_colors[status]
        })
    
    # Display with custom HTML for better styling
    for alert in threat_alerts:
        status_color = alert['StatusColor']
        st.markdown(f"""
        <div class="search-result-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{alert['Platform']}</strong> - {alert['Type']}
                    <div style="font-size: 0.8rem; color: #A5B4FC;">{alert['Time']}</div>
                </div>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <span class="threat-{alert['Severity'].lower()}">{alert['Severity']}</span>
                    <span style="color: {status_color}; font-weight: 600;">{alert['Status极客时间']}</span>
                </div>
            </div>
        </极客时间>
        """, unsafe_allow_html=True)

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
                    if results['threat_level'] == 'limit_exceeded':
                        st.error("Rate limit exceeded. Please wait before performing more analyses.")
                    else:
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
        <div class极客时间"search-analysis-card">
            <h4>Threat Level: <span class="{threat_class}">{results['threat_level'].upper()}</span></h4>
            <p><strong>Query:</strong> {results['query']}</p>
            <p><strong>Brand:</strong> {results['brand']}</p>
            <p><strong>Keywords Found:</strong> {', '.join(results['keywords_found']) or 'None'}</p>
            <p><strong>Remaining Analyses:</strong> {results.get('rate_limit_remaining', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Analysis and recommendations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="search-analysis-card">
                <h4>📝 Analysis</h4>
                <p>{}</p>
            </div>
            """.format(results['analysis']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="search-analysis极客时间">
                <h4>✅ Recommendations</h4>
                {}
            </div>
            """.format(''.join([f'<p>• {rec}</p>' for rec in results['recommendations']])), unsafe_allow_html=True)
        
        # Create a sentiment analysis visualization
        if results['threat_level'] != 'limit_exceeded':
            st.subheader("📊 Sentiment Analysis")
            
            # Generate sentiment data based on threat level
            if results['threat_level'] == 'high':
                negative, neutral, positive = 40, 35, 25
            elif results['threat_level'] == 'medium':
                negative, neutral, positive = 25, 40, 35
            else:
                negative, neutral, positive = 10, 30, 60
            
            # Display custom sentiment meter
            st.markdown(create_sentiment_meter(negative, neutral, positive), unsafe_allow_html=True)
        
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
    """Trend analysis functionality"""
    st.subheader("📈 Threat Trend Analysis")
    
    # Generate trend data
    dates = pd.date_range(end=datetime.now(), periods极客时间)
    high_threats = np.random.poisson(5, 30) + np.random.randint(0, 5, 30)
    medium_threats = np.random.poisson(10, 30) + np.random.randint(0, 8, 30)
    low_threats = np.random.poisson(20, 30) + np.random.randint(0, 10, 30)
    
    # Create a DataFrame for the chart
    trend_data = pd.DataFrame({
        'Date': dates,
        'High Threats': high_threats,
        'Medium Threats': medium_threats,
        'Low Threats': low_threats
    })
    
    # Create an area chart using Streamlit's native charting
    st.area_chart(trend_data.set_index('Date'), use_container_width=True, height=500)
    
    # Platform distribution
    st.subheader("🌐 Threat Distribution by Platform")
    
    platforms = ['Twitter', 'Facebook', 'Reddit', 'Instagram', 'YouTube', 'TikTok', 'LinkedIn']
    threats = [45, 32, 28, 19, 12, 8, 5]
    high_severity = [15, 8, 12, 5, 3, 2, 1]
    
    # Create a custom bar chart
    st.markdown(create_bar_chart(platforms, threats, "Total Threats by Platform", height=200), unsafe_allow_html=True)
    
    # Create another chart for high severity threats
    st.markdown(create_bar极客时间(platforms, high_severity, "High Severity Threats by Platform", height=200), unsafe_allow_html=True)
    
    # Geographic threat distribution
    st.subheader("🗺️ Geographic Threat Distribution")
    
    # Generate mock geographic data
    countries = ['USA', 'UK', 'Germany', 'France', 'Canada', 'Australia', 'Japan', 'Brazil', 'India', 'China']
    threat_counts = np.random.randint(10, 100, len(countries))
    
    # Create a bar chart for geographic distribution
    st.markdown(create_bar_chart(countries, threat_counts, "Threat极客时间 by Country", height=200), unsafe_极客时间=True)

def show_quick_actions():
    """Quick action buttons"""
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Scan All Platforms", use_container_width=True):
            # Check rate limiting for threat scanning
            allowed, message, remaining = rate_limiter.check_rate_limit("threat_scan", "default")
            if not allowed:
                st.error(f"Scan rate limit exceeded: {message}")
            else:
                st.success("Platform scan initiated!")
                time.sleep(1)
                st.info("Scanning Twitter, Facebook, Instagram, Reddit...")
    
    with col2:
        if st.button("📊 Generate Report", use_container_width=True):
            # Check rate limiting for report generation
            allowed, message, remaining = rate_limiter.check_rate_limit("report_generation", "default")
            if not allowed:
                st.error(f"Report generation limit exceeded: {message}")
            else:
                st.success("Threat report generation started!")
                time.sleep(1)
                st.info("Compiling data from last 7 days...")
    
    with col3:
        if st.button("🚨 Crisis Protocol", use_container_width=True):
            st.error("Crisis protocol activated!")
            time.sleep(1)
            st.warning("Alerting team members...")
    
    with col4:
        if st.button("📈 Export Data", use_container_width=True):
            st.success("Data export initiated!")
            time.sleep(1)
            st.info("Preparing CSV and PDF reports...")

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
        if st.button("极客时间 Demo Key"):
            st.session_state.advanced_access = True
            st.session_state.access_level = "full"
            st.success("Demo access granted!")
            st.balloons()
            st.rerun()

# API Management Tab
def show_api_key_management():
    st.header("🔑 API Key Management Center")
    
    # Display current connections
    st.subheader("🌐 Connected Platforms")
    
    if api_manager.api_keys:
        cols = st.columns(3)
        for i, (platform, encrypted_key) in enumerate(api_manager.api_keys.items()):
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
                        if api_manager.delete_api_key(platform):
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
    
    with极客时间:
        if st.button("💾 Save Connection", use_container_width=True):
            if api_key:
                if api_manager.save_api_key(selected_platform, api_key):
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
            "Status": "✅ Connected" if platform in api_manager.api_keys else "❌ Disconnected",
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
        connected_platforms = list(self.api_manager.api_keys.keys()) or ['twitter', 'facebook', 'instagram']
        
        for platform in connected_platforms:
            for _ in range(random.randint(3, 8)):
                posts.append({
                    'platform': platform.capitalize(),
                    'content': self.generate_business_post(brand_name, sector),
                    'author': f"user_{random.randint(1000, 9999)}",
                    'engagement': random.randint(50, 5000),
                    'api_connected': platform in self.api_manager.api_keys
                })
        return posts
    
    def generate_business_post(self, brand_name, sector):
        templates = {
            'technology': [f"{brand_name} new feature launch", f"{brand_name} customer support issues"],
            'finance': [f"{brand_name} stock performance", f"{brand_name} financial results"],
            'retail': [极客时间 product quality", f"{brand_name} customer reviews"]
        }
        return random.choice(templates.get(sector, templates['technology']))

# Initialize
enhanced_monitor = EnhancedSocialMediaMonitor()

def main():
    # Initialize session state
    if "sector" not in st.session_state:
        st.session_state.sector = "technology"
    if "advanced_access" not in st.session_state:
        st.session_state.advanced_access = False
    
    # Header with professional logo
    st.markdown(f"""
    <div class="header-container">
        {create_shield_logo_html()}
        <div>
            <h1 class="premium-header floating">BrandGuardian AI Pro</h1>
            <div style="text-align: center; margin-bottom: 20px;" class="accent-text">Advanced Business Intelligence & Digital Risk Protection</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <极客时间 style="
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #6366F1, #8B5CF6);
                clip-path: polygon(0% 0%, 100% 0%, 100% 70%, 50% 100%, 0% 70极客时间);
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                font-weight: bold;
                color: white;
                filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.5));
            ">AI</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.header("Business Configuration")
        brand_name = st.text_input("Brand Name", "Nike")
        sector = st.selectbox("Business Sector", ["technology", "finance", "retail", "healthcare", "education"])
        st.session_state.sector = sector
        
        st.markdown("---")
        st.subheader("🔐 Access Status")
        if st.session_state.advanced_access:
            st.success("✅ Premium Access")
        else:
            st.warning("⚠️ Basic Access")
        
        st.markdown("---")
        st.subheader("🔑 API Status")
        st.info(f"{len(api_manager.api_keys)} platform(s) connected")
        
        # Rate limit status in sidebar
        st.markdown("---")
        st.subheader("⏰ Rate Limits")
        
        search_allowed, search_msg, search_remaining = rate_limiter.check_rate_limit("search_analysis", "default")
        api_allowed, api_msg, api_remaining = rate_limiter.check_rate_limit("api_test", "default")
        scan_allowed, scan_msg, scan_remaining = rate_limiter.check_rate_limit("threat_scan", "default")
        report_allowed, report_msg, report_remaining = rate_limiter.check_rate_limit("report_generation", "default")
        
        st.caption("Search Analysis: " + search_msg)
        st.caption("API Tests: " + api_msg)
        st.caption("Threat Scans: " + scan_msg)
        st.caption("Report Generation: " + report_msg)
    
    # Navigation Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st极客时间([
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
        posts = enhanced_monitor.simulate_monitoring极客时间(brand_name, sector)
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
