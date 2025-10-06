import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Button,
  CircularProgress
} from '@mui/material';
import axios from 'axios';
import AirQualityDisplay from './AirQualityDisplay';
import IndoorSensors from './IndoorSensors';
import ActivityRecommendation from './ActivityRecommendation';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function Dashboard({ onLogout }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/auth/profile`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProfile(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Failed to fetch profile:', err);
      if (err.response?.status === 401) {
        onLogout();
      }
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">
          Environmental Health Dashboard
        </Typography>
        <Button variant="outlined" onClick={onLogout}>
          Logout
        </Button>
      </Box>

      {profile && (
        <Paper sx={{ p: 2, mb: 3 }}>
          <Typography variant="h6">Welcome, {profile.name || profile.email}</Typography>
          <Typography variant="body2" color="text.secondary">
            Sensitivity Level: {profile.sensitivity_level}
          </Typography>
        </Paper>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <AirQualityDisplay />
        </Grid>
        <Grid item xs={12} md={6}>
          <IndoorSensors />
        </Grid>
        <Grid item xs={12}>
          <ActivityRecommendation />
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;
