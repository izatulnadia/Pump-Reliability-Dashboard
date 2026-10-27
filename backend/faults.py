# The list of known pump faults. This file is only DATA - you can add your own faults.
# FAULTS is a list of possible problems and what grown-ups can do to check and fix them
# main  = parameters that MUST move for this fault ("up" = rises, "down" = falls)
# minor = parameters that may also move a little
# chain = the "why" chain, from the symptom down to the root cause

FAULTS = [
    {
        "name": "Bearing wear or poor lubrication",
        "main": {"vibration": "up", "bearing_temp": "up"},
        "minor": {},
        "chain": [
            "Vibration and bearing temperature are rising",
            "Friction inside the bearing is increasing",
            "The lubricant is low, degraded or contaminated",
            "Root cause: oil not changed on time, or a worn seal lets dirt in",
        ],
        "checks": ["Check oil level and colour",
                   "Take an oil sample and test for metal particles",
                   "Check the vibration spectrum for bearing frequencies"],
        "actions": ["Top up or change the lube oil",
                    "Inspect the bearing and plan a replacement",
                    "Repair or replace the bearing seals"],
        "prevent": "Set an oil analysis and oil change interval, and trend bearing vibration every week.",
    },
    {
        "name": "Impeller wear or internal recirculation",
        "main": {"discharge_pressure": "down", "flow": "down"},
        "minor": {"vibration": "up"},
        "chain": [
            "Discharge pressure and flow are falling",
            "The pump is delivering less head than before",
            "The impeller or wear rings have lost material, so liquid leaks back to suction",
            "Root cause: erosion or corrosion from solids, or running far from the best efficiency point",
        ],
        "checks": ["Check the suction strainer for blockage",
                   "Compare the pump curve with the current head and flow",
                   "Check motor current (it often drops when the impeller is worn)"],
        "actions": ["Clean the suction strainer",
                    "Open the pump and inspect the impeller and wear rings",
                    "Replace worn parts at the next planned shutdown"],
        "prevent": "Filter the process fluid, and keep the pump near its best efficiency point.",
    },
    {
        "name": "Misalignment or unbalance",
        "main": {"vibration": "up"},
        "minor": {"bearing_temp": "up"},
        "chain": [
            "Vibration is rising",
            "The shaft is running off-centre or out of balance",
            "The coupling is misaligned, or the impeller has deposits or damage",
            "Root cause: poor alignment after maintenance, soft foot or pipe strain",
        ],
        "checks": ["Do a laser alignment check",
                   "Check for soft foot and pipe strain",
                   "Look at the vibration spectrum: a peak at 1x or 2x running speed"],
        "actions": ["Realign the pump and motor",
                    "Fix pipe supports and loose bolts",
                    "Balance or clean the impeller"],
        "prevent": "Check alignment after every overhaul and every pipe change.",
    },
    {
        "name": "Seal or cooling problem",
        "main": {"bearing_temp": "up"},
        "minor": {"vibration": "up"},
        "chain": [
            "Bearing temperature is rising",
            "Heat is not being carried away from the bearing",
            "Cooling water or the oil cooler is restricted, or the seal is rubbing",
            "Root cause: fouled cooler or a blocked seal flush line",
        ],
        "checks": ["Check cooling water flow and temperature",
                   "Check the seal flush line",
                   "Check the oil cooler for fouling"],
        "actions": ["Clean the cooler and flush lines",
                    "Replace the seal if it is rubbing",
                    "Confirm the cooling water flow is correct"],
        "prevent": "Add cooling water flow and temperature to the routine inspection round.",
    },
]
