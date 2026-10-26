def health_status(cpu, ram, swap=0):
    peak=max(cpu,ram,swap)
    if peak>=90: return "Critical", "One or more resources are at or above 90%."
    if peak>=75: return "High Load", "A resource is above 75%; sustained load may affect responsiveness."
    if peak>=60: return "Warning", "Utilization is elevated but capacity remains."
    return "Normal", "Resource utilization is within comfortable operating limits."
