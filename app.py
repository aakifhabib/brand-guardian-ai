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

# Modern Tech CSS with Glassmorphism and Neumorphism
st.markdown("""
<style>
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
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #6366F1;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
        background: rgba(255, 255, 255, 0.12);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        cursor: pointer;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #818CF8 0%, #A78BFA 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
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
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .risk-no {
        color: #10B981;
        font-size: 1.8em;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(16, 185, 129, 0.5);
        animation: pulseGreen 3s infinite;
    }
    
    @keyframes pulseGreen {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    
    .accent-text {
        color: #8B5CF6;
        font-weight: 600;
    }
    
    .premium-header {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5em;
        font-weight: 800;
        margin-bottom: 20px;
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
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
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 10px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        background: rgba(255, 255, 255, 0.08);
    }
    
    .glowing-border {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.2);
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
    }
    
    .floating { 
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* Intro panel styles */
    .intro-panel {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .intro-feature {
        margin: 1.5rem 0;
        padding: 1.5rem;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1rem 0;
    }
    
    .logo {
        font-size: 4rem;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.3));
    }
    
    .tech-pattern {
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
        background-size: 50% 50%;
        background-position: 0 0, 100% 100%;
        background-repeat: no-repeat;
    }
    
    .cyber-border {
        position: relative;
        border: 1px solid transparent;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2)) padding-box,
                    linear-gradient(135deg, #6366F1, #8B5CF6) border-box;
    }
    
    /* Dashboard specific styles */
    .dashboard-header {
        font-size: 2rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    .kpi-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #D1D5DB;
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
</style>
""", unsafe_allow_html=True)

# Simple sentiment analysis without external dependencies
class SentimentAnalyzer:
    def analyze_sentiment(self, text: str) -> float:
        try:
            # Simple sentiment analysis based on keywords
            positive_words = ['love', 'great', 'awesome', 'amazing', 'excellent', 'good', 'best', 'fantastic', 'wonderful', 'perfect']
            negative_words = ['hate', 'terrible', 'awful', 'bad', 'worst', 'horrible', 'disappointing', 'poor', 'suck', 'waste']
            
            text_lower = text.lower()
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            total_words = len(text.split())
            
            if total_words == 0:
                return 0.0
                
            # Simple sentiment score calculation
            sentiment = (positive_count - negative_count) / total_words
            return max(-1.0, min(1.0, sentiment * 5))  # Scale and clamp between -1 and 1
            
        except:
            return 0.0

    def is_high_risk(self, text: str, sentiment_score: float) -> bool:
        if sentiment_score > -0.3:
            return False
        if len(text) < 10:
            return False
        negative_keywords = ['hate', 'terrible', 'awful', 'sue', 'legal', 'boycott', 'scam', 'fraud', 'worst', 'never again', 'refund']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in negative_keywords) or sentiment_score < -0.6

# Simple mitigation strategist without OpenAI API
class MitigationStrategist:
    def generate_response_strategy(self, risky_text: str, brand_name: str) -> str:
        strategies = [
            f"1. Immediately acknowledge the concern about {brand_name} on all social channels",
            "2. Direct message the user to address their concerns privately",
            "3. Prepare an official statement addressing the specific issues raised",
            "4. Review internal processes to prevent similar issues in the future",
            "5. Follow up with the customer to ensure resolution and rebuild trust"
        ]
        
        # Customize strategy based on content
        text_lower = risky_text.lower()
        if any(word in text_lower for word in ['sue', 'legal', 'lawyer']):
            strategies.append("6. Consult with legal team before making any public statements")
            
        if any(word in text_lower for word in ['refund', 'money', 'price']):
            strategies.append("7. Review refund policy and consider offering compensation")
            
        return "\n\n".join(strategies)

# Multi-Platform Monitoring Integration
class SocialMediaMonitor:
    def __init__(self):
        self.platforms = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn', 'Reddit', 'YouTube', 'TikTok']
        
    def simulate_feed(self, brand_name):
        # Simulate fetching posts from different platforms
        posts = []
        for _ in range(random.randint(5, 15)):
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
            f"Loving my new {brand_name} product! ❤️",
            f"{brand_name} never disappoints! 👍",
            f"Amazing customer service from {brand_name}!",
            f"Just bought another {brand_name} product - worth every penny! 💰"
        ]
        
        templates_negative = [
            f"Extremely disappointed with {brand_name} service 😠",
            f"Never buying from {brand_name} again!",
            f"{brand_name} product broke after just one week!",
            f"Worst experience with {brand_name} customer support 🤦"
        ]
        
        templates_neutral = [
            f"Just saw an ad from {brand_name}",
            f"Thinking about trying {brand_name} products",
            f"Does anyone have experience with {brand_name}?",
            f"Comparing {brand_name} with competitors"
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
        self.competitors = ['Adidas', 'Puma', 'Reebok', 'Under Armour']  # Example for Nike
        
    def compare_sentiment(self, brand_name, time_period='7d'):
        # Simulate competitive analysis
        results = {}
        results[brand_name] = random.uniform(0.6, 0.8)  # Main brand sentiment
        
        for competitor in self.competitors:
            results[competitor] = random.uniform(0.3, 0.7)
            
        return results
    
    def share_of_voice(self, brand_name):
        # Simulate share of voice analysis
        total_mentions = random.randint(1000, 5000)
        brand_mentions = random.randint(300, 2000)
        competitors_mentions = {}
        
        for competitor in self.competitors:
            competitors_mentions[competitor] = random.randint(100, 800)
            
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
            'Fitness Expert': {'followers': 500000, 'engagement_rate': 4.5, 'category': 'Fitness'},
            'Lifestyle Guru': {'followers': 1200000, 'engagement_rate': 3.2, 'category': 'Lifestyle'},
            'Sports Analyst': {'followers': 800000, 'engagement_rate': 5.1, 'category': 'Sports'},
            'Fashion Icon': {'followers': 300000, 'engagement_rate': 7.8, 'category': 'Fashion'}
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
                'recommendation': 'Partner' if impact_score > 20 else 'Monitor'
            })
        
        return sorted(impact_data, key=lambda x: x['impact_score'], reverse=True)

# Crisis Prediction Algorithm
class CrisisPredictor:
    def __init__(self):
        self.warning_signs = [
            'sudden sentiment drop',
            'viral negative post',
            'multiple complaints about same issue',
            'influencer criticism',
            'competitor capitalizing on issue'
        ]
    
    def predict_crisis_risk(self, brand_name, historical_data):
        # Analyze patterns to predict potential crises
        risk_score = random.uniform(0.1, 0.9)
        
        if risk_score < 0.3:
            level = "Low"
            recommendation = "Continue monitoring"
        elif risk_score < 0.6:
            level = "Medium"
            recommendation = "Increase monitoring frequency"
        else:
            level = "High"
            recommendation = "Prepare crisis response plan"
        
        # Identify potential warning signs
        current_warnings = random.sample(self.warning_signs, random.randint(0, 2))
        
        return {
            'risk_score': risk_score,
            'risk_level': level,
            'warning_signs': current_warnings,
            'recommendation': recommendation,
            'predicted_impact': random.randint(1000, 50000)  # Simulated impact scale
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
                total_score += brand_data[metric] * weight
        
        # Convert to 0-100 scale
        health_score = total_score * 100
        
        if health_score >= 80:
            status = "Excellent"
            color = "green"
        elif health_score >= 60:
            status = "Good"
            color = "blue"
        elif health_score >= 40:
            status = "Fair"
            color = "orange"
        else:
            status = "Poor"
            color = "red"
        
        return {
            'score': health_score,
            'status': status,
            'color': color,
            'breakdown': brand_data
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
    
    # KPI Metrics
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
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Threats Detected (30 days)</div>
            <div class="kpi-value">{total_threats}</div>
            <div>{"🔴 High Alert" if total_threats > 80 else "🟡 Moderate" if total_threats > 50 else "🟢 Normal"}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        avg_response_time = random.uniform(2.5, 12.0)
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Avg. Response Time (hrs)</div>
            <div class="kpi-value">{avg_response_time:.1f}</div>
            <div>{"🟢 On Target" if avg_response_time < 6 else "🟡 Needs Improvement" if avg_response_time < 12 else "🔴 Critical"}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        risk_level = "High" if total_threats > 80 or avg_sentiment < 0.4 else "Medium" if total_threats > 50 or avg_sentiment < 0.6 else "Low"
        risk_color = "negative-kpi" if risk_level == "High" else "neutral-kpi" if risk_level == "Medium" else "positive-kpi"
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Overall Risk Level</div>
            <div class="kpi-value {risk_color}">{risk_level}</div>
            <div>{"⚠️ Immediate Action" if risk_level == "High" else "📋 Review Needed" if risk_level == "Medium" else "✅ All Clear"}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Simple charts using Streamlit's native functions
    st.markdown("#### Sentiment Trend (30 Days)")
    sentiment_data = {
        'Date': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)],
        'Sentiment Score': [random.uniform(0.3, 0.9) for _ in range(30)]
    }
    st.line_chart(sentiment_data, x='Date', y='Sentiment Score')
    
    # Platform distribution
    st.markdown("#### Threats by Platform")
    platform_data = {
        'Platform': ['Twitter', 'Facebook', 'Instagram', 'Reddit', 'News Sites', 'Review Sites'],
        'Count': [random.randint(5, 30) for _ in range(6)]
    }
    st.bar_chart(platform_data, x='Platform', y='Count')

def show_competitive_intelligence(brand_name):
    st.header("Competitive Intelligence")
    
    sentiment_comparison = competitive_analyzer.compare_sentiment(brand_name)
    share_of_voice = competitive_analyzer.share_of_voice(brand_name)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sentiment Comparison")
        comparison_data = {
            'Brand': list(sentiment_comparison.keys()),
            'Sentiment Score': list(sentiment_comparison.values())
        }
        st.bar_chart(comparison_data, x='Brand', y='Sentiment Score')
    
    with col2:
        st.subheader("Market Share of Voice")
        labels = [brand_name] + list(share_of_voice['competitors'].keys())
        values = [share_of_voice['brand_mentions']] + list(share_of_voice['competitors'].values())
        
        # Create a simple pie chart using columns
        col1, col2, col3 = st.columns(3)
        col1.metric(brand_name, f"{share_of_voice['market_share']:.1f}%")
        for i, (competitor, mentions) in enumerate(share_of_voice['competitors'].items()):
            if i == 0:
                col2.metric(competitor, f"{(mentions/share_of_voice['total_mentions'])*100:.1f}%")
            elif i == 1:
                col3.metric(competitor, f"{(mentions/share_of_voice['total_mentions'])*100:.1f}%")

def show_influencer_analysis(brand_name):
    st.header("Influencer Impact Analysis")
    
    influencer_data = influencer_analyzer.analyze_influencer_impact(brand_name)
    
    for influencer in influencer_data:
        with st.expander(f"{influencer['influencer']} - {influencer['followers']:,} followers"):
            st.write(f"**Engagement Rate:** {influencer['engagement_rate']}%")
            st.write(f"**Sentiment:** {influencer['sentiment']:.2f}")
            st.write(f"**Potential Reach:** {influencer['potential_reach']:,}")
            st.write(f"**Impact Score:** {influencer['impact_score']:.1f}")
            st.write(f"**Recommendation:** {influencer['recommendation']}")

def show_brand_health(brand_name):
    st.header("Brand Health Dashboard")
    
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
    
    st.metric("Overall Brand Health Score", f"{health_score['score']:.1f}", health_score['status'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Metric Breakdown")
        for metric, value in brand_data.items():
            st.progress(value, text=f"{metric.capitalize()}: {value:.2%}")
    
    with col2:
        st.subheader("Historical Trend")
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)]
        trend_data = [random.uniform(health_score['score'] - 15, health_score['score'] + 5) for _ in range(30)]
        trend_chart_data = {'Date': dates, 'Health Score': trend_data}
        st.line_chart(trend_chart_data, x='Date', y='Health Score')

def show_social_monitoring(brand_name):
    st.header("Social Media Monitoring")
    
    posts = social_monitor.simulate_feed(brand_name)
    
    for post in posts:
        sentiment_color = "#10B981" if post['sentiment'] > 0.3 else "#EF4444" if post['sentiment'] < -0.3 else "#8B5CF6"
        
        with st.container():
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid {sentiment_color}">
                <div style="display: flex; justify-content: space-between;">
                    <strong>{post['platform']}</strong>
                    <span>Engagement: {post['engagement']}</span>
                </div>
                <p>{post['content']}</p>
                <div style="display: flex; justify-content: space-between;">
                    <span>Sentiment: {post['sentiment']:.2f}</span>
                    <span>{post['date'].strftime('%Y-%m-%d %H:%M')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_crisis_prediction(brand_name):
    st.header("Crisis Prediction")
    
    # Simulate historical data
    historical_data = {
        'sentiment_trend': [random.uniform(0.5, 0.8) for _ in range(30)],
        'threat_count': [random.randint(0, 5) for _ in range(30)]
    }
    
    prediction = crisis_predictor.predict_crisis_risk(brand_name, historical_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk Assessment")
        st.metric("Crisis Risk Score", f"{prediction['risk_score']:.2%}", prediction['risk_level'])
        
        if prediction['risk_score'] > 0.7:
            st.error("🚨 High crisis risk detected. Immediate action recommended.")
        elif prediction['risk_score'] > 0.4:
            st.warning("⚠️ Moderate crisis risk detected. Increased monitoring recommended.")
        else:
            st.success("✅ Low crisis risk. Normal monitoring continues.")
    
    with col2:
        st.subheader("Warning Signs")
        if prediction['warning_signs']:
            for sign in prediction['warning_signs']:
                st.markdown(f"• {sign}")
        else:
            st.info("No significant warning signs detected.")
    
    st.subheader("Recommendation")
    st.info(prediction['recommendation'])

def show_threat_analyzer(brand_name):
    st.header("Threat Analyzer")
    
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
            
            risk_html = f'<span class="risk-yes">🚨 CRITICAL THREAT DETECTED</span>' if st.session_state.is_risk else f'<span class="risk-no">✅ SYSTEM SECURE</span>'
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
