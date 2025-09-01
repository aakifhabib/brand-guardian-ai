# Add subscription management to the EnhancedAuthenticationSystem class
class EnhancedAuthenticationSystem:
    def __init__(self):
        # ... existing initialization code ...
        self.subscription_plans = {
            "basic": {
                "name": "Basic",
                "price": "$99/month",
                "features": [
                    "Basic threat monitoring",
                    "3 social platforms",
                    "100 API calls/day",
                    "Standard reports",
                    "Email support"
                ],
                "color": "#3B82F6"
            },
            "advanced": {
                "name": "Advanced",
                "price": "$299/month",
                "features": [
                    "All Basic features",
                    "5 social platforms",
                    "500 API calls/day",
                    "Advanced analytics",
                    "Priority support",
                    "Custom alerts"
                ],
                "color": "#8B5CF6"
            },
            "premium": {
                "name": "Premium",
                "price": "$599/month",
                "features": [
                    "All Advanced features",
                    "Unlimited platforms",
                    "Unlimited API calls",
                    "Real-time monitoring",
                    "Dedicated account manager",
                    "Custom integrations"
                ],
                "color": "#FFD700"
            }
        }
        # ... rest of initialization ...
    
    def update_user_subscription(self, username, subscription_plan):
        """Update a user's subscription plan"""
        if username in self.users and subscription_plan in self.subscription_plans:
            self.users[username]["subscription"] = subscription_plan
            self.users[username]["subscription_updated"] = datetime.now().isoformat()
            self.save_users()
            return True
        return False
    
    def get_user_subscription(self, username):
        """Get a user's subscription plan"""
        if username in self.users:
            return self.users[username].get("subscription", "basic")
        return "basic"
    
    def check_subscription_feature(self, username, feature):
        """Check if a user's subscription includes a specific feature"""
        subscription = self.get_user_subscription(username)
        
        # Define feature access by subscription level
        feature_access = {
            "basic": ["basic_monitoring", "standard_reports", "email_support"],
            "advanced": ["basic_monitoring", "standard_reports", "email_support", 
                         "advanced_analytics", "priority_support", "custom_alerts"],
            "premium": ["basic_monitoring", "standard_reports", "email_support",
                        "advanced_analytics", "priority_support", "custom_alerts",
                        "real_time_monitoring", "dedicated_manager", "custom_integrations"]
        }
        
        return feature in feature_access.get(subscription, [])
    
    # ... rest of the class ...

# Update the show_user_management function to include subscription management
def show_user_management():
    st.subheader("👥 User Management")
    
    # Check if user is admin
    if st.session_state.get('user_access_level') != 'admin':
        st.error("⛔ Administrator access required")
        st.info("Only administrators can access user management features.")
        return
    
    # Show existing users
    st.write("### Existing Users")
    users_data = []
    for username, user_info in auth_system.users.items():
        subscription = user_info.get("subscription", "basic")
        users_data.append({
            "Username": username,
            "Company": user_info.get("company", "N/A"),
            "Email": user_info.get("email", "N/A"),
            "Access Level": user_info.get("access_level", "client"),
            "Subscription": f"{auth_system.subscription_plans[subscription]['name']} ({subscription})",
            "Last Login": user_info.get("last_login", "Never"),
            "Created": user_info.get("created_at", "N/A")[:10] if user_info.get("created_at") else "N/A"
        })
    
    if users_data:
        st.dataframe(pd.DataFrame(users_data), use_container_width=True)
    else:
        st.info("No users registered yet")
    
    # User registration form
    show_user_registration()
    
    # Subscription management
    st.markdown("---")
    st.subheader("💳 Subscription Management")
    
    user_to_manage = st.selectbox("Select User to Update Subscription", list(auth_system.users.keys()))
    
    if user_to_manage:
        current_subscription = auth_system.get_user_subscription(user_to_manage)
        
        st.write(f"Current Subscription: **{auth_system.subscription_plans[current_subscription]['name']}**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background-color: {auth_system.subscription_plans['basic']['color']}20; 
                        border: 1px solid {auth_system.subscription_plans['basic']['color']}; 
                        border-radius: 10px; padding: 15px;">
                <h4>{auth_system.subscription_plans['basic']['name']}</h4>
                <p>{auth_system.subscription_plans['basic']['price']}</p>
                <ul>
                    {"".join([f"<li>{feature}</li>" for feature in auth_system.subscription_plans['basic']['features']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Set Basic", key=f"basic_{user_to_manage}"):
                auth_system.update_user_subscription(user_to_manage, "basic")
                st.success(f"Updated {user_to_manage} to Basic subscription")
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div style="background-color: {auth_system.subscription_plans['advanced']['color']}20; 
                        border: 1px solid {auth_system.subscription_plans['advanced']['color']}; 
                        border-radius: 10px; padding: 15px;">
                <h4>{auth_system.subscription_plans['advanced']['name']}</h4>
                <p>{auth_system.subscription_plans['advanced']['price']}</p>
                <ul>
                    {"".join([f"<li>{feature}</li>" for feature in auth_system.subscription_plans['advanced']['features']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Set Advanced", key=f"advanced_{user_to_manage}"):
                auth_system.update_user_subscription(user_to_manage, "advanced")
                st.success(f"Updated {user_to_manage} to Advanced subscription")
                st.rerun()
        
        with col3:
            st.markdown(f"""
            <div style="background-color: {auth_system.subscription_plans['premium']['color']}20; 
                        border: 1px solid {auth_system.subscription_plans['premium']['color']}; 
                        border-radius: 10px; padding: 15px;">
                <h4>{auth_system.subscription_plans['premium']['name']}</h4>
                <p>{auth_system.subscription_plans['premium']['price']}</p>
                <ul>
                    {"".join([f"<li>{feature}</li>" for feature in auth_system.subscription_plans['premium']['features']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Set Premium", key=f"premium_{user_to_manage}"):
                auth_system.update_user_subscription(user_to_manage, "premium")
                st.success(f"Updated {user_to_manage} to Premium subscription")
                st.rerun()
    
    # User actions (delete, reset password)
    st.markdown("---")
    st.subheader("User Actions")
    
    user_to_manage = st.selectbox("Select User for Actions", list(auth_system.users.keys()))
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Reset Password", use_container_width=True):
            if user_to_manage:
                # In a real application, you would send a password reset email
                st.info(f"Password reset initiated for {user_to_manage}. An email has been sent with instructions.")
    
    with col2:
        if st.button("Delete User", use_container_width=True, type="secondary"):
            if user_to_manage and user_to_manage != st.session_state.username:
                if st.checkbox(f"Confirm deletion of {user_to_manage}"):
                    del auth_system.users[user_to_manage]
                    auth_system.save_users()
                    st.success(f"User {user_to_manage} deleted")
                    st.rerun()
            elif user_to_manage == st.session_state.username:
                st.error("You cannot delete your own account")

# Update the show_user_ai_dashboard function to check subscription features
def show_user_ai_dashboard():
    st.header("🤖 BrandGuardian AI Dashboard")
    
    # Get user's subscription
    username = st.session_state.get('username')
    subscription = auth_system.get_user_subscription(username)
    subscription_info = auth_system.subscription_plans[subscription]
    
    # Welcome message with subscription info
    brand_name = st.session_state.get('brand_name', 'Your Brand')
    st.success(f"Welcome to your brand protection dashboard, {brand_name}!")
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="background-color: {subscription_info['color']}20; 
                    border: 1px solid {subscription_info['color']}; 
                    border-radius: 20px; padding: 8px 16px; margin-right: 15px;">
            <span style="color: {subscription_info['color']}; font-weight: bold;">
                {subscription_info['name']} Subscription
            </span>
        </div>
        <div>
            <a href="#upgrade" style="color: #FFD700; text-decoration: none;">Upgrade Plan →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Brand Mentions</h3>
            <h1>142</h1>
            <p style="color: #FFD700;">+12 from last week</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Threat Level</h3>
            <h1>Low</h1>
            <p style="color: #FFD700;">Stable</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Response Rate</h3>
            <h1>92%</h1>
            <p style="color: #FFD700;">Excellent</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Create tabs based on subscription
    available_tabs = ["Search Analysis"]  # Available to all subscriptions
    
    if auth_system.check_subscription_feature(username, "advanced_analytics"):
        available_tabs.append("Social Monitoring")
        available_tabs.append("AI Insights")
    
    if auth_system.check_subscription_feature(username, "real_time_monitoring"):
        available_tabs.append("Advanced Threat Analysis")
    
    # Create the tab navigation
    tabs = st.tabs([f"🔍 {tab}" for tab in available_tabs])
    
    # Display tab content
    for i, tab_name in enumerate(available_tabs):
        with tabs[i]:
            if tab_name == "Search Analysis":
                show_search_analysis()
            elif tab_name == "Social Monitoring":
                show_social_monitoring()
            elif tab_name == "AI Insights":
                show_ai_insights()
            elif tab_name == "Advanced Threat Analysis":
                show_advanced_threat_analysis()
    
    # Subscription upgrade section
    st.markdown("---")
    st.subheader("💳 Subscription Plans")
    
    col1, col2, col3 = st.columns(3)
    
    plans = ["basic", "advanced", "premium"]
    
    for i, plan in enumerate(plans):
        plan_info = auth_system.subscription_plans[plan]
        current_plan = subscription == plan
        
        with [col1, col2, col3][i]:
            st.markdown(f"""
            <div style="background-color: {plan_info['color']}20; 
                        border: 1px solid {plan_info['color']}; 
                        border-radius: 15px; padding: 20px; height: 100%;">
                <h3 style="text-align: center;">{plan_info['name']}</h3>
                <h4 style="text-align: center;">{plan_info['price']}</h4>
                <ul>
                    {"".join([f"<li>{feature}</li>" for feature in plan_info['features']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if current_plan:
                st.success("Current Plan")
            else:
                if st.button(f"Upgrade to {plan_info['name']}", key=f"upgrade_{plan}"):
                    st.info(f"Redirecting to payment for {plan_info['name']} plan...")
                    # In a real app, this would redirect to a payment processor

# Add new functions for subscription-specific features
def show_social_monitoring():
    """Social monitoring functionality - requires Advanced subscription"""
    st.header("Social Monitoring")
    
    # Get user's subscription
    username = st.session_state.get('username')
    
    if not auth_system.check_subscription_feature(username, "advanced_analytics"):
        st.warning("⚠️ This feature requires an Advanced or Premium subscription")
        st.info("Upgrade your plan to access social media monitoring features.")
        return
    
    brand_name = st.session_state.get('brand_name', 'Your Brand')
    posts = enhanced_monitor.simulate_monitoring_with_api(brand_name, st.session_state.sector)
    
    # Display posts with AI analysis
    for post in posts[:5]:
        threat_class = f"threat-{post['threat_level']}"
        sentiment_color = "#FF0000" if post['sentiment'] == 'negative' else "#FFD700" if post['sentiment'] == 'positive' else "#FFFFFF"
        
        with st.expander(f"{post['platform']} - {post['content'][:50]}..."):
            st.write(post['content'])
            st.caption(f"Engagement: {post['engagement']}")
            st.markdown(f"""
            <div style="display: flex; gap: 10px; margin-top: 10px;">
                <span class="{threat_class}">Threat: {post['threat_level'].upper()}</span>
                <span style="color: {sentiment_color}; font-weight: 600;">Sentiment: {post['sentiment'].upper()}</span>
            </div>
            """, unsafe_allow_html=True)

def show_ai_insights():
    """AI insights functionality - requires Advanced subscription"""
    st.header("🧠 AI-Powered Insights")
    
    # Get user's subscription
    username = st.session_state.get('username')
    
    if not auth_system.check_subscription_feature(username, "advanced_analytics"):
        st.warning("⚠️ This feature requires an Advanced or Premium subscription")
        st.info("Upgrade your plan to access AI-powered insights.")
        return
    
    brand_name = st.session_state.get('brand_name', 'Your Brand')
    
    # Generate sample analyses
    analyses = []
    for i in range(10):
        text = f"Sample text {i} about {brand_name} with {'high' if i < 3 else 'medium' if i < 6 else 'low'} threat level"
        analysis = ai_engine.detect_threats(text, brand_name)
        analyses.append(analysis)
    
    # Generate report
    report = ai_engine.generate_threat_report(analyses)
    
    # Display report
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="ai-visualization">
            <h4>📊 Threat Summary</h4>
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
        <div class="ai-visualization">
            <h4>✅ AI Recommendations</h4>
            {}
        </div>
        """.format(
            ''.join([f'<p>• {rec}</p>' for rec in report['recommendations']])
        ), unsafe_allow_html=True)
    
    # Keyword frequency analysis
    st.subheader("🔤 Keyword Frequency Analysis")
    
    texts = [a['text'] for a in analyses]
    keyword_freq = ai_engine.create_keyword_frequency(texts)
    
    # Create bar chart
    fig = viz.create_keyword_bar_chart(keyword_freq, "Top Keywords in Threat Analysis")
    st.plotly_chart(fig, use_container_width=True)
    
    # Threat patterns
    st.subheader("🔍 Threat Pattern Analysis")
    
    patterns = ai_engine.create_threat_patterns(analyses)
    
    # Create heatmap
    fig = viz.create_pattern_heatmap(patterns, "Threat Patterns by Platform and Level")
    st.plotly_chart(fig, use_container_width=True)
    
    # Pattern details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="ai-visualization">
            <h4>🎯 Top Threat Keywords</h4>
            {}
        </div>
        """.format(
            ''.join([f'<p>• {word}: {count}</p>' for word, count in list(patterns['high_threat_keywords'].most_common(5))])
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="ai-visualization">
            <h4>📱 Platform Distribution</h4>
            {}
        </div>
        """.format(
            ''.join([f'<p>• {platform}: {count}</p>' for platform, count in patterns['platform_distribution'].most_common()])
        ), unsafe_allow_html=True)

# Update the main function to set user subscription in session state
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
    
    # Header
    st.markdown("""
    <h1 class="premium-header floating">BrandGuardian AI Pro</h1>
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
        # Admin navigation
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📊 Executive Dashboard", 
            "🔍 Advanced Threat Analysis",
            "📱 Social Monitoring",
            "🥊 Competitive Intelligence",
            "🌟 Influencer Network",
            "🛡️ Crisis Prediction",
            "❤️ Brand Health",
            "🔑 API Management"
        ])
        
        with tab1:
            st.header("Executive Dashboard")
            st.write("Overview dashboard content...")
        
        with tab2:
            show_advanced_threat_analysis()
        
        with tab3:
            st.header("Social Monitoring")
            posts = enhanced_monitor.simulate_monitoring_with_api(brand_name, st.session_state.sector)
            for post in posts[:5]:
                with st.expander(f"{post['platform']} - {post['content'][:50]}..."):
                    st.write(post['content'])
                    st.caption(f"Engagement: {post['engagement']}")
        
        # Other tabs
        for tab, title in [(tab4, "Competitive Intelligence"), (tab5, "Influencer Network"), 
                          (tab6, "Crisis Prediction"), (tab7, "Brand Health")]:
            with tab:
                st.header(title)
                st.write(f"{title} content...")
        
        with tab8:
            show_api_key_management()
    else:
        # Regular user navigation
        show_user_ai_dashboard()

if __name__ == "__main__":
    main()
