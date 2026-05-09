from pydantic import BaseModel

class job_application(BaseModel):
	company: str
	job_title:str
	date_applied:str
	application_status:str
	application_id:str #primary key in sb db
	uid:str
	