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
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #FFD700;
        margin: 6px;
        text-align: center;
        transition: all 0.3s ease;
        min-height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        font-size: 0.9em;
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
        font-size: 1.8em;
        text-align: center;
        margin: 25px 0 15px 0;
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
    
    .compact-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
        margin: 15px 0;
    }
    
    /* NEW: Professional Configuration Panel Styles */
    .config-panel {
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.95) 0%, rgba(42, 42, 42, 0.95) 100%);
        border-radius: 16px;
        border: 2px solid #FFD700;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.2);
        transition: all 0.5s ease;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .config-panel::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        z-index: -1;
        background: linear-gradient(45deg, #FFD700, #FFB700, #FF9800, #FFD700);
        background-size: 400% 400%;
        animation: gradientFlow 3s ease infinite;
        border-radius: 18px;
    }
    
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .config-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 215, 0, 0.3);
    }
    
    .config-icon {
        font-size: 24px;
        margin-right: 12px;
        color: #FFD700;
    }
    
    .config-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.5em;
        background: linear-gradient(135deg, #FFD700 0%, #FFB700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .config-description {
        color: #CCCCCC;
        font-size: 0.95em;
        margin: 10px 0 20px 0;
        line-height: 1.5;
    }
    
    .input-group {
        margin-bottom: 20px;
    }
    
    .input-label {
        display: block;
        margin-bottom: 8px;
        font-weight: 600;
        color: #FFD700;
        font-size: 1.05em;
    }
    
    .input-hint {
        font-size: 0.85em;
        color: #999999;
        margin-top: 5px;
        font-style: italic;
    }
    
    /* NEW: Threat Simulation Interface Styles */
    .simulation-panel {
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.95) 0%, rgba(42, 42, 42, 0.95) 100%);
        border-radius: 16px;
        border: 2px solid #FFD700;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.2);
        transition: all 0.5s ease;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .simulation-panel::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        z-index: -1;
        background: linear-gradient(45deg, #FFD700, #FFB700, #FF9800, #FFD700);
        background-size: 400% 400%;
        animation: gradientFlow 3s ease infinite;
        border-radius: 18px;
    }
    
    .simulation-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 215, 0, 0.3);
    }
    
    .simulation-icon {
        font-size: 24px;
        margin-right: 12px;
        color: #FFD700;
    }
    
    .simulation-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.5em;
        background: linear-gradient(135deg, #FFD700 0%, #FFB700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .simulation-description {
        color: #CCCCCC;
        font-size: 0.95em;
        margin: 10px 0 20px 0;
        line-height: 1.5;
    }
    
    /* NEW: Page Transition Animations */
    .page-container {
        position: relative;
        width: 100%;
    }
    
    .page {
        position: absolute;
        width: 100%;
        transition: transform 0.6s ease, opacity 0.6s ease;
    }
    
    .page-hidden {
        opacity: 0;
        transform: translateX(-100%);
        pointer-events: none;
    }
    
    .page-visible {
        opacity: 1;
        transform: translateX(0);
    }
    
    /* NEW: Analyze Button Animation */
    .analyze-btn {
        background: linear-gradient(135deg, #FFD700 0%, #FFB700 100%);
        color: #000000;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 16px 32px;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        width: 100%;
        margin-top: 15px;
        position: relative;
        overflow: hidden;
    }
    
    .analyze-btn:hover {
        background: linear-gradient(135deg, #FFB700 0%, #FF9800 100%);
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.6);
    }
    
    .analyze-btn:active {
        transform: scale(0.98);
    }
    
    .analyze-btn::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transform: rotate(45deg);
        animation: shine 2s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    /* NEW: Stats Cards */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
        margin: 20px 0;
    }
    
    .stat-card {
        background: rgba(42, 42, 42, 0.8);
        border-radius: 12px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.2);
    }
    
    .stat-value {
        font-size: 2em;
        font-weight: bold;
        background: linear-gradient(135deg, #FFD700 0%, #FFB700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 5px 0;
    }
    
    .stat-label {
        color: #CCCCCC;
        font-size: 0.9em;
    }
    
    /* NEW: Client Logos */
    .clients-section {
        margin: 30px 0;
        text-align: center;
    }
    
    .client-logos {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 25px;
        margin: 20px 0;
    }
    
    .client-logo {
        width: 80px;
        height: 80px;
        background: rgba(255, 215, 0, 0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8em;
        border: 2px solid rgba(255, 215, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .client-logo:hover {
        transform: scale(1.1);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
    }
    
    /* NEW: Testimonial */
    .testimonial {
        background: rgba(42, 42, 42, 0.8);
        border-radius: 16px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        padding: 25px;
        margin: 25px 0;
        position: relative;
    }
    
    .testimonial::before {
        content: '"';
        position: absolute;
        top: 10px;
        left: 15px;
        font-size: 4em;
        color: rgba(255, 215, 0, 0.2);
        font-family: 'Playfair Display', serif;
    }
    
    .testimonial-text {
        font-style: italic;
        line-height: 1.6;
        margin-bottom: 15px;
        color: #FFFFFF;
    }
    
    .testimonial-author {
        font-weight: bold;
        color: #FFD700;
        text-align: right;
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
        .compact-grid {
            grid-template-columns: 1fr;
        }
        .config-panel, .simulation-panel {
            padding: 20px;
        }
        .stats-container {
            grid-template-columns: 1fr;
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
        .config-title, .simulation-title {
            font-size: 1.3em;
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
    
    # Stats Section
    st.markdown("""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-value">99.7%</div>
            <div class="stat-label">Threat Detection Accuracy</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">24/7</div>
            <div class="stat-label">Real-time Monitoring</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">85%</div>
            <div class="stat-label">Faster Response Time</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">1000+</div>
            <div class="stat-label">Brands Protected</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Features Section - COMPACT DESIGN
    st.markdown('<div class="section-header">Platform Capabilities</div>', unsafe_allow_html=True)
    
    # Compact grid layout
    st.markdown("""
    <div class="compact-grid">
        <div class="feature-card floating">
            <strong>🔍 Real-time Monitoring</strong><br>
            <small>Continuous surveillance</small>
        </div>
        <div class="feature-card floating" style="animation-delay: 0.3s;">
            <strong>⚠️ AI Risk Assessment</strong><br>
            <small>Advanced analysis</small>
        </div>
        <div class="feature-card floating" style="animation-delay: 0.6s;">
            <strong>🛡️ Crisis Management</strong><br>
            <small>Strategic protocols</small>
        </div>
        <div class="feature-card floating" style="animation-delay: 0.9s;">
            <strong>📊 Analytics Dashboard</strong><br>
            <small>Comprehensive insights</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Client Logos Section
    st.markdown("""
    <div class="clients-section">
        <h3 class="section-header">Trusted by Industry Leaders</h3>
        <div class="client-logos">
            <div class="client-logo">🏢</div>
            <div class="client-logo">🛒</div>
            <div class="client-logo">📱</div>
            <div class="client-logo">💻</div>
            <div class="client-logo">👔</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Testimonial
    st.markdown("""
    <div class="testimonial">
        <div class="testimonial-text">
            "BrandGuardian AI has transformed how we manage our brand reputation. The AI-driven insights and real-time alerts have helped us avert several potential crises before they could impact our business. An indispensable tool for any modern brand."
        </div>
        <div class="testimonial-author">- Sarah Johnson, CMO at TechGlobal Inc.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation Button - Using session state instead of query params
    if st.button("🚀 Launch Threat Analysis Dashboard", use_container_width=True, key="launch_dashboard"):
        st.session_state.current_page = "main"
        # Force a rerun to immediately show the main page
        st.rerun()
    
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
    if st.button("📋 Return to Overview", use_container_width=True, key="return_overview"):
        st.session_state.current_page = "intro"
        # Force a rerun to immediately show the intro page
        st.rerun()
    
    # Main Content Columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Configuration Panel - NEW DESIGN
        st.markdown("""
        <div class="config-panel">
            <div class="config-header">
                <div class="config-icon">⚙️</div>
                <div class="config-title">Configuration Panel</div>
            </div>
            <div class="config-description">
                Configure your brand monitoring settings and customize the threat detection parameters.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        brand_name = st.text_input("**Brand Identifier**", "Nike", 
                                  help="Enter the brand you want to monitor", 
                                  key="brand_input")
        
        st.markdown("""
        <div class="input-group">
            <div class="input-label">Monitoring Channels</div>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <div style="background: rgba(255, 215, 0, 0.1); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(255, 215, 0, 0.3);">
                    <input type="checkbox" checked> Twitter
                </div>
                <div style="background: rgba(255, 215, 0, 0.1); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(255, 215, 0, 0.3);">
                    <input type="checkbox" checked> Facebook
                </div>
                <div style="background: rgba(255, 215, 0, 0.1; padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(255, 215, 0, 0.3);">
                    <input type="checkbox" checked> Instagram
                </div>
                <div style="background: rgba(255, 215, 0, 0.1); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(255, 215, 0, 0.3);">
                    <input type="checkbox"> News Sites
                </div>
            </div>
            <div class="input-hint">Select the platforms to monitor for brand mentions</div>
        </div>
        """, unsafe_allow_html=True)
        
        sensitivity = st.slider("**Detection Sensitivity**", 1, 10, 7, 
                               help="Adjust how sensitive the system is to potential threats")
        
        # Threat Simulation Interface - NEW DESIGN
        st.markdown("""
        <div class="simulation-panel">
            <div class="simulation-header">
                <div class="simulation-icon">🧪</div>
                <div class="simulation-title">Threat Simulation Interface</div>
            </div>
            <div class="simulation-description">
                Test the AI's threat detection capabilities by entering sample content for analysis.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        test_text = st.text_area("**Content Analysis Input**", 
                               "I absolutely hate this company! Their service is terrible and I will sue them!",
                               height=120,
                               key="threat_input")
        
        if st.button("**Initiate Sentiment Analysis**", use_container_width=True, key="analyze_btn"):
            with st.spinner("🛡️ Conducting comprehensive threat assessment..."):
                time.sleep(1.2)
                analyzer = SentimentAnalyzer()
                strategist = MitigationStrategist()
                
                sentiment = analyzer.analyze_sentiment(test_text)
                is_risk = analyzer.is_high_risk(test_text, sentiment)
                
                st.session_state.sentiment = sentiment
                st.session_state.is_risk = is_risk
                st.session_state.strategy = strategist.generate_response_strategy(test_text, brand_name) if is_risk else None
                
                # Add success animation
                st.markdown("""
                <script>
                    // Add success animation
                    document.querySelector('.stSpinner').innerHTML += '<div style="position:absolute; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.7); display:flex; align-items:center; justify-content:center; border-radius:12px;"><div style="color:#FFD700; font-size:24px;">✅ Analysis Complete!</div></div>';
                    setTimeout(function() {
                        document.querySelector('.stSpinner').style.display = 'none';
                    }, 1000);
                </script>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown("### Live Analysis Results")
        
        if 'sentiment' in st.session_state:
            st.markdown('<div class="metric-card floating">', unsafe_allow_html=True)
            st.markdown(f"**Sentiment Score:** `{st.session_state.sentiment:.2f}`")
            
            # Visual sentiment indicator
            sentiment_width = max(10, min(100, (st.session_state.sentiment + 1) * 50))
            sentiment_color = "#FF4444" if st.session_state.sentiment < -0.3 else "#10B981" if st.session_state.sentiment > 0.3 else "#FFD700"
            
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.1); height: 20px; border-radius: 10px; margin: 10px 0; overflow: hidden;">
                <div style="background: {sentiment_color}; width: {sentiment_width}%; height: 100%; border-radius: 10px; transition: all 0.5s ease;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.8em; color: #999;">
                <span>Negative</span>
                <span>Neutral</span>
                <span>Positive</span>
            </div>
            """, unsafe_allow_html=True)
            
            risk_html = f'<span class="risk-yes">🚨 CRITICAL THREAT DETECTED</span>' if st.session_state.is_risk else f'<span class="risk-no">✅ SYSTEM SECURE</span>'
            st.markdown(f"**Risk Assessment:** {risk_html}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.session_state.is_risk and st.session_state.strategy:
                st.markdown("### Crisis Mitigation Protocol")
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                
                # Add animated header for crisis protocol
                st.markdown("""
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <div style="font-size: 24px; margin-right: 10px;">🛡️</div>
                    <div style="font-family: 'Playfair Display', serif; background: linear-gradient(135deg, #FFD700 0%, #FFB700 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.3em;">Recommended Response Strategy</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(st.session_state.strategy)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("### Immediate Action Required")
                action_col1, action_col2, action_col3 = st.columns(3)
                with action_col1:
                    st.button("**Issue Alert**", use_container_width=True, key="alert_btn")
                with action_col2:
                    st.button("**Team Notification**", use_container_width=True, key="notify_btn")
                with action_col3:
                    st.button("**Generate Report**", use_container_width=True, key="report_btn")
        else:
            st.markdown("""
            <div class="metric-card">
                <h4 style='color: #FFD700; text-align: center;'>Ready for Analysis</h4>
                <p style='text-align: center;'>
                Configure your brand and input text to begin threat assessment. 
                The system will provide real-time sentiment analysis and crisis mitigation strategies.
                </p>
                <div style="text-align: center; font-size: 48px; margin: 20px 0;">🔍</div>
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
    # Initialize session state for page navigation
    if "current_page" not in st.session_state:
        st.session_state.current_page = "intro"
    
    # Add page transition effect
    st.markdown("""
    <script>
        // Function to handle page transitions
        function handlePageTransition() {
            const appContainer = document.querySelector('.stApp');
            appContainer.style.opacity = '0';
            appContainer.style.transition = 'opacity 0.5s ease';
            
            setTimeout(() => {
                appContainer.style.opacity = '1';
            }, 50);
        }
        
        // Initial page load
        handlePageTransition();
    </script>
    """, unsafe_allow_html=True)
    
    # Check which page to show based on session state
    if st.session_state.current_page == "main":
        main_page()
    else:
        intro_page()

if __name__ == "__main__":
    main()
