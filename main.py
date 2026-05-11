from re import search
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
def create_application(request: CreateApplicationRequest, authorization: str = Header(...), supabase=Depends(get_supabase_client)):
	try:
		token = authorization.replace("Bearer ", "")
		user = supabase.auth.get_user(token)
		email = user.user.email
	except AuthApiError as e:
		raise HTTPException(detail=e.message, status_code=403)
	application_dict = request.model_dump()
	application_dict['email'] = email
	
	search_response = (supabase.table("applications").select("*")
		.eq("email", email)
		.eq("company", request.company)
		.eq("job_title", request.job_title)
		.execute()
	)

	if len(search_response.data) > 0:
		raise HTTPException(detail="Application already exists", status_code=404)
		
	response = (supabase.table("applications").insert(application_dict).execute())
	return response

@app.get("/api/all_applications")
def get_all_applications(authorization: str = Header(...),supabase=Depends(get_supabase_client)):
	try:
		token = authorization.replace("Bearer ", "")
		user = supabase.auth.get_user(token)
		email = user.user.email
	except AuthApiError as e:
		raise HTTPException(detail=e.message, status_code=403)

	response = (supabase.table("applications").select("*")
		.eq("email", email)
		.execute()
	)

	return response.data

@app.get("/api/applications")
def get_application(request: GetApplicationRequest, authorization: str = Header(...),supabase=Depends(get_supabase_client)) -> ApplicationDatabaseResponse:
	try:
		token = authorization.replace("Bearer ", "")
		user = supabase.auth.get_user(token)
		email = user.user.email
	except AuthApiError as e:
		raise HTTPException(detail=e.message, status_code=403)

	job_title = request.job_title
	company = request.company
	
	response = (supabase.table("applications").select("*")
		.eq("email", email)
		.eq("company", company)
		.eq("job_title", job_title)
		.execute()
	)

	if len(response.data) != 1:
		raise HTTPException(detail="Application not found", status_code=404)

	application = ApplicationDatabaseResponse(**response.data[0])
	return application
	
@app.put("/api/applications")
def update_application(request: UpdateApplicationRequest, authorization: str = Header(...) , supabase=Depends(get_supabase_client)):
	try:
		token = authorization.replace("Bearer ", "")
		user = supabase.auth.get_user(token)
		email = user.user.email
	except AuthApiError as e:
		raise HTTPException(detail=e.message, status_code=403)

	
	old_job_title = request.old_company_identifiers.job_title
	old_company = request.old_company_identifiers.company
	
	response = (supabase.table("applications").select("*")
		.eq("email", email)
		.eq("company", old_company)
		.eq("job_title", old_job_title)
		.execute()
	)

	if len(response.data) != 1:
		raise HTTPException(detail="Application not found", status_code=404)

	application_to_update = ApplicationDatabaseResponse.model_validate(response.data[0])
	id_to_update = application_to_update.id

	raw_updates = request.model_dump()['updates']
	updates = {}
	for u in raw_updates:
		if raw_updates[u]:
			updates[u] = raw_updates[u]
	
	response = (supabase.table("applications").update(updates).eq("id", id_to_update).execute())

	updated_application = ApplicationDatabaseResponse.model_validate((supabase.table("applications").select("*").eq("id", id_to_update).execute()).data[0])
	return {
		"old": application_to_update,
		"new": updated_application
	}

@app.delete("/api/applications")
def delete_application(request: GetApplicationRequest, authorization: str = Header(...), supabase=Depends(get_supabase_client)):
	try:
		token = authorization.replace("Bearer ", "")
		user = supabase.auth.get_user(token)
		email = user.user.email
	except AuthApiError as e:
		raise HTTPException(detail=e.message, status_code=403)
		
	job_title = request.job_title
	company = request.company
	
	response = (supabase.table("applications").select("*")
		.eq("email", email)
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