from pydantic import BaseModel
from typing import Optional

class JobApplication(BaseModel):
	company: str
	job_title:str
	date_applied:str
	application_status:str
	username:str