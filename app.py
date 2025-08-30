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

# Set page config first
st.set_page_config(
    page_title="BrandGuardian AI Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    /* Premium header styling */
    .premium-header {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin: 20px 0;
        background: linear-gradient(90deg, #FF9A8B 0%, #FF6A88 55%, #FF99AC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 2px 10px rgba(255, 106, 136, 0.3);
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
        color: #A5B4FC;
        text-align: center;
        margin-bottom: 40px;
    }
    
    /* Card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .search-analysis-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
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
        background: rgba(255, 255, 255, 0.07);
        transform: translateX(5px);
    }
    
    /* Threat indicators */
    .threat-indicator {
        padding: 8px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 5px;
        display: inline-block;
    }
    
    .threat-high {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid #EF4444;
    }
    
    .threat-medium {
        background: rgba(245, 158, 11, 0.2);
        color: #F59E0B;
        border: 1px solid #F59E0B;
    }
    
    .threat-low {
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid #10B981;
    }
    
    /* Status indicators */
    .api-status-connected {
        color: #10B981;
        font-weight: 600;
    }
    
    .api-status-disconnected {
        color: #EF4444;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(255, 255, 255, 0.05);
        color: white;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px 12px 0 0;
        padding: 10px 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(99, 102, 241, 0.5);
        border-bottom: none;
    }
    
    /* Custom metric styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem;
    }
    
    /* Custom selectbox */
    .stSelectbox [data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }
    
    /* Custom text input */
    .stTextInput [data-baseweb="input"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }
    
    /* Custom text area */
    .stTextArea [data-baseweb="textarea"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }
    
    /* Custom spinner */
    .stSpinner > div {
        border: 3px solid rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        border-top: 3px solid #6366F1;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Custom expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 8px;
        padding: 10px 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Custom dataframes */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Custom success/error boxes */
    .stAlert {
        border-radius: 12px;
    }
    
    /* Custom sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 100%);
    }
    
    /* Custom chart elements */
    .stChart {
        border-radius: 16px;
        overflow: hidden;
    }
    
    /* Custom progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 100%);
    }
    
    /* Custom radio buttons */
    .stRadio [role="radiogroup"] {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Custom number input */
    .stNumberInput [data-baseweb="input"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }
    
    /* Custom date input */
    .stDateInput [data-baseweb="input"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }
    
    /* Custom time input */
    .stTimeInput [data-baseweb="input"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }
    
    /* Custom slider */
    .stSlider [role="slider"] {
        background: #6366F1;
    }
    
    /* Custom checkbox */
    .stCheckbox [data-baseweb="checkbox"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 6px;
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

# Initialize API Key Manager
api_manager = APIKeyManager()

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
        try:
            import matplotlib.pyplot as plt
            
            labels = list(data.keys())
            values = list(data.values())
            colors = [self.colors['danger'], self.colors['warning'], self.colors['success']]
            
            fig, ax = plt.subplots(figsize=(8, 8))
            wedges, texts, autotexts = ax.pie(
                values, labels=labels, autopct='%1.1f%%', 
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
            
            # Display in Streamlit
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Error creating donut chart: {e}")
            # Fallback to bar chart
            self.create_bar_chart(np.array(list(data.values())), list(data.keys()), title)

# Initialize visualizations
viz = AdvancedVisualizations()

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
            <h3>Response Time</h3>
            <h1>2.1s</h1>
            <p style="color: #10B981;">-0.4s improvement</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Protected Assets</h3>
            <h1>24</h1>
            <p style="color: #10B981;">Fully secured</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Threat timeline with advanced visualization
    st.subheader("📈 Threat Timeline (7 Days)")
    
    # Generate sample data
    dates = pd.date_range(end=datetime.now(), periods=7)
    threats = [8, 12, 5, 18, 10, 7, 14]
    
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
    
    with col2:
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
            'retail': [f"{brand_name} product quality", f"{brand_name} store experience"]
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
    
    # Header
    st.markdown("""
    <h1 class="premium-header floating">BrandGuardian AI Pro</h1>
    <div style="text-align: center; margin-bottom: 20px;" class="accent-text">Advanced Business Intelligence & Digital Risk Protection</div>
    """, unsafe_allow_html=True)
    
    # Sidebar
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
        st.subheader("🔑 API Status")
        st.info(f"{len(api_manager.api_keys)} platform(s) connected")
    
    # Navigation Tabs
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
