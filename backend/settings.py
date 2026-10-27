# Settings you may want to change: the pumps and the alarm limits.

# The pumps in the plant. "fault" and "start" are only used to make the fake data
# ("start" = the hour when the fault begins to grow).
PUMPS = {
    "P-101": {"service": "Crude booster pump", "fault": "bearing",  "start": 500},
    "P-102": {"service": "Cooling water pump", "fault": "none",     "start": 0},
    "P-103": {"service": "Export pump",        "fault": "impeller", "start": 500},
    "P-104": {"service": "Injection pump",     "fault": "bearing",  "start": 640},
}

# Alarm limits (these are example values - use your plant's real limits).
# type "high" = alarm when the value rises to the limit
# type "low"  = alarm when the value falls to the limit
LIMITS = {
    "vibration":          {"name": "Vibration",           "unit": "mm/s", "limit": 7.1, "type": "high"},
    "bearing_temp":       {"name": "Bearing temperature", "unit": "°C",   "limit": 90,  "type": "high"},
    "discharge_pressure": {"name": "Discharge pressure",  "unit": "bar",  "limit": 8.0, "type": "low"},
    "flow":               {"name": "Flow",                "unit": "m³/h", "limit": 80,  "type": "low"},
}

FORECAST_HOURS = 336   # how far ahead to forecast: 14 days
WARNING_HOURS = 168    # show a Warning if an alarm is forecast within 7 days
