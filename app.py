import subprocess
import sys
import requests
import streamlit as st
from typing import List, Dict
import time
from streamlit.components.v1 import html
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Install required libraries and setup
def install_and_setup():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "textblob", "openai", "requests", "plotly", "pandas", "numpy"])
        import nltk
        nltk.download('punkt')
        nltk.download('brown')
    except Exception as e:
        st.error(f"Setup error: {e}")

install_and_setup()

from textblob import TextBlob
from openai import OpenAI

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

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Generate sample data for executive dashboard
def generate_sample_data():
    # Generate dates for the last 30 days
    dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
    
    # Generate sample sentiment data
    sentiment_scores = np.random.uniform(-0.8, 0.9, 30)
    
    # Generate sample threat counts
    threat_counts = np.random.poisson(3, 30)
    
    # Generate platform distribution
    platforms = ['Twitter', 'Facebook', 'Instagram', 'Reddit', 'News Sites', 'Review Sites']
    platform_distribution = {platform: np.random.randint(5, 30) for platform in platforms}
    
    # Generate topic distribution
    topics = ['Customer Service', 'Product Quality', 'Shipping', 'Pricing', 'Company Ethics', 'Website Experience']
    topic_distribution = {topic: np.random.randint(5, 25) for topic in topics}
    
    # Generate response time data
    response_times = np.random.uniform(1.5, 18.0, 30)
    
    return {
        'dates': dates,
        'sentiment_scores': sentiment_scores,
        'threat_counts': threat_counts,
        'platform_distribution': platform_distribution,
        'topic_distribution': topic_distribution,
        'response_times': response_times
    }

class SentimentAnalyzer:
    def analyze_sentiment(self, text: str) -> float:
        try:
            analysis = TextBlob(text)
            return analysis.sentiment.polarity
        except:
            return 0.0

    def is_high_risk(self, text: str, sentiment_score: float) -> bool:
        if sentiment_score > -0.3:
            return False
        if len(text) < 10:
            return False
        negative_keywords = ['hate', 'terrible', 'awful', 'sue', 'legal', 'boycott', 'scam', 'fraud', 'worst', 'never again', 'refund']
        return any(keyword in text.lower() for keyword in negative_keywords) or sentiment_score < -0.6

class MitigationStrategist:
    def generate_response_strategy(self, risky_text: str, brand_name: str) -> str:
        try:
            prompt = f"""
            Brand: {brand_name}
            Negative Post: "{risky_text}"
            
            As a PR crisis expert, provide 3-5 immediate, actionable steps to address this situation.
            Focus on: public response, customer service, and reputation management.
            Be specific and professional.
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an experienced PR crisis management specialist."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"""⚠️ AI strategy generation failed. Immediate steps:
            1. Acknowledge the concern publicly within 1 hour
            2. Offer direct message resolution
            3. Prepare official statement addressing: {risky_text[:100]}..."""

def show_executive_dashboard():
    st.markdown('<div class="dashboard-header">Executive Intelligence Dashboard</div>', unsafe_allow_html=True)
    
    # Generate sample data
    data = generate_sample_data()
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_sentiment = np.mean(data['sentiment_scores'])
        sentiment_trend = "📈 Improving" if avg_sentiment > 0.1 else "📉 Declining" if avg_sentiment < -0.1 else "➡️ Stable"
        sentiment_color = "positive-kpi" if avg_sentiment > 0.1 else "negative-kpi" if avg_sentiment < -0.1 else "neutral-kpi"
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Avg. Sentiment Score</div>
            <div class="kpi-value {sentiment_color}">{avg_sentiment:.2f}</div>
            <div>{sentiment_trend}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        total_threats = np.sum(data['threat_counts'])
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Threats Detected (30 days)</div>
            <div class="kpi-value">{total_threats}</div>
            <div>{"🔴 High Alert" if total_threats > 80 else "🟡 Moderate" if total_threats > 50 else "🟢 Normal"}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        avg_response_time = np.mean(data['response_times'])
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Avg. Response Time (hrs)</div>
            <div class="kpi-value">{avg_response_time:.1f}</div>
            <div>{"🟢 On Target" if avg_response_time < 6 else "🟡 Needs Improvement" if avg_response_time < 12 else "🔴 Critical"}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        risk_level = "High" if total_threats > 80 or avg_sentiment < -0.2 else "Medium" if total_threats > 50 or avg_sentiment < 0 else "Low"
        risk_color = "negative-kpi" if risk_level == "High" else "neutral-kpi" if risk_level == "Medium" else "positive-kpi"
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Overall Risk Level</div>
            <div class="kpi-value {risk_color}">{risk_level}</div>
            <div>{"⚠️ Immediate Action" if risk_level == "High" else "📋 Review Needed" if risk_level == "Medium" else "✅ All Clear"}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Sentiment Trend Chart
    st.markdown("#### Sentiment Trend (30 Days)")
    sentiment_df = pd.DataFrame({
        'Date': data['dates'],
        'Sentiment Score': data['sentiment_scores'],
        '7-Day Avg': pd.Series(data['sentiment_scores']).rolling(window=7).mean()
    })
    
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    fig.add_trace(go.Scatter(x=sentiment_df['Date'], y=sentiment_df['Sentiment Score'], 
                            name='Daily Sentiment', line=dict(color='#8B5CF6', width=2)))
    fig.add_trace(go.Scatter(x=sentiment_df['Date'], y=sentiment_df['7-Day Avg'], 
                            name='7-Day Average', line=dict(color='#10B981', width=3)))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#D1D5DB',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Platform and Topic Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Threats by Platform")
        platform_df = pd.DataFrame({
            'Platform': list(data['platform_distribution'].keys()),
            'Count': list(data['platform_distribution'].values())
        })
        
        fig = px.pie(platform_df, values='Count', names='Platform', 
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#D1D5DB',
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Threats by Topic")
        topic_df = pd.DataFrame({
            'Topic': list(data['topic_distribution'].keys()),
            'Count': list(data['topic_distribution'].values())
        })
        
        fig = px.bar(topic_df, x='Count', y='Topic', orientation='h',
                     color='Count', color_continuous_scale='Viridis')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#D1D5DB',
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Threat Timeline
    st.markdown("#### Daily Threat Count")
    threat_df = pd.DataFrame({
        'Date': data['dates'],
        'Threats': data['threat_counts']
    })
    
    fig = px.bar(threat_df, x='Date', y='Threats', 
                 color='Threats', color_continuous_scale='reds')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#D1D5DB',
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Response Time Analysis
    st.markdown("#### Response Time Performance")
    response_df = pd.DataFrame({
        'Date': data['dates'],
        'Response Time (hours)': data['response_times']
    })
    
    fig = px.line(response_df, x='Date', y='Response Time (hours)',
                  markers=True, line_shape='spline')
    fig.add_hline(y=6, line_dash="dash", line_color="green", annotation_text="Target")
    fig.add_hline(y=12, line_dash="dash", line_color="orange", annotation_text="Warning")
    fig.add_hline(y=18, line_dash="dash", line_color="red", annotation_text="Critical")
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#D1D5DB',
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    # Initialize session state
    if "show_intro" not in st.session_state:
        st.session_state.show_intro = True
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "Dashboard"
    
    # Premium Header with Animation
    st.markdown("""
    <div class="logo-container">
        <div class="logo">🛡️</div>
    </div>
    <h1 class="premium-header floating">BrandGuardian AI</h1>
    <div style="text-align: center; margin-bottom: 20px;" class="accent-text">Enterprise Digital Risk Protection Platform</div>
    """, unsafe_allow_html=True)
    
    # Navigation Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Executive Dashboard", "🔍 Threat Analyzer", "ℹ️ About"])
    
    with tab1:
        show_executive_dashboard()
    
    with tab2:
        # Toggle for intro panel
        if st.button("📋 About BrandGuardian AI", key="toggle_intro"):
            st.session_state.show_intro = not st.session_state.show_intro
            st.rerun()
        
        # Intro panel (collapsible)
        if st.session_state.show_intro:
            with st.container():
                st.markdown("""
                <div class="intro-panel tech-pattern">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <h2 style="color: #E5E7EB;">Welcome to BrandGuardian AI</h2>
                        <p style="color: #D1D5DB;">Your comprehensive solution for digital brand protection</p>
                    </div>
                    
                    <div style="color: #D1D5DB; line-height: 1.6; margin-bottom: 25px;">
                        BrandGuardian AI is a comprehensive brand protection solution that leverages advanced artificial intelligence 
                        to monitor, detect, and mitigate digital threats to your brand reputation in real-time. Our platform combines 
                        sophisticated sentiment analysis with crisis management expertise to safeguard your brand across all digital channels.
                    </div>
                    
                    <div class="intro-feature">
                        <h3 style="color: #E5E7EB;">🔍 Real-time Digital Monitoring</h3>
                        <p style="color: #D1D5DB;">24/7 surveillance across social media, review sites, forums, and news outlets to identify potential threats as they emerge</p>
                    </div>
                    
                    <div class="intro-feature">
                        <h3 style="color: #E5E7EB;">⚠️ AI-Powered Threat Detection</h3>
                        <p style="color: #D1D5DB;">Advanced natural language processing to identify emerging brand risks before they escalate into full-blown crises</p>
                    </div>
                    
                    <div class="intro-feature">
                        <h3 style="color: #E5E7EB;">🛡️ Proactive Crisis Mitigation</h3>
                        <p style="color: #D1D5DB;">Immediate, actionable strategies developed by AI trained on PR crisis management protocols from industry experts</p>
                    </div>
                    
                    <div class="intro-feature">
                        <h3 style="color: #E5E7EB;">📊 Executive Intelligence Dashboard</h3>
                        <p style="color: #D1D5DB;">Comprehensive analytics and insights for data-driven brand protection decisions with detailed reporting capabilities</p>
                    </div>
                    
                    <div style="color: #D1D5DB; line-height: 1.6; margin-top: 25px;">
                        <strong>Key Benefits:</strong><br>
                        • Reduce response time to brand threats by up to 85%<br>
                        • Prevent potential revenue loss from reputation damage<br>
                        • Gain actionable insights from comprehensive sentiment analysis<br>
                        • Maintain brand consistency and trust across all channels
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Main Content Columns
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### ⚙️ Configuration Panel")
            st.markdown('<div class="glowing-border cyber-border" style="padding: 20px; margin-bottom: 20px;">', unsafe_allow_html=True)
            brand_name = st.text_input("**🏷️ Brand Name**", "Nike", help="Enter the brand you want to monitor")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("### 🧪 Threat Simulator")
            st.markdown('<div class="glowing-border cyber-border" style="padding: 20px;">', unsafe_allow_html=True)
            test_text = st.text_area("**🔍 Enter text to analyze:**", 
                                   "I absolutely hate this company! Their service is terrible and I will sue them!",
                                   height=150)
            
            if st.button("🚀 Analyze Sentiment", use_container_width=True, key="analyze_btn"):
                with st.spinner("🛡️ Scanning for threats..."):
                    time.sleep(1.5)  # Dramatic pause for effect
                    analyzer = SentimentAnalyzer()
                    strategist = MitigationStrategist()
                    
                    sentiment = analyzer.analyze_sentiment(test_text)
                    is_risk = analyzer.is_high_risk(test_text, sentiment)
                    
                    st.session_state.sentiment = sentiment
                    st.session_state.is_risk = is_risk
                    st.session_state.strategy = strategist.generate_response_strategy(test_text, brand_name) if is_risk else None
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("### 📊 Live Threat Analysis")
            
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

        # Features Section with Animated Cards
        st.markdown("---")
        st.markdown("### ✨ Platform Capabilities")
        
        features_col1, features_col2, features_col3, features_col4 = st.columns(4)
        
        with features_col1:
            st.markdown('<div class="feature-card floating">', unsafe_allow_html=True)
            st.markdown("**🔍 Real-time Monitoring**")
            st.markdown("24/7 digital surveillance")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with features_col2:
            st.markdown('<div class="feature-card floating" style="animation-delay: 0.5s;">', unsafe_allow_html=True)
            st.markdown("**⚠️ AI Risk Detection**")
            st.markdown("Advanced sentiment analysis")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with features_col3:
            st.markdown('<div class="feature-card floating" style="animation-delay: 1s;">', unsafe_allow_html=True)
            st.markdown("**🛡️ Crisis Prevention**")
            st.markdown("Instant mitigation strategies")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with features_col4:
            st.markdown('<div class="feature-card floating" style="animation-delay: 1.5s;">', unsafe_allow_html=True)
            st.markdown("**📊 Executive Reports**")
            st.markdown("Professional insights")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="intro-panel">
            <h2 style="color: #E5E7EB;">About BrandGuardian AI</h2>
            
            <div style="color: #D1D5DB; line-height: 1.6; margin-bottom: 20px;">
                BrandGuardian AI is an enterprise-grade digital risk protection platform that combines advanced AI algorithms 
                with comprehensive monitoring capabilities to safeguard your brand's online reputation.
            </div>
            
            <h3 style="color: #E5E7EB;">How It Works</h3>
            <div style="color: #D1D5DB; line-height: 1.6; margin-bottom: 20px;">
                1. <strong>Continuous Monitoring:</strong> Our system scans social media, review sites, forums, and news outlets 24/7<br>
                2. <strong>AI-Powered Analysis:</strong> Advanced NLP algorithms detect sentiment and identify potential threats<br>
                3. <strong>Real-Time Alerts:</strong> Instant notifications when critical threats are detected<br>
                4. <strong>Actionable Insights:</strong> AI-generated strategies to mitigate reputation damage<br>
                5. <strong>Executive Reporting:</strong> Comprehensive dashboards with key metrics and trends
            </div>
            
            <h3 style="color: #E5E7EB;">Technology Stack</h3>
            <div style="color: #D1D5DB; line-height: 1.6;">
                • Natural Language Processing (TextBlob, OpenAI GPT-3.5)<br>
                • Real-time Data Processing<br>
                • Machine Learning Algorithms<br>
                • Cloud-Based Infrastructure<br>
                • Enterprise-Grade Security
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown('<div style="text-align: center; padding: 20px;" class="accent-text">', unsafe_allow_html=True)
    st.markdown("**🛡️ Protecting Brands in the Digital Age**")
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
