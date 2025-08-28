import subprocess
import sys
import requests
import streamlit as st
from typing import List, Dict

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

# Custom CSS for Black & Gold Theme
st.markdown("""
<style>
    .main {
        background-color: #0A0A0A;
        color: #FFD700;
    }
    .stApp {
        background: linear-gradient(135deg, #0A0A0A 0%, #1A1A1A 100%);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1A1A1A 0%, #2D2D2D 100%);
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #2D2D2D;
        color: #FFD700;
        border: 1px solid #FFD700;
    }
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #FFB700 100%);
        color: #000000;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #FFB700 0%, #FF9800 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
    }
    .risk-yes {
        color: #FF4444;
        font-size: 1.5em;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 68, 68, 0.5);
    }
    .risk-no {
        color: #00FF00;
        font-size: 1.5em;
        font-weight: bold;
    }
    .gold-text {
        color: #FFD700;
        font-weight: bold;
    }
    .header {
        background: linear-gradient(135deg, #FFD700 0%, #FFB700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3em;
        margin-bottom: 20px;
    }
    .metric-card {
        background: rgba(42, 42, 42, 0.8);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #FFD700;
        margin: 10px 0;
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

def main():
    st.markdown('<div class="header">🛡️ BrandGuardian AI</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ⚙️ Configuration")
        brand_name = st.text_input("**Brand Name**", "Nike", help="Enter the brand you want to monitor")
        
        st.markdown("---")
        st.markdown("### 🧪 Test Analyzer")
        test_text = st.text_area("**Enter text to analyze:**", 
                               "I absolutely hate this company! Their service is terrible and I will sue them!",
                               height=120)
        
        if st.button("🚀 Analyze Sentiment", use_container_width=True):
            with st.spinner("Analyzing..."):
                analyzer = SentimentAnalyzer()
                strategist = MitigationStrategist()
                
                sentiment = analyzer.analyze_sentiment(test_text)
                is_risk = analyzer.is_high_risk(test_text, sentiment)
                
                st.session_state.sentiment = sentiment
                st.session_state.is_risk = is_risk
                st.session_state.strategy = strategist.generate_response_strategy(test_text, brand_name) if is_risk else None

    with col2:
        st.markdown("### 📊 Live Analysis Results")
        
        if 'sentiment' in st.session_state:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f"**🎯 Sentiment Score:** `{st.session_state.sentiment:.2f}`")
            
            risk_html = f'<span class="risk-yes">🚨 HIGH RISK</span>' if st.session_state.is_risk else f'<span class="risk-no">✅ LOW RISK</span>'
            st.markdown(f"**📈 Risk Level:** {risk_html}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.session_state.is_risk and st.session_state.strategy:
                st.markdown("### 🛡️ Mitigation Strategy")
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown(st.session_state.strategy)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("### ⚡ Quick Actions")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button("📧 Email Alert", use_container_width=True)
                with col2:
                    st.button("📱 SMS Notification", use_container_width=True)
                with col3:
                    st.button("📊 Generate Report", use_container_width=True)

    st.markdown("---")
    
    # Features section
    st.markdown("### ✨ How It Works")
    features = [
        "🔍 **Real-time Monitoring**: Track brand mentions across platforms",
        "⚠️ **Risk Detection**: AI-powered sentiment analysis",
        "🛡️ **Crisis Prevention**: Immediate mitigation strategies",
        "📊 **Actionable Insights**: Professional PR recommendations"
    ]
    
    for feature in features:
        st.markdown(f'<div class="gold-text">{feature}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
