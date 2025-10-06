"""
Activity recommendation service implementing the jogging recommendation logic
from the specification document.
"""
from typing import Tuple


def calculate_jogging_score(
    pm25: float,
    humidity: float,
    temp_c: float,
    sensitive: bool
) -> Tuple[int, str, str]:
    """
    Calculate jogging feasibility score based on environmental conditions.
    
    Returns:
        Tuple of (score, label, rationale)
    """
    score = 100
    reasons = []
    
    # PM2.5 impact
    if pm25 > 10:
        deduction = int(pm25 - 10)
        score -= deduction
        reasons.append(f"PM2.5 is {pm25:.1f} µg/m³ (elevated)")
    
    # Humidity impact
    if humidity > 85:
        score -= 10
        reasons.append(f"High humidity ({humidity:.0f}%)")
    
    # Temperature impact
    if temp_c > 32:
        score -= 15
        reasons.append(f"High temperature ({temp_c:.1f}°C)")
    elif temp_c < 5:
        score -= 15
        reasons.append(f"Low temperature ({temp_c:.1f}°C)")
    
    # Sensitivity check (hard stop)
    if sensitive and pm25 > 25:
        return 0, "Not Recommended", f"Sensitivity profile + elevated PM2.5 ({pm25:.1f} µg/m³) makes outdoor activity unsafe"
    
    # Determine label based on score
    if score >= 70:
        label = "Good"
        if not reasons:
            rationale = "Conditions are favorable for jogging"
        else:
            rationale = f"Conditions are acceptable. Minor concerns: {', '.join(reasons)}"
    elif score >= 40:
        label = "Caution"
        rationale = f"Exercise with caution. Issues: {', '.join(reasons)}"
    else:
        label = "Avoid"
        rationale = f"Not recommended. Significant issues: {', '.join(reasons)}"
    
    return score, label, rationale


def calculate_activity_recommendation(
    activity_type: str,
    pm25: float,
    humidity: float,
    temp_c: float,
    sensitive: bool
) -> Tuple[int, str, str]:
    """
    Calculate activity recommendation based on type and conditions.
    Currently supports jogging; can be extended for other activities.
    """
    if activity_type.lower() in ["jogging", "running"]:
        return calculate_jogging_score(pm25, humidity, temp_c, sensitive)
    elif activity_type.lower() in ["walking", "cycling"]:
        # Similar logic but with adjusted thresholds
        score = 100
        reasons = []
        
        if pm25 > 15:
            score -= int((pm25 - 15) * 0.8)
            reasons.append(f"PM2.5 is {pm25:.1f} µg/m³")
        
        if humidity > 90:
            score -= 8
            reasons.append(f"High humidity ({humidity:.0f}%)")
        
        if temp_c > 35 or temp_c < 0:
            score -= 12
            reasons.append(f"Extreme temperature ({temp_c:.1f}°C)")
        
        if sensitive and pm25 > 30:
            return 0, "Not Recommended", f"Sensitivity profile + elevated PM2.5 ({pm25:.1f} µg/m³)"
        
        if score >= 70:
            label = "Good"
            rationale = "Conditions are favorable" if not reasons else f"Acceptable. {', '.join(reasons)}"
        elif score >= 40:
            label = "Caution"
            rationale = f"Proceed with caution. {', '.join(reasons)}"
        else:
            label = "Avoid"
            rationale = f"Not recommended. {', '.join(reasons)}"
        
        return score, label, rationale
    else:
        # Default generic assessment
        return 50, "Unknown", "Activity type not yet supported"
