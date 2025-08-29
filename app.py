import streamlit as st
import time
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
import warnings
warnings.filterwarnings('ignore')

# Set page config first
st.set_page_config(
    page_title="BrandGuardian AI Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS with enhanced UI components
st.markdown("""
<style>
    /* Base styles remain the same with enhancements */
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
    
    /* Add more advanced styling components */
    .advanced-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        transition: all 0.3s ease;
    }
    
    .advanced-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.18);
        background: rgba(255, 255, 255, 0.05);
    }
    
    .prediction-high {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
        border-left: 4px solid #EF4444;
    }
    
    .prediction-medium {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.05) 100%);
        border-left: 4px solid #F59E0B;
    }
    
    .prediction-low {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
        border-left: 4px solid #10B981;
    }
    
    .business-model-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .financial-metric {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #8B5CF6;
    }
    
    /* Additional styles for advanced components */
    .network-graph {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .strategy-recommendation {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #6366F1;
    }
</style>
""", unsafe_allow_html=True)

# Advanced Sentiment Analysis with Business Context
class AdvancedSentimentAnalyzer:
    def __init__(self):
        self.business_terms = {
            'revenue': 0.8, 'profit': 0.9, 'growth': 0.7, 'loss': -0.9, 
            'investment': 0.6, 'market share': 0.7, 'acquisition': 0.5,
            'merger': 0.4, 'bankruptcy': -1.0, 'layoff': -0.9, 'expansion': 0.7,
            'innovation': 0.8, 'disruption': 0.3, 'competition': -0.4,
            'dividend': 0.6, 'stock': 0.5, 'IPO': 0.7, 'valuation': 0.6
        }
        
        self.sector_keywords = {
            'technology': ['software', 'hardware', 'cloud', 'AI', 'machine learning', 'data'],
            'finance': ['bank', 'loan', 'interest', 'investment', 'stock', 'market'],
            'healthcare': ['medical', 'health', 'patient', 'hospital', 'pharmaceutical'],
            'retail': ['store', 'shop', 'product', 'customer', 'sale', 'price']
        }
    
    def analyze_sentiment_with_business_context(self, text: str, sector: str = None) -> dict:
        """
        Advanced sentiment analysis with business context awareness
        """
        try:
            # Use TextBlob for baseline sentiment
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Business context adjustment
            business_impact = 0
            business_terms_found = []
            
            for term, weight in self.business_terms.items():
                if term in text.lower():
                    business_impact += weight
                    business_terms_found.append(term)
            
            # Normalize business impact
            if business_terms_found:
                business_impact = business_impact / len(business_terms_found)
                # Adjust polarity based on business context
                polarity = (polarity + business_impact) / 2
            
            # Sector-specific adjustment
            sector_impact = 0
            if sector and sector in self.sector_keywords:
                sector_terms = self.sector_keywords[sector]
                sector_matches = [term for term in sector_terms if term in text.lower()]
                if sector_matches:
                    # Slight adjustment for sector relevance
                    sector_impact = 0.1
                    polarity = polarity * (1 + sector_impact)
            
            # Determine sentiment category
            if polarity > 0.3:
                sentiment_category = "Positive"
            elif polarity < -0.3:
                sentiment_category = "Negative"
            else:
                sentiment_category = "Neutral"
            
            # Calculate confidence score
            confidence = min(0.99, (abs(polarity) + (1 - subjectivity)) / 2)
            
            return {
                'polarity': polarity,
                'subjectivity': subjectivity,
                'sentiment_category': sentiment_category,
                'confidence': confidence,
                'business_terms': business_terms_found,
                'sector_impact': sector_impact
            }
            
        except Exception as e:
            return {
                'polarity': 0,
                'subjectivity': 0,
                'sentiment_category': "Neutral",
                'confidence': 0,
                'business_terms': [],
                'sector_impact': 0
            }
    
    def is_business_critical(self, text: str, sentiment_result: dict) -> bool:
        """
        Determine if the text contains business-critical information
        """
        critical_business_terms = ['bankruptcy', 'layoff', 'merger', 'acquisition', 'IPO', 'stock', 'profit', 'loss']
        text_lower = text.lower()
        
        # Check for critical business terms
        has_critical_terms = any(term in text_lower for term in critical_business_terms)
        
        # Check for high negative sentiment with business context
        is_negative_business = (sentiment_result['polarity'] < -0.5 and 
                               len(sentiment_result['business_terms']) > 0)
        
        return has_critical_terms or is_negative_business

# Advanced Business Impact Predictor
class BusinessImpactPredictor:
    def __init__(self):
        self.impact_factors = {
            'virality': 0.3,
            'author_influence': 0.25,
            'sentiment': 0.2,
            'business_relevance': 0.15,
            'timing': 0.1
        }
    
    def predict_business_impact(self, text: str, sentiment_result: dict, 
                              author_followers: int = 0, platform: str = "twitter") -> dict:
        """
        Predict the potential business impact of a social media post
        """
        try:
            # Calculate virality score based on content characteristics
            virality_score = self._calculate_virality_score(text)
            
            # Calculate author influence score
            author_score = self._calculate_author_score(author_followers, platform)
            
            # Sentiment impact (negative sentiment has higher potential impact)
            sentiment_impact = abs(sentiment_result['polarity']) * (-1 if sentiment_result['polarity'] < 0 else 0.5)
            
            # Business relevance score
            business_relevance = len(sentiment_result['business_terms']) * 0.1
            
            # Timing factor (current time relevance)
            timing_factor = random.uniform(0.7, 1.0)  # Simulated
            
            # Calculate overall impact score
            impact_score = (
                self.impact_factors['virality'] * virality_score +
                self.impact_factors['author_influence'] * author_score +
                self.impact_factors['sentiment'] * sentiment_impact +
                self.impact_factors['business_relevance'] * business_relevance +
                self.impact_factors['timing'] * timing_factor
            )
            
            # Categorize impact level
            if impact_score > 0.7:
                impact_level = "High"
                financial_risk = random.randint(100000, 5000000)  # Simulated financial impact
            elif impact_score > 0.4:
                impact_level = "Medium"
                financial_risk = random.randint(10000, 100000)
            else:
                impact_level = "Low"
                financial_risk = random.randint(0, 10000)
            
            # Generate impact explanation
            explanation = self._generate_impact_explanation(
                impact_level, virality_score, author_score, sentiment_impact, 
                business_relevance, sentiment_result['business_terms']
            )
            
            return {
                'impact_score': impact_score,
                'impact_level': impact_level,
                'financial_risk': financial_risk,
                'explanation': explanation,
                'factors': {
                    'virality': virality_score,
                    'author_influence': author_score,
                    'sentiment_impact': sentiment_impact,
                    'business_relevance': business_relevance,
                    'timing': timing_factor
                }
            }
            
        except Exception as e:
            return {
                'impact_score': 0,
                'impact_level': "Low",
                'financial_risk': 0,
                'explanation': "Unable to calculate impact",
                'factors': {}
            }
    
    def _calculate_virality_score(self, text: str) -> float:
        """Calculate virality potential of text"""
        # Simple heuristic based on text characteristics
        length = len(text)
        has_questions = 1 if '?' in text else 0
        has_exclamations = 1 if '!' in text else 0
        has_emojis = 1 if any(c in text for c in ['😊', '😂', '😍', '😠', '😢']) else 0
        
        # Normalize to 0-1 range
        score = min(1.0, (length * 0.001 + has_questions * 0.2 + has_exclamations * 0.2 + has_emojis * 0.1))
        return score
    
    def _calculate_author_score(self, followers: int, platform: str) -> float:
        """Calculate author influence score"""
        # Base score from follower count (logarithmic scale)
        if followers == 0:
            return 0.1  # Default for unknown authors
        
        follower_score = min(1.0, np.log10(followers) / 7)  # Cap at 10M followers
        
        # Platform multiplier
        platform_multiplier = {
            'twitter': 1.0,
            'facebook': 0.9,
            'instagram': 0.8,
            'linkedin': 1.2,  # Higher for business context
            'tiktok': 0.7,
            'youtube': 1.1,
            'reddit': 0.8,
            'news': 1.3
        }.get(platform.lower(), 1.0)
        
        return follower_score * platform_multiplier
    
    def _generate_impact_explanation(self, impact_level, virality, author, sentiment, business, terms):
        """Generate human-readable explanation of impact"""
        explanations = {
            "High": "This content has high potential for significant business impact due to ",
            "Medium": "This content may have moderate business impact because of ",
            "Low": "This content has limited business impact potential due to "
        }
        
        factors = []
        if virality > 0.6:
            factors.append("high virality potential")
        if author > 0.6:
            factors.append("influential author")
        if abs(sentiment) > 0.6:
            factors.append("strong sentiment")
        if business > 0.3:
            factors.append("business relevance")
        if terms:
            factors.append(f"mention of key business terms: {', '.join(terms[:3])}")
        
        if not factors:
            factors.append("limited engagement factors")
        
        return explanations[impact_level] + ", ".join(factors)

# Advanced Business Model Analyzer
class BusinessModelAnalyzer:
    def __init__(self):
        self.business_models = {
            'b2b': {
                'keywords': ['enterprise', 'business', 'solution', 'platform', 'saas', 'software'],
                'risk_factors': ['customer churn', 'enterprise contract', 'competition', 'pricing']
            },
            'b2c': {
                'keywords': ['consumer', 'customer', 'buy', 'price', 'product', 'service'],
                'risk_factors': ['public sentiment', 'viral negative', 'brand reputation', 'social media']
            },
            'marketplace': {
                'keywords': ['platform', 'buyer', 'seller', 'transaction', 'marketplace', 'fee'],
                'risk_factors': ['trust', 'fraud', 'dispute', 'regulation']
            },
            'subscription': {
                'keywords': ['monthly', 'annual', 'subscribe', 'membership', 'recurring'],
                'risk_factors': ['churn rate', 'payment issue', 'value perception']
            }
        }
    
    def detect_business_model(self, text_corpus: list) -> dict:
        """
        Analyze text to detect probable business model
        """
        try:
            # Flatten corpus and count occurrences of model keywords
            flat_text = " ".join(text_corpus).lower()
            model_scores = {}
            
            for model, data in self.business_models.items():
                score = sum(1 for keyword in data['keywords'] if keyword in flat_text)
                model_scores[model] = score
            
            # Normalize scores
            total = sum(model_scores.values())
            if total > 0:
                for model in model_scores:
                    model_scores[model] = model_scores[model] / total
            
            # Get top model
            top_model = max(model_scores, key=model_scores.get) if model_scores else "unknown"
            
            return {
                'probable_model': top_model,
                'confidence': model_scores[top_model] if top_model != "unknown" else 0,
                'all_scores': model_scores
            }
            
        except Exception as e:
            return {
                'probable_model': "unknown",
                'confidence': 0,
                'all_scores': {}
            }
    
    def model_specific_risks(self, business_model: str, sentiment_data: list) -> dict:
        """
        Identify risks specific to a business model
        """
        if business_model not in self.business_models:
            return {"risks": [], "mitigation_strategies": []}
        
        risks = self.business_models[business_model]['risk_factors']
        
        # Analyze sentiment towards risk factors
        risk_sentiments = {}
        for risk in risks:
            # Simple check for risk mentions with negative sentiment
            negative_mentions = sum(1 for sent in sentiment_data 
                                  if risk in sent.get('text', '').lower() 
                                  and sent.get('sentiment', {}).get('polarity', 0) < 0)
            risk_sentiments[risk] = negative_mentions
        
        # Generate mitigation strategies based on model
        mitigation_strategies = {
            'b2b': [
                "Enhance customer success programs",
                "Develop competitive differentiation",
                "Strengthen contract renewal processes",
                "Improve enterprise communication"
            ],
            'b2c': [
                "Launch brand sentiment campaign",
                "Improve customer service response",
                "Monitor social channels closely",
                "Develop crisis communication plan"
            ],
            'marketplace': [
                "Enhance trust and safety measures",
                "Improve dispute resolution process",
                "Communicate platform security",
                "Strengthen community guidelines"
            ],
            'subscription': [
                "Analyze churn reasons",
                "Improve subscription value",
                "Develop retention programs",
                "Communicate product updates"
            ]
        }.get(business_model, [])
        
        return {
            "risks": risks,
            "risk_sentiments": risk_sentiments,
            "mitigation_strategies": mitigation_strategies
        }

# Advanced Financial Impact Estimator
class FinancialImpactEstimator:
    def __init__(self):
        self.sector_multipliers = {
            'technology': 1.5,
            'finance': 1.2,
            'healthcare': 1.0,
            'retail': 0.8,
            'manufacturing': 0.7
        }
    
    def estimate_financial_impact(self, impact_data: dict, business_model: str, 
                                sector: str, market_cap: float = None) -> dict:
        """
        Estimate potential financial impact of sentiment issues
        """
        try:
            base_impact = impact_data.get('financial_risk', 0)
            
            # Apply business model multiplier
            model_multiplier = {
                'b2b': 1.2,
                'b2c': 1.5,  # B2C more sensitive to public sentiment
                'marketplace': 1.3,
                'subscription': 1.4,
                'unknown': 1.0
            }.get(business_model, 1.0)
            
            # Apply sector multiplier
            sector_multiplier = self.sector_multipliers.get(sector.lower(), 1.0)
            
            # Calculate adjusted impact
            adjusted_impact = base_impact * model_multiplier * sector_multiplier
            
            # If market cap is provided, calculate as percentage
            impact_percentage = None
            if market_cap and market_cap > 0:
                impact_percentage = (adjusted_impact / market_cap) * 100
            
            # Categorize impact severity
            if adjusted_impact > 1000000:
                severity = "High"
            elif adjusted_impact > 100000:
                severity = "Medium"
            else:
                severity = "Low"
            
            return {
                'estimated_impact': adjusted_impact,
                'impact_percentage': impact_percentage,
                'severity': severity,
                'model_multiplier': model_multiplier,
                'sector_multiplier': sector_multiplier
            }
            
        except Exception as e:
            return {
                'estimated_impact': 0,
                'impact_percentage': 0,
                'severity': "Low",
                'model_multiplier': 1.0,
                'sector_multiplier': 1.0
            }

# Network Analysis for Influencer Mapping
class InfluenceNetworkAnalyzer:
    def __init__(self):
        self.graph = nx.Graph()
    
    def build_network(self, posts: list):
        """Build influence network from social posts"""
        try:
            # Extract authors and mentions
            authors = set()
            mentions = set()
            
            for post in posts:
                author = post.get('author', 'unknown')
                authors.add(author)
                
                # Simple mention extraction (in real implementation, use proper NLP)
                text = post.get('content', '')
                potential_mentions = re.findall(r'@(\w+)', text)
                for mention in potential_mentions:
                    mentions.add(mention)
                    self.graph.add_edge(author, mention, weight=1)
            
            # Calculate basic network metrics
            if len(self.graph) > 0:
                centrality = nx.degree_centrality(self.graph)
                betweenness = nx.betweenness_centrality(self.graph)
                pagerank = nx.pagerank(self.graph)
                
                return {
                    'node_count': len(self.graph.nodes()),
                    'edge_count': len(self.graph.edges()),
                    'centrality': centrality,
                    'betweenness': betweenness,
                    'pagerank': pagerank
                }
            else:
                return {
                    'node_count': 0,
                    'edge_count': 0,
                    'centrality': {},
                    'betweenness': {},
                    'pagerank': {}
                }
                
        except Exception as e:
            return {
                'node_count': 0,
                'edge_count': 0,
                'centrality': {},
                'betweenness': {},
                'pagerank': {}
            }

# Initialize advanced analyzers
advanced_sentiment = AdvancedSentimentAnalyzer()
business_impact = BusinessImpactPredictor()
business_model_analyzer = BusinessModelAnalyzer()
financial_impact = FinancialImpactEstimator()
network_analyzer = InfluenceNetworkAnalyzer()

# Enhanced Multi-Platform Monitoring with business context
class AdvancedSocialMediaMonitor:
    def __init__(self):
        self.platforms = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn', 'Reddit', 'YouTube', 'TikTok', 'News']
        
    def simulate_advanced_feed(self, brand_name, sector="technology"):
        # Simulate more realistic posts with business context
        posts = []
        for _ in range(random.randint(10, 25)):
            platform = random.choice(self.platforms)
            content = self.generate_business_post(brand_name, sector)
            
            # Generate more realistic engagement metrics
            engagement = self.generate_engagement(platform, content)
            
            # Generate author information
            author_followers = random.randint(100, 1000000) if random.random() > 0.3 else 0
            
            posts.append({
                'platform': platform,
                'content': content,
                'author': f"user_{random.randint(1000, 9999)}",
                'author_followers': author_followers,
                'date': datetime.now() - timedelta(hours=random.randint(0, 168)),  # Up to 1 week
                'engagement': engagement,
                'sentiment': advanced_sentiment.analyze_sentiment_with_business_context(content, sector),
                'business_impact': None  # To be calculated later
            })
        return posts
    
    def generate_business_post(self, brand_name, sector):
        """Generate posts with business context"""
        sector_templates = {
            'technology': [
                f"{brand_name}'s new AI feature is revolutionizing the industry",
                f"Concerned about {brand_name}'s data privacy practices",
                f"{brand_name} stock is soaring after positive earnings report",
                f"Considering switching from {brand_name} to a competitor",
                f"{brand_name} just announced a major acquisition"
            ],
            'finance': [
                f"{brand_name} reports better than expected Q3 results",
                f"Regulatory concerns mounting for {brand_name}",
                f"{brand_name} announces dividend increase",
                f"Customer complaints about {brand_name}'s fee structure",
                f"{brand_name} expanding into new markets"
            ],
            'retail': [
                f"Love the new {brand_name} product line!",
                f"Disappointed with {brand_name}'s customer service",
                f"{brand_name} holiday sales break records",
                f"Product quality issues at {brand_name}",
                f"{brand_name} announces store expansion plans"
            ]
        }
        
        # Select from sector-specific templates or general ones
        templates = sector_templates.get(sector, [
            f"{brand_name} is doing great things!",
            f"Not happy with {brand_name} recently",
            f"What's everyone's experience with {brand_name}?",
            f"{brand_name} needs to improve their service",
            f"Big announcement coming from {brand_name}"
        ])
        
        return random.choice(templates)
    
    def generate_engagement(self, platform, content):
        """Generate realistic engagement metrics based on platform and content"""
        base_engagement = {
            'Twitter': random.randint(10, 5000),
            'Facebook': random.randint(50, 10000),
            'Instagram': random.randint(100, 15000),
            'LinkedIn': random.randint(5, 2000),
            'Reddit': random.randint(20, 5000),
            'YouTube': random.randint(100, 20000),
            'TikTok': random.randint(500, 25000),
            'News': random.randint(100, 5000)
        }
        
        engagement = base_engagement.get(platform, random.randint(10, 1000))
        
        # Adjust based on sentiment (negative content often gets more engagement)
        blob = TextBlob(content)
        if blob.sentiment.polarity < -0.3:
            engagement = int(engagement * random.uniform(1.2, 2.0))
        elif blob.sentiment.polarity > 0.3:
            engagement = int(engagement * random.uniform(1.1, 1.5))
            
        return engagement

# Enhanced Competitive Intelligence with Market Analysis
class AdvancedCompetitiveAnalyzer:
    def __init__(self):
        self.competitors = {
            'technology': ['Apple', 'Google', 'Microsoft', 'Amazon', 'Meta', 'Tesla'],
            'finance': ['JPMorgan', 'Bank of America', 'Wells Fargo', 'Goldman Sachs', 'Morgan Stanley'],
            'retail': ['Walmart', 'Target', 'Amazon', 'Costco', 'Best Buy']
        }
        
    def advanced_competitive_analysis(self, brand_name, sector="technology"):
        # Get competitors for the sector
        competitors = self.competitors.get(sector, [])
        
        # Simulate market analysis data
        market_share = {}
        growth_rates = {}
        sentiment_scores = {}
        
        # Include the main brand
        all_brands = [brand_name] + competitors
        
        for brand in all_brands:
            market_share[brand] = random.uniform(5, 40)  # Percentage
            growth_rates[brand] = random.uniform(-5, 25)  # Percentage growth
            sentiment_scores[brand] = random.uniform(0.4, 0.8)  # Sentiment score
        
        # Normalize market share to sum to 100
        total_share = sum(market_share.values())
        for brand in market_share:
            market_share[brand] = (market_share[brand] / total_share) * 100
        
        return {
            'market_share': market_share,
            'growth_rates': growth_rates,
            'sentiment_scores': sentiment_scores,
            'competitive_set': competitors
        }
    
    def swot_analysis(self, brand_name, sector="technology"):
        """Generate a simulated SWOT analysis"""
        strengths = [
            "Strong brand recognition",
            "Innovative product portfolio",
            "Loyal customer base",
            "Robust financial performance",
            "Skilled leadership team"
        ]
        
        weaknesses = [
            "Dependence on key markets",
            "Higher prices than competitors",
            "Slower innovation cycle in some areas",
            "Supply chain vulnerabilities",
            "Limited presence in emerging markets"
        ]
        
        opportunities = [
            "Market expansion opportunities",
            "Strategic partnerships",
            "New technology adoption",
            "Growing market demand",
            "Competitive gaps in the market"
        ]
        
        threats = [
            "Intensifying competition",
            "Regulatory changes",
            "Economic downturn",
            "Changing consumer preferences",
            "Technology disruption"
        ]
        
        return {
            'strengths': random.sample(strengths, 3),
            'weaknesses': random.sample(weaknesses, 3),
            'opportunities': random.sample(opportunities, 3),
            'threats': random.sample(threats, 3)
        }

# Enhanced Crisis Prediction with Business Impact
class AdvancedCrisisPredictor:
    def __init__(self):
        self.warning_signs = [
            'sudden sentiment drop >30%',
            'viral negative post with >100K engagement',
            'multiple executive departures',
            'regulatory investigation announcement',
            'major product recall',
            'significant cybersecurity breach',
            'negative earnings surprise',
            'key competitor launching disruptive product'
        ]
        
        self.crisis_types = {
            'financial': ['earnings miss', 'stock crash', 'accounting scandal', 'bankruptcy risk'],
            'reputational': ['CEO scandal', 'product failure', 'customer data breach', 'discrimination lawsuit'],
            'operational': ['supply chain disruption', 'cyber attack', 'factory shutdown', 'key system failure'],
            'competitive': ['disruptive new competitor', 'key patent loss', 'major client loss', 'market share erosion']
        }
    
    def predict_advanced_crisis_risk(self, brand_name, historical_data, sector="technology"):
        """Predict crisis risk with business context"""
        # Simulate risk calculation based on multiple factors
        financial_risk = random.uniform(0.1, 0.9)
        reputational_risk = random.uniform(0.1, 0.9)
        operational_risk = random.uniform(0.1, 0.9)
        competitive_risk = random.uniform(0.1, 0.9)
        
        # Calculate overall risk
        overall_risk = (financial_risk + reputational_risk + operational_risk + competitive_risk) / 4
        
        # Determine risk level
        if overall_risk > 0.7:
            risk_level = "High"
            crisis_type = random.choice(list(self.crisis_types.keys()))
            potential_impact = random.randint(5000000, 50000000)
        elif overall_risk > 0.4:
            risk_level = "Medium"
            crisis_type = random.choice(list(self.crisis_types.keys()))
            potential_impact = random.randint(500000, 5000000)
        else:
            risk_level = "Low"
            crisis_type = None
            potential_impact = random.randint(0, 500000)
        
        # Get warning signs
        current_warnings = random.sample(self.warning_signs, random.randint(0, 3))
        
        # Generate sector-specific recommendations
        recommendations = self.generate_recommendations(risk_level, crisis_type, sector)
        
        return {
            'risk_score': overall_risk,
            'risk_level': risk_level,
            'crisis_type': crisis_type,
            'potential_impact': potential_impact,
            'warning_signs': current_warnings,
            'recommendations': recommendations,
            'category_risks': {
                'financial': financial_risk,
                'reputational': reputational_risk,
                'operational': operational_risk,
                'competitive': competitive_risk
            }
        }
    
    def generate_recommendations(self, risk_level, crisis_type, sector):
        """Generate crisis preparedness recommendations"""
        base_recommendations = [
            "Increase monitoring frequency of social channels",
            "Prepare holding statements for potential issues",
            "Conduct crisis simulation exercises",
            "Review and update crisis communication plan",
            "Identify and prepare spokespeople",
            "Monitor competitor activities closely",
            "Establish media monitoring system",
            "Develop customer communication templates"
        ]
        
        if risk_level == "High":
            additional = [
                "Activate crisis management team",
                "Conduct vulnerability assessment",
                "Prepare for financial impact",
                "Engage with legal counsel",
                "Develop scenario response plans"
            ]
        elif risk_level == "Medium":
            additional = [
                "Review insurance coverage",
                "Update stakeholder communication plans",
                "Conduct media training for executives",
                "Audit digital assets for vulnerabilities"
            ]
        else:
            additional = [
                "Continue regular monitoring",
                "Maintain crisis preparedness",
                "Update contact lists",
                "Review past crisis learnings"
            ]
        
        # Add sector-specific recommendations
        sector_recommendations = {
            'technology': [
                "Monitor tech forums and communities",
                "Prepare for product vulnerability disclosures",
                "Review data security protocols",
                "Monitor patent and intellectual property discussions"
            ],
            'finance': [
                "Monitor financial regulatory news",
                "Prepare for market volatility",
                "Review compliance procedures",
                "Monitor customer complaint channels"
            ],
            'retail': [
                "Monitor supply chain disruptions",
                "Prepare for product quality issues",
                "Review customer feedback channels",
                "Monitor competitor pricing strategies"
            ]
        }.get(sector, [])
        
        return random.sample(base_recommendations + additional + sector_recommendations, 
                           min(6, len(base_recommendations + additional + sector_recommendations)))

# Initialize advanced modules
advanced_monitor = AdvancedSocialMediaMonitor()
advanced_competitive = AdvancedCompetitiveAnalyzer()
advanced_crisis = AdvancedCrisisPredictor()

# Enhanced visualization functions
def create_sentiment_trend_chart(sentiment_data):
    """Create an advanced sentiment trend chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=sentiment_data['date'],
        y=sentiment_data['score'],
        mode='lines+markers',
        name='Sentiment Score',
        line=dict(color='#6366F1', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title='Sentiment Trend Over Time',
        xaxis_title='Date',
        yaxis_title='Sentiment Score',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    return fig

def create_competitive_analysis_chart(analysis_data):
    """Create competitive analysis visualization"""
    brands = list(analysis_data['market_share'].keys())
    shares = list(analysis_data['market_share'].values())
    sentiments = [analysis_data['sentiment_scores'][b] for b in brands]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Market Share', 'Sentiment Comparison'),
        specs=[[{"type": "pie"}, {"type": "bar"}]]
    )
    
    # Market share pie chart
    fig.add_trace(
        go.Pie(
            labels=brands, 
            values=shares, 
            name="Market Share",
            hole=0.4,
            marker_colors=px.colors.qualitative.Set3
        ),
        row=1, col=1
    )
    
    # Sentiment bar chart
    fig.add_trace(
        go.Bar(
            x=brands,
            y=sentiments,
            name="Sentiment Score",
            marker_color=['#6366F1' if i == 0 else '#8B5CF6' for i in range(len(brands))]
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text='Competitive Landscape Analysis',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False
    )
    
    return fig

def create_risk_matrix(crisis_data):
    """Create a risk matrix visualization"""
    categories = list(crisis_data['category_risks'].keys())
    risks = list(crisis_data['category_risks'].values())
    
    fig = go.Figure(data=go.Scatterpolar(
        r=risks + [risks[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Risk Profile',
        line=dict(color='#EF4444')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=False,
        title='Crisis Risk Matrix',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

# Enhanced dashboard sections
def show_advanced_executive_dashboard(brand_name, sector):
    st.markdown('<div class="dashboard-header">Advanced Executive Intelligence Dashboard</div>', unsafe_allow_html=True)
    
    # Get advanced data
    comp_analysis = advanced_competitive.advanced_competitive_analysis(brand_name, sector)
    crisis_prediction = advanced_crisis.predict_advanced_crisis_risk(brand_name, {}, sector)
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        market_share = comp_analysis['market_share'][brand_name]
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Market Share</div>
            <div class="kpi-value">{market_share:.1f}%</div>
            <div>{"📈 Leading" if market_share > 20 else "📉 Challenger" if market_share > 10 else "📊 Niche"}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        risk_score = crisis_prediction['risk_score']
        risk_color = "negative-kpi" if risk_score > 0.7 else "neutral-kpi" if risk_score > 0.4 else "positive-kpi"
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Crisis Risk Score</div>
            <div class="kpi-value {risk_color}">{risk_score:.2%}</div>
            <div>{"🚨 High Alert" if risk_score > 0.7 else "⚠️ Moderate" if risk_score > 0.4 else "🟢 Normal"}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        financial_impact = crisis_prediction['potential_impact']
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Potential Financial Impact</div>
            <div class="kpi-value">${financial_impact:,.0f}</div>
            <div>{"🔴 Significant" if financial_impact > 1000000 else "🟡 Moderate" if financial_impact > 100000 else "🟢 Minimal"}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        growth_rate = comp_analysis['growth_rates'][brand_name]
        growth_color = "positive-kpi" if growth_rate > 10 else "negative-kpi" if growth_rate < 0 else "neutral-kpi"
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-label">Growth Rate</div>
            <div class="kpi-value {growth_color}">{growth_rate:.1f}%</div>
            <div>{"📈 High Growth" if growth_rate > 15 else "📊 Stable" if growth_rate > 5 else "📉 Low Growth"}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Advanced charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_competitive_analysis_chart(comp_analysis), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_risk_matrix(crisis_prediction), use_container_width=True)
    
    # Business model insights
    st.markdown("### Business Model Intelligence")
    posts = advanced_monitor.simulate_advanced_feed(brand_name, sector)
    post_texts = [post['content'] for post in posts]
    model_analysis = business_model_analyzer.detect_business_model(post_texts)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="business-model-card">
            <h4>Detected Business Model</h4>
            <h2>{model_analysis['probable_model'].upper()}</h2>
            <p>Confidence: {model_analysis['confidence']:.2%}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        model_risks = business_model_analyzer.model_specific_risks(model_analysis['probable_model'], posts)
        st.markdown(f'''
        <div class="business-model-card">
            <h4>Model-Specific Risks</h4>
            <ul>
                {"".join(f"<li>{risk}</li>" for risk in model_risks['risks'][:3])}
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="business-model-card">
            <h4>Recommended Strategies</h4>
            <ul>
                {"".join(f"<li>{strategy}</li>" for strategy in model_risks['mitigation_strategies'][:3])}
            </ul>
        </div>
        ''', unsafe_allow_html=True)

def show_advanced_threat_analyzer(brand_name, sector):
    st.header("Advanced Threat Analyzer with Business Context")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🧪 Advanced Threat Simulation")
        st.markdown('<div class="glowing-border cyber-border" style="padding: 20px;">', unsafe_allow_html=True)
        
        # Sector selection
        sector = st.selectbox("Business Sector", 
                            ["technology", "finance", "retail", "healthcare", "manufacturing"],
                            key="sector_select")
        
        # Business context options
        business_context = st.text_input("Business Context (Optional)", 
                                       "quarterly earnings, product launch, merger announcement")
        
        test_text = st.text_area("**🔍 Enter text to analyze:**", 
                               "I'm extremely concerned about the recent earnings report. Stock price dropped 15% and there are rumors of layoffs.",
                               height=150)
        
        author_followers = st.slider("Author Followers (Reach)", 0, 1000000, 10000, 
                                   help="Estimated follower count for impact assessment")
        
        platform = st.selectbox("Platform", 
                              ["Twitter", "Facebook", "LinkedIn", "Instagram", "News", "Reddit", "YouTube"])
        
        if st.button("🚀 Advanced Analysis", use_container_width=True, key="advanced_analyze_btn"):
            with st.spinner("🛡️ Conducting deep analysis with business context..."):
                time.sleep(2)
                
                # Advanced sentiment analysis
                sentiment_result = advanced_sentiment.analyze_sentiment_with_business_context(test_text, sector)
                
                # Business impact prediction
                impact_result = business_impact.predict_business_impact(
                    test_text, sentiment_result, author_followers, platform
                )
                
                # Financial impact estimation
                model_analysis = business_model_analyzer.detect_business_model([test_text])
                financial_result = financial_impact.estimate_financial_impact(
                    impact_result, model_analysis['probable_model'], sector
                )
                
                # Store results in session state
                st.session_state.advanced_sentiment = sentiment_result
                st.session_state.business_impact = impact_result
                st.session_state.financial_impact = financial_result
                st.session_state.business_critical = advanced_sentiment.is_business_critical(test_text, sentiment_result)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### 📊 Advanced Threat Analysis")
        
        if 'advanced_sentiment' in st.session_state:
            # Display results with advanced visualization
            sentiment = st.session_state.advanced_sentiment
            impact = st.session_state.business_impact
            financial = st.session_state.financial_impact
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="advanced-card">', unsafe_allow_html=True)
                st.markdown("##### Sentiment Analysis")
                st.metric("Polarity Score", f"{sentiment['polarity']:.2f}")
                st.metric("Subjectivity", f"{sentiment['subjectivity']:.2f}")
                st.metric("Category", sentiment['sentiment_category'])
                if sentiment['business_terms']:
                    st.write("**Business Terms:**", ", ".join(sentiment['business_terms']))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                risk_class = "prediction-high" if impact['impact_level'] == "High" else \
                           "prediction-medium" if impact['impact_level'] == "Medium" else "prediction-low"
                
                st.markdown(f'<div class="advanced-card {risk_class}">', unsafe_allow_html=True)
                st.markdown("##### Business Impact Prediction")
                st.metric("Impact Score", f"{impact['impact_score']:.2f}")
                st.metric("Impact Level", impact['impact_level'])
                st.metric("Financial Risk", f"${impact['financial_risk']:,.0f}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Financial impact assessment
            st.markdown('<div class="financial-metric">', unsafe_allow_html=True)
            st.markdown("##### Financial Impact Assessment")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Estimated Impact", f"${financial['estimated_impact']:,.0f}")
            with col2:
                st.metric("Severity", financial['severity'])
            with col3:
                if financial['impact_percentage']:
                    st.metric("Market Cap Impact", f"{financial['impact_percentage']:.4f}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Impact explanation
            st.markdown("##### Impact Explanation")
            st.info(impact['explanation'])
            
            # Mitigation strategies
            if impact['impact_level'] in ["High", "Medium"]:
                st.markdown("##### 🛡️ Mitigation Strategies")
                strategies = [
                    "Immediate response protocol activation",
                    "Executive communication plan development",
                    "Stakeholder impact assessment",
                    "Financial contingency planning",
                    "Legal counsel consultation"
                ]
                
                for strategy in strategies:
                    st.markdown(f'<div class="strategy-recommendation">▪️ {strategy}</div>', unsafe_allow_html=True)

def show_advanced_competitive_intelligence(brand_name, sector):
    st.header("Advanced Competitive Intelligence")
    
    # Perform advanced competitive analysis
    comp_analysis = advanced_competitive.advanced_competitive_analysis(brand_name, sector)
    swot_analysis = advanced_competitive.swot_analysis(brand_name, sector)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Market Position Analysis")
        st.plotly_chart(create_competitive_analysis_chart(comp_analysis), use_container_width=True)
        
        # Market share table
        st.markdown("##### Detailed Market Share")
        share_data = []
        for brand, share in comp_analysis['market_share'].items():
            share_data.append({
                'Brand': brand,
                'Market Share': f"{share:.1f}%",
                'Growth Rate': f"{comp_analysis['growth_rates'][brand]:.1f}%",
                'Sentiment': f"{comp_analysis['sentiment_scores'][brand]:.2f}"
            })
        
        st.table(pd.DataFrame(share_data))
    
    with col2:
        st.subheader("SWOT Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="advanced-card" style="border-left: 4px solid #10B981;">', unsafe_allow_html=True)
            st.markdown("##### Strengths")
            for strength in swot_analysis['strengths']:
                st.markdown(f"▪️ {strength}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="advanced-card" style="border-left: 4px solid #EF4444;">', unsafe_allow_html=True)
            st.markdown("##### Weaknesses")
            for weakness in swot_analysis['weaknesses']:
                st.markdown(f"▪️ {weakness}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="advanced-card" style="border-left: 4px solid #3B82F6;">', unsafe_allow_html=True)
            st.markdown("##### Opportunities")
            for opportunity in swot_analysis['opportunities']:
                st.markdown(f"▪️ {opportunity}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="advanced-card" style="border-left: 4px solid #F59E0B;">', unsafe_allow_html=True)
            st.markdown("##### Threats")
            for threat in swot_analysis['threats']:
                st.markdown(f"▪️ {threat}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Competitive strategy recommendations
    st.subheader("Strategic Recommendations")
    
    # Generate recommendations based on competitive position
    market_share = comp_analysis['market_share'][brand_name]
    growth_rate = comp_analysis['growth_rates'][brand_name]
    sentiment = comp_analysis['sentiment_scores'][brand_name]
    
    recommendations = []
    
    if market_share < 10:
        recommendations.append("Focus on niche market differentiation to increase market share")
    elif market_share < 25:
        recommendations.append("Leverage current position to challenge market leaders through innovation")
    else:
        recommendations.append("Defend market leadership through ecosystem development and partnerships")
    
    if growth_rate < 0:
        recommendations.append("Implement aggressive turnaround strategy to reverse negative growth")
    elif growth_rate < 5:
        recommendations.append("Explore new growth avenues through market expansion or product diversification")
    
    if sentiment < 0.5:
        recommendations.append("Launch brand sentiment improvement campaign to address negative perceptions")
    
    for rec in recommendations:
        st.markdown(f'<div class="strategy-recommendation">🔹 {rec}</div>', unsafe_allow_html=True)

def main():
    # Initialize session state for advanced features
    if "sector" not in st.session_state:
        st.session_state.sector = "technology"
    
    # Premium Header with Animation
    st.markdown("""
    <div class="logo-container">
        <div class="logo">🛡️</div>
    </div>
    <h1 class="premium-header floating">BrandGuardian AI Pro</h1>
    <div style="text-align: center; margin-bottom: 20px;" class="accent-text">Advanced Business Intelligence & Digital Risk Protection</div>
    """, unsafe_allow_html=True)
    
    # Sidebar with advanced options
    with st.sidebar:
        st.header("Business Configuration")
        brand_name = st.text_input("Brand Name", "Nike")
        sector = st.selectbox("Business Sector", 
                            ["technology", "finance", "retail", "healthcare", "manufacturing"])
        
        st.session_state.sector = sector
        
        # Additional business context
        st.subheader("Advanced Settings")
        market_cap = st.number_input("Market Capitalization (Optional)", 
                                   min_value=0.0, value=0.0, step=1000000.0,
                                   help="For more accurate financial impact assessment")
        
        business_model = st.selectbox("Business Model (Optional)", 
                                    ["", "B2B", "B2C", "Marketplace", "Subscription", "Hybrid"])
        
        # Real-time monitoring toggle
        real_time = st.toggle("Real-time Monitoring", value=True)
        monitoring_frequency = st.slider("Monitoring Frequency (minutes)", 
                                       1, 60, 5, disabled=not real_time)
    
    # Navigation Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Executive Dashboard", 
        "🔍 Advanced Threat Analysis", 
        "📱 Social Monitoring",
        "🥊 Competitive Intelligence",
        "🌟 Influencer Network",
        "🛡️ Crisis Prediction",
        "❤️ Brand Health"
    ])
    
    with tab1:
        show_advanced_executive_dashboard(brand_name, sector)
    
    with tab2:
        show_advanced_threat_analyzer(brand_name, sector)
    
    with tab3:
        st.header("Advanced Social Monitoring")
        posts = advanced_monitor.simulate_advanced_feed(brand_name, sector)
        
        # Calculate business impact for each post
        for i, post in enumerate(posts):
            if post['business_impact'] is None:
                post['business_impact'] = business_impact.predict_business_impact(
                    post['content'], post['sentiment'], 
                    post['author_followers'], post['platform']
                )
            
            # Display post with advanced formatting
            impact = post['business_impact']
            risk_class = "prediction-high" if impact['impact_level'] == "High" else \
                       "prediction-medium" if impact['impact_level'] == "Medium" else "prediction-low"
            
            with st.expander(f"{post['platform']} - {post['date'].strftime('%Y-%m-%d %H:%M')}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(post['content'])
                    st.caption(f"Author: {post['author']} | Followers: {post['author_followers']:,} | Engagement: {post['engagement']}")
                
                with col2:
                    st.markdown(f'<div class="{risk_class}" style="padding: 10px; border-radius: 8px;">', unsafe_allow_html=True)
                    st.metric("Impact", impact['impact_level'])
                    st.metric("Risk", f"${impact['financial_risk']:,.0f}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Show sentiment analysis
                sentiment = post['sentiment']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Sentiment", f"{sentiment['polarity']:.2f}")
                with col2:
                    st.metric("Category", sentiment['sentiment_category'])
                with col3:
                    st.metric("Confidence", f"{sentiment['confidence']:.2%}")
    
    with tab4:
        show_advanced_competitive_intelligence(brand_name, sector)
    
    with tab5:
        st.header("Influence Network Analysis")
        posts = advanced_monitor.simulate_advanced_feed(brand_name, sector)
        
        # Build network
        network_data = network_analyzer.build_network(posts)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Network Metrics")
            st.metric("Nodes", network_data['node_count'])
            st.metric("Connections", network_data['edge_count'])
            
            if network_data['node_count'] > 0:
                # Identify key influencers
                influencers = sorted(network_data['pagerank'].items(), key=lambda x: x[1], reverse=True)[:5]
                st.markdown("##### Top Influencers")
                for influencer, score in influencers:
                    st.write(f"{influencer} (Score: {score:.4f})")
        
        with col2:
            st.markdown("##### Influence Distribution")
            if network_data['node_count'] > 0:
                # Create simple bar chart of influence scores
                influencers = dict(sorted(network_data['pagerank'].items(), key=lambda x: x[1], reverse=True)[:10])
                fig = px.bar(
                    x=list(influencers.keys()), 
                    y=list(influencers.values()),
                    title="Top Influencers by PageRank Score"
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Not enough data to build influence network")
    
    with tab6:
        st.header("Advanced Crisis Prediction")
        crisis_data = advanced_crisis.predict_advanced_crisis_risk(brand_name, {}, sector)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Crisis Risk Assessment")
            risk_class = "prediction-high" if crisis_data['risk_level'] == "High" else \
                       "prediction-medium" if crisis_data['risk_level'] == "Medium" else "prediction-low"
            
            st.markdown(f'<div class="{risk_class}" style="padding: 20px; border-radius: 12px;">', unsafe_allow_html=True)
            st.metric("Overall Risk Score", f"{crisis_data['risk_score']:.2%}")
            st.metric("Risk Level", crisis_data['risk_level'])
            if crisis_data['crisis_type']:
                st.metric("Predicted Crisis Type", crisis_data['crisis_type'].title())
            st.metric("Potential Impact", f"${crisis_data['potential_impact']:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Warning signs
            if crisis_data['warning_signs']:
                st.markdown("##### 🚨 Warning Signs Detected")
                for sign in crisis_data['warning_signs']:
                    st.error(f"▪️ {sign}")
        
        with col2:
            st.plotly_chart(create_risk_matrix(crisis_data), use_container_width=True)
            
            # Category risks
            st.markdown("##### Risk by Category")
            for category, risk in crisis_data['category_risks'].items():
                st.write(f"{category.title()}: {risk:.2%}")
                st.progress(risk)
        
        # Recommendations
        st.markdown("##### Preparedness Recommendations")
        for recommendation in crisis_data['recommendations']:
            st.markdown(f'<div class="strategy-recommendation">🔸 {recommendation}</div>', unsafe_allow_html=True)
    
    with tab7:
        st.header("Advanced Brand Health Analytics")
        
        # Simulate brand health data
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        health_scores = np.random.normal(70, 10, 30).clip(0, 100)
        
        # Create brand health chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=health_scores,
            mode='lines+markers',
            name='Brand Health Score',
            line=dict(color='#10B981', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Brand Health Trend (30 Days)',
            xaxis_title='Date',
            yaxis_title='Health Score',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Health metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
            st.metric("Current Health Score", f"{health_scores[-1]:.1f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
            change = health_scores[-1] - health_scores[-2]
            st.metric("30-Day Change", f"{change:+.1f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
            st.metric("Average Score", f"{np.mean(health_scores):.1f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
            st.metric("Volatility", f"{np.std(health_scores):.1f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Health drivers
        st.markdown("##### Brand Health Drivers")
        drivers = [
            {"name": "Brand Sentiment", "score": random.randint(60, 90), "impact": "High"},
            {"name": "Customer Satisfaction", "score": random.randint(65, 95), "impact": "High"},
            {"name": "Market Position", "score": random.randint(50, 85), "impact": "Medium"},
            {"name": "Innovation Perception", "score": random.randint(55, 80), "impact": "Medium"},
            {"name": "Social Presence", "score": random.randint(70, 95), "impact": "Low"},
        ]
        
        for driver in drivers:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(driver['name'])
            with col2:
                st.progress(driver['score'] / 100)
            with col3:
                st.write(f"{driver['score']}% ({driver['impact']} Impact)")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p class="accent-text"><strong>🛡️ Advanced Brand Protection with AI-Driven Business Intelligence</strong></p>
        <p>Powered by Next-Generation Sentiment Analysis, Business Impact Forecasting, and Competitive Strategy Insights</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
