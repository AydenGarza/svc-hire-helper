from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from supabase_client import get_supabase_client
from supabase import AuthApiError
from data_models import CreateApplicationRequest, GetApplicationRequest, UpdateApplicationRequest, ApplicationDatabaseResponse, LoginRequest, RegisterRequest, AuthInfo

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:3000"],
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.post("/api/applications")
def create_application(request: CreateApplicationRequest, supabase=Depends(get_supabase_client)):
	print("this happens")
	response = (supabase.table("applications").insert(request.model_dump()).execute())
	return response

@app.get("/api/applications")
def get_application(request: GetApplicationRequest, supabase=Depends(get_supabase_client)) -> ApplicationDatabaseResponse:
	username = None
	job_title = request.job_title
	company = request.company
	
	response = (supabase.table("applications").select("*")
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
def update_application(request: UpdateApplicationRequest, supabase=Depends(get_supabase_client)):
	username = None
	job_title = request.job_title
	company = request.company
	
	response = (supabase.table("applications").select("*")
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

	response = (supabase.table("applications").update(request.model_dump(exclude_none=True)).eq("id", id_to_update).execute())
	
	return response

@app.delete("/api/applications")
def delete_application(request: GetApplicationRequest, supabase=Depends(get_supabase_client)):
	username = request.username
	job_title = request.job_title
	company = request.company
	
	response = (supabase.table("applications").select("*")
		.eq("username", username)
		.eq("company", company)
		.eq("job_title", job_title)
		.execute()
	)

	if len(response.data) != 1:
		raise HTTPException(detail="Application not found", status_code=404)

	application_to_delete = ApplicationDatabaseResponse.model_validate(response.data[0])
	id_to_delete = application_to_delete.id
	
	response = (supabase.table("applications").delete().eq("id", id_to_delete).execute())
	
	return response	

@app.post("/accounts/register")
def register_account(request: RegisterRequest, supabase=Depends(get_supabase_client)):
	try:
		response = (supabase.auth.sign_up(request.model_dump()))
	except AuthApiError as e:
		raise HTTPException(detail=e.message, status_code=400)
		
	auth_info = AuthInfo.model_validate(
		{
			"access_token": response.session.access_token,
			"refresh_token": response.session.refresh_token
		}
	)
	return auth_info

@app.post("/accounts/login")
def login(request: LoginRequest, supabase=Depends(get_supabase_client)) -> AuthInfo:
	try:
		response = (supabase.auth.sign_in_with_password(request.model_dump()))
	except AuthApiError as e:
		raise HTTPException(detail=e.message, status_code=400)
	
	auth_info = AuthInfo.model_validate(
		{
			"access_token": response.session.access_token,
			"refresh_token": response.session.refresh_token
		}
	)
	return auth_info