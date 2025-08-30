# Add this at the top of your imports section
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    st.warning("Matplotlib is not installed. Some visualizations will be simplified.")

# Then in your AdvancedVisualizations class, modify the chart creation methods:

def create_radar_chart(self, data, labels, title):
    """Create a radar chart using matplotlib and streamlit"""
    if not MATPLOTLIB_AVAILABLE:
        st.warning("Matplotlib not available. Using simplified visualization.")
        return self.create_bar_chart(data, labels, title)
    
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        
        # Set up the figure
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        
        # Calculate angles for each category
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]  # Close the circle
        
        # Close the data
        values = data.tolist()
        values += values[:1]
        
        # Plot the data
        ax.plot(angles, values, color=self.colors['primary'], linewidth=2, linestyle='solid')
        ax.fill(angles, values, color=self.colors['primary'], alpha=0.25)
        
        # Add labels
        ax.set_thetagrids(np.degrees(angles[:-1]), labels)
        
        # Set ylim
        ax.set_ylim(0, max(data) * 1.1)
        
        # Add title
        plt.title(title, size=14, fontweight='bold', pad=20)
        
        # Style the plot
        ax.spines['polar'].set_color('white')
        ax.tick_params(colors='white')
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        
        # Display in Streamlit
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error creating radar chart: {e}")
        # Fallback to bar chart
        self.create_bar_chart(data, labels, title)

def create_threat_distribution(self, data, title):
    """Create a donut chart for threat distribution"""
    if not MATPLOTLIB_AVAILABLE:
        st.warning("Matplotlib not available. Using simplified visualization.")
        return self.create_bar_chart(np.array(list(data.values())), list(data.keys()), title)
    
    try:
        import matplotlib.pyplot as plt
        
        labels = list(data.keys())
        values = list(data.values())
        colors = [self.colors['danger'], self.colors['warning'], self.colors['success']]
        
        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(
            values, labels=labels, autopct='%1.1f%%', 
            colors=colors, startangle=90, wedgeprops=dict(width=0.3)
        )
        
        # Style the text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        for text in texts:
            text.set_color('white')
            text.set_fontsize(12)
        
        # Add center circle to make it a donut
        centre_circle = plt.Circle((0, 0), 0.70, fc='none')
        ax.add_artist(centre_circle)
        
        # Add title
        plt.title(title, color='white', fontsize=16, fontweight='bold', pad=20)
        
        # Style the plot
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        
        # Display in Streamlit
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error creating donut chart: {e}")
        # Fallback to bar chart
        self.create_bar_chart(np.array(list(data.values())), list(data.keys()), title)
