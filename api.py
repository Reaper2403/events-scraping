import os
from dotenv import load_dotenv
from supabase import create_client, Client


# To maintain consistency in data
def fix_data(events):
    keys = ['heading', 'date', 'location', 'organiser', 'registration_link', 'image']
    for event in events:
        for key in keys:
            if key not in event.keys():
                event[key] = 'None'


def add_events(event_data):
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    supabase.table('events').insert(event_data).execute()

