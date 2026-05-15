from typing import Optional
from pydantic import BaseModel
from datetime import datetime   

class Action(BaseModel):
    action_id: str
    action_category: str
    action_type: str
    user_id: str
    hours_invested: int
    description: str
    media: Optional[str] = None
    created_at: datetime
    updated_at: datetime