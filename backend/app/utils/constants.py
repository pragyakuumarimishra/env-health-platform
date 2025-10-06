"""
Constants and configuration values used throughout the application
"""

# WHO Air Quality Guidelines (µg/m³)
WHO_PM25_24H_GUIDELINE = 15
WHO_PM10_24H_GUIDELINE = 45
WHO_NO2_24H_GUIDELINE = 25
WHO_O3_8H_GUIDELINE = 100

# Activity recommendation thresholds
JOGGING_GOOD_SCORE = 70
JOGGING_CAUTION_SCORE = 40
JOGGING_PM25_THRESHOLD = 10
JOGGING_HUMIDITY_THRESHOLD = 85
JOGGING_TEMP_HIGH = 32
JOGGING_TEMP_LOW = 5
JOGGING_SENSITIVE_PM25_LIMIT = 25

# Sensitivity levels
SENSITIVITY_LOW = 1
SENSITIVITY_MODERATE = 2
SENSITIVITY_HIGH = 3
SENSITIVITY_VERY_HIGH = 4
SENSITIVITY_SEVERE = 5

# Alert types
ALERT_TYPE_PM25_THRESHOLD = "pm25_threshold"
ALERT_TYPE_VENTILATION = "ventilation"
ALERT_TYPE_EXPOSURE_BUDGET = "exposure_budget"
ALERT_TYPE_SYMPTOM_CORRELATION = "symptom_correlation"
ALERT_TYPE_FIRE_PROXIMITY = "fire_proximity"

# Sensor data quality
SENSOR_READING_MAX_AGE_MINUTES = 60
SENSOR_CO2_THRESHOLD = 1000
SENSOR_VOC_NORMAL_MAX = 150

# AQI breakpoints (US EPA)
AQI_BREAKPOINTS = [
    (0, 12.0, 0, 50),      # Good
    (12.1, 35.4, 51, 100),  # Moderate
    (35.5, 55.4, 101, 150), # Unhealthy for Sensitive Groups
    (55.5, 150.4, 151, 200),# Unhealthy
    (150.5, 250.4, 201, 300),# Very Unhealthy
    (250.5, 350.4, 301, 400),# Hazardous
    (350.5, 500.4, 401, 500),# Hazardous
]
