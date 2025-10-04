import streamlit as st
import folium
from streamlit_folium import st_folium
from typing import Dict, Optional
from utils.map_utils import MapUtils

def render_interactive_map(lat: float, lon: float, weather_data: Optional[Dict] = None, air_quality_data: Optional[Dict] = None, map_type: str = "overview"):
    """Render interactive map based on selected type"""
    
    map_utils = MapUtils()
    
    # Create base map
    m = map_utils.create_base_map(lat, lon, zoom=11)
    
    if map_type == "overview":
        render_overview_map(m, lat, lon, weather_data, air_quality_data)
    elif map_type == "heat_island":
        render_heat_island_map(m)
    elif map_type == "water_monitoring":
        render_water_monitoring_map(m)
    elif map_type == "air_quality":
        render_air_quality_map(m)
    elif map_type == "urban_growth":
        render_urban_growth_map(m)
    
    # Display the map
    map_data = st_folium(m, width=700, height=500)
    
    # Handle map interactions
    if map_data['last_clicked']:
        handle_map_click(map_data['last_clicked'], map_type)

def render_overview_map(m: folium.Map, lat: float, lon: float, weather_data: Optional[Dict], air_quality_data: Optional[Dict]):
    """Render overview map with all key features"""
    
    map_utils = MapUtils()
    
    # Add weather and air quality markers
    m = map_utils.add_weather_markers(m, weather_data, air_quality_data)
    
    # Add water bodies
    m = map_utils.add_water_bodies(m)
    
    # Add air quality zones
    m = map_utils.add_air_quality_zones(m)
    
    # Add major landmarks
    add_city_landmarks(m)

def render_heat_island_map(m: folium.Map):
    """Render heat island focused map"""
    
    map_utils = MapUtils()
    
    # Add heat island layer
    m = map_utils.add_heat_island_layer(m)
    
    # Add temperature monitoring stations
    add_temperature_stations(m)
    
    st.info("🌡️ **Heat Island Map**: Red areas show urban heat islands, blue areas show cooling zones.")

def render_water_monitoring_map(m: folium.Map):
    """Render water body monitoring map"""
    
    map_utils = MapUtils()
    
    # Add water bodies with detailed information
    m = map_utils.add_water_bodies(m)
    
    # Add water quality monitoring points
    add_water_quality_stations(m)
    
    st.info("💧 **Water Monitoring**: Click on lakes to see health status and quality metrics.")

def render_air_quality_map(m: folium.Map):
    """Render air quality monitoring map"""
    
    map_utils = MapUtils()
    
    # Add air quality zones
    m = map_utils.add_air_quality_zones(m)
    
    # Add pollution sources
    add_pollution_sources(m)
    
    st.info("🌬️ **Air Quality Map**: Green circles show good air quality, red circles show poor air quality.")

def render_urban_growth_map(m: folium.Map):
    """Render urban growth and development map"""
    
    map_utils = MapUtils()
    
    # Add urban growth markers
    m = map_utils.add_urban_growth_markers(m)
    
    # Add development zones
    add_development_zones(m)
    
    st.info("🏗️ **Urban Growth Map**: Purple markers show IT hubs, blue markers show residential areas.")

def add_city_landmarks(m: folium.Map):
    """Add important city landmarks"""
    
    landmarks = [
        {"name": "Vidhana Soudha", "lat": 12.979, "lon": 77.590, "type": "government"},
        {"name": "Bangalore Palace", "lat": 12.998, "lon": 77.592, "type": "heritage"},
        {"name": "UB City Mall", "lat": 12.972, "lon": 77.595, "type": "commercial"},
        {"name": "Kempegowda Airport", "lat": 13.199, "lon": 77.706, "type": "transport"},
        {"name": "Majestic Bus Station", "lat": 12.977, "lon": 77.571, "type": "transport"}
    ]
    
    icon_map = {
        "government": {"color": "purple", "icon": "university"},
        "heritage": {"color": "darkred", "icon": "monument"},
        "commercial": {"color": "orange", "icon": "shopping-cart"},
        "transport": {"color": "blue", "icon": "plane"}
    }
    
    for landmark in landmarks:
        icon_info = icon_map.get(landmark["type"], {"color": "gray", "icon": "info-sign"})
        
        folium.Marker(
            location=[landmark["lat"], landmark["lon"]],
            popup=folium.Popup(f"<b>{landmark['name']}</b><br>Type: {landmark['type'].title()}", max_width=200),
            tooltip=landmark["name"],
            icon=folium.Icon(color=icon_info["color"], icon=icon_info["icon"], prefix='fa')
        ).add_to(m)

def add_temperature_stations(m: folium.Map):
    """Add temperature monitoring stations"""
    
    stations = [
        {"name": "HAL Airport", "lat": 12.960, "lon": 77.644, "temp": 28.5},
        {"name": "IISC Campus", "lat": 13.021, "lon": 77.566, "temp": 26.8},
        {"name": "Electronic City", "lat": 12.845, "lon": 77.661, "temp": 32.1},
        {"name": "Whitefield", "lat": 12.970, "lon": 77.750, "temp": 31.4}
    ]
    
    for station in stations:
        # Color based on temperature
        if station["temp"] > 30:
            color = "red"
        elif station["temp"] > 28:
            color = "orange"
        else:
            color = "green"
        
        popup_content = f"""
        <div style='width: 150px;'>
            <h4>{station['name']}</h4>
            <p><strong>Temperature:</strong> {station['temp']}°C</p>
        </div>
        """
        
        folium.CircleMarker(
            location=[station["lat"], station["lon"]],
            radius=8,
            popup=folium.Popup(popup_content, max_width=200),
            tooltip=f"{station['name']}: {station['temp']}°C",
            color=color,
            fillColor=color,
            fillOpacity=0.7
        ).add_to(m)

def add_water_quality_stations(m: folium.Map):
    """Add water quality monitoring stations"""
    
    monitoring_points = [
        {"name": "Bellandur Inlet", "lat": 12.930, "lon": 77.670, "quality": "Poor"},
        {"name": "Bellandur Outlet", "lat": 12.922, "lon": 77.680, "quality": "Very Poor"},
        {"name": "Ulsoor Lake Center", "lat": 12.976, "lon": 77.625, "quality": "Good"},
        {"name": "Sankey Tank Inlet", "lat": 12.993, "lon": 77.565, "quality": "Excellent"},
        {"name": "Hebbal Lake", "lat": 13.036, "lon": 77.597, "quality": "Fair"}
    ]
    
    quality_colors = {
        "Excellent": "darkgreen",
        "Good": "green", 
        "Fair": "orange",
        "Poor": "red",
        "Very Poor": "darkred"
    }
    
    for point in monitoring_points:
        color = quality_colors.get(point["quality"], "gray")
        
        popup_content = f"""
        <div style='width: 150px;'>
            <h4>{point['name']}</h4>
            <p><strong>Water Quality:</strong> {point['quality']}</p>
        </div>
        """
        
        folium.Marker(
            location=[point["lat"], point["lon"]],
            popup=folium.Popup(popup_content, max_width=200),
            tooltip=f"Water Quality: {point['quality']}",
            icon=folium.Icon(color=color, icon='tint', prefix='fa')
        ).add_to(m)

def add_pollution_sources(m: folium.Map):
    """Add major pollution sources"""
    
    pollution_sources = [
        {"name": "Industrial Area - Peenya", "lat": 13.030, "lon": 77.520, "type": "Industrial"},
        {"name": "Traffic Junction - Silk Board", "lat": 12.918, "lon": 77.623, "type": "Traffic"},
        {"name": "Construction Zone - Outer Ring Road", "lat": 12.935, "lon": 77.692, "type": "Construction"},
        {"name": "Waste Processing - Mavallipura", "lat": 13.181, "lon": 77.486, "type": "Waste"}
    ]
    
    type_colors = {
        "Industrial": "purple",
        "Traffic": "red",
        "Construction": "orange", 
        "Waste": "brown"
    }
    
    for source in pollution_sources:
        color = type_colors.get(source["type"], "gray")
        
        popup_content = f"""
        <div style='width: 150px;'>
            <h4>{source['name']}</h4>
            <p><strong>Type:</strong> {source['type']} Pollution</p>
        </div>
        """
        
        folium.Marker(
            location=[source["lat"], source["lon"]],
            popup=folium.Popup(popup_content, max_width=200),
            tooltip=f"{source['type']} Pollution Source",
            icon=folium.Icon(color=color, icon='warning-sign', prefix='fa')
        ).add_to(m)

def add_development_zones(m: folium.Map):
    """Add planned development zones"""
    
    development_zones = [
        {"name": "Aerospace Park", "lat": 13.140, "lon": 77.560, "status": "Planned"},
        {"name": "Peripheral Ring Road", "lat": 12.850, "lon": 77.450, "status": "Under Construction"},
        {"name": "New Metro Extension", "lat": 12.920, "lon": 77.720, "status": "Approved"},
        {"name": "IT Corridor Extension", "lat": 12.800, "lon": 77.700, "status": "Proposed"}
    ]
    
    status_colors = {
        "Planned": "blue",
        "Under Construction": "orange",
        "Approved": "green",
        "Proposed": "purple"
    }
    
    for zone in development_zones:
        color = status_colors.get(zone["status"], "gray")
        
        popup_content = f"""
        <div style='width: 150px;'>
            <h4>{zone['name']}</h4>
            <p><strong>Status:</strong> {zone['status']}</p>
        </div>
        """
        
        folium.CircleMarker(
            location=[zone["lat"], zone["lon"]],
            radius=15,
            popup=folium.Popup(popup_content, max_width=200),
            tooltip=f"{zone['name']} ({zone['status']})",
            color=color,
            fillColor=color,
            fillOpacity=0.3,
            weight=3
        ).add_to(m)

def handle_map_click(clicked_data: Dict, map_type: str):
    """Handle map click events"""
    
    if not clicked_data:
        return
    
    lat = clicked_data.get('lat')
    lon = clicked_data.get('lng')
    
    if lat and lon:
        st.sidebar.subheader("📍 Location Info")
        st.sidebar.write(f"**Coordinates:** {lat:.4f}, {lon:.4f}")
        
        # Provide context-specific information
        if map_type == "heat_island":
            estimated_temp = 28 + (abs(lat - 12.972) + abs(lon - 77.594)) * 50  # Simple estimation
            st.sidebar.write(f"**Estimated Temperature:** {estimated_temp:.1f}°C")
            
        elif map_type == "air_quality":
            # Estimate air quality based on location (simplified)
            urban_factor = min(1.0, (abs(lat - 12.972) + abs(lon - 77.594)) * 10)
            estimated_pm25 = 30 + urban_factor * 20
            st.sidebar.write(f"**Estimated PM2.5:** {estimated_pm25:.1f} μg/m³")
        
        # Suggest nearby points of interest
        suggest_nearby_locations(lat, lon, map_type)

def suggest_nearby_locations(lat: float, lon: float, map_type: str):
    """Suggest nearby locations based on map type"""
    
    st.sidebar.subheader("🎯 Nearby Points of Interest")
    
    if map_type == "water_monitoring":
        st.sidebar.write("• Nearest monitoring station")
        st.sidebar.write("• Water treatment facilities")
        st.sidebar.write("• Lake restoration projects")
        
    elif map_type == "air_quality":
        st.sidebar.write("• Air quality monitoring stations")
        st.sidebar.write("• Green spaces for better air")
        st.sidebar.write("• Low-pollution routes")
        
    elif map_type == "heat_island":
        st.sidebar.write("• Cooling centers/parks")
        st.sidebar.write("• Shaded walking paths")
        st.sidebar.write("• Public facilities with AC")
        
    else:
        st.sidebar.write("• Weather stations")
        st.sidebar.write("• Public amenities")
        st.sidebar.write("• Transport hubs")
