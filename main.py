from fastapi import FastAPI, Depends
from supabase import Client
from db import get_db
from job_application import JobApplication 

app = FastAPI()

@app.get("/db_test")
def get_data(db = Depends(get_db)):
	response = db.table("applications").select("*").execute()
	return response

@app.post("/create_application")
def create_application(application: JobApplication, db = Depends(get_db)):
	print("this happens")
	response = (db.table("applications").insert(application.model_dump()).execute())
	return response