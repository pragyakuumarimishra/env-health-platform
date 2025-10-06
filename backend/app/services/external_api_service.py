"""
Service for fetching data from external APIs (OpenAQ, OpenWeatherMap, etc.)
"""
import httpx
from typing import Optional, Dict, List
from datetime import datetime
from app.core.config import settings


class ExternalAPIService:
    """Service for interacting with external air quality and weather APIs"""
    
    @staticmethod
    async def fetch_openweather_current(lat: float, lon: float) -> Optional[Dict]:
        """
        Fetch current weather data from OpenWeatherMap API
        """
        if not settings.OPENWEATHER_API_KEY:
            return None
        
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric"
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                return {
                    "temperature": data.get("main", {}).get("temp"),
                    "humidity": data.get("main", {}).get("humidity"),
                    "pressure": data.get("main", {}).get("pressure"),
                    "weather": data.get("weather", [{}])[0].get("main"),
                    "timestamp": datetime.utcnow()
                }
        except Exception as e:
            print(f"Error fetching OpenWeather data: {e}")
            return None
    
    @staticmethod
    async def fetch_openaq_data(lat: float, lon: float, radius: int = 10000) -> Optional[List[Dict]]:
        """
        Fetch air quality data from OpenAQ API
        """
        url = "https://api.openaq.org/v2/latest"
        params = {
            "coordinates": f"{lat},{lon}",
            "radius": radius,
            "limit": 10
        }
        
        headers = {}
        if settings.OPENAQ_API_KEY:
            headers["X-API-Key"] = settings.OPENAQ_API_KEY
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                results = []
                for result in data.get("results", []):
                    measurements = {}
                    for measurement in result.get("measurements", []):
                        param = measurement.get("parameter")
                        value = measurement.get("value")
                        measurements[param] = value
                    
                    results.append({
                        "station_id": result.get("location"),
                        "lat": result.get("coordinates", {}).get("latitude"),
                        "lon": result.get("coordinates", {}).get("longitude"),
                        "pm25": measurements.get("pm25"),
                        "pm10": measurements.get("pm10"),
                        "no2": measurements.get("no2"),
                        "o3": measurements.get("o3"),
                        "so2": measurements.get("so2"),
                        "timestamp": result.get("measurements", [{}])[0].get("lastUpdated")
                    })
                
                return results
        except Exception as e:
            print(f"Error fetching OpenAQ data: {e}")
            return None
    
    @staticmethod
    def calculate_aqi_from_pm25(pm25: float) -> int:
        """
        Calculate AQI from PM2.5 using US EPA formula
        """
        if pm25 < 0:
            return 0
        elif pm25 <= 12.0:
            return int((50 - 0) / (12.0 - 0.0) * (pm25 - 0.0) + 0)
        elif pm25 <= 35.4:
            return int((100 - 51) / (35.4 - 12.1) * (pm25 - 12.1) + 51)
        elif pm25 <= 55.4:
            return int((150 - 101) / (55.4 - 35.5) * (pm25 - 35.5) + 101)
        elif pm25 <= 150.4:
            return int((200 - 151) / (150.4 - 55.5) * (pm25 - 55.5) + 151)
        elif pm25 <= 250.4:
            return int((300 - 201) / (250.4 - 150.5) * (pm25 - 150.5) + 201)
        elif pm25 <= 350.4:
            return int((400 - 301) / (350.4 - 250.5) * (pm25 - 250.5) + 301)
        else:
            return int((500 - 401) / (500.4 - 350.5) * (pm25 - 350.5) + 401)
