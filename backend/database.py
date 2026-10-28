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


def add_reading(row):                            # CREATE
    run(lambda db: db.table("readings").insert(row))


def update_reading(reading_id, values):          # UPDATE
    run(lambda db: db.table("readings").update(values).eq("id", reading_id))


def delete_reading(reading_id):                  # DELETE
    run(lambda db: db.table("readings").delete().eq("id", reading_id))


def delete_all():
    run(lambda db: db.table("readings").delete().neq("id", 0))
