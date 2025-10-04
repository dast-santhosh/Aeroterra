# Aeroterra - Climate Resilience Dashboard

## Overview

Aeroterra is an interactive geospatial decision-support platform for Bengaluru that integrates NASA Earth observation data, real-time climate APIs, and an AI-powered chatbot. The platform serves multiple stakeholders (citizens, city planners, water board, electricity board, parks department, and researchers) with climate and environmental insights.

**Core Purpose**: Provide stakeholder-specific dashboards and AI-assisted climate insights to support urban resilience planning and daily decision-making in Bengaluru.

**Key Capabilities**:
- Multi-stakeholder dashboards with role-specific metrics
- Real-time weather and air quality monitoring
- Interactive geospatial maps with satellite imagery overlays
- AI chatbot (Terrabot) for natural language climate queries
- Heat island detection and water body monitoring

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework**: Streamlit-based single-page application with component-based architecture

**Design Pattern**: The application follows a modular component structure where each major feature is isolated into its own component module:
- `components/dashboard.py` - Stakeholder-specific dashboard views
- `components/chatbot.py` - AI assistant chat interface
- `components/maps.py` - Interactive geospatial visualizations

**Rationale**: Streamlit was chosen for rapid prototyping of data-driven applications with minimal frontend code. The component-based approach allows for independent development and testing of features while maintaining a cohesive user experience.

**UI/UX Approach**: 
- Wide layout with expandable sidebar for stakeholder and module selection
- Custom CSS for professional styling and fixed footer
- Plotly for interactive charts and visualizations
- Folium/Leaflet integration for map rendering via `streamlit-folium`

**State Management**: Session state is used for chat history persistence and user interactions across reruns.

### Backend Architecture

**Service Layer Pattern**: The application implements a service-oriented architecture with three core services:

1. **NASAService** (`services/nasa_service.py`)
   - Integrates NASA Earth observation APIs (Landsat, MODIS, VIIRS)
   - Provides satellite imagery and temperature data
   - Uses NASA API key authentication (defaults to DEMO_KEY)

2. **WeatherService** (`services/weather_service.py`)
   - Integrates Open-Meteo API for real-time weather data
   - Provides current conditions and forecasts
   - No authentication required (open API)

3. **GeminiService** (`services/gemini_service.py`)
   - Integrates Google Gemini AI for natural language processing
   - Powers the Terrabot chatbot with context-aware responses
   - Requires GEMINI_API_KEY environment variable

**Design Rationale**: Service abstraction isolates external API dependencies, making the system resilient to API changes and enabling mock implementations for testing. Each service handles its own error handling and API communication.

**Utility Modules**:
- `utils/data_utils.py` - Metric calculations (heat index, AQI, comfort index, lake health)
- `utils/map_utils.py` - Map creation and layer management utilities

**Data Flow**: 
1. User selects stakeholder/module in sidebar
2. Main app fetches data from services (NASA, Weather, Gemini)
3. Data is processed through utility functions
4. Components render visualizations based on processed data

### Data Processing

**Metric Calculations**: Custom algorithms for derived metrics:
- Heat index from temperature and humidity
- Simplified AQI from PM2.5 and PM10 values
- Lake health estimates based on environmental conditions
- Comfort index for outdoor activity recommendations

**Geographic Data**: Bengaluru coordinates (12.9716, 77.5946) are hardcoded as the primary location. The system supports coordinate-based queries for specific locations within the city.

### AI Integration

**Gemini API Implementation**: 
- System prompt defines Terrabot as a Bengaluru-focused climate assistant
- Context injection includes real-time weather, air quality, and NASA data
- Generates natural language responses to user queries about climate conditions

**Conversation Management**: Chat history stored in Streamlit session state with role-based message tracking (user/assistant).

**Sample Query Support**: Predefined questions help users understand chatbot capabilities (air quality checks, heat island locations, lake health, weather forecasts).

## External Dependencies

### Third-Party APIs

1. **NASA Earth Observation APIs**
   - **Purpose**: Satellite imagery and Earth observation data
   - **Endpoints**: Landsat imagery, MODIS temperature data
   - **Authentication**: API key via `NASA_API_KEY` environment variable (defaults to DEMO_KEY)
   - **Base URL**: `https://api.nasa.gov`

2. **Open-Meteo Weather API**
   - **Purpose**: Real-time weather conditions and forecasts
   - **Data Points**: Temperature, humidity, wind speed/direction, weather codes
   - **Authentication**: None required (open API)
   - **Base URL**: `https://api.open-meteo.com/v1`
   - **Timezone**: Asia/Kolkata

3. **Google Gemini AI**
   - **Purpose**: Natural language processing for chatbot
   - **Authentication**: API key via `GEMINI_API_KEY` environment variable
   - **Library**: `google-genai` Python SDK
   - **Model**: Uses client.models.generate_content()

### Visualization Libraries

- **Plotly Express & Graph Objects**: Interactive charts and metrics visualization
- **Folium**: Map creation with multiple tile layers (OpenStreetMap, Satellite/Esri, CartoDB)
- **streamlit-folium**: Bridge between Folium maps and Streamlit interface

### Map Tile Providers

1. **OpenStreetMap**: Default base layer
2. **Esri World Imagery**: Satellite view layer
3. **CartoDB Positron**: Clean light map alternative

### Python Packages

- `streamlit` - Web application framework
- `pandas` - Data manipulation
- `numpy` - Numerical computations (for metric calculations)
- `requests` - HTTP client for API calls
- `folium` - Interactive maps
- `plotly` - Data visualization
- `google-genai` - Gemini AI SDK

### Environment Configuration

Required environment variables:
- `GEMINI_API_KEY` - Google Gemini API authentication (required for chatbot)
- `NASA_API_KEY` - NASA API authentication (optional, defaults to DEMO_KEY)

### Data Sources

**No Database**: The application does not use persistent data storage. All data is fetched on-demand from external APIs and processed in-memory. This design choice prioritizes real-time data freshness over historical analysis.

**Future Considerations**: If historical trend analysis becomes a requirement, a time-series database (e.g., InfluxDB, TimescaleDB) would be recommended for storing weather and air quality measurements.