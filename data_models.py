from typing import Optional
from pydantic import BaseModel

class CreateApplicationRequest(BaseModel):
	company: str
	job_title:str
	date_applied:str
	application_status:str
	username:str

class GetApplicationRequest(BaseModel):
	company: str
	job_title: str
	username: str

class UpdateApplicationRequest(BaseModel):
	company: str
	job_title:str
	date_applied:Optional[str] = None
	application_status:Optional[str] = None
	username:str

class ApplicationDatabaseResponse(BaseModel):
	company: str
	job_title:str
	date_applied:str
	application_status:str
	username:str
	id: int

class LoginRequest(BaseModel):
	email: str
	password:str