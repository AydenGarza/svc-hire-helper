from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET")

if not SUPABASE_KEY or not SUPABASE_URL:
	raise Exception("Supabase credentials were not loaded from environment")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

response = (supabase.table("applications").select("*").execute())

print(response)

app = FastAPI()

