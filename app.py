import subprocess
import sys
import requests
import streamlit as st
from typing import List, Dict
import time
from streamlit.components.v1 import html

# Install required libraries and setup
def install_and_setup():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "textblob", "openai", "requests"])
        import nltk
        nltk.download('punkt')
        nltk.download('brown')
    except Exception as e:
        st.error(f"Setup error: {e}")

install_and_setup()

from textblob import TextBlob
from openai import OpenAI

# Custom CSS for Premium Black & Gold Theme with Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400;600&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0A0A0A 0%, #1A1A1A 50%, #0A0A0A 100%);
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1A1A1A 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1A1A1A 0%, #2D2D2D 100%);
        border-right: 2px solid #FFD700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(42, 42, 42, 0.8);
        color: #FFD700;
        border: 2px solid #FFD700;
        border-radius: 10px;
        padding: 12px;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #FFB700;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
        transform: scale(1.02);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #FFB700 100%);
        color: #000000;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 15px 30px;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        cursor: pointer;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #FFB700 0%, #FF9800 100%);
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.6);
    }
    
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    .risk-yes {
        color: #FF4444;
        font-size: 1.8em;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(255, 68, 68, 0.7);
        animation: pulseRed 2s infinite;
    }
    
    @keyframes pulseRed {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .risk-no {
        color: #00FF00;
        font-size: 1.8em;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
        animation: pulseGreen 3s infinite;
    }
    
    @keyframes pulseGreen {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    
    .gold-text {
        color: #FFD700;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.4);
    }
    
    .premium-header {
        background: linear-gradient(135deg, #FFD700 0%, #FFB700 50%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5em;
        font-family: 'Playfair Display', serif;
        margin-bottom: 30px;
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .metric-card {
        background: rgba(42, 42, 42, 0.9);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #FFD700;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(255, 215, 0, 0.2);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(255, 215, 0, 0.3);
    }
    
    .feature-card {
        background: rgba(42, 42, 42, 0.8);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #FFD700;
        margin: 10px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.2);
    }
    
    .glowing-border {
        border: 2px solid #FFD700;
        border-radius: 15px;
        animation: glow 2s infinite alternate;
        box-shadow: 0 0 5px #FFD700;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 5px #FFD700; }
        to { box-shadow: 0 0 20px #FFD700, 0 0 30px #FFB700; }
    }
    
    .floating { 
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .typewriter {
        overflow: hidden;
        border-right: .15em solid #FFD700;
        white-space: nowrap;
        animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #FFD700; }
    }
    
    /* Fix for button alignment issues */
    .stButton {
        text-align: center;
    }
    
    /* Fix for animation performance */
    .stApp, .premium-header, .floating, .metric-card, .feature-card {
        will-change: transform;
        backface-visibility: hidden;
        perspective: 1000px;
    }
    
    /* Intro page specific styles */
    .intro-container {
        padding: 2rem;
        text-align: center;
    }
    
    .intro-heading {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #FFD700 0%, #FFB700 50%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Playfair Display', serif;
    }
    
    .intro-subheading {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        color: #FFD700;
    }
    
    .intro-feature {
        margin: 1.5rem 0;
        padding: 1.5rem;
        border-radius: 15px;
        background: rgba(42, 42, 42, 0.7);
        border: 1px solid #FFD700;
    }
    
    .start-button {
        margin-top: 2rem;
        padding: 1rem 2rem;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

def show_intro_page():
    st.markdown("""
    <div class="intro-container">
        <h1 class="intro-heading floating">🛡️ BrandGuardian AI</h1>
        <p class="intro-subheading">Enterprise-Grade Brand Protection Suite</p>
        
        <div class="intro-feature floating" style="animation-delay: 0.2s;">
            <h3>🔍 Real-time Monitoring</h3>
            <p>24/7 surveillance of social media and online platforms</p>
        </div>
        
        <div class="intro-feature floating" style="animation-delay: 0.4s;">
            <h3>⚠️ AI-Powered Risk Detection</h3>
            <p>Advanced sentiment analysis to identify potential threats</p>
        </div>
        
        <div class="intro-feature floating" style="animation-delay: 0.6s;">
            <h3>🛡️ Crisis Mitigation</h3>
            <p>Immediate actionable strategies to protect your brand</p>
        </div>
        
        <div class="intro-feature floating" style="animation-delay: 0.8s;">
            <h3>📊 Comprehensive Reporting</h3>
            <p>Detailed analytics and insights for executive decision-making</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Started", use_container_width=True, key="start_btn"):
            st.session_state.page = "main"
            st.rerun()

def main_app():
    # Premium Header with Animation
    st.markdown('<div class="premium-header floating">🛡️ BrandGuardian AI</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; margin-bottom: 40px;" class="gold-text">Enterprise-Grade Brand Protection Suite</div>', unsafe_allow_html=True)
    
    # Main Content Columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ⚙️ Configuration Panel")
        st.markdown('<div class="glowing-border" style="padding: 20px; margin-bottom: 20px;">', unsafe_allow_html=True)
        brand_name = st.text_input("**🏷️ Brand Name**", "Nike", help="Enter the brand you want to monitor")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 🧪 Threat Simulator")
        st.markdown('<div class="glowing-border" style="padding: 20px;">', unsafe_allow_html=True)
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
    st.markdown("### ✨ Premium Features")
    
    features_col1, features_col2, features_col3, features_col4 = st.columns(4)
    
    with features_col1:
        st.markdown('<div class="feature-card floating">', unsafe_allow_html=True)
        st.markdown("**🔍 Real-time Monitoring**")
        st.markdown("24/7 brand surveillance")
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

    # Footer
    st.markdown("---")
    st.markdown('<div style="text-align: center; padding: 20px;" class="gold-text">', unsafe_allow_html=True)
    st.markdown("**🛡️ Protecting Brands Since 2024**")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add a button to go back to intro
    if st.button("🏠 Back to Introduction", use_container_width=True, key="back_btn"):
        st.session_state.page = "intro"
        st.rerun()

def main():
    # Initialize session state for page navigation
    if "page" not in st.session_state:
        st.session_state.page = "intro"
    
    # Show the appropriate page based on session state
    if st.session_state.page == "intro":
        show_intro_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
