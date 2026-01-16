from datetime import datetime,timezone
from enum import Enum
from typing import Optional
from .user import User
from beanie import Document,Link
from pydantic import Field

#Defining Enums
class Difficulty(str,Enum):
    easy="easy"
    medium="medium" 
    hard="hard"
    
class SessionStatus(str,Enum):
    active="active"
    completed="completed"

class Session(Document):
    problem:str
    difficulty:Difficulty
    
#References(Equivalent to ref:"User")
#Link handles MongoDB ObjectIDs and DB preferences automatically

    host:Link["User"]
    participant:Optional[Link["User"]]=None

    status:SessionStatus=SessionStatus.active

#Stream video call ID
    call_id:str=Field(default="",alias="callId")

#TimeStamps(Equivalent to {timestamps:true})
    created_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))
    updated_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))

    class Settings:
        name="sessions"
        validate_on_save=True