from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET")

if not SUPABASE_KEY or not SUPABASE_URL:
	raise Exception("Supabase credentials were not loaded from environment")

app = FastAPI()

