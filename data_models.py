from typing import Optional
from pydantic import BaseModel, EmailStr

class CreateApplicationRequest(BaseModel):
	company: str
	job_title:str
	date_applied:str
	application_status:str

class GetApplicationRequest(BaseModel):
	company: str
	job_title: str

class ApplicationUpdateFields(BaseModel):
	new_company: Optional[str] = None
	new_job_title:Optional[str] = None
	new_date_applied:Optional[str] = None
	new_application_status:Optional[str] = None

class UpdateApplicationRequest(BaseModel):
	old_company_identifiers: GetApplicationRequest
	updates: ApplicationUpdateFields

class ApplicationDatabaseResponse(BaseModel):
	company: str
	job_title:str
	date_applied:str
	application_status:str
	email:str
	id: int

class LoginRequest(BaseModel):
	email: EmailStr 
	password:str

class RegisterRequest(BaseModel):
	email: EmailStr 
	password:str

class AuthInfo(BaseModel):
	access_token:str
	refresh_token: str