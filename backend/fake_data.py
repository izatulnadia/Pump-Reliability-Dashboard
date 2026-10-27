# Makes fake sensor readings, so you can try the app without a real pump.
import random
from datetime import datetime, timedelta

from settings import PUMPS


def make_reading(pump, hour):
    """Make the reading of one pump for one hour (hour 0 = first hour)."""
    # How many hours since the fault started? (0 for a healthy pump)
    hours_of_fault = max(0, hour - PUMPS[pump]["start"])
    fault = PUMPS[pump]["fault"]

    # Healthy values
    vibration, temp, pressure, flow = 3.0, 70.0, 10.0, 100.0

    # A fault slowly changes the values
    if fault == "bearing":              # bearing wear: vibration and temperature rise
        vibration += hours_of_fault * 0.012
        temp += hours_of_fault * 0.06
    if fault == "impeller":             # impeller wear: pressure and flow fall
        pressure -= hours_of_fault * 0.0075
        flow -= hours_of_fault * 0.07
        vibration += hours_of_fault * 0.004

    # random.gauss adds a little random noise, like a real sensor
    return {
        "pump": pump,
        "time": (datetime(2026, 9, 21) + timedelta(hours=hour)).isoformat(),
        "vibration": round(vibration + random.gauss(0, 0.1), 2),
        "bearing_temp": round(temp + random.gauss(0, 0.5), 1),
        "discharge_pressure": round(pressure + random.gauss(0, 0.05), 2),
        "flow": round(flow + random.gauss(0, 0.8), 1),
    }
