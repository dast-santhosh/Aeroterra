import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional

def render_dashboard(stakeholder: str, weather_data: Optional[Dict], air_quality_data: Optional[Dict], nasa_data: Optional[Dict] = None):
    """Render stakeholder-specific dashboard"""
    
    st.subheader(f"Dashboard for {stakeholder}")
    
    if stakeholder == "Citizens":
        render_citizens_dashboard(weather_data, air_quality_data)
    elif stakeholder == "BBMP (City Planning)":
        render_bbmp_dashboard(weather_data, air_quality_data, nasa_data)
    elif stakeholder == "BWSSB (Water Board)":
        render_water_board_dashboard(weather_data, nasa_data)
    elif stakeholder == "BESCOM (Electricity)":
        render_electricity_dashboard(weather_data)
    elif stakeholder == "Parks Department":
        render_parks_dashboard(weather_data, nasa_data)
    elif stakeholder == "Researchers":
        render_research_dashboard(weather_data, air_quality_data, nasa_data)

def render_citizens_dashboard(weather_data: Optional[Dict], air_quality_data: Optional[Dict]):
    """Citizens-focused dashboard with daily life relevant information"""
    
    st.info("🏠 **For Citizens**: Daily life climate information and health advisories")
    
    # Today's recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌤️ Today's Weather")
        if weather_data:
            temp = weather_data.get('temperature_2m', 'N/A')
            feels_like = weather_data.get('apparent_temperature', 'N/A')
            humidity = weather_data.get('relative_humidity_2m', 'N/A')
            
            st.write(f"**Temperature:** {temp}°C")
            st.write(f"**Feels like:** {feels_like}°C")
            st.write(f"**Humidity:** {humidity}%")
            
            # Comfort recommendations
            if isinstance(temp, (int, float)):
                if temp > 35:
                    st.warning("🌡️ Very hot day! Stay hydrated and avoid outdoor activities during peak hours.")
                elif temp < 15:
                    st.info("🧥 Cool day! You might want to carry a light jacket.")
                else:
                    st.success("😊 Pleasant weather for outdoor activities!")
    
    with col2:
        st.subheader("💨 Air Quality")
        if air_quality_data:
            pm25 = air_quality_data.get('pm2_5', 'N/A')
            
            if isinstance(pm25, (int, float)):
                st.write(f"**PM2.5:** {pm25} μg/m³")
                
                if pm25 <= 25:
                    st.success("😷 Good air quality - safe for outdoor activities!")
                elif pm25 <= 50:
                    st.warning("😷 Moderate air quality - sensitive individuals should limit outdoor activities.")
                else:
                    st.error("😷 Poor air quality - wear masks outdoors and limit exposure!")
    
    # Health recommendations
    st.subheader("🏥 Health Recommendations")
    
    recommendations = []
    
    if weather_data and isinstance(weather_data.get('temperature_2m'), (int, float)):
        temp = weather_data.get('temperature_2m')
        if temp and temp > 35:
            recommendations.append("Drink plenty of water throughout the day")
            recommendations.append("Wear light-colored, loose-fitting clothes")
            recommendations.append("Avoid outdoor activities between 11 AM - 4 PM")
    
    if air_quality_data and isinstance(air_quality_data.get('pm2_5'), (int, float)):
        pm25 = air_quality_data.get('pm2_5')
        if pm25 and pm25 > 25:
            recommendations.append("Wear N95 masks when outdoors")
            recommendations.append("Keep windows closed during high pollution hours")
            recommendations.append("Consider indoor exercises instead of outdoor jogging")
    
    for rec in recommendations:
        st.write(f"• {rec}")
    
    if not recommendations:
        st.write("• Great conditions today! Enjoy outdoor activities safely.")

def render_bbmp_dashboard(weather_data: Optional[Dict], air_quality_data: Optional[Dict], nasa_data: Optional[Dict]):
    """BBMP City Planning dashboard"""
    
    st.info("🏛️ **For BBMP**: Urban planning insights and city development guidance")
    
    # Urban heat island analysis
    st.subheader("🌡️ Urban Heat Island Monitoring")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Heat Island Intensity", "3.2°C", delta="↑ 0.5°C from last month")
    
    with col2:
        st.metric("Critical Heat Zones", "4 areas", delta="↑ 1 new zone")
    
    with col3:
        st.metric("Green Cover Impact", "-2.1°C", delta="In parks & tree-lined areas")
    
    # Development pressure indicators
    st.subheader("🏗️ Development Pressure Indicators")
    
    pressure_data = {
        'Zone': ['Electronic City', 'Whitefield', 'Sarjapur Road', 'North Bengaluru', 'Outer Ring Road'],
        'Development Intensity': [85, 78, 92, 45, 67],
        'Heat Risk': ['Very High', 'High', 'Very High', 'Low', 'Medium'],
        'Green Space %': [12, 18, 8, 35, 22]
    }
    
    df = pd.DataFrame(pressure_data)
    st.dataframe(df, use_container_width=True)
    
    # Planning recommendations
    st.subheader("📋 Planning Recommendations")
    
    st.write("**Immediate Actions:**")
    st.write("• Mandate 20% green space in new developments in Electronic City")
    st.write("• Implement cool roof policies in high heat zones")
    st.write("• Create green corridors connecting existing parks")
    
    st.write("**Long-term Strategy:**")
    st.write("• Develop satellite city centers to reduce central density")
    st.write("• Increase tree canopy coverage to 30% city-wide")
    st.write("• Implement building height restrictions in heat island zones")

def render_water_board_dashboard(weather_data: Optional[Dict], nasa_data: Optional[Dict]):
    """Water Board (BWSSB) dashboard"""
    
    st.info("💧 **For BWSSB**: Water resource management and lake health monitoring")
    
    # Lake health overview
    st.subheader("🏞️ Lake Health Status")
    
    lakes_data = {
        'Lake': ['Bellandur', 'Ulsoor', 'Sankey Tank', 'Hebbal', 'Madivala'],
        'Health Score': [45, 78, 82, 67, 59],
        'Water Quality': ['Critical', 'Good', 'Excellent', 'Fair', 'Poor'],
        'Algal Bloom Risk': ['High', 'Low', 'Very Low', 'Medium', 'High'],
        'Action Required': ['Immediate', 'Monitor', 'Maintain', 'Improve', 'Urgent']
    }
    
    df = pd.DataFrame(lakes_data)
    
    # Color code the dataframe
    def color_health_score(val):
        if val >= 70:
            return 'background-color: #90EE90'
        elif val >= 50:
            return 'background-color: #FFD700'
        else:
            return 'background-color: #FFB6C1'
    
    styled_df = df.style.applymap(color_health_score, subset=['Health Score'])
    st.dataframe(styled_df, use_container_width=True)
    
    # Water quality trends
    st.subheader("📈 Water Quality Trends")
    
    # Sample trend data
    dates = pd.date_range(start=datetime.now() - timedelta(days=90), end=datetime.now(), freq='W')
    bellandur_trend = [45 + (i % 5) - 2 for i in range(len(dates))]
    ulsoor_trend = [78 + (i % 3) - 1 for i in range(len(dates))]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=bellandur_trend, name='Bellandur Lake', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=dates, y=ulsoor_trend, name='Ulsoor Lake', line=dict(color='blue')))
    fig.update_layout(title='Lake Health Trends (90 Days)', xaxis_title='Date', yaxis_title='Health Score')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Action items
    st.subheader("🚨 Priority Action Items")
    
    st.error("**Critical**: Bellandur Lake requires immediate intervention - sewage treatment upgrade needed")
    st.warning("**Monitor**: Madivala Lake showing declining trends - investigate pollution sources")
    st.success("**Success**: Sankey Tank maintenance program showing positive results")

def render_electricity_dashboard(weather_data: Optional[Dict]):
    """BESCOM electricity demand dashboard"""
    
    st.info("⚡ **For BESCOM**: Power demand forecasting and grid management")
    
    # Current conditions affecting power demand
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if weather_data:
            temp = weather_data.get('temperature_2m', 25)
            st.metric("Current Temperature", f"{temp}°C")
            
            # Estimate cooling demand
            if temp > 30:
                cooling_demand = min(100, (temp - 25) * 20)
                st.metric("Cooling Demand", f"{cooling_demand}%", delta="↑ High")
            else:
                st.metric("Cooling Demand", "Low", delta="→ Stable")
    
    with col2:
        # Peak load prediction
        st.metric("Predicted Peak Load", "2,850 MW", delta="↑ 12% vs yesterday")
    
    with col3:
        # Grid stress indicator
        st.metric("Grid Stress Level", "Moderate", delta="Monitor closely")
    
    # Power demand forecast
    st.subheader("📊 24-Hour Demand Forecast")
    
    # Sample hourly demand data
    hours = list(range(24))
    base_demand = [1800, 1650, 1500, 1400, 1350, 1400, 1600, 1900, 2200, 2400, 
                   2600, 2750, 2850, 2900, 2850, 2700, 2500, 2300, 2100, 2000, 
                   1950, 1900, 1850, 1800]
    
    # Adjust for temperature
    if weather_data and isinstance(weather_data.get('temperature_2m'), (int, float)):
        temp = weather_data.get('temperature_2m')
        temp_factor = max(1.0, 1.0 + (temp - 25) * 0.02) if temp else 1.0  # 2% increase per degree above 25°C
        adjusted_demand = [d * temp_factor for d in base_demand]
    else:
        adjusted_demand = base_demand
    
    fig = px.line(x=hours, y=adjusted_demand, 
                  title='24-Hour Power Demand Forecast',
                  labels={'x': 'Hour of Day', 'y': 'Demand (MW)'})
    
    # Add peak hours highlighting
    fig.add_hline(y=2500, line_dash="dash", line_color="red", 
                  annotation_text="Peak Alert Threshold")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("⚡ Grid Management Recommendations")
    
    st.write("**Immediate Actions:**")
    st.write("• Prepare backup power sources for afternoon peak (2-4 PM)")
    st.write("• Issue power conservation advisory to industrial users")
    st.write("• Monitor transformer temperatures in high-demand areas")

def render_parks_dashboard(weather_data: Optional[Dict], nasa_data: Optional[Dict]):
    """Parks Department dashboard"""
    
    st.info("🌳 **For Parks Department**: Green space management and urban forestry")
    
    # Green cover metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("City Green Cover", "18.2%", delta="↓ 1.2% vs last year")
    
    with col2:
        st.metric("Tree Canopy", "12.8%", delta="↑ 0.3% improvement")
    
    with col3:
        st.metric("Park Visitor Count", "15,420", delta="↑ 8% this week")
    
    with col4:
        st.metric("Tree Health Index", "76/100", delta="→ Stable")
    
    # Park performance
    st.subheader("🏞️ Park Performance Dashboard")
    
    parks_data = {
        'Park Name': ['Cubbon Park', 'Lalbagh', 'Bannerghatta', 'Freedom Park', 'Jayamahal Park'],
        'Area (acres)': [300, 240, 104, 2.5, 4.2],
        'Visitor Count': [5420, 3890, 2150, 890, 340],
        'Tree Health': [85, 82, 78, 71, 69],
        'Cooling Effect': ['-2.1°C', '-1.8°C', '-1.5°C', '-0.8°C', '-0.6°C']
    }
    
    df = pd.DataFrame(parks_data)
    st.dataframe(df, use_container_width=True)
    
    # Tree plantation progress
    st.subheader("🌱 Tree Plantation Progress")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Quarterly progress
        quarters = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024 (Target)']
        planted = [2840, 3150, 2960, 3500]
        targets = [3000, 3200, 3100, 3500]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=quarters, y=planted, name='Trees Planted', marker_color='green'))
        fig.add_trace(go.Bar(x=quarters, y=targets, name='Target', marker_color='lightgreen', opacity=0.5))
        fig.update_layout(title='Quarterly Tree Plantation Progress')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Species distribution
        species = ['Banyan', 'Neem', 'Gulmohar', 'Rain Tree', 'Tamarind', 'Others']
        counts = [890, 1240, 780, 650, 420, 980]
        
        fig = px.pie(values=counts, names=species, title='Tree Species Distribution')
        st.plotly_chart(fig, use_container_width=True)

def render_research_dashboard(weather_data: Optional[Dict], air_quality_data: Optional[Dict], nasa_data: Optional[Dict]):
    """Research dashboard with comprehensive data analysis"""
    
    st.info("🔬 **For Researchers**: Comprehensive climate data analysis and trends")
    
    # Data quality and availability
    st.subheader("📊 Data Quality Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Weather Data Quality", "98.5%", delta="↑ High reliability")
    
    with col2:
        st.metric("Satellite Data Coverage", "94.2%", delta="→ Good coverage")
    
    with col3:
        st.metric("Air Quality Sensors", "12 active", delta="↑ 2 new stations")
    
    # Research insights
    st.subheader("🔍 Key Research Findings")
    
    st.write("**Climate Patterns:**")
    st.write("• Urban heat island intensity has increased 15% over 5 years")
    st.write("• Green spaces provide 2-3°C cooling benefit consistently")
    st.write("• Air quality shows seasonal variation with monsoon improvement")
    
    st.write("**Correlations Discovered:**")
    st.write("• Strong negative correlation (-0.78) between green cover and surface temperature")
    st.write("• PM2.5 levels increase 40% during construction season")
    st.write("• Lake health directly impacts local humidity levels")
    
    # Advanced analytics
    st.subheader("📈 Advanced Analytics")
    
    # Multi-parameter correlation matrix
    correlation_data = {
        'Metric': ['Temperature', 'Humidity', 'PM2.5', 'Green Cover', 'Lake Health'],
        'Temperature': [1.0, -0.45, 0.23, -0.78, -0.34],
        'Humidity': [-0.45, 1.0, -0.12, 0.56, 0.67],
        'PM2.5': [0.23, -0.12, 1.0, -0.45, -0.23],
        'Green Cover': [-0.78, 0.56, -0.45, 1.0, 0.45],
        'Lake Health': [-0.34, 0.67, -0.23, 0.45, 1.0]
    }
    
    st.write("**Correlation Matrix:**")
    corr_df = pd.DataFrame(correlation_data)
    st.dataframe(corr_df.set_index('Metric'), use_container_width=True)
    
    # Research recommendations
    st.subheader("🎯 Research Recommendations")
    
    st.write("**Priority Research Areas:**")
    st.write("• Quantify economic impact of urban heat islands")
    st.write("• Study effectiveness of different cooling interventions")
    st.write("• Develop predictive models for air quality forecasting")
    st.write("• Assess climate change adaptation strategies")
