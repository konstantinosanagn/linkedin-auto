import requests
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from config import Config
from models import PhantomResult, Contact, ContactStatus
from db import db_manager

logger = logging.getLogger(__name__)

class PhantomBusterAPI:
    def __init__(self):
        self.api_base = Config.PHANTOMBUSTER_API_BASE
        self.api_key = Config.PHANTOMBUSTER_API_KEY
        self.phantom_id = Config.PHANTOM_ID
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {"X-Phantombuster-Key-1": self.api_key}
    
    def launch_campaign(self, spreadsheet_url: str, variant: str, connection_template: Optional[str] = None) -> Dict[str, Any]:
        """Launch a PhantomBuster campaign"""
        url = f"{self.api_base}/agents/launch"
        headers = self._get_headers()
        
        payload = {
            "id": self.phantom_id,
            "argument": {
                "spreadsheetUrl": spreadsheet_url,
                "variant": variant,
                "connectionTemplate": connection_template or Config.DEFAULT_CONNECTION_TEMPLATE
            }
        }
        
        try:
            logger.info(f"Launching PhantomBuster campaign with variant: {variant}")
            resp = requests.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            result = resp.json()
            logger.info(f"Campaign launched successfully: {result}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to launch campaign: {e}")
            raise
    
    def fetch_results(self) -> List[PhantomResult]:
        """Fetch results from PhantomBuster"""
        url = f"{self.api_base}/agents/fetch"
        params = {"id": self.phantom_id}
        headers = self._get_headers()
        
        try:
            logger.info("Fetching results from PhantomBuster")
            resp = requests.get(url, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            
            results = []
            for entry in data.get("data", []):
                try:
                    result = PhantomResult(
                        linkedin_url=entry.get("linkedinUrl", ""),
                        first_name=entry.get("firstName", ""),
                        last_name=entry.get("lastName", ""),
                        company=entry.get("company", ""),
                        job_title=entry.get("jobTitle", ""),
                        status=entry.get("status", ContactStatus.INVITATION_SENT.value),
                        variant=entry.get("variant", "networking"),
                        replied=entry.get("replied", False),
                        followup_sent=entry.get("followUpSent", False),
                        error_message=entry.get("errorMessage")
                    )
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error parsing result entry: {e}, entry: {entry}")
                    continue
            
            logger.info(f"Fetched {len(results)} results from PhantomBuster")
            return results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch results: {e}")
            raise
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get the current status of the PhantomBuster agent"""
        url = f"{self.api_base}/agents/fetch"
        params = {"id": self.phantom_id}
        headers = self._get_headers()
        
        try:
            resp = requests.get(url, params=params, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get agent status: {e}")
            raise

# Global PhantomBuster API instance
phantom_api = PhantomBusterAPI()

def launch_phantom(spreadsheet_url: str, variant: str, connection_template: Optional[str] = None) -> Dict[str, Any]:
    """Launch a PhantomBuster campaign (legacy function for backward compatibility)"""
    return phantom_api.launch_campaign(spreadsheet_url, variant, connection_template)

def fetch_results() -> List[PhantomResult]:
    """Fetch results from PhantomBuster (legacy function for backward compatibility)"""
    return phantom_api.fetch_results()

def sync_phantom_results_to_db(results: List[PhantomResult]) -> int:
    """Sync PhantomBuster results to the database"""
    synced_count = 0
    
    for result in results:
        try:
            # Check if contact already exists
            existing_contact = db_manager.get_contact_by_url(result.linkedin_url)
            
            if existing_contact:
                # Update existing contact
                existing_contact.status = result.status
                existing_contact.replied_connection = result.replied
                existing_contact.replied_followup = result.followup_sent
                existing_contact.updated_at = datetime.now()
                
                if db_manager.update_contact(existing_contact):
                    synced_count += 1
                    logger.debug(f"Updated contact: {result.linkedin_url}")
            else:
                # Create new contact
                contact = Contact(
                    linkedin_url=result.linkedin_url,
                    name=f"{result.first_name} {result.last_name}".strip(),
                    first_name=result.first_name,
                    last_name=result.last_name,
                    company=result.company,
                    job_title=result.job_title,
                    status=result.status,
                    variant=result.variant,
                    replied_connection=result.replied,
                    replied_followup=result.followup_sent,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                db_manager.insert_contact(contact)
                synced_count += 1
                logger.debug(f"Created new contact: {result.linkedin_url}")
                
        except Exception as e:
            logger.error(f"Error syncing result for {result.linkedin_url}: {e}")
            continue
    
    logger.info(f"Synced {synced_count} results to database")
    return synced_count
