import folium
from folium import plugins
from typing import Dict, List, Optional, Tuple
import pandas as pd

class MapUtils:
    """Utilities for creating interactive maps"""
    
    @staticmethod
    def create_base_map(lat: float, lon: float, zoom: int = 11) -> folium.Map:
        """Create base map centered on Bengaluru"""
        m = folium.Map(
            location=[lat, lon],
            zoom_start=zoom,
            tiles='OpenStreetMap'
        )
        
        # Add satellite layer option
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satellite',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Add CartoDB Positron for clean look
        folium.TileLayer(
            tiles='CartoDB positron',
            name='Light Map',
            overlay=False,
            control=True
        ).add_to(m)
        
        folium.LayerControl().add_to(m)
        
        return m
    
    @staticmethod
    def add_weather_markers(m: folium.Map, weather_data: Optional[Dict], air_quality_data: Optional[Dict]) -> folium.Map:
        """Add weather and air quality markers"""
        if weather_data and weather_data.get("location"):
            location = weather_data["location"]
            
            # Weather popup content
            popup_content = f"""
            <div style='width: 200px;'>
                <h4>Current Conditions</h4>
                <p><strong>Temperature:</strong> {weather_data.get('temperature_2m', 'N/A')}°C</p>
                <p><strong>Feels like:</strong> {weather_data.get('apparent_temperature', 'N/A')}°C</p>
                <p><strong>Humidity:</strong> {weather_data.get('relative_humidity_2m', 'N/A')}%</p>
                <p><strong>Wind:</strong> {weather_data.get('wind_speed_10m', 'N/A')} km/h</p>
            </div>
            """
            
            folium.Marker(
                location=[location["lat"], location["lon"]],
                popup=folium.Popup(popup_content, max_width=250),
                tooltip="Weather Station",
                icon=folium.Icon(color='blue', icon='thermometer-half', prefix='fa')
            ).add_to(m)
        
        if air_quality_data and air_quality_data.get("location"):
            location = air_quality_data["location"]
            pm25 = air_quality_data.get('pm2_5', 0)
            
            # Color code based on air quality
            if pm25 <= 12:
                color = 'green'
                quality = 'Good'
            elif pm25 <= 35:
                color = 'orange'
                quality = 'Moderate'
            else:
                color = 'red'
                quality = 'Unhealthy'
            
            popup_content = f"""
            <div style='width: 200px;'>
                <h4>Air Quality</h4>
                <p><strong>PM2.5:</strong> {pm25} μg/m³</p>
                <p><strong>PM10:</strong> {air_quality_data.get('pm10', 'N/A')} μg/m³</p>
                <p><strong>NO₂:</strong> {air_quality_data.get('nitrogen_dioxide', 'N/A')} μg/m³</p>
                <p><strong>Status:</strong> <span style='color: {color};'>{quality}</span></p>
            </div>
            """
            
            folium.Marker(
                location=[location["lat"], location["lon"]],
                popup=folium.Popup(popup_content, max_width=250),
                tooltip=f"Air Quality: {quality}",
                icon=folium.Icon(color=color, icon='wind', prefix='fa')
            ).add_to(m)
        
        return m
    
    @staticmethod
    def add_heat_island_layer(m: folium.Map, heat_data: Optional[Dict] = None) -> folium.Map:
        """Add heat island visualization"""
        if not heat_data:
            # Default heat island hotspots for Bengaluru
            heat_spots = [
                [12.845, 77.661, 4.2],  # Electronic City
                [12.970, 77.750, 3.8],  # Whitefield
                [12.935, 77.610, 3.1],  # Koramangala
                [12.904, 77.600, 2.9],  # Banashankari
            ]
            
            cooling_zones = [
                [12.976, 77.590, -2.1],  # Cubbon Park
                [12.950, 77.584, -1.8],  # Lalbagh
                [12.976, 77.625, -1.3],  # Ulsoor Lake
            ]
        else:
            heat_spots = [[spot["lat"], spot["lon"], spot["intensity"]] 
                         for spot in heat_data.get("hotspots", [])]
            cooling_zones = [[zone["lat"], zone["lon"], abs(zone["cooling"])] 
                           for zone in heat_data.get("cooling_zones", [])]
        
        # Heat island heatmap
        if heat_spots:
            plugins.HeatMap(
                data=heat_spots,
                name='Heat Islands',
                radius=20,
                blur=15,
                gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'}
            ).add_to(m)
        
        # Add markers for specific hotspots
        for spot in heat_spots:
            folium.CircleMarker(
                location=[spot[0], spot[1]],
                radius=10,
                popup=f"Heat Island: +{spot[2]}°C",
                tooltip="Heat Island Hotspot",
                color='red',
                fillColor='red',
                fillOpacity=0.6
            ).add_to(m)
        
        # Add markers for cooling zones
        for zone in cooling_zones:
            folium.CircleMarker(
                location=[zone[0], zone[1]],
                radius=8,
                popup=f"Cooling Zone: -{zone[2]}°C",
                tooltip="Cooling Zone",
                color='blue',
                fillColor='lightblue',
                fillOpacity=0.6
            ).add_to(m)
        
        return m
    
    @staticmethod
    def add_water_bodies(m: folium.Map) -> folium.Map:
        """Add Bengaluru lakes and water bodies"""
        lakes = [
            {"name": "Bellandur Lake", "lat": 12.926, "lon": 77.675, "health": 45},
            {"name": "Ulsoor Lake", "lat": 12.976, "lon": 77.625, "health": 78},
            {"name": "Sankey Tank", "lat": 12.991, "lon": 77.567, "health": 82},
            {"name": "Hebbal Lake", "lat": 13.036, "lon": 77.597, "health": 67},
            {"name": "Madivala Lake", "lat": 12.925, "lon": 77.623, "health": 59}
        ]
        
        for lake in lakes:
            # Color based on health score
            if lake["health"] >= 70:
                color = 'green'
                status = 'Good'
            elif lake["health"] >= 50:
                color = 'orange'
                status = 'Fair'
            else:
                color = 'red'
                status = 'Poor'
            
            popup_content = f"""
            <div style='width: 150px;'>
                <h4>{lake['name']}</h4>
                <p><strong>Health Score:</strong> {lake['health']}/100</p>
                <p><strong>Status:</strong> <span style='color: {color};'>{status}</span></p>
            </div>
            """
            
            folium.Marker(
                location=[lake["lat"], lake["lon"]],
                popup=folium.Popup(popup_content, max_width=200),
                tooltip=lake["name"],
                icon=folium.Icon(color=color, icon='tint', prefix='fa')
            ).add_to(m)
        
        return m
    
    @staticmethod
    def add_urban_growth_markers(m: folium.Map) -> folium.Map:
        """Add urban growth and development markers"""
        development_areas = [
            {"name": "Electronic City Phase 2", "lat": 12.835, "lon": 77.675, "type": "IT Hub"},
            {"name": "Whitefield Extension", "lat": 12.975, "lon": 77.760, "type": "Residential"},
            {"name": "Sarjapur Road Corridor", "lat": 12.905, "lon": 77.700, "type": "Mixed Development"},
            {"name": "North Bengaluru", "lat": 13.050, "lon": 77.580, "type": "Residential"}
        ]
        
        for area in development_areas:
            icon_color = {
                "IT Hub": "purple",
                "Residential": "blue", 
                "Mixed Development": "orange"
            }.get(area["type"], "gray")
            
            popup_content = f"""
            <div style='width: 150px;'>
                <h4>{area['name']}</h4>
                <p><strong>Type:</strong> {area['type']}</p>
                <p><strong>Status:</strong> Under Development</p>
            </div>
            """
            
            folium.Marker(
                location=[area["lat"], area["lon"]],
                popup=folium.Popup(popup_content, max_width=200),
                tooltip=area["name"],
                icon=folium.Icon(color=icon_color, icon='building', prefix='fa')
            ).add_to(m)
        
        return m
    
    @staticmethod
    def add_air_quality_zones(m: folium.Map, air_quality_data: Optional[Dict] = None) -> folium.Map:
        """Add air quality monitoring zones"""
        # Air quality monitoring stations across Bengaluru
        stations = [
            {"name": "City Railway Station", "lat": 12.977, "lon": 77.571, "pm25": 45},
            {"name": "BTM Layout", "lat": 12.912, "lon": 77.610, "pm25": 52},
            {"name": "Whitefield", "lat": 12.970, "lon": 77.750, "pm25": 38},
            {"name": "Electronic City", "lat": 12.845, "lon": 77.661, "pm25": 67},
            {"name": "Jayanagar", "lat": 12.926, "lon": 77.583, "pm25": 41}
        ]
        
        for station in stations:
            pm25 = station["pm25"]
            
            # Color coding for air quality
            if pm25 <= 25:
                color = 'green'
                status = 'Good'
            elif pm25 <= 50:
                color = 'orange'
                status = 'Moderate'
            else:
                color = 'red'
                status = 'Unhealthy'
            
            popup_content = f"""
            <div style='width: 150px;'>
                <h4>{station['name']}</h4>
                <p><strong>PM2.5:</strong> {pm25} μg/m³</p>
                <p><strong>Status:</strong> <span style='color: {color};'>{status}</span></p>
            </div>
            """
            
            folium.CircleMarker(
                location=[station["lat"], station["lon"]],
                radius=12,
                popup=folium.Popup(popup_content, max_width=200),
                tooltip=f"{station['name']}: {status}",
                color=color,
                fillColor=color,
                fillOpacity=0.7
            ).add_to(m)
        
        return m
