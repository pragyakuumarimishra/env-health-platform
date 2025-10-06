"""
Tests for activity recommendation service
"""
import pytest
from app.services.activity_service import calculate_jogging_score, calculate_activity_recommendation


def test_jogging_score_good_conditions():
    """Test jogging score with favorable conditions"""
    score, label, rationale = calculate_jogging_score(
        pm25=8.0,
        humidity=60.0,
        temp_c=22.0,
        sensitive=False
    )
    
    assert score == 100
    assert label == "Good"
    assert "favorable" in rationale.lower()


def test_jogging_score_high_pm25():
    """Test jogging score with elevated PM2.5"""
    score, label, rationale = calculate_jogging_score(
        pm25=25.0,
        humidity=60.0,
        temp_c=22.0,
        sensitive=False
    )
    
    assert score == 85  # 100 - (25-10) = 85
    assert label == "Good"
    assert "PM2.5" in rationale


def test_jogging_score_high_humidity():
    """Test jogging score with high humidity"""
    score, label, rationale = calculate_jogging_score(
        pm25=8.0,
        humidity=90.0,
        temp_c=22.0,
        sensitive=False
    )
    
    assert score == 90  # 100 - 10
    assert label == "Good"
    assert "humidity" in rationale.lower()


def test_jogging_score_extreme_temp_high():
    """Test jogging score with high temperature"""
    score, label, rationale = calculate_jogging_score(
        pm25=8.0,
        humidity=60.0,
        temp_c=35.0,
        sensitive=False
    )
    
    assert score == 85  # 100 - 15
    assert label == "Good"
    assert "temperature" in rationale.lower()


def test_jogging_score_extreme_temp_low():
    """Test jogging score with low temperature"""
    score, label, rationale = calculate_jogging_score(
        pm25=8.0,
        humidity=60.0,
        temp_c=2.0,
        sensitive=False
    )
    
    assert score == 85  # 100 - 15
    assert label == "Good"
    assert "temperature" in rationale.lower()


def test_jogging_score_caution():
    """Test jogging score resulting in caution"""
    score, label, rationale = calculate_jogging_score(
        pm25=45.0,
        humidity=88.0,
        temp_c=22.0,
        sensitive=False
    )
    
    # 100 - (45-10) - 10 = 55
    assert 40 <= score < 70
    assert label == "Caution"


def test_jogging_score_avoid():
    """Test jogging score resulting in avoid"""
    score, label, rationale = calculate_jogging_score(
        pm25=65.0,
        humidity=88.0,
        temp_c=35.0,
        sensitive=False
    )
    
    # 100 - (65-10) - 10 - 15 = 20
    assert score < 40
    assert label == "Avoid"


def test_jogging_score_sensitive_hard_stop():
    """Test jogging score with sensitive user and high PM2.5"""
    score, label, rationale = calculate_jogging_score(
        pm25=30.0,
        humidity=60.0,
        temp_c=22.0,
        sensitive=True
    )
    
    assert score == 0
    assert label == "Not Recommended"
    assert "Sensitivity" in rationale


def test_activity_recommendation_walking():
    """Test activity recommendation for walking"""
    score, label, rationale = calculate_activity_recommendation(
        activity_type="walking",
        pm25=12.0,
        humidity=60.0,
        temp_c=22.0,
        sensitive=False
    )
    
    assert score >= 70
    assert label == "Good"


def test_activity_recommendation_cycling():
    """Test activity recommendation for cycling"""
    score, label, rationale = calculate_activity_recommendation(
        activity_type="cycling",
        pm25=12.0,
        humidity=60.0,
        temp_c=22.0,
        sensitive=False
    )
    
    assert score >= 70
    assert label == "Good"


def test_activity_recommendation_unknown():
    """Test activity recommendation for unknown activity"""
    score, label, rationale = calculate_activity_recommendation(
        activity_type="unknown_activity",
        pm25=12.0,
        humidity=60.0,
        temp_c=22.0,
        sensitive=False
    )
    
    assert label == "Unknown"
