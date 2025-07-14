import logging
from typing import Dict, List, Optional
from datetime import datetime

from config import Config
from models import Contact, MessageTemplate, MessageVariant
from db import db_manager

logger = logging.getLogger(__name__)

class MessageManager:
    def __init__(self):
        self.default_connection_template = Config.DEFAULT_CONNECTION_TEMPLATE
    
    def build_connection_message(self, contact: Contact, template: Optional[str] = None) -> str:
        """Build a connection message using template and contact data"""
        template = template or self.default_connection_template
        
        # Replace placeholders with contact data
        message = template.format(
            first_name=contact.first_name,
            last_name=contact.last_name,
            name=contact.name,
            company=contact.company,
            job_title=contact.job_title,
            linkedin_url=contact.linkedin_url
        )
        
        logger.debug(f"Built connection message for {contact.name}: {message[:50]}...")
        return message
    
    def build_followup_message(self, contact: Contact, template: Optional[str] = None) -> str:
        """Build a follow-up message using template and contact data"""
        if template:
            # Use provided template
            message = template.format(
                first_name=contact.first_name,
                last_name=contact.last_name,
                name=contact.name,
                company=contact.company,
                job_title=contact.job_title,
                linkedin_url=contact.linkedin_url
            )
        else:
            # Use LLM to generate personalized message
            from llm import llm
            message = llm.generate_followup_message(contact)
        
        logger.debug(f"Built follow-up message for {contact.name}: {message[:50]}...")
        return message
    
    def save_message_template(self, name: str, variant: str, template_type: str, content: str) -> int:
        """Save a new message template to the database"""
        template = MessageTemplate(
            name=name,
            variant=variant,
            template_type=template_type,
            content=content,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        template_id = db_manager.insert_message_template(template)
        logger.info(f"Saved message template '{name}' with ID {template_id}")
        return template_id
    
    def get_message_templates(self, template_type: Optional[str] = None, variant: Optional[str] = None) -> List[MessageTemplate]:
        """Get message templates with optional filtering"""
        return db_manager.get_message_templates(template_type, variant)
    
    def get_default_templates(self) -> Dict[str, Dict[str, str]]:
        """Get default message templates for different variants"""
        return {
            MessageVariant.NETWORKING.value: {
                "connection": "Hi {first_name}, I noticed your work at {company}. Would love to connect and exchange ideas about the industry.",
                "followup": "Hi {first_name}, thanks for connecting! I'd love to learn more about your work at {company}. Would you be open to a quick chat about {job_title} trends?"
            },
            MessageVariant.BUSINESS_OPPORTUNITY.value: {
                "connection": "Hi {first_name}, I came across your profile and was impressed by your work at {company}. I'd love to connect and explore potential collaboration opportunities.",
                "followup": "Hi {first_name}, thanks for connecting! I'd love to discuss potential business opportunities that could benefit both of us. Are you open to a brief call?"
            },
            MessageVariant.INDUSTRY_INSIGHTS.value: {
                "connection": "Hi {first_name}, I've been following the great work you're doing at {company}. Would love to connect and share insights about {job_title} developments.",
                "followup": "Hi {first_name}, thanks for connecting! I'd love to share some industry insights I've gathered and hear your perspective. Would you be interested in a quick discussion?"
            },
            MessageVariant.COLLABORATION.value: {
                "connection": "Hi {first_name}, I'm impressed by your {job_title} work at {company}. I'd love to connect and explore potential collaboration opportunities.",
                "followup": "Hi {first_name}, thanks for connecting! I'd love to discuss potential collaboration opportunities that could be mutually beneficial. Are you open to exploring this further?"
            },
            MessageVariant.MENTORSHIP.value: {
                "connection": "Hi {first_name}, I admire your career journey and work at {company}. I'd love to connect and potentially learn from your experience in {job_title}.",
                "followup": "Hi {first_name}, thanks for connecting! I'd love to learn from your experience in {job_title}. Would you be open to sharing some insights or advice?"
            }
        }
    
    def initialize_default_templates(self):
        """Initialize default message templates in the database"""
        default_templates = self.get_default_templates()
        
        for variant, templates in default_templates.items():
            for template_type, content in templates.items():
                # Check if template already exists
                existing_templates = db_manager.get_message_templates(template_type, variant)
                if not existing_templates:
                    template_name = f"Default {template_type.title()} - {variant.title()}"
                    self.save_message_template(template_name, variant, template_type, content)
                    logger.info(f"Initialized default template: {template_name}")

# Global message manager instance
message_manager = MessageManager()

def build_connection_message(entry):
    """Legacy function for backward compatibility"""
    contact = Contact(
        first_name=entry.get("firstName", ""),
        name=entry.get("firstName", ""),
        company=entry.get("company", "")
    )
    return message_manager.build_connection_message(contact)
