import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import hashlib
import re
from datetime import datetime, timedelta
import random

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
            "Unlimited keyword monitors"
        ],
        "limits": {
            "social_platforms": 999, 
            "keywords": 999, 
            "historical_data": 365
        }
    }
}

# Database Class
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
                    "monitoring_keywords": ["acme", "acme corp", "acme corporation"],
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
            "monitoring_keywords": [],
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

# Sentiment Analysis Engine
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

# Social Media Monitor
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

# Crisis Detector
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

# OAuth Manager
class OAuthManager:
    def __init__(self):
        self.platforms = {
            "twitter": {
                "auth_url": "https://twitter.com/i/oauth2/authorize",
                "scopes": ["tweet.read", "users.read", "offline.access"]
            },
            "facebook": {
                "auth_url": "https://www.facebook.com/dialog/oauth",
                "scopes": ["pages_read_engagement", "public_profile"]
            },
            "instagram": {
                "auth_url": "https://api.instagram.com/oauth/authorize",
                "scopes": ["user_profile", "user_media"]
            }
        }
    
    def get_auth_url(self, platform, brand_id):
        if platform in self.platforms:
            return f"{self.platforms[platform]['auth_url']}?client_id=bgai_{platform}&redirect_uri=https://yourdomain.com/oauth/callback&state={brand_id}_{platform}"
        return None
    
    def simulate_connection(self, platform, brand_id):
        # Simulate successful OAuth connection
        return {
            "access_token": f"simulated_token_{platform}_{brand_id}",
            "connected_at": datetime.now().isoformat(),
            "platform": platform
        }

# Initialize components
db = SimpleDB()
oauth_manager = OAuthManager()
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

# Application sections
def platform_connection_section():
    st.header("🔌 Platform Connections")
    
    brand_data = db.get_brand(st.session_state.current_brand)
    tier_limits = SUBSCRIPTION_TIERS[st.session_state.subscription_tier]["limits"]
    
    connected_count = len(brand_data.get("connected_platforms", {}))
    max_connections = tier_limits["social_platforms"]
    
    st.write(f"**Connected:** {connected_count} of {max_connections} platforms")
    
    for platform in ["twitter", "facebook", "instagram"]:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(platform.title())
        with col2:
            if platform in brand_data.get("connected_platforms", {}):
                if st.button(f"Disconnect", key=f"disconnect_{platform}"):
                    updated_platforms = brand_data.get("connected_platforms", {})
                    updated_platforms.pop(platform, None)
                    db.update_brand(st.session_state.current_brand, {"connected_platforms": updated_platforms})
                    st.success(f"Disconnected from {platform}")
                    st.rerun()
            else:
                if connected_count < max_connections:
                    if st.button(f"Connect", key=f"connect_{platform}"):
                        auth_url = oauth_manager.get_auth_url(platform, st.session_state.current_brand)
                        st.info(f"🔗 [Connect to {platform.title()}]({auth_url})")
                        
                        # Simulate connection for demo
                        token_data = oauth_manager.simulate_connection(platform, st.session_state.current_brand)
                        updated_platforms = brand_data.get("connected_platforms", {})
                        updated_platforms[platform] = token_data
                        db.update_brand(st.session_state.current_brand, {"connected_platforms": updated_platforms})
                        st.success(f"✅ Successfully connected to {platform}!")
                        st.rerun()
                else:
                    st.warning("⚠️ Upgrade plan for more connections")

def dashboard_section():
    st.header("📊 Brand Dashboard")
    
    brand_data = db.get_brand(st.session_state.current_brand)
    connected_platforms = brand_data.get("connected_platforms", {})
    keywords = brand_data.get("monitoring_keywords", [])
    
    if not connected_platforms:
        st.warning("Connect at least one platform to start monitoring")
        return
    
    # Generate simulated posts
    all_posts = []
    for platform in connected_platforms:
        posts = social_monitor.generate_posts(platform, keywords, count=15)
        all_posts.extend(posts)
    
    # Calculate metrics
    total_mentions = len(all_posts)
    avg_sentiment = np.mean([p["sentiment"] for p in all_posts]) if all_posts else 0
    total_engagement = sum(p["engagement"] for p in all_posts)
    
    # Crisis detection
    crisis_data = crisis_detector.detect_crisis(all_posts, keywords)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Mentions", total_mentions)
    with col2:
        st.metric("Avg Sentiment", f"{avg_sentiment:.2f}")
    with col3:
        st.metric("Total Engagement", f"{total_engagement:,}")
    with col4:
        st.metric("Crisis Level", crisis_data["crisis_level"].title())
    
    # Sentiment timeline
    st.subheader("📈 Sentiment Trend")
    if all_posts:
        timeline_data = []
        for hour in range(72, 0, -6):
            time_point = datetime.now() - timedelta(hours=hour)
            period_posts = [p for p in all_posts if p["timestamp"] > time_point - timedelta(hours=6)]
            if period_posts:
                period_sentiment = np.mean([p["sentiment"] for p in period_posts])
                timeline_data.append({
                    "time": time_point.strftime("%m/%d %H:00"),
                    "sentiment": period_sentiment
                })
        
        if timeline_data:
            chart_data = pd.DataFrame(timeline_data)
            st.line_chart(chart_data.set_index("time"))
    
    # Recent mentions
    st.subheader("💬 Recent Mentions")
    for post in sorted(all_posts, key=lambda x: x["timestamp"], reverse=True)[:5]:
        sentiment_icon = "😊" if post["sentiment"] > 0.3 else "😠" if post["sentiment"] < -0.3 else "😐"
        with st.expander(f"{sentiment_icon} {post['text'][:50]}...", expanded=False):
            st.write(f"**Platform:** {post['platform']}")
            st.write(f"**Sentiment:** {post['sentiment']:.2f}")
            st.write(f"**Engagement:** {post['engagement']}")
            st.write(f"**Time:** {post['timestamp'].strftime('%Y-%m-%d %H:%M')}")
    
    # Crisis alerts
    if crisis_data["crisis_posts"]:
        st.subheader("🚨 Crisis Alerts")
        for crisis in crisis_data["crisis_posts"][:3]:
            st.markdown(f"""
            <div class="crisis-alert">
                <strong>{crisis['post']['text']}</strong><br>
                Score: {crisis['crisis_score']:.1f} • Platform: {crisis['post']['platform']}
            </div>
            """, unsafe_allow_html=True)

def subscription_section():
    st.header("💰 Subscription Management")
    
    brand_data = db.get_brand(st.session_state.current_brand)
    current_tier = st.session_state.subscription_tier
    current_tier_data = SUBSCRIPTION_TIERS[current_tier]
    
    # Current plan
    st.subheader("Current Plan")
    st.info(f"**{current_tier.title()} Plan** - ${current_tier_data['price']}/month")
    
    for feature in current_tier_data["features"]:
        st.write(f"✅ {feature}")
    
    # Upgrade options
    st.subheader("Upgrade Options")
    for tier, data in SUBSCRIPTION_TIERS.items():
        if tier != current_tier:
            with st.expander(f"{tier.title()} - ${data['price']}/month"):
                for feature in data["features"]:
                    st.write(f"▪️ {feature}")
                if st.button(f"Upgrade to {tier.title()}", key=f"upgrade_{tier}"):
                    db.update_brand(st.session_state.current_brand, {"subscription_tier": tier})
                    st.session_state.subscription_tier = tier
                    st.success(f"Upgraded to {tier} plan!")
                    st.rerun()

def settings_section():
    st.header("⚙️ Brand Settings")
    
    brand_data = db.get_brand(st.session_state.current_brand)
    
    # Keyword monitoring
    st.subheader("Monitoring Keywords")
    current_keywords = brand_data.get("monitoring_keywords", [])
    max_keywords = SUBSCRIPTION_TIERS[st.session_state.subscription_tier]["limits"]["keywords"]
    
    st.write(f"**Current keywords:** {len(current_keywords)} of {max_keywords}")
    
    new_keyword = st.text_input("Add new keyword to monitor")
    if st.button("Add Keyword") and new_keyword:
        if len(current_keywords) < max_keywords:
            updated_keywords = current_keywords + [new_keyword.lower()]
            db.update_brand(st.session_state.current_brand, {"monitoring_keywords": updated_keywords})
            st.success(f"Added keyword: {new_keyword}")
            st.rerun()
        else:
            st.error(f"Keyword limit reached. Upgrade plan to monitor more keywords.")
    
    # Display current keywords
    for keyword in current_keywords:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"▪️ {keyword}")
        with col2:
            if st.button("Remove", key=f"remove_{keyword}"):
                updated_keywords = [k for k in current_keywords if k != keyword]
                db.update_brand(st.session_state.current_brand, {"monitoring_keywords": updated_keywords})
                st.success(f"Removed keyword: {keyword}")
                st.rerun()
    
    # Alert preferences
    st.subheader("🔔 Alert Preferences")
    email_alerts = st.checkbox("Email alerts for critical issues", value=True)
    daily_digest = st.checkbox("Daily summary report", value=True)
    
    if st.button("Save Preferences"):
        st.success("Preferences saved!")

def landing_page():
    st.title("🛡️ BrandGuardian AI")
    st.write("### Complete Brand Protection & Intelligence Platform")
    
    # Pricing columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Starter")
        st.metric("Price", "$299/month")
        st.write("**Ideal for small businesses**")
        for feature in SUBSCRIPTION_TIERS['starter']['features'][:3]:
            st.write(f"▪️ {feature}")
        if st.button("Get Started - Starter", key="starter_btn"):
            st.info("Please register to get started")
    
    with col2:
        st.subheader("Professional")
        st.metric("Price", "$799/month")
        st.write("**Perfect for growing brands**")
        for feature in SUBSCRIPTION_TIERS['professional']['features'][:4]:
            st.write(f"▪️ {feature}")
        if st.button("Get Started - Professional", key="professional_btn"):
            st.info("Please register to get started")
    
    with col3:
        st.subheader("Enterprise")
        st.metric("Price", "$1,999/month")
        st.write("**Complete protection for enterprises**")
        for feature in SUBSCRIPTION_TIERS['enterprise']['features'][:5]:
            st.write(f"▪️ {feature}")
        if st.button("Contact Sales - Enterprise", key="enterprise_btn"):
            st.info("Contact sales@brandguardian.ai for enterprise pricing")
    
    # Demo credentials
    with st.expander("Demo Access"):
        st.write("Use these demo credentials:")
        st.code("Brand ID: acme_corp\nPassword: demo123")

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
    
    app_sections = {
        "Dashboard": dashboard_section,
        "Platform Connections": platform_connection_section,
        "Subscription": subscription_section,
        "Settings": settings_section
    }
    
    selected_section = st.sidebar.selectbox("Navigation", list(app_sections.keys()))
    app_sections[selected_section]()

if __name__ == "__main__":
    main()
