# The brain: detects anomalies, forecasts when each parameter hits its alarm limit,
# and decides the status (Normal, Warning or Alarm) of each parameter.
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from rca import find_causes, make_insights
from settings import FORECAST_HOURS, LIMITS, WARNING_HOURS

RANK = {"Normal": 0, "Warning": 1, "Alarm": 2}


def reached_limit(value, info):
    """Has this value reached its alarm limit?"""
    if info["type"] == "high":
        return value >= info["limit"]
    return value <= info["limit"]


def forecast(values):
    """TIME SERIES FORECAST using Holt's exponential smoothing.
    It follows two things: the LEVEL (where the value is now) and the TREND (how fast it moves).
    Returns the next 14 days, one value for every hour."""
    if len(values) < 24:
        return []
    model = ExponentialSmoothing(
        values[-120:],
        trend="add",
        bounds={"smoothing_level": (0.01, 0.3), "smoothing_trend": (0.001, 0.05)},
    )                                                               # use the last 5 days
    # Low smoothing values keep the trend steady, so noise does not cause false alarms
    fitted = model.fit()
    return list(fitted.forecast(FORECAST_HOURS))


def hours_until_alarm(future, info):
    """In which hour does the forecast reach the alarm limit? (None = not within 14 days)"""
    for hour, value in enumerate(future, start=1):
        if reached_limit(value, info):
            return hour
    return None


def get_status(value, z, hours, info):
    if reached_limit(value, info):
        return "Alarm"
    if abs(z) > 3:                                    # far from normal = anomaly
        return "Warning"
    if hours is not None and hours < WARNING_HOURS:   # alarm expected within 7 days
        return "Warning"
    return "Normal"


def analyse_parameter(key, info, first, recent):
    """Analyse ONE parameter, for example vibration."""
    values = recent[key].tolist()
    value = values[-1]                                # the latest reading

    # ANOMALY: how many standard deviations is the pump away from its healthy self?
    # (average of the last 6 readings, so one noisy reading cannot cause a false alarm)
    normal = first[key].mean()
    spread = first[key].std()
    z = 0
    if spread > 0:                                    # (spread is 0 or missing if there is too little data)
        z = (recent[key].tail(6).mean() - normal) / spread

    future = forecast(values)
    hours = hours_until_alarm(future, info)
    status = get_status(value, z, hours, info)

    # For the bar on the card: 0% = normal value, 100% = alarm limit
    percent = (value - normal) / (info["limit"] - normal) * 100
    percent = max(0, min(100, percent))

    per_day = None
    if len(future) > 24:
        per_day = future[24] - future[0]              # how much it changes in 24 hours

    return {
        "name": info["name"], "unit": info["unit"], "limit": info["limit"],
        "value": round(value, 2), "normal": round(normal, 2), "z": round(z, 1),
        "hours": hours, "status": status, "percent": round(percent, 1),
        "per_day": None if per_day is None else round(per_day, 2),
        "history": [round(v, 2) for v in values[-72:]],       # last 72 hours, for the graph
        "forecast": [round(v, 2) for v in future[:168]],      # next 7 days, for the graph
    }


def danger(p):
    """A number that is higher when the parameter is in worse shape."""
    return RANK[p["status"]] * 1000 + p["percent"]


def make_summary(params, recent):
    """The numbers for the indicator tiles at the top of the dashboard."""
    items = list(params.values())
    worst = max(items, key=danger)
    alarm_hours = [p["hours"] for p in items if p["hours"]]
    needs_attention = [p for p in items if p["status"] != "Normal"]

    return {
        "health": round(100 - max(p["percent"] for p in items)),    # 100 = far from all alarms
        "status": worst["status"],
        "first_alarm": min(alarm_hours) if alarm_hours else None,
        "attention": len(needs_attention),
        "critical": worst["name"] if worst["status"] != "Normal" else "None",
        "last_time": str(recent["time"].iloc[-1])[:16].replace("T", " "),
    }


def analyse(first, recent):
    """first = the first 200 readings (healthy pump). recent = the latest 200 readings."""
    params = {}
    for key, info in LIMITS.items():
        params[key] = analyse_parameter(key, info, first, recent)

    return {
        "summary": make_summary(params, recent),
        "parameters": params,
        "insights": make_insights(params),
        "rca": find_causes(params),
    }
