# Add these new classes and functions after the existing imports

class BrandHealthAnalyzer:
    def __init__(self):
        self.metrics = {
            'sentiment': {'weight': 0.3, 'current': 0.75},
            'engagement': {'weight': 0.25, 'current': 0.82},
            'reach': {'weight': 0.2, 'current': 0.68},
            'reputation': {'weight': 0.15, 'current': 0.91},
            'loyalty': {'weight': 0.1, 'current': 0.77}
        }
    
    def calculate_health_score(self):
        total_score = sum(metric['current'] * metric['weight'] for metric in self.metrics.values())
        return round(total_score * 100, 1)
    
    def get_health_grade(self, score):
        if score >= 90:
            return "Excellent", "#10B981"
        elif score >= 75:
            return "Good", "#3B82F6"
        elif score >= 60:
            return "Fair", "#F59E0B"
        else:
            return "Poor", "#EF4444"
    
    def generate_metrics_data(self, days=30):
        dates = pd.date_range(end=datetime.now(), periods=days)
        data = {
            'Date': dates,
            'Sentiment': np.random.normal(0.75, 0.1, days),
            'Engagement': np.random.normal(0.82, 0.08, days),
            'Reach': np.random.normal(0.68, 0.12, days),
            'Reputation': np.random.normal(0.91, 0.05, days),
            'Loyalty': np.random.normal(0.77, 0.09, days)
        }
        return pd.DataFrame(data)

class CompetitorAnalyzer:
    def __init__(self):
        self.competitors = ["Competitor A", "Competitor B", "Competitor C"]
    
    def generate_comparison_data(self, brand_name):
        metrics = ['Sentiment', 'Engagement', 'Reach', 'Mentions', 'Growth']
        data = {
            'Metric': metrics,
            brand_name: np.random.uniform(0.6, 0.95, len(metrics)),
            **{comp: np.random.uniform(0.5, 0.9, len(metrics)) for comp in self.competitors}
        }
        return pd.DataFrame(data)

class CrisisManager:
    def __init__(self):
        self.crisis_levels = {
            'low': {
                'name': 'Low Impact',
                'color': '#10B981',
                'response_time': '24 hours',
                'team': 'Social Media Team'
            },
            'medium': {
                'name': 'Medium Impact',
                'color': '#F59E0B',
                'response_time': '4 hours',
                'team': 'PR Team'
            },
            'high': {
                'name': 'High Impact',
                'color': '#EF4444',
                'response_time': '1 hour',
                'team': 'Crisis Management Team'
            },
            'critical': {
                'name': 'Critical Impact',
                'color': '#8B0000',
                'response_time': '30 minutes',
                'team': 'Executive Team'
            }
        }
        self.response_templates = {
            'negative_review': "We appreciate your feedback and take your concerns seriously. Our team is investigating this matter and will reach out to you directly to resolve this issue.",
            'product_issue': "We're aware of the issue you've reported and our technical team is working on a solution. We apologize for any inconvenience caused and appreciate your patience.",
            'misinformation': "We'd like to clarify that the information circulating is inaccurate. Here are the facts: [insert facts]. We're committed to transparency and accuracy.",
            'crisis': "We're aware of the situation and are taking immediate action. Our priority is the safety and well-being of our customers. We'll provide updates as soon as they're available."
        }
    
    def assess_crisis_level(self, threat_count, sentiment_score, reach):
        score = (threat_count * 0.5) + ((1 - sentiment_score) * 0.3) + (reach * 0.2)
        
        if score >= 0.8:
            return 'critical'
        elif score >= 0.6:
            return 'high'
        elif score >= 0.4:
            return 'medium'
        else:
            return 'low'
    
    def get_response_plan(self, level):
        crisis_info = self.crisis_levels.get(level, self.crisis_levels['low'])
        return {
            'level': crisis_info['name'],
            'color': crisis_info['color'],
            'response_time': crisis_info['response_time'],
            'team': crisis_info['team'],
            'actions': self.get_response_actions(level)
        }
    
    def get_response_actions(self, level):
        actions = {
            'low': [
                "Monitor situation closely",
                "Prepare response templates",
                "Inform customer service team"
            ],
            'medium': [
                "Activate social media monitoring",
                "Prepare holding statement",
                "Notify PR team",
                "Monitor competitor responses"
            ],
            'high': [
                "Activate crisis communication plan",
                "Prepare official statement",
                "Notify executive team",
                "Schedule press briefing",
                "Monitor all channels"
            ],
            'critical': [
                "Activate full crisis response team",
                "Issue immediate statement",
                "Executive press conference",
                "Continuous monitoring",
                "Stakeholder notifications",
                "Legal team consultation"
            ]
        }
        return actions.get(level, actions['low'])

class ReportGenerator:
    def __init__(self):
        self.report_templates = {
            'executive': {
                'title': 'Executive Brand Protection Report',
                'sections': ['Executive Summary', 'Threat Landscape', 'Brand Health', 'Competitive Analysis', 'Recommendations']
            },
            'threat': {
                'title': 'Threat Intelligence Report',
                'sections': ['Threat Overview', 'High-Alert Items', 'Thrend Analysis', 'Mitigation Strategies']
            },
            'comprehensive': {
                'title': 'Comprehensive Brand Protection Report',
                'sections': ['Executive Summary', 'Threat Analysis', 'Brand Health Metrics', 'Competitive Intelligence', 'Crisis Preparedness', 'Action Plan']
            }
        }
    
    def generate_html_report(self, report_type, data, brand_name):
        template = self.report_templates.get(report_type, self.report_templates['comprehensive'])
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{template['title']} - {brand_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%); color: #FFD700; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 30px; }}
                .section {{ margin-bottom: 30px; padding: 20px; border-left: 4px solid #FFD700; background: #f9f9f9; }}
                .metric {{ display: inline-block; margin: 10px; padding: 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; min-width: 150px; }}
                .metric-value {{ font-size: 2em; font-weight: bold; color: #FFD700; }}
                .threat-high {{ color: #EF4444; font-weight: bold; }}
                .threat-medium {{ color: #F59E0B; font-weight: bold; }}
                .threat-low {{ color: #10B981; font-weight: bold; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
                .footer {{ text-align: center; margin-top: 40px; font-size: 0.9em; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{template['title']}</h1>
                <h2>{brand_name}</h2>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
        """
        
        # Add sections based on report type
        for section in template['sections']:
            html += f"""
            <div class="section">
                <h2>{section}</h2>
            """
            
            if section == 'Executive Summary':
                html += f"""
                <p>This report provides a comprehensive analysis of {brand_name}'s brand protection status as of {datetime.now().strftime('%Y-%m-%d')}.</p>
                <p>Key findings include {data.get('summary', 'a stable brand protection environment with minor threats detected')}.</p>
                """
            elif section == 'Threat Landscape':
                html += self._generate_threat_section(data)
            elif section == 'Brand Health':
                html += self._generate_brand_health_section(data)
            elif section == 'Competitive Analysis':
                html += self._generate_competitive_section(data)
            elif section == 'Recommendations':
                html += self._generate_recommendations_section(data)
            
            html += "</div>"
        
        html += """
            <div class="footer">
                <p>Generated by BrandGuardian AI Pro</p>
                <p>Confidential - For Internal Use Only</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _generate_threat_section(self, data):
        threats = data.get('threats', {
            'high': 3,
            'medium': 7,
            'low': 12
        })
        
        return f"""
        <h3>Threat Distribution</h3>
        <div class="metric">
            <div class="metric-value">{threats['high']}</div>
            <div>High Threats</div>
        </div>
        <div class="metric">
            <div class="metric-value">{threats['medium']}</div>
            <div>Medium Threats</div>
        </div>
        <div class="metric">
            <div class="metric-value">{threats['low']}</div>
            <div>Low Threats</div>
        </div>
        <p>Threat activity has been {data.get('threat_trend', 'stable')} over the past week.</p>
        """
    
    def _generate_brand_health_section(self, data):
        health_score = data.get('health_score', 78.5)
        grade, color = data.get('health_grade', ("Good", "#3B82F6"))
        
        return f"""
        <h3>Brand Health Score</h3>
        <div class="metric">
            <div class="metric-value" style="color: {color};">{health_score}%</div>
            <div>Overall Health</div>
        </div>
        <div class="metric">
            <div class="metric-value">{grade}</div>
            <div>Health Grade</div>
        </div>
        <p>Brand health is {data.get('health_trend', 'improving')} compared to last month.</p>
        """
    
    def _generate_competitive_section(self, data):
        competitors = data.get('competitors', ["Competitor A", "Competitor B"])
        
        html = """
        <h3>Competitive Position</h3>
        <table>
            <tr>
                <th>Competitor</th>
                <th>Sentiment</th>
                <th>Engagement</th>
                <th>Market Share</th>
            </tr>
        """
        
        for comp in competitors:
            html += f"""
            <tr>
                <td>{comp}</td>
                <td>{random.uniform(0.6, 0.9):.1%}</td>
                <td>{random.uniform(0.5, 0.8):.1%}</td>
                <td>{random.uniform(10, 30):.1f}%</td>
            </tr>
            """
        
        html += "</table>"
        return html
    
    def _generate_recommendations_section(self, data):
        recommendations = data.get('recommendations', [
            "Continue monitoring high-priority threats",
            "Increase engagement on underperforming platforms",
            "Review crisis response protocols"
        ])
        
        html = "<h3>Key Recommendations</h3><ul>"
        for rec in recommendations:
            html += f"<li>{rec}</li>"
        html += "</ul>"
        return html

class ActivityLogger:
    def __init__(self):
        self.log_file = "user_activity.log"
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write("timestamp,user_id,action,details\n")
    
    def log_activity(self, user_id, action, details=""):
        timestamp = datetime.now().isoformat()
        with open(self.log_file, 'a') as f:
            f.write(f"{timestamp},{user_id},{action},{details}\n")
    
    def get_activity_logs(self, user_id=None, limit=100):
        logs = []
        with open(self.log_file, 'r') as f:
            next(f)  # Skip header
            for line in f:
                parts = line.strip().split(',', 3)
                if len(parts) >= 3:
                    timestamp, log_user_id, action = parts[:3]
                    details = parts[3] if len(parts) > 3 else ""
                    
                    if user_id is None or log_user_id == user_id:
                        logs.append({
                            'timestamp': timestamp,
                            'user_id': log_user_id,
                            'action': action,
                            'details': details
                        })
        
        # Sort by timestamp (newest first) and limit
        logs.sort(key=lambda x: x['timestamp'], reverse=True)
        return logs[:limit]

# Initialize new components
brand_health_analyzer = BrandHealthAnalyzer()
competitor_analyzer = CompetitorAnalyzer()
crisis_manager = CrisisManager()
report_generator = ReportGenerator()
activity_logger = ActivityLogger()

# Add these new functions after existing functions

def show_threat_intelligence():
    st.header("🛡️ Threat Intelligence Dashboard")
    
    # Threat metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Active Threats</h3>
            <h1>24</h1>
            <p style="color: #FF0000;">+3 from yesterday</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Threat Level</h3>
            <h1>Medium</h1>
            <p style="color: #FFA500;">Elevated risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Response Time</h3>
            <h1>1.8s</h1>
            <p style="color: #FFD700;">-0.2s improvement</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Protected Assets</h3>
            <h1>32</h1>
            <p style="color: #FFD700;">Fully secured</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Threat timeline
    st.subheader("📈 Threat Activity Timeline")
    
    dates = pd.date_range(end=datetime.now(), periods=14)
    high_threats = np.random.poisson(3, 14)
    medium_threats = np.random.poisson(7, 14)
    low_threats = np.random.poisson(12, 14)
    
    threat_data = pd.DataFrame({
        'Date': dates,
        'High Threats': high_threats,
        'Medium Threats': medium_threats,
        'Low Threats': low_threats
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=threat_data['Date'],
        y=threat_data['High Threats'],
        mode='lines+markers',
        name='High Threats',
        line=dict(color='#EF4444', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=threat_data['Date'],
        y=threat_data['Medium Threats'],
        mode='lines+markers',
        name='Medium Threats',
        line=dict(color='#F59E0B', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=threat_data['Date'],
        y=threat_data['Low Threats'],
        mode='lines+markers',
        name='Low Threats',
        line=dict(color='#10B981', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Threat Activity Over Time",
        title_x=0.5,
        xaxis_title='Date',
        yaxis_title='Number of Threats',
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Threat distribution
    st.subheader("🌡️ Threat Distribution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        threat_data = {'High': 8, 'Medium': 12, 'Low': 24}
        fig = viz.create_threat_distribution(threat_data, "Threat Severity Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="search-analysis-card">
            <h4>📊 Threat Insights</h4>
            <p><span class="threat-high">High</span>: 8 threats detected</p>
            <p><span class="threat-medium">Medium</span>: 12 threats detected</p>
            <p><span class="threat-low">Low</span>: 24 threats detected</p>
            <p>Most active platform: Twitter</p>
            <p>Peak time: 14:00-16:00</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent threats
    st.subheader("🚨 Recent Threat Alerts")
    
    threat_alerts = []
    threat_types = ['Impersonation', 'Negative Review', 'Fake Account', 'Copyright', 'Data Leak', 'Phishing']
    platforms = ['Twitter', 'Facebook', 'Reddit', 'Instagram', 'LinkedIn', 'Dark Web']
    
    for i in range(10):
        threat_alerts.append({
            'Time': (datetime.now() - timedelta(hours=i*2)).strftime("%Y-%m-%d %H:%M"),
            'Platform': random.choice(platforms),
            'Type': random.choice(threat_types),
            'Severity': random.choice(['High', 'Medium', 'Low']),
            'Status': random.choice(['Active', 'Resolved', 'Monitoring']),
            'Description': f"Detected {random.choice(threat_types).lower()} related to brand"
        })
    
    alert_df = pd.DataFrame(threat_alerts)
    st.dataframe(
        alert_df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Time": st.column_config.TextColumn("Time", width="medium"),
            "Platform": st.column_config.TextColumn("Platform", width="small"),
            "Type": st.column_config.TextColumn("Type", width="medium"),
            "Severity": st.column_config.TextColumn("Severity", width="small"),
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Description": st.column_config.TextColumn("Description", width="large")
        }
    )

def show_brand_health():
    st.header("❤️ Brand Health Metrics")
    
    # Calculate health score
    health_score = brand_health_analyzer.calculate_health_score()
    grade, color = brand_health_analyzer.get_health_grade(health_score)
    
    # Display health score
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <h3>Brand Health Score</h3>
            <h1 style="color: {color};">{health_score}%</h1>
            <p style="color: {color}; font-weight: bold;">{grade}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>Health Components</h4>
        """, unsafe_allow_html=True)
        
        for metric, data in brand_health_analyzer.metrics.items():
            st.write(f"**{metric.title()}**: {data['current']:.1%}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Health trends
    st.subheader("📈 Health Trends (30 Days)")
    
    metrics_data = brand_health_analyzer.generate_metrics_data(30)
    
    fig = go.Figure()
    
    for metric in ['Sentiment', 'Engagement', 'Reach', 'Reputation', 'Loyalty']:
        fig.add_trace(go.Scatter(
            x=metrics_data['Date'],
            y=metrics_data[metric],
            mode='lines+markers',
            name=metric,
            line=dict(width=2),
            marker=dict(size=4)
        ))
    
    fig.update_layout(
        title="Brand Health Metrics Over Time",
        title_x=0.5,
        xaxis_title='Date',
        yaxis_title='Score',
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Health radar chart
    st.subheader("📊 Health Radar Chart")
    
    radar_data = [data['current'] for data in brand_health_analyzer.metrics.values()]
    radar_labels = list(brand_health_analyzer.metrics.keys())
    
    fig = viz.create_radar_chart(radar_data, radar_labels, "Brand Health Components")
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("💡 Health Improvement Recommendations")
    
    recommendations = [
        "Increase engagement on underperforming platforms",
        "Address negative sentiment with targeted campaigns",
        "Expand reach through influencer partnerships",
        "Enhance reputation management strategies",
        "Implement customer loyalty programs"
    ]
    
    for rec in recommendations:
        st.markdown(f"""
        <div class="search-result-card">
            <p>{rec}</p>
        </div>
        """, unsafe_allow_html=True)

def show_competitor_analysis():
    st.header("🥊 Competitive Intelligence")
    
    brand_name = st.session_state.get('brand_name', 'Your Brand')
    
    # Get comparison data
    comparison_data = competitor_analyzer.generate_comparison_data(brand_name)
    
    # Display comparison chart
    st.subheader("📊 Competitive Comparison")
    
    fig = go.Figure()
    
    metrics = comparison_data['Metric']
    
    for col in comparison_data.columns:
        if col != 'Metric':
            fig.add_trace(go.Bar(
                name=col,
                x=metrics,
                y=comparison_data[col],
                marker_color='#FFD700' if col == brand_name else '#FFA500'
            ))
    
    fig.update_layout(
        title="Brand vs Competitors",
        title_x=0.5,
        xaxis_title='Metrics',
        yaxis_title='Score',
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Market share visualization
    st.subheader("🌐 Market Share Analysis")
    
    market_share = {
        brand_name: random.uniform(25, 40),
        'Competitor A': random.uniform(15, 30),
        'Competitor B': random.uniform(10, 25),
        'Competitor C': random.uniform(5, 20),
        'Others': random.uniform(10, 25)
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=list(market_share.keys()),
        values=list(market_share.values()),
        hole=0.4,
        textinfo='label+percent',
        textposition='auto'
    )])
    
    fig.update_layout(
        title="Market Share Distribution",
        title_x=0.5,
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Competitor threat analysis
    st.subheader("⚠️ Competitor Threat Assessment")
    
    threat_data = []
    for comp in competitor_analyzer.competitors:
        threat_level = random.choice(['Low', 'Medium', 'High'])
        threat_data.append({
            'Competitor': comp,
            'Threat Level': threat_level,
            'Market Position': random.choice(['Challenger', 'Follower', 'Leader']),
            'Recent Activity': random.choice(['Product Launch', 'Marketing Campaign', 'Price Change', 'Partnership'])
        })
    
    threat_df = pd.DataFrame(threat_data)
    st.dataframe(threat_df, use_container_width=True, hide_index=True)
    
    # Strategic recommendations
    st.subheader("🎯 Strategic Recommendations")
    
    recommendations = [
        "Monitor Competitor A's new product developments",
        "Counter Competitor B's marketing campaigns with targeted messaging",
        "Leverage strengths against Competitor C's weaknesses",
        "Expand into markets where competitors have low presence",
        "Form strategic partnerships to counter competitive threats"
    ]
    
    for rec in recommendations:
        st.markdown(f"""
        <div class="search-result-card">
            <p>{rec}</p>
        </div>
        """, unsafe_allow_html=True)

def show_crisis_management():
    st.header("🛡️ Crisis Management Center")
    
    # Crisis assessment
    st.subheader("📊 Current Crisis Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        threat_count = st.number_input("Active Threats", min_value=0, value=5)
    
    with col2:
        sentiment_score = st.slider("Sentiment Score", 0.0, 1.0, 0.4)
    
    with col3:
        reach = st.slider("Reach Impact", 0.0, 1.0, 0.7)
    
    # Assess crisis level
    crisis_level = crisis_manager.assess_crisis_level(threat_count, sentiment_score, reach)
    response_plan = crisis_manager.get_response_plan(crisis_level)
    
    # Display crisis level
    st.markdown(f"""
    <div class="search-analysis-card" style="border-left: 5px solid {response_plan['color']};">
        <h4>Crisis Level: {response_plan['level']}</h4>
        <p><strong>Response Time:</strong> {response_plan['response_time']}</p>
        <p><strong>Response Team:</strong> {response_plan['team']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Response actions
    st.subheader("🚀 Response Actions")
    
    for action in response_plan['actions']:
        st.markdown(f"""
        <div class="search-result-card">
            <p>{action}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Response templates
    st.subheader("📝 Response Templates")
    
    template_type = st.selectbox("Select Template Type", list(crisis_manager.response_templates.keys()))
    
    template_text = crisis_manager.response_templates[template_type]
    
    st.text_area("Template", value=template_text, height=150, disabled=True)
    
    if st.button("Use Template", use_container_width=True):
        st.success("Template copied to clipboard!")
    
    # Crisis simulation
    st.subheader("🎭 Crisis Simulation")
    
    if st.button("Run Crisis Simulation", use_container_width=True):
        with st.spinner("Simulating crisis scenario..."):
            time.sleep(2)
            
            # Generate simulation results
            simulation_results = {
                'scenario': random.choice(['Product Recall', 'Data Breach', 'Executive Scandal', 'Negative Viral Campaign']),
                'impact': random.choice(['Low', 'Medium', 'High', 'Critical']),
                'duration': f"{random.randint(1, 14)} days",
                'reputation_damage': f"-{random.randint(5, 30)}%",
                'financial_impact': f"${random.randint(10000, 500000):,}"
            }
            
            st.markdown(f"""
            <div class="search-analysis-card">
                <h4>Simulation Results</h4>
                <p><strong>Scenario:</strong> {simulation_results['scenario']}</p>
                <p><strong>Impact Level:</strong> {simulation_results['impact']}</p>
                <p><strong>Estimated Duration:</strong> {simulation_results['duration']}</p>
                <p><strong>Reputation Damage:</strong> {simulation_results['reputation_damage']}</p>
                <p><strong>Financial Impact:</strong> {simulation_results['financial_impact']}</p>
            </div>
            """, unsafe_allow_html=True)

def show_report_generation():
    st.header("📊 Report Generation")
    
    # Report configuration
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox("Report Type", [
            "executive", "threat", "comprehensive"
        ], format_func=lambda x: x.title())
    
    with col2:
        date_range = st.selectbox("Date Range", [
            "Last 7 Days", "Last 30 Days", "Last 90 Days", "Custom"
        ])
    
    # Report content options
    st.subheader("📋 Report Content")
    
    include_threats = st.checkbox("Include Threat Analysis", value=True)
    include_health = st.checkbox("Include Brand Health Metrics", value=True)
    include_competitors = st.checkbox("Include Competitive Intelligence", value=True)
    include_recommendations = st.checkbox("Include Recommendations", value=True)
    
    # Generate report button
    if st.button("Generate Report", use_container_width=True):
        with st.spinner("Generating report..."):
            time.sleep(2)
            
            # Prepare report data
            brand_name = st.session_state.get('brand_name', 'Your Brand')
            
            report_data = {
                'summary': 'a stable brand protection environment with minor threats detected',
                'threats': {'high': 3, 'medium': 7, 'low': 12},
                'threat_trend': 'stable',
                'health_score': brand_health_analyzer.calculate_health_score(),
                'health_grade': brand_health_analyzer.get_health_grade(brand_health_analyzer.calculate_health_score()),
                'health_trend': 'improving',
                'competitors': competitor_analyzer.competitors,
                'recommendations': [
                    "Continue monitoring high-priority threats",
                    "Increase engagement on underperforming platforms",
                    "Review crisis response protocols"
                ]
            }
            
            # Generate HTML report
            html_report = report_generator.generate_html_report(report_type, report_data, brand_name)
            
            # Create download button
            st.success("Report generated successfully!")
            
            # Display report preview
            st.subheader("📄 Report Preview")
            st.components.v1.html(html_report, height=500, scrolling=True)
            
            # Download button
            st.download_button(
                label="Download Report",
                data=html_report,
                file_name=f"{brand_name}_brand_report_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html"
            )
            
            # Log activity
            activity_logger.log_activity(
                st.session_state.get('user_id', 'unknown'),
                "Generated Report",
                f"Type: {report_type}, Date Range: {date_range}"
            )

def show_activity_logs():
    st.header("📋 User Activity Logs")
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        user_filter = st.selectbox("Filter by User", ["All Users"] + list(auth_system.users.keys()))
    
    with col2:
        limit = st.number_input("Number of Records", min_value=10, max_value=500, value=100)
    
    # Get activity logs
    user_id = None if user_filter == "All Users" else user_filter
    logs = activity_logger.get_activity_logs(user_id=user_id, limit=limit)
    
    # Display logs
    if logs:
        log_df = pd.DataFrame(logs)
        st.dataframe(log_df, use_container_width=True, hide_index=True)
    else:
        st.info("No activity logs found")
    
    # Export logs
    if st.button("Export Logs", use_container_width=True):
        if logs:
            # Create CSV content
            csv_content = "timestamp,user_id,action,details\n"
            for log in logs:
                csv_content += f"{log['timestamp']},{log['user_id']},{log['action']},{log['details']}\n"
            
            # Create download button
            st.download_button(
                label="Download Activity Logs",
                data=csv_content,
                file_name=f"activity_logs_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No logs to export")

# Update the main function to include new tabs

def main():
    # Add animated particles
    add_particles()
    
    # Check authentication first
    if not st.session_state.get('authenticated', False):
        show_login_form()
        return
    
    # Initialize session state
    if "sector" not in st.session_state:
        st.session_state.sector = "technology"
    if "brand_name" not in st.session_state:
        st.session_state.brand_name = "Your Brand"
    
    # Set user subscription in session state
    username = st.session_state.get('username')
    if username and "user_subscription" not in st.session_state:
        st.session_state.user_subscription = auth_system.get_user_subscription(username)
    
    # Header with new generation logo design
    st.markdown("""
    <div class="logo-container">
        <div class="logo-shield">
            <div class="shield-base"></div>
            <div class="shield-inner">
                <div class="shield-icon">🛡️</div>
            </div>
            <div class="shield-ring"></div>
        </div>
        <div class="logo-text">
            <div class="logo-main">BRANDGUARDIAN</div>
            <div class="logo-subtitle">AI PRO</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;" class="accent-text">Advanced Business Intelligence & Digital Risk Protection</div>
    """, unsafe_allow_html=True)
    
    # Sidebar with user info and logout button
    with st.sidebar:
        # User info
        subscription_info = auth_system.subscription_plans[st.session_state.user_subscription]
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 3rem;">👤</div>
            <h3>{st.session_state.username}</h3>
            <p>{st.session_state.get('user_access_level', 'user').title()} Access</p>
            <p>{auth_system.users[st.session_state.username]['company']}</p>
            <div style="background-color: {subscription_info['color']}20; 
                        border: 1px solid {subscription_info['color']}; 
                        border-radius: 20px; padding: 8px 16px; margin-top: 10px; display: inline-block;">
                <span style="color: {subscription_info['color']}; font-weight: bold;">
                    {subscription_info['name']} Subscription
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.header("Business Configuration")
        brand_name = st.text_input("Brand Name", st.session_state.brand_name)
        st.session_state.brand_name = brand_name
        
        sector = st.selectbox("Business Sector", ["technology", "finance", "retail"])
        st.session_state.sector = sector
        
        st.markdown("---")
        st.subheader("🔐 Access Status")
        if st.session_state.user_subscription == "premium":
            st.success("✅ Premium Access")
            st.markdown('<span class="premium-badge">PREMIUM</span>', unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ {subscription_info['name']} Access")
        
        st.markdown("---")
        user_id = st.session_state.get('user_id')
        api_keys = api_manager.load_api_keys(user_id) if user_id else {}
        st.subheader("🔑 API Status")
        st.info(f"{len(api_keys)} platform(s) connected")
        
        # User management for admin only
        if st.session_state.get('user_access_level') == 'admin':
            st.markdown("---")
            if st.button("👥 User Management", use_container_width=True):
                st.session_state.show_user_management = True
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Show user management if admin clicked the button
    if st.session_state.get('show_user_management', False):
        show_user_management()
        if st.button("Back to Dashboard", use_container_width=True):
            st.session_state.show_user_management = False
            st.rerun()
        return
    
    # Different navigation based on user role
    if st.session_state.get('user_access_level') == 'admin':
        # Admin navigation with new tabs
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
            "📊 Executive Dashboard", 
            "🔍 Threat Intelligence",
            "❤️ Brand Health",
            "🥊 Competitive Analysis",
            "🛡️ Crisis Management",
            "📱 Social Monitoring",
            "🌟 Influencer Network",
            "📊 Report Generation",
            "📋 Activity Logs",
            "🔑 API Management"
        ])
        
        with tab1:
            st.header("Executive Dashboard")
            st.write("Overview dashboard content...")
        
        with tab2:
            show_threat_intelligence()
        
        with tab3:
            show_brand_health()
        
        with tab4:
            show_competitor_analysis()
        
        with tab5:
            show_crisis_management()
        
        with tab6:
            st.header("Social Monitoring")
            posts = enhanced_monitor.simulate_monitoring_with_api(brand_name, st.session_state.sector)
            for post in posts[:5]:
                with st.expander(f"{post['platform']} - {post['content'][:50]}..."):
                    st.write(post['content'])
                    st.caption(f"Engagement: {post['engagement']}")
        
        with tab7:
            st.header("Influencer Network")
            st.write("Influencer network analysis content...")
        
        with tab8:
            show_report_generation()
        
        with tab9:
            show_activity_logs()
        
        with tab10:
            show_api_key_management()
    else:
        # Regular user navigation
        show_user_ai_dashboard()

if __name__ == "__main__":
    main()
