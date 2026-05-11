from typing import Optional
from pydantic import BaseModel
from datetime import datetime   

Class UserProfile(BaseModel):
    user_id: str
    full_name: str
    user_image: Optional[str] = None
    email: Optional[str] = None
    mobile_no: Optional[str] = None
    category: str
    location: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    bio:Optional[str] = None
    interest:Optional[str] = None
    