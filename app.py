import subprocess
import sys
import requests
import streamlit as st
from typing import List, Dict
import time
import random
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
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #FFB700 0%, #FF9800 100%);
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.6);
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
        margin-bottom: 20px;
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .metric-card {
        background: rgba(42, 42, 42, 0.9);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #FFD700;
        margin: 10px 0;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.2);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.25);
    }
    
    .feature-card {
        background: rgba(42, 42, 42, 0.8);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #FFD700;
        margin: 8px;
        text-align: center;
        transition: all 0.3s ease;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.15);
    }
    
    .glowing-border {
        border: 2px solid #FFD700;
        border-radius: 12px;
        animation: glow 2s infinite alternate;
        box-shadow: 0 0 5px #FFD700;
        padding: 15px;
        margin: 10px 0;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 5px #FFD700; }
        to { box-shadow: 0 0 15px #FFD700, 0 0 25px #FFB700; }
    }
    
    .floating { 
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }
    
    .slideshow-container {
        position: relative;
        max-width: 100%;
        margin: 30px 0;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.25);
    }
    
    .slide {
        display: none;
        padding: 30px;
        text-align: center;
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(42, 42, 42, 0.9) 100%);
        border: 2px solid #FFD700;
        border-radius: 15px;
    }
    
    .slide-active {
        display: block;
        animation: fadeIn 1.2s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-number {
        color: #FFD700;
        font-size: 1.1em;
        font-weight: bold;
        margin-bottom: 12px;
    }
    
    .slide-title {
        font-size: 1.8em;
        font-family: 'Playfair Display', serif;
        background: linear-gradient(135deg, #FFD700 0%, #FFB700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }
    
    .slide-content {
        font-size: 1.1em;
        line-height: 1.5;
        color: #FFFFFF;
        margin-bottom: 20px;
    }
    
    .section-header {
        font-family: 'Playfair Display', serif;
        background: linear-gradient(135deg, #FFD700 0%, #FFB700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2em;
        text-align: center;
        margin: 30px 0 20px 0;
    }
    
    .professional-subheader {
        font-size: 1.2em;
        color: #FFD700;
        text-align: center;
        margin-bottom: 30px;
        font-weight: 300;
    }
    
    .nav-button {
        background: linear-gradient(135deg, #FFD700 0%, #FFB700 100%);
        color: #000000 !important;
        padding: 12px 25px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 8px;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        font-size: 14px;
    }
    
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
    }
    
    .center-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        margin: 20px 0;
    }
    
    /* Responsive adjustments */
    @media (max-width: 1200px) {
        .premium-header {
            font-size: 2.8em;
        }
        .slide-title {
            font-size: 1.6em;
        }
    }
    
    @media (max-width: 768px) {
        .premium-header {
            font-size: 2.2em;
            margin-bottom: 15px;
        }
        .professional-subheader {
            font-size: 1.1em;
            margin-bottom: 20px;
        }
        .slide {
            padding: 20px;
        }
        .slide-title {
            font-size: 1.4em;
        }
        .slide-content {
            font-size: 1em;
        }
        .section-header {
            font-size: 1.6em;
        }
        .metric-card {
            padding: 15px;
            margin: 8px 0;
        }
    }
    
    @media (max-width: 480px) {
        .premium-header {
            font-size: 1.8em;
        }
        .professional-subheader {
            font-size: 1em;
        }
        .slide-title {
            font-size: 1.2em;
        }
        .nav-button {
            padding: 10px 20px;
            font-size: 12px;
        }
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

def create_slideshow():
    slideshow_html = """
    <div class="slideshow-container">
        <div class="slide slide-active">
            <div class="slide-number">01/04</div>
            <div class="slide-title">Enterprise Brand Protection</div>
            <div class="slide-content">Advanced AI-powered monitoring system designed to safeguard your brand's reputation across digital platforms. Proactively identify and mitigate potential PR crises before they escalate.</div>
        </div>
    </div>
    <script>
        const slides = [
            {
                number: "01/04",
                title: "Enterprise Brand Protection",
                content: "Advanced AI-powered monitoring system designed to safeguard your brand's reputation across digital platforms. Proactively identify and mitigate potential PR crises before they escalate."
            },
            {
                number: "02/04",
                title: "Real-Time Threat Detection",
                content: "Our sophisticated algorithms analyze sentiment, context, and emerging patterns to detect brand risks in real-time, providing instant alerts for immediate action."
            },
            {
                number: "03/04",
                title: "Intelligent Crisis Management",
                content: "Receive AI-generated mitigation strategies crafted by simulated PR experts. Transform potential disasters into opportunities for demonstrating exceptional customer care."
            },
            {
                number: "04/04",
                title: "Comprehensive Risk Analytics",
                content: "Gain deep insights into brand sentiment trends, threat patterns, and reputation metrics with our comprehensive dashboard and reporting system."
            }
        ];
        
        let currentSlide = 0;
        
        function showSlide(n) {
            const slide = document.querySelector('.slide');
            slide.innerHTML = `
                <div class="slide-number">${slides[n].number}</div>
                <div class="slide-title">${slides[n].title}</div>
                <div class="slide-content">${slides[n].content}</div>
            `;
            slide.classList.remove('slide-active');
            void slide.offsetWidth;
            slide.classList.add('slide-active');
        }
        
        function nextSlide() {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        }
        
        // Change slide every 5 seconds
        setInterval(nextSlide, 5000);
    </script>
    """
    return slideshow_html

def intro_page():
    # Premium Header with Animation
    st.markdown('<div class="premium-header floating">🛡️ BrandGuardian AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="professional-subheader">Enterprise-Grade Digital Reputation Management Platform</div>', unsafe_allow_html=True)
    
    # Interactive Slideshow
    st.markdown(create_slideshow(), unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="metric-card">
        <h3 style='color: #FFD700; text-align: center;'>Welcome to BrandGuardian AI</h3>
        <p style='text-align: center; font-size: 1.1em;'>
        Our cutting-edge artificial intelligence platform provides comprehensive brand protection through 
        advanced sentiment analysis, real-time threat detection, and intelligent crisis management solutions. 
        Trusted by leading enterprises to safeguard their most valuable asset - their reputation.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown('<div class="section-header">Platform Capabilities</div>', unsafe_allow_html=True)
    
    features_col1, features_col2, features_col3, features_col4 = st.columns(4)
    
    with features_col1:
        st.markdown('<div class="feature-card floating">', unsafe_allow_html=True)
        st.markdown("**Real-time Monitoring**")
        st.markdown("Continuous digital surveillance")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with features_col2:
        st.markdown('<div class="feature-card floating" style="animation-delay: 0.5s;">', unsafe_allow_html=True)
        st.markdown("**AI Risk Assessment**")
        st.markdown("Advanced sentiment analysis")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with features_col3:
        st.markdown('<div class="feature-card floating" style="animation-delay: 1s;">', unsafe_allow_html=True)
        st.markdown("**Crisis Management**")
        st.markdown("Strategic mitigation protocols")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with features_col4:
        st.markdown('<div class="feature-card floating" style="animation-delay: 1.5s;">', unsafe_allow_html=True)
        st.markdown("**Analytics Dashboard**")
        st.markdown("Comprehensive insights")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation Button
    st.markdown("""
    <div class="center-container">
        <button class="nav-button" onclick="window.location.href='./?page=main'">
            🚀 Launch Threat Analysis Dashboard
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px;" class="gold-text">
        <h4>BrandGuardian AI Enterprise Solutions</h4>
        <p>Protecting brand integrity through advanced artificial intelligence</p>
        <p>© 2024 BrandGuardian AI. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

def main_page():
    # Premium Header with Animation
    st.markdown('<div class="premium-header floating">🛡️ Threat Analysis Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="professional-subheader">Real-Time Brand Protection Monitoring System</div>', unsafe_allow_html=True)
    
    # Navigation Button
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <button class="nav-button" onclick="window.location.href='./'">
            📋 Return to Overview
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Content Columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Configuration Panel")
        st.markdown('<div class="glowing-border">', unsafe_allow_html=True)
        brand_name = st.text_input("**Brand Identifier**", "Nike", help="Enter the brand you want to monitor")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### Threat Simulation Interface")
        st.markdown('<div class="glowing-border">', unsafe_allow_html=True)
        test_text = st.text_area("**Content Analysis Input**", 
                               "I absolutely hate this company! Their service is terrible and I will sue them!",
                               height=120)
        
        if st.button("**Initiate Sentiment Analysis**", use_container_width=True):
            with st.spinner("🛡️ Conducting comprehensive threat assessment..."):
                time.sleep(1.2)
                analyzer = SentimentAnalyzer()
                strategist = MitigationStrategist()
                
                sentiment = analyzer.analyze_sentiment(test_text)
                is_risk = analyzer.is_high_risk(test_text, sentiment)
                
                st.session_state.sentiment = sentiment
                st.session_state.is_risk = is_risk
                st.session_state.strategy = strategist.generate_response_strategy(test_text, brand_name) if is_risk else None
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### Live Analysis Results")
        
        if 'sentiment' in st.session_state:
            st.markdown('<div class="metric-card floating">', unsafe_allow_html=True)
            st.markdown(f"**Sentiment Score:** `{st.session_state.sentiment:.2f}`")
            
            risk_html = f'<span class="risk-yes">🚨 CRITICAL THREAT DETECTED</span>' if st.session_state.is_risk else f'<span class="risk-no">✅ SYSTEM SECURE</span>'
            st.markdown(f"**Risk Assessment:** {risk_html}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.session_state.is_risk and st.session_state.strategy:
                st.markdown("### Crisis Mitigation Protocol")
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown(st.session_state.strategy)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("### Immediate Action Required")
                action_col1, action_col2, action_col3 = st.columns(3)
                with action_col1:
                    st.button("**Issue Alert**", use_container_width=True)
                with action_col2:
                    st.button("**Team Notification**", use_container_width=True)
                with action_col3:
                    st.button("**Generate Report**", use_container_width=True)
        else:
            st.markdown("""
            <div class="metric-card">
                <h4 style='color: #FFD700; text-align: center;'>Ready for Analysis</h4>
                <p style='text-align: center;'>
                Configure your brand and input text to begin threat assessment. 
                The system will provide real-time sentiment analysis and crisis mitigation strategies.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px;" class="gold-text">
        <h4>BrandGuardian AI Threat Analysis System</h4>
        <p>Advanced AI-powered brand protection and crisis management</p>
        <p>© 2024 BrandGuardian AI. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Check which page to show - FIXED: Using st.query_params instead of experimental_get_query_params
    query_params = st.query_params
    page = query_params.get("page", ["intro"])[0]
    
    if page == "main":
        main_page()
    else:
        intro_page()

if __name__ == "__main__":
    main()
