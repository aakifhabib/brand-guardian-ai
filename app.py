import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import hashlib
import re
import requests
from datetime import datetime, timedelta
import random
from urllib.parse import urlencode

# Set page configuration
st.set_page_config(
    page_title="BrandGuardian AI Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    .main { background-color: #0f1116; color: #ffffff; }
    .stApp { background-color: #0f1116; }
    .metric-card { 
        background: rgba(255, 255, 255, 0.05); 
        padding: 20px; 
        border-radius: 10px; 
        margin: 10px 0;
    }
    .positive { color: #00cc96; }
    .negative { color: #ef553b; }
    .subscription-card {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin: 15px 0;
    }
    .api-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #8B5CF6;
    }
    .connected { border-left: 4px solid #10B981; }
    .disconnected { border-left: 4px solid #EF4444; }
    .crisis-alert {
        background-color: #ff4b4b;
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Subscription Tiers
SUBSCRIPTION_TIERS = {
    "starter": {
        "price": 299,
        "features": [
            "Basic sentiment monitoring", 
            "1 social platform", 
            "Daily reports", 
            "Email alerts", 
            "5 keyword monitors"
        ],
        "limits": {
            "social_platforms": 1, 
            "keywords": 5, 
            "historical_data": 30
        }
    },
    "professional": {
        "price": 799,
        "features": [
            "Advanced sentiment analysis", 
            "3 social platforms", 
            "Real-time alerts", 
            "Competitive analysis", 
            "20 keyword monitors"
        ],
        "limits": {
            "social_platforms": 3, 
            "keywords": 20, 
            "historical_data": 90
        }
    },
    "enterprise": {
        "price": 1999,
        "features": [
            "Full AI-powered protection", 
            "All social platforms", 
            "Multi-language support", 
            "Advanced crisis prediction", 
            "Unlimited keyword monitors",
            "API access",
            "Webhook integrations"
        ],
        "limits": {
            "social_platforms": 999, 
            "keywords": 999, 
            "historical_data": 365
        }
    }
}

# Database Class with API Key Storage
class SimpleDB:
    def __init__(self):
        self.data_file = "brands_data.json"
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.brands = json.load(f)
        else:
            # Initialize with demo account
            self.brands = {
                "acme_corp": {
                    "password": self._hash_password("demo123"),
                    "brand_name": "Acme Corporation",
                    "email": "marketing@acme-corp.com",
                    "subscription_tier": "enterprise",
                    "subscription_status": "active",
                    "connected_platforms": {},
                    "api_keys": {},
                    "monitoring_keywords": ["acme", "acme corp", "acme corporation"],
                    "webhook_urls": {},
                    "created_at": datetime.now().isoformat()
                }
            }
            self.save_data()
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.brands, f, indent=2)
    
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
            "created_at": datetime.now().isoformat()
        }
        self.save_data()
        return True
    
    def authenticate(self, brand_id, password):
        brand = self.brands.get(brand_id)
        if brand and brand["password"] == self._hash_password(password):
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

    def add_api_key(self, brand_id, platform, api_key, api_secret=None, additional_data=None):
        brand = self.get_brand(brand_id)
        if brand:
            if "api_keys" not in brand:
                brand["api_keys"] = {}
            
            brand["api_keys"][platform] = {
                "key": api_key,
                "secret": api_secret,
                "additional_data": additional_data,
                "added_date": datetime.now().isoformat(),
                "last_used": None
            }
            return self.update_brand(brand_id, {"api_keys": brand["api_keys"]})
        return False

    def add_webhook(self, brand_id, webhook_type, webhook_url):
        brand = self.get_brand(brand_id)
        if brand:
            if "webhook_urls" not in brand:
                brand["webhook_urls"] = {}
            
            brand["webhook_urls"][webhook_type] = {
                "url": webhook_url,
                "added_date": datetime.now().isoformat(),
                "last_triggered": None
            }
            return self.update_brand(brand_id, {"webhook_urls": brand["webhook_urls"]})
        return False

# API Manager Class
class APIManager:
    def __init__(self):
        self.supported_platforms = {
            "twitter": {
                "name": "Twitter/X API",
                "help_url": "https://developer.twitter.com/",
                "fields": [
                    {"name": "API Key", "type": "password", "required": True},
                    {"name": "API Secret", "type": "password", "required": True},
                    {"name": "Bearer Token", "type": "password", "required": False}
                ]
            },
            "facebook": {
                "name": "Facebook Graph API",
                "help_url": "https://developers.facebook.com/",
                "fields": [
                    {"name": "App ID", "type": "text", "required": True},
                    {"name": "App Secret", "type": "password", "required": True},
                    {"name": "Access Token", "type": "password", "required": True}
                ]
            },
            "instagram": {
                "name": "Instagram Graph API",
                "help_url": "https://developers.facebook.com/docs/instagram-api",
                "fields": [
                    {"name": "Access Token", "type": "password", "required": True},
                    {"name": "Business Account ID", "type": "text", "required": True}
                ]
            },
            "google_analytics": {
                "name": "Google Analytics",
                "help_url": "https://developers.google.com/analytics",
                "fields": [
                    {"name": "Property ID", "type": "text", "required": True},
                    {"name": "API Key", "type": "password", "required": True}
                ]
            },
            "youtube": {
                "name": "YouTube Data API",
                "help_url": "https://developers.google.com/youtube",
                "fields": [
                    {"name": "API Key", "type": "password", "required": True},
                    {"name": "Channel ID", "type": "text", "required": False}
                ]
            },
            "reddit": {
                "name": "Reddit API",
                "help_url": "https://www.reddit.com/dev/api/",
                "fields": [
                    {"name": "Client ID", "type": "text", "required": True},
                    {"name": "Client Secret", "type": "password", "required": True},
                    {"name": "User Agent", "type": "text", "required": True}
                ]
            }
        }
    
    def get_platforms(self):
        return self.supported_platforms
    
    def test_connection(self, platform, credentials):
        # Simulate API connection test
        # In production, this would make actual API calls
        time.sleep(2)  # Simulate API call delay
        
        # Simulate 80% success rate for demo
        if random.random() < 0.8:
            return {
                "success": True,
                "message": f"Successfully connected to {platform}",
                "rate_limit": f"{random.randint(100, 1000)} calls/hour"
            }
        else:
            return {
                "success": False,
                "message": "Connection failed: Invalid credentials",
                "suggestion": "Please check your API keys and try again"
            }

# Webhook Manager Class
class WebhookManager:
    def __init__(self):
        self.supported_webhooks = {
            "slack": {
                "name": "Slack Webhook",
                "help_url": "https://api.slack.com/messaging/webhooks",
                "example": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
            },
            "discord": {
                "name": "Discord Webhook",
                "help_url": "https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks",
                "example": "https://discord.com/api/webhooks/1234567890/abcdefghijk"
            },
            "teams": {
                "name": "Microsoft Teams Webhook",
                "help_url": "https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook",
                "example": "https://outlook.office.com/webhook/abc123/IncomingWebhook/def456"
            },
            "custom": {
                "name": "Custom Webhook",
                "help_url": "",
                "example": "https://your-domain.com/webhook/alerts"
            }
        }
    
    def test_webhook(self, webhook_url, webhook_type):
        # Simulate webhook test
        time.sleep(1)
        
        # Simulate 90% success rate for demo
        if random.random() < 0.9:
            return {
                "success": True,
                "message": f"Webhook test successful for {webhook_type}"
            }
        else:
            return {
                "success": False,
                "message": "Webhook test failed: Invalid URL or server not responding"
            }

# Sentiment Analysis Engine (unchanged from previous)
class SentimentAnalyzer:
    def __init__(self):
        self.positive_words = {
            'excellent': 1.0, 'amazing': 0.9, 'great': 0.8, 'good': 0.7, 'love': 0.9,
            'best': 0.8, 'awesome': 0.9, 'fantastic': 0.9, 'perfect': 1.0, 'wonderful': 0.8,
            'outstanding': 0.9, 'superb': 0.9, 'brilliant': 0.8, 'favorite': 0.7, 'recommend': 0.6
        }
        
        self.negative_words = {
            'terrible': 1.0, 'awful': 0.9, 'bad': 0.7, 'hate': 0.9, 'worst': 1.0,
            'disappointing': 0.8, 'poor': 0.7, 'failure': 0.8, 'rubbish': 0.7, 'waste': 0.6,
            'avoid': 0.6, 'broken': 0.7, 'useless': 0.8, 'horrible': 0.9, 'disaster': 0.9
        }
        
        self.intensifiers = {'very': 1.3, 'extremely': 1.5, 'really': 1.2, 'so': 1.2}
        self.negators = {'not': -1, 'no': -1, 'never': -1, "n't": -1}
    
    def analyze_text(self, text):
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        sentiment_score = 0
        word_count = 0
        
        i = 0
        while i < len(words):
            word = words[i]
            modifier = 1.0
            
            # Check for intensifiers
            if i > 0 and words[i-1] in self.intensifiers:
                modifier = self.intensifiers[words[i-1]]
            
            # Check for negators
            negate = False
            if i > 0 and words[i-1] in self.negators:
                negate = True
                modifier *= -1
            
            # Calculate word sentiment
            if word in self.positive_words:
                sentiment_score += self.positive_words[word] * modifier
                word_count += 1
            elif word in self.negative_words:
                sentiment_score += self.negative_words[word] * modifier
                word_count += 1
            
            i += 1
        
        # Normalize score
        if word_count > 0:
            final_score = sentiment_score / word_count
            return max(-1.0, min(1.0, final_score))
        return 0.0

# Social Media Monitor (unchanged from previous)
class SocialMonitor:
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.platform_templates = {
            "twitter": {
                "positive": [
                    "Loving my new {} product! 🔥",
                    "{} has the best customer service! 👏",
                    "Just tried {} - absolutely amazing!",
                    "Shoutout to {} for their fantastic support!",
                    "{} never disappoints! 💯"
                ],
                "negative": [
                    "Really disappointed with {} service 😞",
                    "{} product broke after one week!",
                    "Never buying from {} again 👎",
                    "Terrible experience with {} support",
                    "{} needs to improve quality control"
                ],
                "neutral": [
                    "Just saw an ad from {}",
                    "Has anyone tried {} products?",
                    "Thinking about buying from {}",
                    "{} is having a sale right now",
                    "Comparing {} with other brands"
                ]
            },
            "facebook": {
                "positive": [
                    "I'm really impressed with {}!",
                    "Great experience with {} customer service",
                    "{} products are top quality!",
                    "Highly recommend {} to everyone",
                    "{} exceeded my expectations!"
                ],
                "negative": [
                    "Very disappointed with {} quality",
                    "{} customer service was unhelpful",
                    "Won't be purchasing from {} again",
                    "Poor experience with {} delivery",
                    "{} product didn't meet expectations"
                ],
                "neutral": [
                    "Saw a post about {}",
                    "Considering {} for my business",
                    "{} has new products available",
                    "Looking for reviews of {}",
                    "What's everyone's experience with {}?"
                ]
            },
            "instagram": {
                "positive": [
                    "Love the new {} collection! ❤️",
                    "{} always delivers quality 📦",
                    "So happy with my {} purchase!",
                    "{} has the best products!",
                    "Couldn't be happier with {}! 😊"
                ],
                "negative": [
                    "Really unhappy with {} service",
                    "{} product quality is declining",
                    "Disappointed in {} recently",
                    "{} needs to do better",
                    "Not satisfied with {} at all"
                ],
                "neutral": [
                    "Checking out {} products",
                    "Heard about {} from a friend",
                    "{} has some interesting offers",
                    "Looking at {} options",
                    "Researching {} products"
                ]
            }
        }
    
    def generate_posts(self, platform, brand_keywords, count=10):
        posts = []
        
        for _ in range(count):
            # Choose sentiment weighted toward positive/neutral
            sentiment_type = random.choices(
                ["positive", "negative", "neutral"], 
                weights=[0.5, 0.2, 0.3]
            )[0]
            
            template = random.choice(self.platform_templates[platform][sentiment_type])
            brand_keyword = random.choice(brand_keywords)
            post_text = template.format(brand_keyword)
            
            # Generate engagement based on sentiment
            base_engagement = random.randint(10, 100)
            if sentiment_type == "positive":
                engagement = base_engagement * random.randint(2, 5)
            elif sentiment_type == "negative":
                engagement = base_engagement * random.randint(3, 6)  # Negative often gets more engagement
            else:
                engagement = base_engagement
            
            posts.append({
                "text": post_text,
                "platform": platform,
                "engagement": engagement,
                "author": f"user_{random.randint(1000, 9999)}",
                "timestamp": datetime.now() - timedelta(hours=random.randint(0, 72)),
                "sentiment": self.sentiment_analyzer.analyze_text(post_text)
            })
        
        return posts

# Crisis Detector (unchanged from previous)
class CrisisDetector:
    def __init__(self):
        self.crisis_keywords = {
            'sue': 0.8, 'lawsuit': 0.9, 'boycott': 0.7, 'scam': 1.0, 'fraud': 1.0,
            'fake': 0.7, 'dangerous': 0.9, 'recall': 0.8, 'unsafe': 0.8, 'harmful': 0.9,
            'broken': 0.6, 'exploded': 0.9, 'fire': 0.8, 'injured': 0.9, 'hospital': 0.8
        }
        
        self.crisis_patterns = [
            r"class action",
            r"legal action against",
            r"never.*again",
            r"worst.*ever",
            r"dangerous.*product",
            r"hurt.*by",
            r"hospitalized.*from"
        ]
    
    def detect_crisis(self, posts, brand_keywords):
        crisis_score = 0
        crisis_posts = []
        
        for post in posts:
            text_lower = post["text"].lower()
            post_score = 0
            
            # Check for crisis keywords
            for keyword, weight in self.crisis_keywords.items():
                if keyword in text_lower:
                    post_score += weight
            
            # Check for crisis patterns
            for pattern in self.crisis_patterns:
                if re.search(pattern, text_lower):
                    post_score += 0.5
            
            # Check if brand is mentioned
            brand_mentioned = any(brand_kw.lower() in text_lower for brand_kw in brand_keywords)
            
            if brand_mentioned and post_score > 0.5:
                crisis_score += post_score
                crisis_posts.append({
                    "post": post,
                    "crisis_score": post_score,
                    "reasons": self._get_crisis_reasons(text_lower)
                })
        
        # Determine crisis level
        if crisis_score > 5:
            level = "critical"
        elif crisis_score > 3:
            level = "high"
        elif crisis_score > 1:
            level = "medium"
        else:
            level = "low"
        
        return {
            "crisis_score": min(10, crisis_score),
            "crisis_level": level,
            "crisis_posts": crisis_posts
        }
    
    def _get_crisis_reasons(self, text):
        reasons = []
        for keyword in self.crisis_keywords:
            if keyword in text:
                reasons.append(f"Crisis keyword: {keyword}")
        
        for pattern in self.crisis_patterns:
            if re.search(pattern, text):
                reasons.append(f"Crisis pattern: {pattern}")
        
        return reasons

# Initialize components
db = SimpleDB()
api_manager = APIManager()
webhook_manager = WebhookManager()
social_monitor = SocialMonitor()
crisis_detector = CrisisDetector()

# Authentication functions
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_brand' not in st.session_state:
        st.session_state.current_brand = None
    if 'subscription_tier' not in st.session_state:
        st.session_state.subscription_tier = None

def login_section():
    st.sidebar.header("Brand Login")
    
    with st.sidebar.form("login_form"):
        brand_id = st.text_input("Brand ID")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if db.authenticate(brand_id, password):
                st.session_state.authenticated = True
                st.session_state.current_brand = brand_id
                st.session_state.subscription_tier = db.get_brand(brand_id)["subscription_tier"]
                st.sidebar.success(f"Welcome {db.get_brand(brand_id)['brand_name']}!")
            else:
                st.sidebar.error("Invalid credentials")
    
    if st.session_state.authenticated:
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.current_brand = None
            st.session_state.subscription_tier = None
            st.rerun()

def registration_section():
    with st.sidebar.expander("New Brand Registration"):
        with st.form("register_form"):
            brand_id = st.text_input("Choose Brand ID")
            brand_name = st.text_input("Brand Name")
            email = st.text_input("Contact Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            tier = st.selectbox("Subscription Tier", ["starter", "professional", "enterprise"])
            
            submitted = st.form_submit_button("Register")
            
            if submitted:
                if password != confirm_password:
                    st.error("Passwords don't match")
                elif db.create_brand(brand_id, password, brand_name, email, tier):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Brand ID already exists")

# NEW: API Management Section
def api_management_section():
    st.header("🔑 API & Integration Management")
    
    brand_data = db.get_brand(st.session_state.current_brand)
    
    # API Keys Management
    st.subheader("📊 Connected APIs")
    
    # Display current API connections
    if "api_keys" in brand_data and brand_data["api_keys"]:
        for platform, details in brand_data["api_keys"].items():
            status = "🟢 Connected" if details.get("key") else "🔴 Disconnected"
            with st.expander(f"{platform.title()} - {status}"):
                st.write(f"**Last used:** {details.get('last_used', 'Never')}")
                if st.button(f"Disconnect {platform}", key=f"disconnect_{platform}"):
                    updated_keys = brand_data["api_keys"]
                    updated_keys.pop(platform)
                    db.update_brand(st.session_state.current_brand, {"api_keys": updated_keys})
                    st.success(f"Disconnected from {platform}")
                    st.rerun()
    else:
        st.info("No API connections yet. Add your first API below.")
    
    # Add new API connection
    st.subheader("➕ Add New API Connection")
    
    platforms = api_manager.get_platforms()
    selected_platform = st.selectbox("Select Platform", list(platforms.keys()), 
                                   format_func=lambda x: platforms[x]["name"])
    
    platform_info = platforms[selected_platform]
    
    st.write(f"**Documentation:** [{platform_info['name']} Guide]({platform_info['help_url']})")
    
    with st.form(f"add_{selected_platform}_api"):
        credentials = {}
        for field in platform_info["fields"]:
            if field["type"] == "password":
                credentials[field["name"]] = st.text_input(field["name"], type="password")
            else:
                credentials[field["name"]] = st.text_input(field["name"])
        
        submitted = st.form_submit_button("Connect API")
        
        if submitted:
            # Validate required fields
            missing_fields = []
            for field in platform_info["fields"]:
                if field["required"] and not credentials[field["name"]]:
                    missing_fields.append(field["name"])
            
            if missing_fields:
                st.error(f"Missing required fields: {', '.join(missing_fields)}")
            else:
                # Test connection
                with st.spinner("Testing connection..."):
                    result = api_manager.test_connection(selected_platform, credentials)
                
                if result["success"]:
                    # Save API keys
                    db.add_api_key(st.session_state.current_brand, selected_platform, 
                                 credentials, additional_data=result)
                    st.success(f"✅ {result['message']}")
                    if "rate_limit" in result:
                        st.info(f"Rate limit: {result['rate_limit']}")
                else:
                    st.error(f"❌ {result['message']}")
                    if "suggestion" in result:
                        st.info(result["suggestion"])

    # Webhook Management
    st.subheader("🔔 Webhook Integrations")
    
    # Display current webhooks
    if "webhook_urls" in brand_data and brand_data["webhook_urls"]:
        for webhook_type, details in brand_data["webhook_urls"].items():
            with st.expander(f"{webhook_type.title()} Webhook"):
                st.write(f"**URL:** {details['url']}")
                st.write(f"**Added:** {details['added_date']}")
                if st.button(f"Remove {webhook_type} Webhook", key=f"remove_{webhook_type}"):
                    updated_webhooks = brand_data["webhook_urls"]
                    updated_webhooks.pop(webhook_type)
                    db.update_brand(st.session_state.current_brand, {"webhook_urls": updated_webhooks})
                    st.success(f"Removed {webhook_type} webhook")
                    st.rerun()
    else:
        st.info("No webhooks configured yet. Add your first webhook below.")
    
    # Add new webhook
    st.subheader("➕ Add New Webhook")
    
    webhook_types = webhook_manager.supported_webhooks
    selected_webhook = st.selectbox("Webhook Type", list(webhook_types.keys()),
                                  format_func=lambda x: webhook_types[x]["name"])
    
    webhook_info = webhook_types[selected_webhook]
    
    if webhook_info["help_url"]:
        st.write(f"**Documentation:** [{webhook_info['name']} Guide]({webhook_info['help_url']})")
    
    webhook_url = st.text_input("Webhook URL", placeholder=webhook_info["example"])
    
    if st.button("Test Webhook"):
        if webhook_url:
            with st.spinner("Testing webhook..."):
                result = webhook_manager.test_webhook(webhook_url, selected_webhook)
            
            if result["success"]:
                st.success(f"✅ {result['message']}")
            else:
                st.error(f"❌ {result['message']}")
        else:
            st.warning("Please enter a webhook URL first")
    
    if st.button("Save Webhook") and webhook_url:
        db.add_webhook(st.session_state.current_brand, selected_webhook, webhook_url)
        st.success(f"✅ {selected_webhook} webhook saved successfully!")

# Other sections (Dashboard, Platform Connections, Subscription, Settings) remain unchanged
# [Previous code for these sections would go here]

def dashboard_section():
    # ... (unchanged from previous implementation)
    pass

def platform_connection_section():
    # ... (unchanged from previous implementation)
    pass

def subscription_section():
    # ... (unchanged from previous implementation)
    pass

def settings_section():
    # ... (unchanged from previous implementation)
    pass

def landing_page():
    # ... (unchanged from previous implementation)
    pass

# Main application
def main():
    init_session_state()
    login_section()
    registration_section()
    
    if not st.session_state.authenticated:
        landing_page()
        return
    
    # Authenticated user navigation
    brand_data = db.get_brand(st.session_state.current_brand)
    st.sidebar.title(f"👋 {brand_data['brand_name']}")
    st.sidebar.write(f"**Plan:** {st.session_state.subscription_tier.title()}")
    
    # Updated navigation to include API Management
    app_sections = {
        "Dashboard": dashboard_section,
        "Platform Connections": platform_connection_section,
        "API Management": api_management_section,  # NEW SECTION
        "Subscription": subscription_section,
        "Settings": settings_section
    }
    
    selected_section = st.sidebar.selectbox("Navigation", list(app_sections.keys()))
    app_sections[selected_section]()

if __name__ == "__main__":
    main()
