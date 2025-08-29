import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pandas as pd

# Set page config first
st.set_page_config(
    page_title="BrandGuardian AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple CSS without complex animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #24243e 50%, #302b63 100%);
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #24243e 50%, #302b63 100%);
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.08);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 14px;
        font-size: 14px;
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
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #818CF8 0%, #A78BFA 100%);
        transform: translateY(-2px);
    }
    
    .risk-yes {
        color: #EF4444;
        font-size: 1.8em;
        font-weight: bold;
    }
    
    .risk-no {
        color: #10B981;
        font-size: 1.8em;
        font-weight: bold;
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
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 15px 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 10px;
        text-align: center;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .kpi-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin: 10px 0;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
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

# Initialize session state variables
if 'sentiment' not in st.session_state:
    st.session_state.sentiment = None
if 'is_risk' not in st.session_state:
    st.session_state.is_risk = None
if 'strategy' not in st.session_state:
    st.session_state.strategy = None

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

# Simple mitigation strategist
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
        if any(word in text_lower for word in ['sue', 'legal', 'lawyer', 'court']):
            strategies.append("⚖️ **Legal Consultation**: Engage legal team before making any detailed public statements")
            
        if any(word in text_lower for word in ['refund', 'money', 'price', 'cost']):
            strategies.append("💰 **Compensation Review**: Evaluate refund policy and consider appropriate compensation")
            
        if any(word in text_lower for word in ['boycott', 'never again', 'stop using']):
            strategies.append("📈 **Loyalty Program**: Consider implementing a special loyalty offer for affected customers")
            
        return "\n\n".join(strategies)

# Initialize analyzers
sentiment_analyzer = SentimentAnalyzer()
mitigation_strategist = MitigationStrategist()

def show_executive_dashboard(brand_name):
    st.markdown(f'<div class="premium-header">Executive Intelligence Dashboard</div>', unsafe_allow_html=True)
    
    # Real-time status indicator
    st.markdown(f'<div class="accent-text">Real-time monitoring active | Brand: {brand_name}</div>', unsafe_allow_html=True)
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
        response_status = "🟢 On Target" if avg_response_time < 6 else "🟡 Needs Improvement" if avg_response_time < 12 else "🔴 Critical"
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Avg. Response Time (hrs)</div>
            <div class="kpi-value">{avg_response_time:.1f}</div>
            <div>{response_status}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        risk_level = "High" if total_threats > 80 or avg_sentiment < 0.4 else "Medium" if total_threats > 50 or avg_sentiment < 0.6 else "Low"
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
        dates = [(datetime.now() - timedelta(days=i)).strftime('%m-%d') for i in range(30, 0, -1)]
        sentiment_scores = [random.uniform(0.3, 0.9) for _ in range(30)]
        
        # Create DataFrame for chart
        sentiment_data = pd.DataFrame({
            'Date': dates,
            'Sentiment Score': sentiment_scores
        })
        st.line_chart(sentiment_data, x='Date', y='Sentiment Score', height=300)
    
    with col_chart2:
        st.markdown("#### Engagement Metrics")
        platforms = ['Twitter', 'Facebook', 'Instagram', 'Reddit', 'YouTube']
        engagement_values = [random.randint(1000, 10000) for _ in range(5)]
        
        # Create DataFrame for chart
        engagement_data = pd.DataFrame({
            'Platform': platforms,
            'Engagement': engagement_values
        })
        st.bar_chart(engagement_data, x='Platform', y='Engagement', height=300)

def show_threat_analyzer(brand_name):
    st.header("🔍 Threat Analyzer")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🧪 Threat Simulator")
        st.markdown('<div style="padding: 20px; margin-bottom: 20px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);">', unsafe_allow_html=True)
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
        
        if st.session_state.sentiment is not None:
            # Results Card
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
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

def show_competitive_intelligence(brand_name):
    st.header("🥊 Competitive Intelligence")
    
    # Simulate competitive analysis
    competitors = ['Adidas', 'Puma', 'Reebok', 'Under Armour', 'New Balance']
    sentiment_comparison = {brand_name: random.uniform(0.6, 0.8)}
    for competitor in competitors:
        sentiment_comparison[competitor] = random.uniform(0.3, 0.7)
    
    # Simulate share of voice analysis
    total_mentions = random.randint(5000, 15000)
    brand_mentions = random.randint(1500, 4000)
    competitors_mentions = {}
    for competitor in competitors:
        competitors_mentions[competitor] = random.randint(500, 2500)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Sentiment Comparison")
        # Create DataFrame for chart
        comparison_data = pd.DataFrame({
            'Brand': list(sentiment_comparison.keys()),
            'Sentiment Score': list(sentiment_comparison.values())
        })
        st.bar_chart(comparison_data, x='Brand', y='Sentiment Score', height=350)
    
    with col2:
        st.markdown("#### 📢 Market Share of Voice")
        
        # Create metrics for market share
        market_share = (brand_mentions / total_mentions) * 100
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{brand_name} Market Share</div>
            <div class="kpi-value">{market_share:.1f}%</div>
            <div>of total industry mentions</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Competitor analysis
        st.markdown("##### Competitor Analysis")
        for competitor, mentions in competitors_mentions.items():
            share = (mentions / total_mentions) * 100
            st.progress(share/100, text=f"{competitor}: {share:.1f}%")

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
    
    # Calculate overall brand health score
    metrics = {
        'sentiment': 0.3,
        'engagement': 0.2,
        'reach': 0.15,
        'consistency': 0.15,
        'response_time': 0.1,
        'share_of_voice': 0.1
    }
    
    total_score = 0
    for metric, weight in metrics.items():
        if metric in brand_data:
            total_score += brand_data[metric] * weight
    
    # Convert to 0-100 scale
    health_score = total_score * 100
    
    if health_score >= 80:
        status = "Excellent"
        icon = "🌟"
    elif health_score >= 60:
        status = "Good"
        icon = "👍"
    elif health_score >= 40:
        status = "Fair"
        icon = "⚠️"
    else:
        status = "Poor"
        icon = "🔴"
    
    # Overall health score
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-label">Overall Brand Health Score</div>
            <div class="kpi-value">{icon} {health_score:.1f}/100</div>
            <div>Status: {status}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Health trend
        st.markdown("##### Health Trend (30 Days)")
        dates = [(datetime.now() - timedelta(days=i)).strftime('%m-%d') for i in range(30, 0, -1)]
        trend_data = [random.uniform(health_score - 15, health_score + 5) for _ in range(30)]
        
        # Create DataFrame for chart
        trend_chart_data = pd.DataFrame({
            'Date': dates,
            'Health Score': trend_data
        })
        st.line_chart(trend_chart_data, x='Date', y='Health Score', height=200)
    
    with col2:
        st.markdown("##### Component Scores")
        for metric, value in brand_data.items():
            st.progress(value, text=f"{metric.capitalize()}: {value:.0%}")

def main():
    # Premium Header
    st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 4rem;">🛡️</div>
        <h1 class="premium-header">BrandGuardian AI</h1>
        <div style="text-align: center; margin-bottom: 20px;" class="accent-text">Enterprise Digital Risk Protection Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Brand selection
    brand_name = st.sidebar.text_input("Brand Name", "Nike")
    
    # Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Executive Dashboard", 
        "🔍 Threat Analyzer", 
        "🥊 Competitive Intel",
        "❤️ Brand Health"
    ])
    
    with tab1:
        show_executive_dashboard(brand_name)
    
    with tab2:
        show_threat_analyzer(brand_name)
    
    with tab3:
        show_competitive_intelligence(brand_name)
    
    with tab4:
        show_brand_health(brand_name)

    # Footer
    st.markdown("---")
    st.markdown('<div style="text-align: center; padding: 20px;" class="accent-text">', unsafe_allow_html=True)
    st.markdown("**🛡️ Protecting Brands in the Digital Age**")
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
