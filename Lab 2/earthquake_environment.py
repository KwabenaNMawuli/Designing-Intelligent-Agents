import random
from datetime import datetime

class EarthquakeEnvironment:
    LOCATIONS = [
        "Accra", "Kumasi", "Tamale", "Takoradi", "Cape Coast",
        "Sunyani", "Koforidua", "Ho", "Bolgatanga", "Wa"
    ]
    
    FAULT_LINES = ["Akwapim Fault", "Coastal Fault", "Northern Fault Zone"]

    def get_reading(self):
        magnitude = round(random.uniform(1.0, 9.0), 1)
        depth_km = round(random.uniform(1.0, 700.0), 1)
        
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "magnitude": magnitude,
            "severity": self._get_severity(magnitude),
            "depth_km": depth_km,
            "location": random.choice(self.LOCATIONS),
            "fault_line": random.choice(self.FAULT_LINES),
            "aftershock_probability": self._aftershock_probability(magnitude),
            "tsunami_risk": self._tsunami_risk(magnitude, depth_km)
        }

    def _get_severity(self, magnitude):
        if magnitude < 2.0:
            return "Micro (Not felt)"
        elif magnitude < 4.0:
            return "Minor (Felt slightly)"
        elif magnitude < 5.0:
            return "Light (Minor damage)"
        elif magnitude < 6.0:
            return "Moderate (Some damage)"
        elif magnitude < 7.0:
            return "Strong (Major damage)"
        elif magnitude < 8.0:
            return "Major (Serious damage)"
        else:
            return "GREAT (Catastrophic)"

    def _aftershock_probability(self, magnitude):
        if magnitude < 4.0:
            return "Low"
        elif magnitude < 6.0:
            return "Moderate"
        else:
            return "High"

    def _tsunami_risk(self, magnitude, depth_km):
        if magnitude >= 7.0 and depth_km < 70:
            return "YES - EVACUATE COASTAL AREAS"
        elif magnitude >= 6.0 and depth_km < 70:
            return "Possible - Monitor coastlines"
        else:
            return "Low"