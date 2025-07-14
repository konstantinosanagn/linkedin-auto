import requests
import logging
from typing import Optional, Dict, Any
from datetime import datetime

from config import Config
from models import Contact, MessageVariant

logger = logging.getLogger(__name__)

class DeepSeekLLM:
    def __init__(self):
        self.api_url = Config.DEEPSEEK_API_URL
        self.api_key = Config.DEEPSEEK_API_KEY
        self.model = Config.DEEPSEEK_MODEL
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_followup_message(self, contact: Contact, variant: Optional[str] = None) -> str:
        """Generate a personalized follow-up message for a contact"""
        variant = variant or contact.variant
        
        # Create context-aware prompt based on variant
        variant_contexts = {
            MessageVariant.NETWORKING.value: "networking and professional relationship building",
            MessageVariant.BUSINESS_OPPORTUNITY.value: "potential business collaboration or partnership",
            MessageVariant.INDUSTRY_INSIGHTS.value: "sharing industry insights and knowledge",
            MessageVariant.COLLABORATION.value: "collaboration opportunities",
            MessageVariant.MENTORSHIP.value: "mentorship or guidance"
        }
        
        context = variant_contexts.get(variant, "professional networking")
        
        prompt = f"""
        Write a personalized, professional LinkedIn follow-up message to {contact.first_name} {contact.last_name}, 
        a {contact.job_title} at {contact.company}. 
        
        Context: This is for {context}. They accepted your connection request but haven't replied yet.
        
        Requirements:
        - Keep it under 150 words
        - Be professional but friendly
        - Reference their role and company naturally
        - Include a specific question or call to action
        - Don't be pushy or salesy
        - Make it feel personal and genuine
        
        Format the message as plain text without any markdown or formatting.
        """
        
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are a professional LinkedIn outreach assistant. Write concise, personalized follow-up messages that are professional, friendly, and include a specific call to action."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "stream": False,
                "max_tokens": 300,
                "temperature": 0.7
            }
            
            logger.info(f"Generating follow-up message for {contact.name} ({contact.company})")
            resp = requests.post(self.api_url, headers=self._get_headers(), json=payload)
            resp.raise_for_status()
            
            data = resp.json()
            message = data["choices"][0]["message"]["content"].strip()
            
            logger.info(f"Generated follow-up message for {contact.name}")
            return message
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to generate follow-up message: {e}")
            raise
        except KeyError as e:
            logger.error(f"Unexpected response format from DeepSeek API: {e}")
            raise
    
    def generate_connection_message(self, contact: Contact, variant: Optional[str] = None) -> str:
        """Generate a personalized connection message for a contact"""
        variant = variant or contact.variant
        
        prompt = f"""
        Write a personalized LinkedIn connection request message to {contact.first_name} {contact.last_name}, 
        a {contact.job_title} at {contact.company}.
        
        Context: This is for {variant} outreach.
        
        Requirements:
        - Keep it under 100 words
        - Be professional and respectful
        - Reference their role and company
        - Explain why you want to connect
        - Don't be overly salesy
        - Make it feel genuine and personal
        
        Format the message as plain text without any markdown or formatting.
        """
        
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are a professional LinkedIn outreach assistant. Write concise, personalized connection request messages that are professional and explain the reason for connecting."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "stream": False,
                "max_tokens": 200,
                "temperature": 0.7
            }
            
            logger.info(f"Generating connection message for {contact.name} ({contact.company})")
            resp = requests.post(self.api_url, headers=self._get_headers(), json=payload)
            resp.raise_for_status()
            
            data = resp.json()
            message = data["choices"][0]["message"]["content"].strip()
            
            logger.info(f"Generated connection message for {contact.name}")
            return message
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to generate connection message: {e}")
            raise
        except KeyError as e:
            logger.error(f"Unexpected response format from DeepSeek API: {e}")
            raise
    
    def analyze_contact_response(self, contact: Contact, response_text: str) -> Dict[str, Any]:
        """Analyze a contact's response to determine sentiment and next steps"""
        prompt = f"""
        Analyze this LinkedIn message response from {contact.first_name} {contact.last_name} ({contact.job_title} at {contact.company}):
        
        Response: "{response_text}"
        
        Please analyze:
        1. Sentiment (positive, neutral, negative)
        2. Interest level (high, medium, low)
        3. Response type (acceptance, question, decline, request for info)
        4. Recommended next action (follow up, schedule call, send info, no action needed)
        5. Key topics mentioned
        
        Provide your analysis in a structured format.
        """
        
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are a professional communication analyst. Analyze LinkedIn messages to determine sentiment, interest level, and recommend next actions."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "stream": False,
                "max_tokens": 400,
                "temperature": 0.3
            }
            
            resp = requests.post(self.api_url, headers=self._get_headers(), json=payload)
            resp.raise_for_status()
            
            data = resp.json()
            analysis = data["choices"][0]["message"]["content"].strip()
            
            # Parse the analysis (this is a simplified version)
            return {
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to analyze contact response: {e}")
            raise

# Global LLM instance
llm = DeepSeekLLM()

def generate_followup(name: str, company: str, job_title: str) -> str:
    """Legacy function for backward compatibility"""
    # Create a temporary contact object for the legacy function
    contact = Contact(
        name=name,
        first_name=name.split()[0] if name else "",
        company=company,
        job_title=job_title
    )
    
    return llm.generate_followup_message(contact)
