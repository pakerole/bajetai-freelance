from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class SubmissionBase(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    project_type: str
    description: str


class SubmissionOut(SubmissionBase):
    id: int
    created_at: datetime
    filename: Optional[str] = None

    model_config = {"from_attributes": True}
