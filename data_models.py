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

class UpdateApplicationRequest(BaseModel):
	company: str
	job_title:str
	date_applied:Optional[str] = None
	application_status:Optional[str] = None

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