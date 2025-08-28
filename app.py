import subprocess
import sys
import requests
import streamlit as st
from typing import List, Dict

# Install required libraries and setup
def install_and_setup():
    try:
        # Install libraries
        subprocess.check_call([sys.executable, "-m", "pip", "install", "textblob", "openai", "requests"])
        # Download NLTK data
        import nltk
        nltk.download('punkt')
        nltk.download('brown')
    except Exception as e:
        st.error(f"Setup error: {e}")

# Run setup
install_and_setup()

# Now import the libraries
from textblob import TextBlob
from openai import OpenAI

# Streamlit UI
st.set_page_config(page_title="BrandGuardian AI", page_icon="🛡️")
st.title("🛡️ BrandGuardian AI")
st.write("Monitor your brand's online reputation in real-time")

# Initialize OpenAI client - SECURE WAY using Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

class SentimentAnalyzer:
    def analyze_sentiment(self, text: str) -> float:
        """Returns a sentiment polarity score between -1 (negative) and 1 (positive)."""
        try:
            analysis = TextBlob(text)
            return analysis.sentiment.polarity
        except:
            return 0.0

    def is_high_risk(self, text: str, sentiment_score: float) -> bool:
        """Determines if a post is a high-risk threat."""
        if sentiment_score > -0.3:
            return False
        
        if len(text) < 10:
            return False
            
        negative_keywords = ['hate', 'terrible', 'awful', 'sue', 'legal', 'boycott', 'scam', 'fraud', 'worst', 'never again', 'refund', 'angry', 'disgusting']
        if any(keyword in text.lower() for keyword in negative_keywords):
            return True
            
        return sentiment_score < -0.6

class MitigationStrategist:
    def generate_response_strategy(self, risky_text: str, brand_name: str) -> str:
        """Generates an AI-powered mitigation strategy using OpenAI."""
        try:
            # Create a prompt for OpenAI
            prompt = f"""
            A high-risk post has been detected for the brand {brand_name}. 
            Post Content: "{risky_text}"
            
            As a PR crisis management expert, generate a concise, professional mitigation strategy.
            Provide 3-5 bullet points with immediate, actionable steps the company should take.
            Focus on public response, customer service, and reputation management.
            """
            
            # Call OpenAI API
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
            # Fallback strategy if API fails
            return f"""⚠️ AI strategy generation failed. Recommended steps:
            1. Acknowledge the concern publicly within 1 hour
            2. Offer to move the conversation to private messages
            3. Prepare an official statement addressing the specific issue: {risky_text[:100]}...
            """

# Main application
def main():
    analyzer = SentimentAnalyzer()
    strategist = MitigationStrategist()
    
    st.sidebar.header("Configuration")
    brand_name = st.sidebar.text_input("Brand Name to Monitor", "YourBrand")
    
    st.sidebar.header("Test the AI")
    test_text = st.sidebar.text_area("Enter text to analyze:", "I absolutely hate this company! Their service is terrible and I will sue them!")
    
    if st.sidebar.button("Analyze Text"):
        sentiment = analyzer.analyze_sentiment(test_text)
        is_risk = analyzer.is_high_risk(test_text, sentiment)
        
        st.sidebar.write(f"Sentiment Score: {sentiment:.2f}")
        st.sidebar.write(f"High Risk: {'🚨 YES' if is_risk else '✅ NO'}")
        
        if is_risk:
            st.sidebar.write("**Mitigation Strategy:**")
            strategy = strategist.generate_response_strategy(test_text, brand_name)
            st.sidebar.write(strategy)
    
    st.header("How It Works")
    st.write("""
    1. **Enter your brand name** in the sidebar
    2. **Test with sample text** to see the AI in action
    3. **Get real-time alerts** for brand reputation risks
    4. **Receive AI-powered mitigation strategies**
    """)
    
    st.header("Get Started")
    st.write("""
    This tool helps you monitor online mentions and identify potential PR crises before they escalate.
    The AI analyzes sentiment and context to flag only high-risk situations.
    """)
    
    # Disclaimer
    st.info("""
    **Note:** This is a live version using AI. For continuous monitoring, you need to:
    - Integrate with social media APIs (Twitter, Reddit, etc.)
    - Set up automated scanning schedules
    """)

if __name__ == "__main__":
    main()
