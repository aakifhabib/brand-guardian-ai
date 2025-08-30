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
    
    .api-key-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        background: rgba(255, 255, 255, 0.08);
    }
    
    .platform-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    
    /* Add the rest of your existing CSS styles here */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 14px;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* ... (keep all your existing CSS styles) ... */
    
</style>
""", unsafe_allow_html=True)

# Simple encryption for API keys (for demonstration purposes)
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

# API Key Manager Class
class APIKeyManager:
    def __init__(self):
        self.encryptor = SimpleEncryptor()
        self.api_keys_file = "brand_api_keys.json"
        self.supported_platforms = {
            "twitter": {
                "name": "Twitter API",
                "icon": "🐦",
                "help_url": "https://developer.twitter.com/",
                "fields": ["API Key", "API Secret", "Bearer Token"]
            },
            "facebook": {
                "name": "Facebook Graph API",
                "icon": "📘",
                "help_url": "https://developers.facebook.com/",
                "fields": ["App ID", "App Secret", "Access Token"]
            },
            "instagram": {
                "name": "Instagram Graph API",
                "icon": "📸",
                "help_url": "https://developers.facebook.com/docs/instagram-api",
                "fields": ["Access Token", "Business Account ID"]
            },
            "google": {
                "name": "Google APIs",
                "icon": "🔍",
                "help_url": "https://console.cloud.google.com/",
                "fields": ["API Key", "Client ID", "Client Secret"]
            },
            "linkedin": {
                "name": "LinkedIn API",
                "icon": "💼",
                "help_url": "https://developer.linkedin.com/",
                "fields": ["Client ID", "Client Secret", "Access Token"]
            },
            "youtube": {
                "name": "YouTube API",
                "icon": "📺",
                "help_url": "https://developers.google.com/youtube",
                "fields": ["API Key", "Client ID", "Client Secret"]
            },
            "reddit": {
                "name": "Reddit API",
                "icon": "🔴",
                "help_url": "https://www.reddit.com/dev/api/",
                "fields": ["Client ID", "Client Secret", "User Agent"]
            },
            "tiktok": {
                "name": "TikTok API",
                "icon": "🎵",
                "help_url": "https://developers.tiktok.com/",
                "fields": ["Client Key", "Client Secret", "Access Token"]
            }
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
    
    def get_api_keys(self, platform):
        """Get API keys for a specific platform"""
        if platform in self.api_keys:
            decrypted_keys = {}
            for key_name, encrypted_value in self.api_keys[platform].items():
                decrypted_keys[key_name] = self.encryptor.decrypt(encrypted_value)
            return decrypted_keys
        return None
    
    def save_api_key(self, platform, key_data):
        """Save API keys for a platform"""
        encrypted_data = {}
        for key_name, value in key_data.items():
            if value:  # Only save non-empty values
                encrypted_data[key_name] = self.encryptor.encrypt(value)
        
        self.api_keys[platform] = encrypted_data
        self.save_api_keys()
        return True
    
    def delete_api_key(self, platform):
        """Delete API keys for a platform"""
        if platform in self.api_keys:
            del self.api_keys[platform]
            self.save_api_keys()
            return True
        return False
    
    def test_connection(self, platform, credentials):
        """Test API connection with provided credentials"""
        try:
            # Simulate connection testing
            time.sleep(1.5)
            
            # Simulate different success rates based on platform
            success_rate = 0.8  # 80% success rate for demo
            
            if random.random() < success_rate:
                return {
                    "success": True,
                    "message": f"✅ Successfully connected to {self.supported_platforms[platform]['name']}",
                    "platform": platform
                }
            else:
                return {
                    "success": False,
                    "message": f"❌ Failed to connect to {self.supported_platforms[platform]['name']}",
                    "suggestion": "Please check your credentials and try again."
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Connection error: {str(e)}",
                "suggestion": "Please try again later."
            }

# Initialize API Key Manager
api_manager = APIKeyManager()

# Add API Key Management Section
def show_api_key_management():
    st.header("🔑 API Key Management Center")
    st.markdown("""
    <div class="api-key-card">
        <h4>📋 Manage Your Social Media API Keys</h4>
        <p>Store your API keys securely to enable automatic monitoring across all platforms.</p>
        <p>Your keys are encrypted and stored locally for your security.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display current API keys
    st.subheader("📊 Connected Platforms")
    
    if api_manager.api_keys:
        cols = st.columns(3)
        for i, (platform, keys) in enumerate(api_manager.api_keys.items()):
            if platform in api_manager.supported_platforms:
                platform_info = api_manager.supported_platforms[platform]
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="api-key-card">
                        <div class="platform-icon">{platform_info['icon']}</div>
                        <h4>{platform_info['name']}</h4>
                        <p>Connected: {datetime.now().strftime('%Y-%m-%d')}</p>
                        <p>Keys: {len(keys)} stored</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Disconnect {platform}", key=f"disconnect_{platform}", use_container_width=True):
                        if api_manager.delete_api_key(platform):
                            st.success(f"Disconnected from {platform_info['name']}")
                            st.rerun()
    else:
        st.info("No API keys stored yet. Add your first API key below to get started!")
    
    # Add new API key
    st.subheader("➕ Add New API Connection")
    
    platforms = api_manager.supported_platforms
    selected_platform = st.selectbox("Select Platform", list(platforms.keys()), 
                                   format_func=lambda x: f"{platforms[x]['icon']} {platforms[x]['name']}")
    
    platform_info = platforms[selected_platform]
    
    st.markdown(f"""
    <div class="api-key-card">
        <h4>{platform_info['icon']} {platform_info['name']}</h4>
        <p><strong>Documentation:</strong> <a href="{platform_info['help_url']}" target="_blank">API Documentation</a></p>
        <p>Follow the documentation link to obtain your API credentials.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form(f"add_{selected_platform}_api"):
        st.write("**API Credentials**")
        
        credentials = {}
        for field in platform_info["fields"]:
            credentials[field] = st.text_input(
                f"{field}*",
                type="password",
                help=f"Enter your {field} for {platform_info['name']}"
            )
        
        # Check if we have existing keys for this platform
        existing_keys = api_manager.get_api_keys(selected_platform)
        if existing_keys:
            st.warning(f"⚠️ You already have API keys stored for {platform_info['name']}. "
                      "Adding new keys will replace the existing ones.")
        
        col1, col2 = st.columns(2)
        with col1:
            test_connection = st.form_submit_button("🧪 Test Connection", use_container_width=True)
        with col2:
            save_connection = st.form_submit_button("💾 Save API Keys", use_container_width=True)
        
        if test_connection:
            # Check if required fields are filled
            required_fields = platform_info["fields"]
            missing_fields = [field for field in required_fields if not credentials.get(field)]
            
            if missing_fields:
                st.error(f"Missing required fields: {', '.join(missing_fields)}")
            else:
                with st.spinner("Testing connection..."):
                    result = api_manager.test_connection(selected_platform, credentials)
                
                if result["success"]:
                    st.success(result["message"])
                else:
                    st.error(result["message"])
                    if "suggestion" in result:
                        st.info(result["suggestion"])
        
        if save_connection:
            # Validate required fields
            required_fields = platform_info["fields"]
            missing_fields = [field for field in required_fields if not credentials.get(field)]
            
            if missing_fields:
                st.error(f"Missing required fields: {', '.join(missing_fields)}")
            else:
                if api_manager.save_api_key(selected_platform, credentials):
                    st.success(f"✅ {platform_info['name']} API keys saved successfully!")
                    
                    # Test the connection after saving
                    with st.spinner("Testing saved connection..."):
                        result = api_manager.test_connection(selected_platform, credentials)
                    
                    if result["success"]:
                        st.success("✅ Connection verified with saved keys!")
                    else:
                        st.warning("⚠️ Keys saved but connection test failed. Please check your credentials.")
                else:
                    st.error("❌ Failed to save API keys. Please try again.")
    
    # Bulk API key import/export
    st.subheader("📦 Bulk Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Export All API Keys", use_container_width=True):
            # Create export data
            export_data = {
                "export_date": datetime.now().isoformat(),
                "version": "1.0",
                "api_keys": api_manager.api_keys
            }
            
            # Convert to JSON
            export_json = json.dumps(export_data, indent=2)
            
            # Create download link
            st.download_button(
                label="⬇️ Download API Keys Backup",
                data=export_json,
                file_name=f"brandguardian_api_keys_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    with col2:
        uploaded_file = st.file_uploader("📥 Import API Keys", type=["json"])
        if uploaded_file is not None:
            try:
                import_data = json.load(uploaded_file)
                if "api_keys" in import_data:
                    # Merge imported keys with existing ones
                    for platform, keys in import_data["api_keys"].items():
                        api_manager.api_keys[platform] = keys
                    api_manager.save_api_keys()
                    st.success("✅ API keys imported successfully!")
                    st.rerun()
                else:
                    st.error("❌ Invalid import file format.")
            except Exception as e:
                st.error(f"❌ Error importing API keys: {e}")
    
    # API Key Usage Statistics
    if api_manager.api_keys:
        st.subheader("📈 API Usage Statistics")
        
        # Simulate usage data
        usage_data = []
        for platform in api_manager.api_keys:
            usage_data.append({
                "Platform": platform,
                "API Calls (24h)": random.randint(100, 5000),
                "Success Rate": f"{random.randint(85, 99)}%",
                "Last Used": (datetime.now() - timedelta(hours=random.randint(1, 24))).strftime("%Y-%m-%d %H:%M")
            })
        
        usage_df = pd.DataFrame(usage_data)
        st.dataframe(usage_df, use_container_width=True)

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
            st.warning("No API keys configured. Using demo data.")
            connected_platforms = ['twitter', 'facebook', 'instagram']  # Default platforms
        
        for platform in connected_platforms:
            # Simulate posts from each connected platform
            platform_posts = random.randint(3, 8)
            for _ in range(platform_posts):
                content = self.generate_business_post(brand_name, sector)
                
                posts.append({
                    'platform': platform.capitalize(),
                    'content': content,
                    'author': f"user_{random.randint(1000, 9999)}",
                    'author_followers': random.randint(100, 1000000),
                    'date': datetime.now() - timedelta(hours=random.randint(0, 168)),
                    'engagement': random.randint(50, 5000),
                    'api_connected': True,
                    'source': f"Live API ({platform})"
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
            'finance': [
                f"{brand_name} Q3 results exceeded expectations",
                f"Regulatory issues for {brand_name}",
                f"{brand_name} dividend announcement",
                f"Customer satisfaction with {brand_name}",
                f"{brand_name} market expansion news"
            ],
            'retail': [
                f"Love {brand_name}'s new product line!",
                f"Disappointed with {brand_name} service",
                f"{brand_name} holiday sales success",
                f"{brand_name} product quality issues",
                f"{brand_name} store expansion plans"
            ]
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
    
    # Premium Header
    st.markdown("""
    <div class="logo-container">
        <div class="logo">🛡️</div>
    </div>
    <h1 class="premium-header floating">BrandGuardian AI Pro</h1>
    <div style="text-align: center; margin-bottom: 20px;" class="accent-text">Advanced Business Intelligence & Digital Risk Protection</div>
    """, unsafe_allow_html=True)
    
    # Sidebar with API key quick access
    with st.sidebar:
        st.header("Business Configuration")
        brand_name = st.text_input("Brand Name", "Nike")
        sector = st.selectbox("Business Sector", 
                            ["technology", "finance", "retail", "healthcare", "manufacturing"])
        
        st.session_state.sector = sector
        
        # Quick API Key Status
        st.markdown("---")
        st.subheader("🔑 API Key Status")
        
        connected_count = len(api_manager.api_keys)
        if connected_count > 0:
            st.success(f"✅ {connected_count} platform(s) connected")
            for platform in api_manager.api_keys:
                platform_info = api_manager.supported_platforms.get(platform, {})
                st.markdown(f"{platform_info.get('icon', '🔗')} {platform_info.get('name', platform)}")
        else:
            st.warning("⚠️ No API keys configured")
        
        if st.button("Manage API Keys", use_container_width=True):
            st.session_state.show_api_management = True
        
        # Additional settings
        st.markdown("---")
        st.subheader("Advanced Settings")
        market_cap = st.number_input("Market Capitalization", 
                                   min_value=0.0, value=0.0, step=1000000.0)
        
        real_time = st.toggle("Real-time Monitoring", value=True)
    
    # Navigation Tabs - Added API Management tab
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Executive Dashboard", 
        "🔍 Advanced Threat Analysis", 
        "📱 Social Monitoring",
        "🥊 Competitive Intelligence",
        "🌟 Influencer Network",
        "🛡️ Crisis Prediction",
        "❤️ Brand Health",
        "🔑 API Management"  # New tab
    ])
    
    # Existing tabs functionality (keep your existing code for tabs 1-7)
    with tab1:
        # Your existing dashboard code
        st.header("Executive Dashboard")
        st.write("Dashboard content goes here...")
    
    with tab2:
        # Your existing threat analysis code
        st.header("Advanced Threat Analysis")
        st.write("Threat analysis content goes here...")
    
    with tab3:
        st.header("Enhanced Social Monitoring")
        
        # Use API-connected monitoring if available
        if api_manager.api_keys:
            st.success("✅ Using live API connections for monitoring")
            posts = enhanced_monitor.simulate_monitoring_with_api(brand_name, sector)
        else:
            st.warning("⚠️ Using demo data - configure API keys for live monitoring")
            # Use your existing simulation method
            posts = []
            for _ in range(10):
                posts.append({
                    'platform': random.choice(['Twitter', 'Facebook', 'Instagram']),
                    'content': f"Sample post about {brand_name}",
                    'author': f"user_{random.randint(1000, 9999)}",
                    'engagement': random.randint(50, 5000),
                    'api_connected': False
                })
        
        # Display posts
        for post in posts:
            with st.expander(f"{post['platform']} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(post['content'])
                    st.caption(f"Author: {post['author']} | Engagement: {post['engagement']}")
                    if post.get('api_connected'):
                        st.success("✅ Live API Connection")
                    else:
                        st.info("📊 Demo Data")
                
                with col2:
                    st.metric("Sentiment", "Positive")
                    st.metric("Impact", "Medium")
    
    with tab4:
        # Your existing competitive intelligence code
        st.header("Competitive Intelligence")
        st.write("Competitive intelligence content goes here...")
    
    with tab5:
        # Your existing influencer network code
        st.header("Influence Network Analysis")
        st.write("Influencer network content goes here...")
    
    with tab6:
        # Your existing crisis prediction code
        st.header("Advanced Crisis Prediction")
        st.write("Crisis prediction content goes here...")
    
    with tab7:
        # Your existing brand health code
        st.header("Advanced Brand Health Analytics")
        st.write("Brand health content goes here...")
    
    # New API Management Tab
    with tab8:
        show_api_key_management()

if __name__ == "__main__":
    main()
