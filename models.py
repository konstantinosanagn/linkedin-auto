from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ContactStatus(Enum):
    INVITATION_SENT = "Invitation sent"
    INVITATION_ACCEPTED = "Invitation accepted"
    REPLIED_CONNECTION = "Replied (Connection request)"
    REPLIED_FOLLOWUP = "Replied (Follow-up)"
    CONNECTION_DECLINED = "Connection declined"
    NO_RESPONSE = "No response"

class MessageVariant(Enum):
    NETWORKING = "networking"
    BUSINESS_OPPORTUNITY = "business_opportunity"
    INDUSTRY_INSIGHTS = "industry_insights"
    COLLABORATION = "collaboration"
    MENTORSHIP = "mentorship"

@dataclass
class Contact:
    id: Optional[int] = None
    linkedin_url: str = ""
    linkedin_id: str = ""
    name: str = ""
    first_name: str = ""
    last_name: str = ""
    company: str = ""
    job_title: str = ""
    status: str = ContactStatus.INVITATION_SENT.value
    variant: str = MessageVariant.NETWORKING.value
    replied_connection: bool = False
    replied_followup: bool = False
    followup_attempts: int = 0
    connection_message: str = ""
    followup_message: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_followup_sent: Optional[datetime] = None

@dataclass
class Campaign:
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    variant: str = MessageVariant.NETWORKING.value
    connection_template: str = ""
    spreadsheet_url: str = ""
    status: str = "active"  # active, paused, completed
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class MessageTemplate:
    id: Optional[int] = None
    name: str = ""
    variant: str = MessageVariant.NETWORKING.value
    template_type: str = ""  # connection, followup
    content: str = ""
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class PhantomResult:
    linkedin_url: str
    first_name: str
    last_name: str
    company: str
    job_title: str
    status: str
    variant: str
    replied: bool = False
    followup_sent: bool = False
    error_message: Optional[str] = None
