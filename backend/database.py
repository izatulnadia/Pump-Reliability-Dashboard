# Everything that talks to Supabase (the database) is in this file.
import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()                                    # reads your keys from the .env file
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])


def get_oldest(pump, count):
    """The first readings of a pump (when it was healthy)."""
    result = supabase.table("readings").select("*").eq("pump", pump).order("id").limit(count).execute()
    return result.data


def get_newest(pump, count):
    """The latest readings of a pump, newest first."""
    result = supabase.table("readings").select("*").eq("pump", pump).order("id", desc=True).limit(count).execute()
    return result.data


def count_readings(pump):
    result = supabase.table("readings").select("id", count="exact").eq("pump", pump).execute()
    return result.count


def add_reading(row):                            # CREATE
    supabase.table("readings").insert(row).execute()


def update_reading(reading_id, values):          # UPDATE
    supabase.table("readings").update(values).eq("id", reading_id).execute()


def delete_reading(reading_id):                  # DELETE
    supabase.table("readings").delete().eq("id", reading_id).execute()


def delete_all():
    supabase.table("readings").delete().neq("id", 0).execute()
