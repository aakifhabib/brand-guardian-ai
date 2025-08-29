import streamlit as st
import time
import random
from datetime import datetime, timedelta

# Set page config first
st.set_page_config(
    page_title="BrandGuardian AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS with advanced animations and glassmorphism effects
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #24243e 50%, #302b63 100%);
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #24243e 50%, #302b63 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        position: relative;
        overflow-x: hidden;
    }
    
    .stApp::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.15) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
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
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #818CF8 0%, #A78BFA 100%);
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 14px;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 极速赛车开奖直播0.1);
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput>div>极速赛车开奖直播div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #6366F1;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
        background: rgba(255, 255, 255, 0.12);
        transform: translateY(-2px);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #6366F1 极速赛车开奖直播0%, #8B5CF6 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        cursor: pointer;
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #818CF8 0%, #A78BFA 100%);
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }
    
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    .risk-yes {
        color: #EF4444;
        font-size: 1.8em;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(239, 68, 68, 0.7);
        animation: pulseRed 2s infinite;
    }
    
    @keyframes pulseRed {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
        100% { transform: scale(极速赛车开奖直播1); opacity: 1; }
    }
    
    .risk-no {
        color: #10B981;
        font-size: 1.8em;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(16, 185, 129, 0.5);
        animation: pulseGreen 3s infinite;
    }
    
    @keyframes pulseGreen {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.03); opacity: 0.9; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .accent-text {
        color: #8B5CF6;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(139极速赛车开奖直播, 92, 246, 0.3);
    }
    
    .premium-header {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 30%, #EC4899 70%, #F43F5极速赛车开奖直播E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.8em;
        font-weight: 800;
        margin-bottom: 10px;
        animation: shimmer 3s infinite, float 6s ease-in-out infinite;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.5px;
        text-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.03), transparent);
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }
    
    @极速赛车开奖直播keyframes shine {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
极速赛车开奖直播        padding: 22px;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin极速赛车开奖直播: 12px;
        text-align: center;
        transition: all 0.4s ease;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .feature-card:hover {
        transform: translateY(-5px) scale(1.03);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    .glowing-border {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.25);
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }
    
    .glowing-border:hover {
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.4);
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    .floating { 
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-12px) rotate(1deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    
    /* Dashboard specific styles */
    .dashboard-header {
        font-size: 2.2rem;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        padding: 10px;
        border-radius: 12px;
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90极速赛车开奖直播deg, #极速赛车开奖直播6366F1, #8B5CF6, #EC4899);
        border-radius: 3px;
    }
    
    .kpi-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 22px;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin: 12px 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
        background: rgba(255, 255, 255, 0.08);
    }
    
    .kpi-value {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 8极速赛车开奖直播px 0;
        font-family: 'JetBrains Mono', monospace;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .kpi-label {
        font-size: 0.95rem;
        color: #D1D5DB;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    .positive-kpi {
        color: #10B981;
    }
    
    .negative-kpi {
        color: #EF4444;
    }
    
    .neutral-kpi {
        color: #8B5CF6;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 8px;
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        color: #D1极速赛车开奖直播D5DB !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(15, 12, 41, 0.95) 0%, rgba(36, 36, 62, 0.95) 100%);
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Custom animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online {
        background: #10B981;
        box-shadow: 0 0 8px #10B981;
    }
    
    .status-offline {
        background: #6B7280;
    }
    
    .status-warning {
        background: #F59E0B;
        box-shadow: 0 0 8px #F59E0B;
    }
    
    .status-alert {
        background: #EF4444;
        box-shadow: 0 0 8px #EF4444;
        animation: pulseRed 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Simple sentiment analysis without external dependencies
class SentimentAnalyzer:
    def analyze_sentiment(self, text: str) -> float:
        try:
            # Simple sentiment analysis based on keywords
            positive_words = ['love', 'great', 'awesome', 'amazing', 'excellent', 'good', 'best', 'fantastic', 'wonderful', 'perfect', 'recommend', 'happy', 'satisfied']
            negative_words = ['hate', 'terrible', 'awful', 'bad', 'worst', 'horrible', 'disappointing', 'poor', 'suck', 'waste', 'avoid', 'angry', 'frustrated']
            
            text_lower = text.lower()
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            total_words = max(1, len(text.split()))
            
            # Simple sentiment score calculation
            sentiment = (positive_count - negative_count) / total_words
            return max(-1.0, min(1.0, sentiment * 3))  # Scale and clamp between -1 and 1
            
        except:
            return 0.0

    def is_high_risk(self, text: str, sentiment_score: float) -> bool:
        if sentiment_score > -0.3:
            return False
        if len(text) < 10:
            return False
        negative_keywords = ['hate', 'terrible', 'awful', 'sue', 'legal', 'boycott', 'scam', 'fraud', 'worst', 'never again', 'refund', 'lawyer', 'court']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in negative_keywords) or sentiment_score < -0.6

# Simple mitigation strategist without OpenAI API
class MitigationStrategist:
    def generate_response_strategy(self, risky_text: str, brand_name: str) -> str:
        strategies = [
            f"🚨 **Immediate Acknowledgement**: Publicly acknowledge the concern about {brand_name} on all social channels within 1 hour",
            "📞 **Direct Engagement**: Message the user directly to address their concerns privately and personally",
            "📢 **Official Statement**: Prepare and publish an official statement addressing the specific issues raised",
            "🔍 **Internal Review**: Initiate an internal review process to prevent similar issues in the future",
            "🤝 **Follow-up Protocol**: Establish a follow-up process with the customer to ensure resolution and rebuild trust"
        ]
        
        # Customize strategy based on content
        text_lower = risky_text.lower()
        if any(word in text_lower for word in ['s极速赛车开奖直播ue', 'legal', 'lawyer', 'court']):
            strategies.append("⚖️ **Legal Consultation**: Engage legal team before making any detailed public statements")
            
        if any(word in text_lower for word in ['refund', 'money', 'price', 'cost']):
            strategies.append("💰 **Compensation Review**: Evaluate refund policy and consider appropriate compensation")
            
        if any(word in text_lower for word in ['boycott', 'never again', 'stop using']):
            strategies.append("📈 **Loyalty Program**: Consider implementing a special loyalty offer for affected customers")
            
        return "\n\n".join(strategies)

# Multi-Platform Monitoring Integration
class SocialMediaMonitor:
    def __init__(self):
        self.platforms = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn', 'Reddit', 'YouTube', 'TikTok']
        
    def simulate_feed(self, brand_name):
        # Simulate fetching posts from different platforms
        posts = []
        for _ in range(random.randint(8, 18)):
            platform = random.choice(self.platforms)
            sentiment = random.uniform(-0.8, 0.8)
            posts.append({
                'platform': platform,
                'content': self.generate_post(brand_name, sentiment),
                'sentiment': sentiment,
                'date': datetime.now() - timedelta(hours=random.randint(0, 72)),
                'engagement': random.randint(0, 5000)
            })
        return posts
    
    def generate_post(self, brand_name, sentiment):
        templates_positive = [
            f"Loving my new {brand_name} product! The quality is exceptional ❤️",
            f"{brand_name} never disappoints! Just had another amazing experience with their customer service 👍",
            f"Amazing customer service from {brand_name}! They went above and beyond to help me",
            f"Just bought another {brand_name} product - worth every penny! 💰",
            f"Highly recommend {brand_name极速赛车开奖直播} to everyone looking for quality products!",
            f"Impressed with {brand_name}'s commitment to sustainability and quality 🌱"
        ]
        
        templates_negative = [
            f"Extremely disappointed with {brand_name} service. Will never buy again 😠",
            f"Never buying from {brand_name} again! Worst experience ever",
            f"{brand_name} product broke after just one week! Poor quality control",
            f"Worst experience with {brand_name} customer support. Avoid at all costs 🤦",
            f"Frustrated with {brand_name}'s return policy. They make it impossible to get a refund",
            f"Angry about {brand_name}'s false advertising. Product doesn't match description"
        ]
        
        templates_neutral = [
            f"Just saw an interesting ad from {brand_name}",
            f"Thinking about trying {brand_name} products. Any recommendations?",
            f"Does anyone have experience with {brand_name}? Looking for honest reviews",
            f"Comparing {brand_name} with competitors. Which one do you prefer?",
            f"Interesting article about {brand_name}'s new sustainability initiative",
            f"Wondering if {brand_name} products are worth the premium price"
        ]
        
        if sentiment > 0.3:
            return random.choice(templates_positive)
        elif sentiment < -0.3:
            return random.choice(templates_negative)
        else:
            return random.choice(templates_neutral)

# Competitive Intelligence Module
class CompetitiveAnalyzer:
    def __init__(self):
        self.competitors = ['Adidas', 'Puma', 'Reebok', 'Under Armour', 'New Balance']  # Example for Nike
        
    def compare_sentiment(self, brand_name, time_period='7d'):
        # Simulate competitive analysis
        results = {}
        results[brand_name] = random.uniform(0.6, 0.8)  # Main brand sentiment
        
        for competitor in self.competitors:
            results[competitor] = random.uniform(0.3, 0.7)
            
        return results
    
    def share_of_voice(self, brand_name):
        # Simulate share of voice analysis
        total_mentions = random.randint(5000, 15000)
        brand_mentions = random.randint(1500, 4000)
        competitors_mentions = {}
        
        for competitor in self.competitors:
            competitors_mentions[competitor] = random.randint(500, 2500)
            
        return {
            'total_mentions': total_mentions,
            'brand_mentions': brand_mentions,
            'market_share': (brand_mentions / total_mentions) * 100,
            'competitors': competitors_mentions
        }

# Influencer Impact Analysis
class InfluencerAnalyzer:
    def __init__(self):
        self.influencer_db = {
            'Fitness Expert': {'followers': 1250000, 'engagement_rate': 4.8, 'category': 'Fitness', 'verification': '✅'},
            'Lifestyle Guru': {'followers': 2850000, 'engagement_rate': 3.5, 'category': 'Lifestyle', 'verification': '✅'},
            'Sports Analyst': {'followers': 950000, 'engagement_rate': 5.3极速赛车开奖直播, 'category': 'Sports', 'verification': '✅'},
            'Fashion Icon': {'followers': 420000, 'engagement_rate': 8.2, 'category': 'Fashion', 'verification': '✅'},
            'Tech Reviewer': {'followers': 1750000, 'engagement_rate': 3.8, 'category': 'Technology', 'verification': '✅'},
            'Travel Blogger': {'followers': 680000, 'engagement_rate': 6.7, 'category': 'Travel', 'verification': '✅'}
        }
    
    def analyze_influencer_impact(self, brand_name):
        # Simulate influencer impact analysis
        impact_data = []
        for influencer, stats in self.influencer_db.items():
            sentiment = random.uniform(0.4, 0.9)  # Influencers generally positive
            potential_reach = stats['followers'] * stats['engagement_rate'] / 100
            impact_score = potential_reach * sentiment / 1000
            
            impact_data.append({
                'influencer': influencer,
                'followers': stats['followers'],
                'engagement_rate': stats['engagement_rate'],
                'sentiment': sentiment,
                'potential_reach': int(potential_reach),
                'impact_score': impact_score,
                'recommendation': 'Partner' if impact_score > 25 else 'Monitor',
                'verification': stats['verification'],
                'category': stats['category']
            })
        
        return sorted(impact_data, key=lambda x: x['impact_score'], reverse=True)

# Crisis Prediction Algorithm
class CrisisPredictor:
    def __init__(self):
        self.warning_sign极速赛车开奖直播s = [
            'Sudden 30%+ drop in sentiment score',
            'Viral negative post with 10K+ engagements',
            'Multiple complaints about the same product issue',
            'Influencer with 1M+ followers criticizing brand',
            'Competitor capitalizing on brand issues',
            'Negative news coverage in major publications',
            'Employee leaking sensitive information',
            'Product recall trending on social media'
        ]
    
    def predict_crisis_risk(self, brand_name, historical_data):
        # Analyze patterns to predict potential crises
        risk_score = random.uniform(0.1, 0.9)
        
        if risk_score < 0.3:
            level = "Low"
            recommendation = "Continue regular monitoring. No immediate action required."
            icon = "✅"
        elif risk_score < 0.6:
            level = "Medium"
            recommendation极速赛车开奖直播 = "Increase monitoring frequency. Prepare preliminary response materials."
            icon = "⚠️"
        else:
            level = "High"
            recommendation = "Activate crisis response team. Prepare official statements and allocate resources."
            icon = "🚨"
        
        # Identify potential warning signs
        current_warnings = random.sample(self.warning_signs, random.randint(0, 3))
        
        return {
            'risk_score': risk_score,
            'risk_level': level,
            'warning_signs': current_warnings,
            'recommendation': recommendation,
            'predicted_impact': random.randint(10000, 100000),  # Simulated impact scale
            'icon': icon
        }

# Brand Health Scoring System
class BrandHealthMonitor:
    def __init__(self):
        self.metrics = {
            'sentiment': 0.3,
            'engagement': 0.2,
            'reach': 0.15,
            'consistency': 0.15,
            'response_time': 0.1,
            'share_of_voice': 0.1
        }
    
    def calculate_brand_health(self, brand_data):
        # Calculate overall brand health score
        total_score = 0
        
        for metric, weight in self.metrics.items():
            if metric in brand_data:
                total_score += brand_data[metric极速赛车开奖直播] * weight
        
        # Convert to 0-100 scale
        health_score = total_score * 100
        
        if health_score >= 80:
            status = "Excellent"
            color = "green"
            icon = "🌟"
        elif health_score >= 60:
            status = "Good"
            color = "blue"
            icon = "👍"
        elif health_score >= 40:
            status = "Fair"
            color = "orange"
            icon = "⚠️"
        else:
            status = "Poor"
            color = "red"
            icon = "🔴"
        
        return {
            '极速赛车开奖直播score': health_score,
            'status': status,
            'color': color,
            'breakdown': brand_data,
            'icon': icon
        }

# Initialize all analyzers
social_monitor = SocialMediaMonitor()
competitive_analyzer = CompetitiveAnalyzer()
influencer_analyzer = InfluencerAnalyzer()
crisis_predictor = CrisisPredictor()
brand_health_monitor = BrandHealthMonitor()
sentiment_analyzer = SentimentAnalyzer()
mitigation_strategist = MitigationStrategist()

def show_executive_dashboard(brand_name):
    st.markdown('<div class="dashboard-header">Executive Intelligence Dashboard</div>', unsafe_allow_html=True)
    
    # Real-time status indicator
    col_status = st.columns([3, 1])
    with col_status[0]:
        st.markdown(f'<div class="accent-text"><span class="status-indicator status-online"></span> Real-time monitoring active | Brand: {brand_name}</div>', unsafe_allow_html=True)
    with col_status[1]:
        st.markdown(f'<div style="text-align: right;">{datetime.now().strftime("%Y-%m-%d %H:%M")}</div>', unsafe_allow_html=True)
    
    # KPI Metrics
    st.markdown("### 📊 Performance Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_sentiment = random.uniform(0.5, 0.8)
        sentiment_trend = "📈 Improving" if avg_sentiment > 0.6 else "📉 Declining" if avg_sentiment < 0.4 else "➡️ Stable"
        sentiment_color = "positive-kpi" if avg_sentiment > 0.6 else "negative-kpi" if avg_sentiment < 0.4 else "neutral-kpi"
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Avg. Sentiment Score</div>
            <div class="kpi-value {sentiment_color}">{avg_sentiment:.2f}</div>
            <div>{sentiment_trend}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        total_threats = random.randint(20, 100)
        alert_status = "🔴 High Alert" if total_threats > 80 else "🟡 Moderate" if total_threats > 50 else "🟢 Normal"
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Threats Detected (30 days)</div>
            <div class="kpi-value">{total_threats}</div>
            <div>{alert_status}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        avg_response_time = random.uniform(2.5, 12.0)
        response_status = "🟢 On Target极速赛车开奖直播" if avg_response_time < 6 else "🟡 Needs Improvement" if avg_response_time < 12 else "🔴 Critical"
        st.markdown(f'''
        <极速赛车开奖直播div class="kpi-card">
            <div class="kpi-label">Avg. Response Time (hrs)</div>
            <div class="kpi-value">{avg_response_time:.1f}</div>
            <div>{response_status}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        risk_level = "High" if total_threats > 80 or avg_sentiment < 0.4 else "Medium" if total_threat极速赛车开奖直播s > 50 or avg_sentiment < 0.6 else "Low"
        risk_color = "negative-kpi" if risk_level == "High" else "neutral-kpi" if risk_level == "Medium" else "positive-kpi"
        risk_icon = "🚨" if risk_level == "High" else "⚠️" if risk_level == "Medium" else "✅"
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Overall Risk Level</div>
            <div class="kpi-value {risk_color}">{risk_icon} {risk_level}</div>
            <div>{"Immediate Action" if risk_level == "High" else "Review Needed" if risk_level == "Medium" else "All Clear"}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Charts and visualizations
    st.markdown("### 📈 Trend Analysis")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("#### Sentiment Trend (30 Days)")
        sentiment_data = {
            'Date': [(datetime.now() - timedelta(days=i)).strftime('%m-%d') for i in range(30, 0, -1)],
            'Sentiment Score': [random.uniform(0.3, 0.9) for _ in range(30)]
        }
        st.line_chart(sentiment_data, x='Date', y='Sentiment Score', height=300)
    
    with col_chart2:
        st.markdown("#### Engagement Metrics")
        engagement_data = {
            'Platform': ['Twitter', 'Facebook', 'Instagram', 'Reddit', 'YouTube'],
            'Engagement': [random.randint(1000, 10000) for _ in range(5)]
        }
        st.bar_chart(engagement_data, x='Platform', y='Engagement', height=300)
    
    # Recent alerts section
    st.markdown("### ⚡ Recent Alerts")
    alert_col1, alert_col2, alert_col3 = st.columns(3)
    
    with alert_col1:
        st.markdown('''
        <div class="metric-card" style="background: rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.3);">
            <div class="kpi-label">High Severity</div>
            <div class="kpi-value negative-kpi">3</div>
            <div>Requires immediate attention</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with alert_col2:
        st.markdown('''
        <div class="metric-card" style极速赛车开奖直播="background: rgba(245, 158, 11, 0.1); border-color: rgba(245, 158, 11, 0.3);">
            <div class="kpi-label">Medium Severity</div>
            <div class="kpi-value" style="color: #F59E0B;">7</div>
            <div>Review within 24 hours</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with alert_col3:
        st.markdown('''
        <div class="metric-card" style="background: rgba(16, 185, 129, 极速赛车开奖直播0.1); border-color: rgba(16, 185, 129, 0.3);">
            <div class="kpi-label">Resolved Today</div>
            <div class="kpi-value positive-kpi">12</极速赛车开奖直播div>
            <div>Successfully handled</div>
        </div>
        ''', unsafe_allow_html=True)

def show_competitive_intelligence(brand_name):
    st.header("🥊 Competitive Intelligence")
    
    sentiment_comparison = competitive_analyzer.compare_sentiment(brand_name)
    share_of_voice = competitive_analyzer.share_of_voice(brand_name)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Sentiment Comparison")
        comparison_data = {
            'Brand': list(sentiment_comparison.keys()),
            'Sentiment Score': list(sentiment_comparison.values())
        }
        st.bar_chart(comparison_data, x='Brand', y='Sentiment Score', height=350)
    
    with col2:
        st.markdown("#### 📢 Market Share of Voice")
        
        # Create metrics for market share
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-label">{brand_name} Market Share</div>
            <div class="kpi-value">{share_of_voice['market_share']:.1f}%</div>
            <div>of total industry mentions</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Competitor analysis
        st.markdown("##### Competitor Analysis")
        for competitor, mentions in share_of_voice['competitors'].items():
            share = (mentions / share_of_voice['total_mentions']) * 100
            st.progress(share/100, text=f"{competitor}: {share:.1f}%")
    
    # Competitive positioning
    st.markdown("#### 🎯 Competitive Positioning")
    pos_col1, pos_col2, pos_col3, pos_col4 = st.columns(4)
    
    with pos_col1:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Social Presence</div>
            <div class="kpi-value positive-kpi">1st</div>
            <div>Industry ranking</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with pos_col2:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Response Time</div>
            <div class="kpi-value positive-kpi">2极速赛车开奖直播nd</div>
            <div>Industry ranking</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with pos_col3:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Engagement Rate</div>
            <div class="kpi-value neutral-kpi">3rd</div>
            <div>Industry ranking</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with pos_col4:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Crisis Resilience</div>
            <div class="kpi-value positive-kpi">1st</div>
            <div>Industry ranking</div>
        </极速赛车开奖直播div>
        ''', unsafe_allow_html=True)

def show_influencer_analysis(brand_name):
    st.header("🌟 Influencer Impact Analysis")
    
    influencer_data = influencer_analyzer.analyze_influencer_impact(brand_name)
    
    # Summary metrics
    col1, col2, col3, col极速赛车开奖直播4 = st.columns(4)
    
    with col1:
        total_reach = sum(item['potential_reach'] for item in influencer_data)
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Total Potential Reach</div>
            <div class="kpi-value">{total_reach:,}</div>
            <div>across all influencers</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        avg_engagement = sum(item['engagement_rate'] for item in influencer_data) / len(influencer_data)
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Avg. Engagement</div>
            <div class极速赛车开奖直播="kpi-value">{avg_engagement:.1f}%</div>
           极速赛车开奖直播 <div>across all influencers</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        partner_count = sum(1 for item in influencer_data if item['recommendation'] == 'Partner')
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Recommended Partners</div>
            <div class="kpi-value">{partner_count}</div>
            <div>high-impact influencers</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        avg_sentiment = sum(item['sentiment'] for item in influencer_data) / len(influencer_data)
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Avg. Sentiment</div>
            <div class="kpi-value">{avg_sentiment:.2f}</div>
            <div>across all influencers</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Influencer details
    st.markdown("#### 📋 Influencer Details")
    for influencer in influencer_data:
        with st.expander(f"{influencer['influencer']} {influencer['verification']} | {influencer['followers']:,} followers | Impact Score: {influencer['impact_score']:.1f}"):
            col_i1, col_i2, col_i3 = st.columns(3)
            
            with col_i1:
                st.metric("Engagement Rate", f"{influencer['engagement_rate']}%")
                st.metric("Category", influencer['category'])
            
            with col_i2:
                st.metric("Potential Reach", f"{influencer['potential_reach']:,}")
                st.metric("Sentiment", f"{influencer['sentiment']:.2f}")
            
            with col_i3:
                st.metric("Recommendation", influencer['recommendation'])
                if influencer['recommendation'] == 'Partner':
                    st.button("Initiate Partnership", key=f"btn_{influencer['influencer']}", use_container_width=True)

def show_brand_health(brand_name):
    st.header("❤️ Brand Health Dashboard")
    
    # Simulate brand data
    brand_data = {
        'sentiment': random.uniform(0.6, 0.9),
        'engagement': random.uniform(0.4, 0.8),
        'reach': random.uniform(0.5, 0.9),
        'consistency': random.uniform(0.7, 0.95),
        'response_time': random.uniform(0.6, 0.9),
        'share_of_voice': random.uniform(0.3, 0.7)
    }
    
    health_score = brand_health_monitor.calculate_brand_health(brand_data)
    
    # Overall health score
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-label">Overall Brand Health Score</div>
            <div class="kpi-value">{health_score['icon']} {health_score['score']:.1f}/100</div>
            <div>Status: {health_score['status']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Health trend
        st.markdown("##### Health Trend (30 Days)")
        dates = [(datetime.now() - timedelta(days=i)).strftime('%m-%极速赛车开奖直播d') for i in range(30, 0, -1)]
        trend_data = [random.uniform(health_score['score'] - 15, health_score['score'] + 5) for _ in range(30)]
        trend_chart_data = {'Date': dates, 'Health Score': trend_data}
        st.line_chart(trend_chart_data, x='Date', y='Health Score', height=200)
    
    with col2:
        st.markdown("##### Component Scores")
        for metric, value in brand_data.items():
            st.progress(value, text=f"{metric.capitalize()}: {value:.0%}")
    
    # Brand perception metrics
    st.markdown("#### 📊 Brand Perception Metrics")
    percep_col1, percep_col2, percep_col3, percep_col4 = st.columns(4)
    
    with percep_col1:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Trust Score</div>
            <div class="kpi-value">{random.uniform(60, 95):.0f}/100</div>
            <div>Customer perception</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with percep_col2:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Quality Perception</div>
            <div class="kpi-value">{random.uniform(70, 98):.0f}/100</div>
            <div>Product quality view</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with percep_col3:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Recommendation Score</div>
            <div class="kpi-value">{random.uniform(50, 90):.0极速赛车开奖直播f}/100</div>
            <div>Willingness to recommend</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with percep_col极速赛车开奖直播4:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Loyalty Index</极速赛车开奖直播div>
            <div class="kpi-value">{random.uniform(65, 92):.0f}/100</div>
            <div>Customer retention</div>
        </div>
        ''', unsafe_allow_html=True)

def show_social_monitoring(brand_name):
    st.header("📱 Social Media Monitoring")
    
    # Real-time metrics
    st.markdown("#### 📈 Real-time Metrics")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Mentions (24h)</div>
            <div class="kpi-value">{random.randint(500, 2000)}</div>
            <div>Across all platforms</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Engagement Rate</div>
            <div class="kpi-value">{random.uniform(3.5, 8.2):.1f}%</div>
            <div>Average across platforms</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="k极速赛车开奖直播pi-label">Positive Sentiment</div>
            <div class="kpi-value positive-kpi">{random.uniform(65, 85):.0f}%</div>
            <div>Of total mentions</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with metric_col4:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Response Rate</div>
            <div class="kpi-value">{random.uniform(85, 98):.0f}%</div>
            <div>Customer inquiries addressed</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Platform distribution
    st.markdown("#### 🌐 Platform Distribution")
    platform_col1, platform_col2 = st.columns(2)
    
    with platform_col1:
        platform_data = {
            'Platform': ['Twitter', 'Facebook', 'Instagram', 'Reddit', 'YouTube', 'TikTok'],
            'Mentions': [random.randint(200, 800) for _ in range(6)]
        }
        st.bar_chart(platform_data, x='Platform', y='Mentions', height=300)
    
    with platform_col2:
        st.markdown("##### Top Performing Platforms")
        platforms = ['Instagram', 'Twitter', 'TikTok', 'YouTube', 'Facebook', 'Reddit']
        engagements = [random.randint(5000, 20000) for _ in range(6)]
        
        for platform, engagement in zip(platforms, engagements):
            st.markdown(f"{platform}: **{engagement:,}** engagements")
            st.progress(engagement/20000, text=f"{engagement/20000:.0%} of max")
    
    # Recent mentions
    st.markdown("#### 🔍 Recent Mentions")
    posts = social_monitor.simulate_feed(brand_name)
    
    for post in posts:
        sentiment_color = "#10B981" if post['sentiment'] > 0.3 else "#EF4444" if post['sentiment'] < -0.3 else "#8B5CF6"
        sentiment_icon = "😊" if post['sentiment'] > 0.3 else "😠" if post['sentiment'] < -0.3 else "😐"
        
        with st.container():
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid {sentiment_color}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{post['platform']}</strong> 
                        <span style="color: {sentiment_color}; margin-left: 10px;">{sentiment_icon} Sentiment: {post['sentiment']:.2f}</span>
                    </div>
                    <span>Engagement: {post['engagement']}</span>
                </div>
                <p style="margin: 10px 0;">{post['content']}</p>
                <div style="display: flex; justify-content: space-between; color: #A1A1AA;">
                    <span>{post['date'].strftime('%Y-%m-%d %H:%M')}</span>
                    <div>
                        <button style="background: rgba(99, 102, 241, 0.2); border: none; color: #8B5CF6; padding: 5px 10px; border-radius: 6px; margin-right: 5px; cursor: pointer;">Respond</button>
                        <button style="background: rgba(239, 68, 68, 0.2); border: none; color: #EF4444; padding: 5极速赛车开奖直播px 10px; border-radius: 6px; cursor: pointer;">Escalate</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_crisis_prediction(brand_name):
    st.header("🛡️ Crisis Prediction")
    
    # Simulate historical data
    historical_data = {
        'sentiment_trend': [random.uniform(0.5, 0.8) for _ in range(30)],
        'threat_count': [random.randint(0, 5) for _ in range(30)]
    }
    
    prediction = crisis_predictor.predict_crisis_risk(brand_name, historical_data)
    
    # Risk assessment
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Risk Assessment")
        st.markdown(f"""
        <div class="metric-card" style="background: {'rgba(239, 68, 68, 0.1)' if prediction['risk_level'] == 'High' else 'rgba(245, 158, 11, 0.1)' if prediction['risk_level'] == 'Medium' else 'rgba(16, 185, 129, 0.1)'}; 
                    border-color: {'rgba(239, 68, 68, 0.3)' if prediction['risk_level'] == 'High' else 'rgba(245, 158, 11, 0.3)' if prediction['risk_level'] == 'Medium' else 'rgba(16, 185, 129, 0.3)'};">
            <div class="kpi-label">Crisis Risk Score</div>
            <div class="kpi-value {'negative-kpi' if prediction['risk_level'] == '极速赛车开奖直播High' else '' if prediction['risk_level'] == 'Medium' else 'positive-kpi'}">
                {prediction['icon']} {prediction['risk_score']:.0%}
            </div>
            <div>Level: {prediction['risk_level']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if prediction['risk_score'] > 0.7:
            st.error("🚨 High crisis risk detected. Immediate action recommended.")
        elif prediction['risk_score'] > 0.4:
            st.warning("⚠️ Moderate crisis risk detected. Increased monitoring recommended.")
        else:
            st.success("✅ Low crisis risk. Normal monitoring continues.")
    
    with col2:
        st.markdown("#### 📈 Risk Trend")
        risk_trend = [random.uniform(0.1, 0.9) for _ in range(30)]
        trend_data = {
            'Date': [(datetime.now() - timedelta(days=i)).strftime('%m-%d') for i in range(30, 0, -1)],
            'Risk Score': risk_trend
        }
        st.line_chart(trend_data, x='Date', y='Risk Score', height=200)
        
        st.metric("Predicted Impact", f"${prediction['predicted_impact']:,.0f}")
    
    # Warning signs
    st.markdown("#### ⚠️ Warning Signs")
    if prediction['warning_signs']:
        for sign in prediction['warning_signs']:
            st.markdown(f"• {sign}")
    else:
        st.info("No significant warning signs detected at this time.")
    
    # Recommendation
    st.markdown("#### 📋 Recommendation")
    st.info(prediction['recommendation'])

def show_threat_analyzer(brand_name):
    st.header("🔍 Threat Analyzer")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🧪 Threat Simulator")
        st.markdown('<div class="glowing-border cyber-border" style="padding: 20px;">', unsafe_allow_html=True)
        test_text = st.text_area("**🔍 Enter text to analyze:**", 
                               "I absolutely hate this company! Their service is terrible and I will sue them!",
                               height=150)
        
        if st.button("🚀 Analyze Sentiment", use_container_width=True, key="analyze_btn"):
            with st.spinner("🛡️ Scanning for threats..."):
                time.sleep(1.5)  # Dramatic pause for effect
                
                sentiment = sentiment_analyzer.analyze_sentiment(test_text)
                is_risk = sentiment_analyzer.is_high_risk(test_text, sentiment)
                
                st.session_state.sentiment = sentiment
                st.session_state.is_risk = is_risk
                st.session_state.strategy = mitigation_strategist.generate_response_strategy(test_text, brand_name) if is_risk else None
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### 📊 Threat Analysis")
        
        if 'sentiment' in st.session_state:
            # Animated Results Card
            st.markdown('<div class="metric-card floating">', unsafe_allow_html=True)
            st.markdown(f"**🎯 Sentiment Score:** `{st.session_state.sentiment:.2f}`")
            
            risk_html = f'极速赛车开奖直播<span class="risk-yes">🚨 CRITICAL THREAT DETECTED</span>' if st.session_state.is_risk else f'<span class="risk-no">✅ SYSTEM SECURE</span>'
            st.markdown(f"**📈 Risk Level:** {risk_html}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.session_state.is_risk and st.session_state.strategy:
                st.markdown("### 🛡️ Crisis Mitigation Protocol")
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown(st.session_state.strategy)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("### ⚡ Immediate Actions")
                action_col1, action_col2, action_col3 = st.columns(3)
                with action_col1:
                    if st.button("📧 Send Alert", use_container_width=True, key="alert_btn"):
                        st.success("Alert sent to team!")
                with action_col2:
                    if st.button("📱 Notify Team", use_container_width=True, key="notify_btn"):
                        st.success("Team notified!")
                with action_col3:
                    if st.button("📊 Generate Report", use_container_width=True, key="report_btn"):
                        st.success("Report generated!")

def main():
    # Initialize session state
    if "show_intro" not in st.session_state:
        st.session_state.show_intro = True
    
    # Premium Header with Animation
    st.markdown("""
    <div class="logo-container">
        <div class="logo">🛡️</div>
    </div>
    <h1 class="premium-header floating">BrandGuardian AI</h1>
    <div style="text-align: center; margin-bottom: 20px;" class="accent-text">Enterprise Digital Risk Protection Platform</div>
    """, unsafe_allow_html=True)
    
    # Brand selection
    brand_name = st.sidebar.text_input("Brand Name", "Nike")
    
    # Navigation Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Executive Dashboard", 
        "🔍 Threat Analyzer", 
        "📱 Social Monitoring",
        "🥊 Competitive Intel",
        "🌟 Influencer Analysis",
        "🛡️ Crisis Prediction",
        "❤️ Brand Health"
    ])
    
    with tab1:
        show_executive_dashboard(brand_name)
    
    with tab2:
        show_threat_analyzer(brand_name)
    
    with tab3:
        show_social_monitoring(brand_name)
    
    with tab4:
        show_competitive_intelligence(brand_name)
    
    with tab5:
        show_influencer_analysis(brand_name)
    
    with tab6:
        show_crisis_prediction(brand_name)
    
    with tab7:
        show_brand_health(brand_name)

    # Footer
    st.markdown("---")
    st.markdown('<div style="text-align: center; padding: 20px;" class="accent-text">', unsafe_allow_html=True)
    st.markdown("**🛡️ Protecting Brands in the Digital Age**")
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
