from fastapi import FastAPI, Depends, HTTPException
from db import get_db
from data_models import CreateApplicationRequest, GetApplicationRequest, UpdateApplicationRequest, ApplicationDatabaseResponse, LoginRequest
import supabase

app = FastAPI()

@app.post("/api/applications")
def create_application(request: CreateApplicationRequest, db = Depends(get_db)):
	print("this happens")
	response = (db.table("applications").insert(request.model_dump()).execute())
	return response

@app.get("/api/applications")
def get_application(request: GetApplicationRequest, db=Depends(get_db)) -> ApplicationDatabaseResponse:
	username = request.username
	job_title = request.job_title
	company = request.company
	
	response = (db.table("applications").select("*")
		.eq("username", username)
		.eq("company", company)
		.eq("job_title", job_title)
		.execute()
	)

	if len(response.data) != 1:
		raise HTTPException(detail="Application not found", status_code=404)

	application = ApplicationDatabaseResponse(**response.data[0])
	return application
	
@app.put("/api/applications")
def update_application(request: UpdateApplicationRequest, db=Depends(get_db)):
	username = request.username
	job_title = request.job_title
	company = request.company
	
	response = (db.table("applications").select("*")
		.eq("username", username)
		.eq("company", company)
		.eq("job_title", job_title)
		.execute()
	)

	if len(response.data) != 1:
		raise HTTPException(detail="Application not found", status_code=404)

	application_to_update = ApplicationDatabaseResponse.model_validate(response.data[0])
	id_to_update = application_to_update.id

	if username != application_to_update.username:
		raise HTTPException(detail="You cannot update the username for an application", status_code=403)

	response = (db.table("applications").update(request.model_dump(exclude_none=True)).eq("id", id_to_update).execute())
	
	return response

@app.delete("/api/applications")
def delete_application(request: GetApplicationRequest, db=Depends(get_db)):
	username = request.username
	job_title = request.job_title
	company = request.company
	
	response = (db.table("applications").select("*")
		.eq("username", username)
		.eq("company", company)
		.eq("job_title", job_title)
		.execute()
	)

	if len(response.data) != 1:
		raise HTTPException(detail="Application not found", status_code=404)

	application_to_delete = ApplicationDatabaseResponse.model_validate(response.data[0])
	id_to_delete = application_to_delete.id
	
	response = (db.table("applications").delete().eq("id", id_to_delete).execute())
	
	return response	

@app.post("/login")
def login(request: LoginRequest, db=Depends(get_db)):
	raise HTTPException(detail="Auth isn't implemented yet :(", status_code=500)