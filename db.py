import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET")

if not SUPABASE_KEY or not SUPABASE_URL:
	raise Exception("Supabase credentials were not loaded from environment")

db: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_db() -> Client:
	return db