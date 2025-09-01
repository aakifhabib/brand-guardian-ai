# Add the new animation CSS to the existing CSS block
st.markdown("""
<style>
    /* ... existing CSS ... */
    
    /* Enhanced AI Analysis Animation */
    .ai-analysis-container {
        position: relative;
        width: 100%;
        height: 200px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 20px 0;
    }
    
    .ai-brain {
        position: relative;
        width: 120px;
        height: 120px;
        margin-bottom: 20px;
    }
    
    .brain-icon {
        font-size: 80px;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 2;
        animation: brainPulse 2s infinite ease-in-out;
    }
    
    @keyframes brainPulse {
        0% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        50% { transform: translate(-50%, -50%) scale(1.1); opacity: 0.8; }
        100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
    }
    
    .brain-ring {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: 3px solid rgba(255, 215, 0, 0.7);
        border-radius: 50%;
        animation: ringRotate 3s linear infinite;
    }
    
    @keyframes ringRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .brain-ring:nth-child(2) {
        width: 90%;
        height: 90%;
        top: 5%;
        left: 5%;
        border-color: rgba(255, 165, 0, 0.5);
        animation-duration: 4s;
        animation-direction: reverse;
    }
    
    .brain-ring:nth-child(3) {
        width: 80%;
        height: 80%;
        top: 10%;
        left: 10%;
        border-color: rgba(255, 140, 0, 0.3);
        animation-duration: 5s;
    }
    
    .scan-line {
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.6), transparent);
        animation: scanLine 2s linear infinite;
        z-index: 1;
    }
    
    @keyframes scanLine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .analysis-text {
        font-size: 1.2rem;
        font-weight: 600;
        color: #FFD700;
        text-align: center;
        animation: textBlink 1.5s infinite;
    }
    
    @keyframes textBlink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .analysis-steps {
        display: flex;
        justify-content: center;
        margin-top: 15px;
        width: 100%;
    }
    
    .analysis-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 0 10px;
        opacity: 0.3;
        transition: opacity 0.5s;
    }
    
    .analysis-step.active {
        opacity: 1;
    }
    
    .step-icon {
        font-size: 1.5rem;
        margin-bottom: 5px;
    }
    
    .step-text {
        font-size: 0.8rem;
        color: #FFD700;
    }
    
    .threat-level-indicator {
        display: flex;
        justify-content: space-between;
        width: 80%;
        margin-top: 15px;
        height: 10px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        overflow: hidden;
    }
    
    .threat-level {
        height: 100%;
        width: 0%;
        border-radius: 5px;
        transition: width 1s, background-color 1s;
    }
    
    .threat-level.low {
        background: linear-gradient(90deg, #10B981, #34D399);
    }
    
    .threat-level.medium {
        background: linear-gradient(90deg, #F59E0B, #FBBF24);
    }
    
    .threat-level.high {
        background: linear-gradient(90deg, #EF4444, #F87171);
    }
</style>
""", unsafe_allow_html=True)

# Add the new animation function
def show_threat_analysis_animation():
    """Display an enhanced threat analysis animation"""
    placeholder = st.empty()
    
    with placeholder.container():
        st.markdown("""
        <div class="ai-analysis-container">
            <div class="ai-brain">
                <div class="brain-icon">🧠</div>
                <div class="brain-ring"></div>
                <div class="brain-ring"></div>
                <div class="brain-ring"></div>
                <div class="scan-line"></div>
            </div>
            <div class="analysis-text">AI Analyzing Threats...</div>
            
            <div class="analysis-steps">
                <div class="analysis-step active" id="step1">
                    <div class="step-icon">🔍</div>
                    <div class="step-text">Scanning</div>
                </div>
                <div class="analysis-step" id="step2">
                    <div class="step-icon">🧠</div>
                    <div class="step-text">Processing</div>
                </div>
                <div class="analysis-step" id="step3">
                    <div class="step-icon">📊</div>
                    <div class="step-text">Analyzing</div>
                </div>
                <div class="analysis-step" id="step4">
                    <div class="step-icon">✅</div>
                    <div class="step-text">Complete</div>
                </div>
            </div>
            
            <div class="threat-level-indicator">
                <div class="threat-level" id="threatBar"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # JavaScript to animate the steps and threat level
        st.markdown("""
        <script>
        // Animate analysis steps
        const steps = document.querySelectorAll('.analysis-step');
        const threatBar = document.getElementById('threatBar');
        
        // Function to update active step
        function updateActiveStep(index) {
            steps.forEach((step, i) => {
                if (i <= index) {
                    step.classList.add('active');
                } else {
                    step.classList.remove('active');
                }
            });
        }
        
        // Function to update threat level
        function updateThreatLevel(level) {
            threatBar.style.width = level + '%';
            
            if (level < 33) {
                threatBar.className = 'threat-level low';
            } else if (level < 66) {
                threatBar.className = 'threat-level medium';
            } else {
                threatBar.className = 'threat-level high';
            }
        }
        
        // Animation sequence
        let stepIndex = 0;
        let threatLevel = 0;
        
        const stepInterval = setInterval(() => {
            if (stepIndex < steps.length - 1) {
                updateActiveStep(stepIndex);
                threatLevel = Math.min(threatLevel + 25, 100);
                updateThreatLevel(threatLevel);
                stepIndex++;
            } else {
                clearInterval(stepInterval);
                updateActiveStep(steps.length - 1);
                updateThreatLevel(75); // Final threat level
            }
        }, 800);
        </script>
        """, unsafe_allow_html=True)
    
    return placeholder

# Update the show_search_analysis function to use the new animation
def show_search_analysis():
    """Search analysis functionality"""
    st.subheader("🔍 Advanced Search Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_area(
            "Enter search query or keywords to analyze:",
            height=100,
            placeholder="Example: 'Your Brand scam complaints customer service issues'",
            help="Enter keywords, phrases, or full sentences to analyze for brand threats"
        )
        
        # Get the brand name from session state or use a default
        brand_name = st.session_state.get('brand_name', 'Your Brand')
        
        if st.button("🚀 Analyze Threats", use_container_width=True):
            if search_query and brand_name:
                # Show the enhanced animation
                animation_placeholder = show_threat_analysis_animation()
                
                # Simulate analysis with the animation running
                time.sleep(3.5)  # Allow time for animation to complete
                
                # Clear the animation
                animation_placeholder.empty()
                
                # Perform the actual analysis
                results = search_analyzer.analyze_search(search_query, brand_name)
                st.session_state.search_results = results
                st.success("Analysis complete!")
            else:
                st.error("Please enter both search query and brand name")
    
    # Rest of the function remains the same
    with col2:
        st.markdown("""
        <div class="search-analysis-card">
            <h4>🎯 Search Analysis Tips</h4>
            <p>• Use specific keywords</p>
            <p>• Include brand names</p>
            <p>• Add negative modifiers</p>
            <p>• Use quotation marks for phrases</p>
            <p>• Include platform names</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="search-analysis-card">
            <h4>📊 Threat Levels</h4>
            <p><span class="threat-high">High</span> - Immediate action needed</p>
            <p><span class="threat-medium">Medium</span> - Monitor closely</p>
            <p><span class="threat-low">Low</span> - Standard monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display results if available
    if 'search_results' in st.session_state:
        results = st.session_state.search_results
        
        st.markdown("---")
        st.subheader("📋 Analysis Results")
        
        # Threat level indicator
        threat_class = f"threat-{results['threat_level']}"
        st.markdown(f"""
        <div class="search-analysis-card">
            <h4>Threat Level: <span class="{threat_class}">{results['threat_level'].upper()}</span></h4>
            <p><strong>Query:</strong> {results['query']}</p>
            <p><strong>Brand:</strong> {results['brand']}</p>
            <p><strong>Keywords Found:</strong> {', '.join(results['keywords_found']) or 'None'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Analysis and recommendations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="search-analysis-card">
                <h4>📝 Analysis</h4>
                <p>{results['analysis']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="search-analysis-card">
                <h4>✅ Recommendations</h4>
                {''.join([f'<p>• {rec}</p>' for rec in results['recommendations']])}
            </div>
            """, unsafe_allow_html=True)
        
        # Similar threat examples
        st.subheader("🔍 Similar Threat Patterns")
        similar_threats = generate_similar_threats(results)
        for threat in similar_threats:
            st.markdown(f"""
            <div class="search-result-card">
                <p><strong>{threat['platform']}</strong> - {threat['content']}</p>
                <p>Severity: <span class="threat-{threat['severity']}">{threat['severity']}</span></p>
            </div>
            """, unsafe_allow_html=True)

# The rest of the code remains unchanged
