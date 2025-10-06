import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  TextField,
  Button,
  Alert,
  Chip
} from '@mui/material';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function ActivityRecommendation() {
  const [activity, setActivity] = useState('jogging');
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleRecommend = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_URL}/activity/recommend`,
        {
          activity_type: activity,
          location_lat: 40.7128,
          location_lon: -74.0060
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setRecommendation(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Failed to get recommendation:', err);
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 70) return 'success';
    if (score >= 40) return 'warning';
    return 'error';
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Activity Recommendation
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <TextField
            fullWidth
            label="Activity Type"
            value={activity}
            onChange={(e) => setActivity(e.target.value)}
            placeholder="e.g., jogging, cycling, walking"
          />
          <Button
            variant="contained"
            onClick={handleRecommend}
            disabled={loading}
          >
            Get Recommendation
          </Button>
        </Box>
        {recommendation && (
          <Alert severity={recommendation.score >= 70 ? 'success' : recommendation.score >= 40 ? 'warning' : 'error'}>
            <Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                <Typography variant="subtitle1">
                  {recommendation.activity_type}
                </Typography>
                <Chip
                  label={`Score: ${recommendation.score}`}
                  color={getScoreColor(recommendation.score)}
                  size="small"
                />
              </Box>
              <Typography variant="body2">
                {recommendation.rationale}
              </Typography>
            </Box>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
}

export default ActivityRecommendation;
