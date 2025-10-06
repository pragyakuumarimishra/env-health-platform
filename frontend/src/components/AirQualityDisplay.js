import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  CircularProgress
} from '@mui/material';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function AirQualityDisplay() {
  const [aqData, setAqData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAirQuality();
  }, []);

  const fetchAirQuality = async () => {
    try {
      const token = localStorage.getItem('token');
      // Default location (can be replaced with user's location)
      const response = await axios.get(`${API_URL}/aq/current`, {
        params: { lat: 40.7128, lon: -74.0060 },
        headers: { Authorization: `Bearer ${token}` }
      });
      setAqData(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Failed to fetch air quality:', err);
      setLoading(false);
    }
  };

  const getAQIColor = (aqi) => {
    if (aqi <= 50) return 'success';
    if (aqi <= 100) return 'warning';
    if (aqi <= 150) return 'error';
    return 'error';
  };

  const getAQILabel = (aqi) => {
    if (aqi <= 50) return 'Good';
    if (aqi <= 100) return 'Moderate';
    if (aqi <= 150) return 'Unhealthy for Sensitive Groups';
    if (aqi <= 200) return 'Unhealthy';
    if (aqi <= 300) return 'Very Unhealthy';
    return 'Hazardous';
  };

  if (loading) {
    return (
      <Card>
        <CardContent>
          <Box display="flex" justifyContent="center" p={3}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Outdoor Air Quality
        </Typography>
        {aqData && (
          <Box>
            <Box sx={{ mb: 2 }}>
              <Chip
                label={`AQI: ${aqData.aqi} - ${getAQILabel(aqData.aqi)}`}
                color={getAQIColor(aqData.aqi)}
                size="large"
              />
            </Box>
            <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
              <Box>
                <Typography variant="body2" color="text.secondary">PM2.5</Typography>
                <Typography variant="h6">{aqData.pm25?.toFixed(1)} µg/m³</Typography>
              </Box>
              <Box>
                <Typography variant="body2" color="text.secondary">PM10</Typography>
                <Typography variant="h6">{aqData.pm10?.toFixed(1)} µg/m³</Typography>
              </Box>
              <Box>
                <Typography variant="body2" color="text.secondary">NO₂</Typography>
                <Typography variant="h6">{aqData.no2?.toFixed(1)} µg/m³</Typography>
              </Box>
              <Box>
                <Typography variant="body2" color="text.secondary">O₃</Typography>
                <Typography variant="h6">{aqData.o3?.toFixed(1)} µg/m³</Typography>
              </Box>
            </Box>
            <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
              Updated: {new Date(aqData.ts).toLocaleString()}
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
}

export default AirQualityDisplay;
