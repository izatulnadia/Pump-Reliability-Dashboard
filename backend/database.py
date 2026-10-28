# Everything that talks to Supabase (the database) is in this file.
import os

import httpx
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()                                    # reads your keys from the .env file


def connect():
    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])


supabase = connect()


def run(query):
    """Run a database query. If the connection went stale while the app was
    idle (e.g. "Broken pipe"), reconnect and try once more."""
    global supabase
    try:
        return query(supabase).execute()
    except httpx.TransportError:
        supabase = connect()
        return query(supabase).execute()


def get_oldest(pump, count):
    """The first readings of a pump (when it was healthy)."""
    return run(lambda db: db.table("readings").select("*").eq("pump", pump).order("id").limit(count)).data


def get_newest(pump, count):
    """The latest readings of a pump, newest first."""
    return run(lambda db: db.table("readings").select("*").eq("pump", pump).order("id", desc=True).limit(count)).data


def count_readings(pump):
    return run(lambda db: db.table("readings").select("id", count="exact").eq("pump", pump)).count


def add_reading(row):                            # CREATE (gives back the new id)
    rows = run(lambda db: db.table("readings").insert(row)).data
    return rows[0]["id"] if rows else None


def update_reading(reading_id, values):          # UPDATE
    run(lambda db: db.table("readings").update(values).eq("id", reading_id))


def delete_reading(reading_id):                  # DELETE
    run(lambda db: db.table("readings").delete().eq("id", reading_id))


def delete_all():
    run(lambda db: db.table("readings").delete().neq("id", 0))


# ---------------------------------------------------------------
# HISTORY of changes (the "activity_log" table)
# ---------------------------------------------------------------
def get_reading(reading_id):
    rows = run(lambda db: db.table("readings").select("*").eq("id", reading_id)).data
    return rows[0] if rows else None


def add_log(action, pump, reading_id, details):
    """Write one line of history. A problem here never stops the change itself."""
    try:
        run(lambda db: db.table("activity_log").insert(
            {"action": action, "pump": pump, "reading_id": reading_id, "details": details}))
    except Exception as error:
        print("Could not write to activity_log:", error)


def get_log(pump, count):
    """The latest history lines of a pump, newest first."""
    return run(lambda db: db.table("activity_log").select("*").eq("pump", pump).order("id", desc=True).limit(count)).data
