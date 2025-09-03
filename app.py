def show_ai_insights():
    """AI insights functionality with enhanced visualization"""
    st.header("🧠 Neural Intelligence Insights")
    
    # Get user's subscription
    username = st.session_state.get('username')
    
    if not auth_system.check_subscription_feature(username, "advanced_analytics"):
        st.warning("⚠️ This feature requires an Advanced or Premium subscription")
        st.info("Upgrade your plan to access AI-powered insights.")
        return
    
    brand_name = st.session_state.get('brand_name', 'Your Brand')
    
    # AI Processing Animation
    st.markdown("""
    <div class="ai-processing">
        <div class="ai-node"></div>
        <div class="ai-node"></div>
        <div class="ai-node"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate sample analyses
    analyses = []
    for i in range(10):
        text = f"Sample text {i} about {brand_name} with {'high' if i < 3 else 'medium' if i < 6 else 'low'} threat level"
        analysis = ai_engine.detect_threats(text, brand_name)
        analyses.append(analysis)
    
    # Generate report
    report = ai_engine.generate_threat_report(analyses)
    
    # Display report in AI-themed cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="ai-visualization-card">
            <h4>📊 Neural Threat Analysis</h4>
            <p>Total Analyses: {}</p>
            <p>High Threats: {}</p>
            <p>Medium Threats: {}</p>
            <p>Low Threats: {}</p>
            <p>Average Sentiment: {:.2f}</p>
        </div>
        """.format(
            report['total_analyses'],
            report['threat_counts']['high'],
            report['threat_counts']['medium'],
            report['threat_counts']['low'],
            report['average_sentiment']
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="ai-visualization-card">
            <h4>✅ AI Recommendations</h4>
            {}
        </div>
        """.format(
            ''.join([f'<p>• {rec}</p>' for rec in report['recommendations']])
        ), unsafe_allow_html=True)
    
    # Keyword frequency analysis
    st.subheader("🔤 Neural Keyword Analysis")
    
    texts = [a['text'] for a in analyses]
    keyword_freq = ai_engine.create_keyword_frequency(texts)
    
    # Create bar chart with AI theme
    fig = viz.create_keyword_bar_chart(keyword_freq, "Neural Keyword Frequency Analysis")
    st.plotly_chart(fig, use_container_width=True)
    
    # Threat patterns
    st.subheader("🔍 Neural Pattern Recognition")
    
    patterns = ai_engine.create_threat_patterns(analyses)
    
    # Create heatmap with AI theme
    fig = viz.create_pattern_heatmap(patterns, "Neural Threat Pattern Analysis")
    st.plotly_chart(fig, use_container_width=True)
    
    # Pattern details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="ai-visualization-card">
            <h4>🎯 Top Threat Keywords</h4>
            {}
        </div>
        """.format(
            ''.join([f'<p>• {word}: {count}</p>' for word, count in list(patterns['high_threat_keywords'].most_common(5))])
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="ai-visualization-card">
            <h4>📱 Platform Distribution</h4>
            {}
        </div>
        """.format(
            ''.join([f'<p>• {platform}: {count}</p>' for platform, count in patterns['platform_distribution'].most_common()])
        ), unsafe_allow_html=True)
