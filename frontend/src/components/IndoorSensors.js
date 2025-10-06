import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  CircularProgress,
  Alert
} from '@mui/material';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function IndoorSensors() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDevices();
  }, []);

  const fetchDevices = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/indoor/devices`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setDevices(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Failed to fetch devices:', err);
      setLoading(false);
    }
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
          Indoor Sensors
        </Typography>
        {devices.length === 0 ? (
          <Alert severity="info">
            No indoor sensors registered yet. Add a sensor to monitor indoor air quality.
          </Alert>
        ) : (
          <Box>
            {devices.map((device) => (
              <Box key={device.id} sx={{ mb: 2, p: 2, border: '1px solid #e0e0e0', borderRadius: 1 }}>
                <Typography variant="subtitle1">{device.label}</Typography>
                <Typography variant="body2" color="text.secondary">
                  {device.indoor ? 'Indoor' : 'Outdoor'} Sensor
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Firmware: {device.firmware_version || 'Unknown'}
                </Typography>
              </Box>
            ))}
          </Box>
        )}
        <Button variant="outlined" fullWidth sx={{ mt: 2 }}>
          Add Sensor
        </Button>
      </CardContent>
    </Card>
  );
}

export default IndoorSensors;
