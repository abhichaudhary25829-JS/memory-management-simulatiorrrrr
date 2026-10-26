def pressure_level(utilization):
    if utilization >= 90: return "Critical"
    if utilization >= 75: return "High"
    if utilization >= 50: return "Moderate"
    return "Normal"
