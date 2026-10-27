# Root cause analysis (rules, no AI) and the short "insight" sentences.
from faults import FAULTS


def find_abnormal(params):
    """Which parameters are not normal, and which way did they move? Example: {"vibration": "up"}"""
    abnormal = {}
    for key, p in params.items():
        if p["status"] != "Normal":
            if p["value"] > p["normal"]:
                abnormal[key] = "up"
            else:
                abnormal[key] = "down"
    return abnormal


def score_fault(fault, abnormal):
    """How well does this fault match what we see? Returns 0 to 100."""
    # 1. Count the "main" symptoms that match
    matched = 0
    for key, way in fault["main"].items():
        if abnormal.get(key) == way:
            matched += 1
    if matched == 0:
        return 0

    # 2. Abnormal parameters that this fault cannot explain count against it
    unexplained = 0
    for key, way in abnormal.items():
        if key in fault["main"]:
            if fault["main"][key] != way:
                unexplained += 1          # it moved the wrong way
        elif fault["minor"].get(key) == way:
            unexplained += 0.5            # explained only partly
        else:
            unexplained += 1              # not explained at all

    return round(matched / (len(fault["main"]) + unexplained) * 100)


def find_causes(params):
    """Score every known fault. Returns the list with the best match first."""
    abnormal = find_abnormal(params)
    causes = []
    for fault in FAULTS:
        score = score_fault(fault, abnormal)
        if score == 0:
            continue

        # Evidence = the readings that support this fault
        evidence = []
        for key, way in fault["main"].items():
            if abnormal.get(key) == way:
                p = params[key]
                side = "above" if way == "up" else "below"
                evidence.append(f"{p['name']} is {side} normal: {p['value']} {p['unit']} (normal {p['normal']})")

        if score >= 70:
            confidence = "High"
        elif score >= 40:
            confidence = "Medium"
        else:
            confidence = "Low"

        causes.append({"name": fault["name"], "score": score, "confidence": confidence,
                       "evidence": evidence, "chain": fault["chain"], "checks": fault["checks"],
                       "actions": fault["actions"], "prevent": fault["prevent"]})

    causes.sort(key=lambda c: c["score"], reverse=True)       # best match first
    return causes


def make_insights(params):
    """A few plain sentences that explain what the numbers mean."""
    notes = []
    items = list(params.values())

    # Anything already at its alarm limit?
    for p in items:
        if p["status"] == "Alarm":
            notes.append(f"{p['name']} is already at its alarm limit ({p['value']} {p['unit']}).")

    # Which parameter will reach its alarm limit first?
    with_alarm = [p for p in items if p["hours"]]
    if with_alarm:
        first = min(with_alarm, key=lambda p: p["hours"])
        notes.append(f"{first['name']} will reach its alarm limit first, "
                     f"in about {first['hours']} hours ({first['hours'] / 24:.1f} days).")

    for p in items:
        if p["hours"]:                                        # a speed only makes sense if an alarm is coming
            way = "rising" if p["per_day"] > 0 else "falling"
            notes.append(f"{p['name']} is {way} by about {abs(p['per_day'])} {p['unit']} per day.")
        elif p["status"] == "Warning":
            notes.append(f"{p['name']} is {abs(p['z'])} standard deviations from normal, "
                         "but no alarm is forecast within 14 days.")

    if not notes:
        notes.append("All four parameters are within their normal range.")
    return notes[:5]                                          # keep the first 5 only
