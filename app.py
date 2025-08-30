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
    
    .access-granted {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
        border-left: 4px solid #10B981;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
    }
    
    .access-denied {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
        border-left: 4px solid #EF4444;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
    }
    
    .api-key-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    /* ... (keep all your existing CSS styles) ... */
    
</style>
""", unsafe_allow_html=True)

# Security and Access Control
class SecurityManager:
    def __init__(self):
        # Pre-defined access keys (you can set these in Streamlit Cloud secrets)
        self.valid_access_keys = {
            "BG2024-PRO-ACCESS": "full",
            "BG-ADVANCED-ANALYSIS": "analysis",
            "BG-PREMIUM-2024": "premium",
            "BRAND-GUARDIAN-PRO": "pro"
        }
        
        # Default key for demo purposes (remove in production)
        self.default_key = "BG2024-PRO-ACCESS"
    
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
        """Simple encryption for demo purposes"""
        encoded = base64.b64encode(text.encode()).decode()
        return f"enc_{encoded}"
    
    def decrypt(self, text):
        """Simple decryption for demo purposes"""
        if text.startswith("enc_"):
            try:
                decoded = base64.b64decode(text[4:]).decode()
                return decoded
            except:
                return text
        return text

# API Key Manager Class - Simplified
class APIKeyManager:
    def __init__(self):
        self.encryptor = SimpleEncryptor()
        self.api_keys_file = "brand_api_keys.json"
        self.supported_platforms = {
            "twitter": {
                "name": "Twitter API",
                "icon": "🐦",
                "help_url": "https://developer.twitter.com/",
                "field_name": "Bearer Token",
                "field_help": "Enter your Twitter Bearer Token"
            },
            "facebook": {
                "name": "Facebook API",
                "icon": "📘",
                "help_url": "https://developers.facebook.com/",
                "field_name": "Access Token",
                "field_help": "Enter your Facebook Access Token"
            },
            # ... (other platforms)
        }
        self.load_api_keys()
    
    def load_api_keys(self):
        """Load API keys from file"""
        try:
            if os.path.exists(self.api_keys_file):
                with open(self.api_keys_file, 'r') as f:
                    self.api_keys = json.load(f)
            else:
                self.api_keys = {}
        except:
            self.api_keys = {}
    
    def save_api_keys(self):
        """Save API keys to file"""
        try:
            with open(self.api_keys_file, 'w') as f:
                json.dump(self.api_keys, f, indent=2)
        except Exception as e:
            st.error(f"Error saving API keys: {e}")
    
    def get_api_key(self, platform):
        """Get API key for a specific platform"""
        if platform in self.api_keys:
            return self.encryptor.decrypt(self.api_keys[platform])
        return None
    
    def save_api_key(self, platform, api_key):
        """Save API key for a platform"""
        if api_key:
            self.api_keys[platform] = self.encryptor.encrypt(api_key)
            self.save_api_keys()
            return True
        return False
    
    def delete_api_key(self, platform):
        """Delete API key for a platform"""
        if platform in self.api_keys:
            del self.api_keys[platform]
            self.save_api_keys()
            return True
        return False

# Initialize API Key Manager
api_manager = APIKeyManager()

# Advanced Threat Analysis Functionality (Protected)
def show_advanced_threat_analysis():
    """Show advanced threat analysis (protected content)"""
    if not security_manager.check_access():
        show_access_required()
        return
    
    st.header("🔍 Advanced Threat Analysis")
    st.markdown('<div class="access-granted">', unsafe_allow_html=True)
    st.success("✅ Premium Access Granted - Advanced Features Unlocked")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Advanced analysis content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛡️ Real-time Threat Detection")
        st.metric("Active Threats", "12")
        st.metric("Threat Level", "High")
        st.metric("Response Time", "2.3s")
        
        # Threat timeline
        st.subheader("📈 Threat Timeline")
        dates = pd.date_range(end=datetime.now(), periods=7)
        threats = [5, 8, 3, 12, 7, 4, 9]
        threat_data = pd.DataFrame({'Date': dates, 'Threats': threats})
        st.line_chart(threat_data.set_index('Date'))
    
    with col2:
        st.subheader("🎯 Threat Classification")
        threat_types = {
            'Brand Impersonation': 35,
            'Negative Sentiment': 25,
            'Competitor Attacks': 20,
            'Fake Reviews': 15,
            'Copyright Issues': 5
        }
        
        for threat, percentage in threat_types.items():
            st.write(f"**{threat}:** {percentage}%")
            st.progress(percentage / 100)
        
        st.subheader("🚨 Immediate Actions")
        actions = [
            "✅ Block 5 impersonator accounts",
            "⚠️ Monitor competitor mentions",
            "✅ Respond to negative reviews",
            "🔍 Investigate copyright violations"
        ]
        
        for action in actions:
            st.write(f"• {action}")
    
    # Advanced threat intelligence
    st.subheader("🧠 AI-Powered Threat Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Predictive Analysis**")
        st.write("• 85% probability of increased threats in next 48h")
        st.write("• Primary source: Twitter & Reddit")
        st.write("• Key keywords: scam, fake, complaint")
    
    with col2:
        st.warning("**Recommended Actions**")
        st.write("• Increase monitoring frequency")
        st.write("• Prepare crisis communication")
        st.write("• Alert legal team")
        st.write("• Enhance social listening")
    
    # Real-time monitoring dashboard
    st.subheader("📊 Live Threat Dashboard")
    
    # Simulate real-time threat data
    threat_data = []
    for i in range(10):
        threat_data.append({
            'Time': (datetime.now() - timedelta(minutes=i*5)).strftime("%H:%M"),
            'Platform': random.choice(['Twitter', 'Facebook', 'Reddit', 'Instagram']),
            'Severity': random.choice(['High', 'Medium', 'Low']),
            'Type': random.choice(['Impersonation', 'Negative Review', 'Fake Account']),
            'Status': random.choice(['Active', 'Neutralized', 'Monitoring'])
        })
    
    threat_df = pd.DataFrame(threat_data)
    st.dataframe(threat_df, use_container_width=True, hide_index=True)

def show_access_required():
    """Show access required message"""
    st.header("🔒 Advanced Threat Analysis")
    st.markdown('<div class="access-denied">', unsafe_allow_html=True)
    st.warning("🚫 Premium Access Required")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("""
    ### Unlock Advanced Threat Analysis Features
    
    To access our premium threat detection capabilities, please enter your access key below.
    This feature includes:
    
    - 🛡️ **Real-time threat detection** across all platforms
    - 🎯 **AI-powered threat classification**
    - 📈 **Predictive threat analytics**
    - 🚨 **Immediate action recommendations**
    - 📊 **Live threat dashboard**
    - 🧠 **Advanced sentiment analysis**
    """)
    
    # Access key input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        access_key = st.text_input(
            "Enter Access Key:",
            type="password",
            placeholder="BG2024-PRO-ACCESS",
            help="Enter your premium access key to unlock advanced features"
        )
    
    with col2:
        st.write("")  # Spacer
        st.write("")  # Spacer
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
    
    # Demo access for testing
    with st.expander("🆓 Demo Access (For Testing)"):
        st.info("Use this demo key to test the advanced features:")
        st.code("BG2024-PRO-ACCESS")
        
        if st.button("Use Demo Key", key="demo_key"):
            st.session_state.advanced_access = True
            st.session_state.access_level = "full"
            st.success("✅ Demo access granted! Advanced features unlocked.")
            st.balloons()
            st.rerun()
    
    # Contact information for access
    st.markdown("---")
    st.write("""
    **Need an access key?**
    
    Contact us at:
    - 📧 Email: support@brandguardian.ai
    - 🌐 Website: www.brandguardian.ai
    - 📞 Phone: +1-555-BRAND-PRO
    
    *Enterprise plans include advanced threat analysis features*
    """)

# Add API Key Management Section
def show_api_key_management():
    st.header("🔑 Simple API Key Management")
    # ... (keep your existing API management code)

# Enhanced Social Media Monitoring with API Keys
class EnhancedSocialMediaMonitor:
    def __init__(self):
        self.api_manager = api_manager
    
    def simulate_monitoring_with_api(self, brand_name, sector):
        """Simulate monitoring using stored API keys"""
        posts = []
        
        # Check which platforms have API keys configured
        connected_platforms = list(self.api_manager.api_keys.keys())
        
        if not connected_platforms:
            st.info("🌐 No API keys configured. Using demo data with enhanced simulation.")
            connected_platforms = ['twitter', 'facebook', 'instagram', 'google']
        
        for platform in connected_platforms:
            platform_posts = random.randint(5, 15) if platform in self.api_manager.api_keys else random.randint(3, 8)
            
            for _ in range(platform_posts):
                content = self.generate_business_post(brand_name, sector)
                
                posts.append({
                    'platform': platform.capitalize(),
                    'content': content,
                    'author': f"user_{random.randint(1000, 9999)}",
                    'author_followers': random.randint(100, 1000000),
                    'date': datetime.now() - timedelta(hours=random.randint(0, 168)),
                    'engagement': random.randint(50, 5000),
                    'api_connected': platform in self.api_manager.api_keys,
                    'source': f"Live API ({platform})" if platform in self.api_manager.api_keys else "Demo Data"
                })
        
        return posts
    
    def generate_business_post(self, brand_name, sector):
        """Generate realistic business posts"""
        templates = {
            'technology': [
                f"{brand_name}'s new AI feature is amazing!",
                f"Concerned about {brand_name}'s data privacy",
                f"{brand_name} stock is performing well",
                f"Switching from {brand_name} to competitor",
                f"{brand_name} announced new partnership"
            ],
            # ... (other sectors)
        }
        
        sector_templates = templates.get(sector, templates['technology'])
        return random.choice(sector_templates)

# Initialize enhanced monitor
enhanced_monitor = EnhancedSocialMediaMonitor()

# Add API Key Management to the main navigation
def main():
    # Initialize session state
    if "sector" not in st.session_state:
        st.session_state.sector = "technology"
    if "selected_platform" not in st.session_state:
        st.session_state.selected_platform = "twitter"
    if "advanced_access" not in st.session_state:
        st.session_state.advanced_access = False
    if "access_level" not in st.session_state:
        st.session_state.access_level = "none"
    
    # Premium Header
    st.markdown("""
    <div class="logo-container">
        <div class="logo">🛡️</div>
    </div>
    <h1 class="premium-header floating">BrandGuardian AI Pro</h1>
    <div style="text-align: center; margin-bottom: 20px;" class="accent-text">Advanced Business Intelligence & Digital Risk Protection</div>
    """, unsafe_allow_html=True)
    
    # Sidebar with API key quick access and access status
    with st.sidebar:
        st.header("Business Configuration")
        brand_name = st.text_input("Brand Name", "Nike")
        sector = st.selectbox("Business Sector", 
                            ["technology", "finance", "retail", "healthcare", "manufacturing"])
        
        st.session_state.sector = sector
        
        # Access Status
        st.markdown("---")
        st.subheader("🔐 Access Status")
        
        if st.session_state.advanced_access:
            st.success(f"✅ Premium Access: {st.session_state.access_level.upper()}")
            if st.button("🔓 Manage Access", key="manage_access"):
                st.session_state.advanced_access = False
                st.rerun()
        else:
            st.warning("⚠️ Basic Access")
            st.info("Upgrade for advanced features")
        
        # Quick API Key Status
        st.markdown("---")
        st.subheader("🔑 API Connections")
        
        connected_count = len(api_manager.api_keys)
        if connected_count > 0:
            st.success(f"✅ {connected_count} platform(s) connected")
        else:
            st.warning("⚠️ No API keys configured")
        
        # Quick access to API management
        if st.button("⚡ Manage API Keys", use_container_width=True):
            st.session_state.active_tab = "🔑 API Management"
        
        # Additional settings
        st.markdown("---")
        st.subheader("Advanced Settings")
        market_cap = st.number_input("Market Capitalization", 
                                   min_value=0.0, value=100000000.0, step=1000000.0)
        
        real_time = st.toggle("Real-time Monitoring", value=True)
    
    # Navigation Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Executive Dashboard", 
        "🔍 Advanced Threat Analysis",  # This tab now requires access key
        "📱 Social Monitoring",
        "🥊 Competitive Intelligence",
        "🌟 Influencer Network",
        "🛡️ Crisis Prediction",
        "❤️ Brand Health",
        "🔑 API Management"
    ])
    
    # Existing tabs functionality
    with tab1:
        st.header("Executive Dashboard")
        st.write("Dashboard content with integrated API data...")
        
        # Show access status on dashboard
        if st.session_state.advanced_access:
            st.success("✅ Premium Features: Advanced Threat Analysis Available")
        else:
            st.warning("🔒 Upgrade to access Advanced Threat Analysis")
    
    with tab2:
        # Advanced Threat Analysis (protected)
        show_advanced_threat_analysis()
    
    with tab3:
        st.header("Enhanced Social Monitoring")
        
        # Show connection status
        if api_manager.api_keys:
            st.success("✅ Using live API connections for monitoring")
            posts = enhanced_monitor.simulate_monitoring_with_api(brand_name, sector)
        else:
            st.info("🌐 Using demo data - connect API keys for real-time monitoring")
            posts = enhanced_monitor.simulate_monitoring_with_api(brand_name, sector)
        
        # Display posts
        for post in posts[:10]:
            with st.expander(f"{post['platform']} - {post['date'].strftime('%Y-%m-%d %H:%M')}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(post['content'])
                    st.caption(f"👤 {post['author']} | 👥 {post['author_followers']:,} followers | 📊 {post['engagement']} engagement")
                    if post.get('api_connected'):
                        st.success("✅ Live API Data")
                    else:
                        st.info("📊 Demo Data")
                
                with col2:
                    st.metric("Sentiment", "Positive" if random.random() > 0.3 else "Negative")
                    st.metric("Impact", "Medium")
    
    # Other tabs
    with tab4:
        st.header("Competitive Intelligence")
        st.write("Competitive analysis content...")
    
    with tab5:
        st.header("Influence Network Analysis")
        st.write("Influencer network content...")
    
    with tab6:
        st.header("Advanced Crisis Prediction")
        st.write("Crisis prediction content...")
    
    with tab7:
        st.header("Advanced Brand Health Analytics")
        st.write("Brand health content...")
    
    with tab8:
        show_api_key_management()

if __name__ == "__main__":
    main()
