from fastapi import FastAPI, Depends
from supabase import Client
from db import get_db

app = FastAPI()

@app.get("/db_test")
def get_data(db = Depends(get_db)):
	response = db.table("applications").select("*").execute()
	return response