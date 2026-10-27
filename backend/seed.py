# Run this ONCE:  python seed.py
# It puts 30 days of fake readings (720 hours) for every pump into Supabase.
from database import add_reading, delete_all
from fake_data import make_reading
from settings import PUMPS

delete_all()                                     # start fresh
for pump in PUMPS:
    rows = [make_reading(pump, hour) for hour in range(720)]
    add_reading(rows)                            # add all 720 rows at once
    print("Added data for", pump)
