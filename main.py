#!/usr/bin/env python3
"""
LinkedIn Automation System
==========================

A comprehensive system for automating LinkedIn outreach campaigns using PhantomBuster API
and DeepSeek LLM for personalized messaging.

Features:
- Automated connection requests with personalized messages
- Follow-up message generation using AI
- Campaign management and analytics
- Message variant testing and performance tracking
- Database management for contact tracking
"""

import sys
import logging
import argparse
from datetime import datetime
from typing import Optional, List

from config import Config
from db import db_manager
from phantom import phantom_api, sync_phantom_results_to_db
from llm import llm
from messaging import message_manager
from models import Contact, Campaign, ContactStatus, MessageVariant

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class LinkedInAutomation:
    def __init__(self):
        self.db = db_manager
        self.phantom = phantom_api
        self.llm = llm
        self.messaging = message_manager
    
    def initialize_system(self, skip_api_validation=False):
        """Initialize the system and validate configuration"""
        logger.info("Initializing LinkedIn Automation System...")
        
        # Validate configuration (optional for testing)
        if not skip_api_validation:
            if not Config.validate_config():
                logger.warning("Configuration validation failed. Some features may not work without proper API keys.")
                logger.info("Continuing with database initialization for testing purposes...")
        
        # Initialize database
        try:
            self.db.init_db()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            return False
        
        # Initialize default message templates
        try:
            self.messaging.initialize_default_templates()
            logger.info("Default message templates initialized")
        except Exception as e:
            logger.error(f"Failed to initialize message templates: {e}")
            return False
        
        logger.info("System initialization completed successfully")
        return True
    
    def create_campaign(self, name: str, description: str, variant: str, 
                       spreadsheet_url: str, connection_template: Optional[str] = None) -> int:
        """Create a new campaign"""
        campaign = Campaign(
            name=name,
            description=description,
            variant=variant,
            connection_template=connection_template or "",
            spreadsheet_url=spreadsheet_url,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        campaign_id = self.db.insert_campaign(campaign)
        logger.info(f"Created campaign '{name}' with ID {campaign_id}")
        return campaign_id
    
    def launch_campaign(self, campaign_id: int) -> bool:
        """Launch a campaign using PhantomBuster"""
        try:
            campaign = self.db.get_campaigns()[0]  # Simplified - should get by ID
            if not campaign:
                logger.error(f"Campaign with ID {campaign_id} not found")
                return False
            
            logger.info(f"Launching campaign: {campaign.name}")
            
            # Launch PhantomBuster campaign
            result = self.phantom.launch_campaign(
                spreadsheet_url=campaign.spreadsheet_url,
                variant=campaign.variant,
                connection_template=campaign.connection_template
            )
            
            logger.info(f"Campaign launched successfully: {result}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to launch campaign: {e}")
            return False
    
    def sync_results(self) -> int:
        """Sync results from PhantomBuster to database"""
        try:
            logger.info("Fetching results from PhantomBuster...")
            results = self.phantom.fetch_results()
            
            if not results:
                logger.info("No new results to sync")
                return 0
            
            synced_count = sync_phantom_results_to_db(results)
            logger.info(f"Synced {synced_count} results to database")
            return synced_count
            
        except Exception as e:
            logger.error(f"Failed to sync results: {e}")
            return 0
    
    def process_followups(self) -> int:
        """Process follow-up messages for contacts who accepted connections"""
        try:
            contacts_for_followup = self.db.get_contacts_for_followup()
            
            if not contacts_for_followup:
                logger.info("No contacts need follow-up messages")
                return 0
            
            processed_count = 0
            
            for contact in contacts_for_followup:
                try:
                    logger.info(f"Processing follow-up for {contact.name} ({contact.company})")
                    
                    # Generate personalized follow-up message
                    followup_message = self.llm.generate_followup_message(contact)
                    
                    # Update contact with follow-up message
                    contact.followup_message = followup_message
                    contact.followup_attempts += 1
                    contact.last_followup_sent = datetime.now()
                    contact.updated_at = datetime.now()
                    
                    # Save to database
                    if self.db.update_contact(contact):
                        processed_count += 1
                        logger.info(f"Generated follow-up for {contact.name}: {followup_message[:50]}...")
                    
                    # TODO: Send message via PhantomBuster or other method
                    # For now, just log the message
                    
                except Exception as e:
                    logger.error(f"Failed to process follow-up for {contact.name}: {e}")
                    continue
            
            logger.info(f"Processed {processed_count} follow-up messages")
            return processed_count
            
        except Exception as e:
            logger.error(f"Failed to process follow-ups: {e}")
            return 0
    
    def get_analytics(self) -> dict:
        """Get campaign analytics"""
        try:
            analytics = self.db.get_analytics()
            logger.info("Retrieved analytics data")
            return analytics
        except Exception as e:
            logger.error(f"Failed to get analytics: {e}")
            return {}
    
    def run_campaign_workflow(self, campaign_id: int) -> bool:
        """Run the complete campaign workflow"""
        logger.info(f"Starting campaign workflow for campaign ID: {campaign_id}")
        
        # Launch campaign
        if not self.launch_campaign(campaign_id):
            logger.error("Failed to launch campaign")
            return False
        
        # Wait for some time (in real implementation, you'd poll for completion)
        logger.info("Campaign launched. Waiting for completion...")
        
        # Sync results
        synced_count = self.sync_results()
        if synced_count == 0:
            logger.warning("No results synced")
        
        # Process follow-ups
        followup_count = self.process_followups()
        logger.info(f"Processed {followup_count} follow-up messages")
        
        # Get analytics
        analytics = self.get_analytics()
        logger.info(f"Campaign analytics: {analytics}")
        
        logger.info("Campaign workflow completed")
        return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="LinkedIn Automation System")
    parser.add_argument("--init", action="store_true", help="Initialize the system")
    parser.add_argument("--campaign", type=int, help="Campaign ID to run")
    parser.add_argument("--sync", action="store_true", help="Sync results from PhantomBuster")
    parser.add_argument("--followup", action="store_true", help="Process follow-up messages")
    parser.add_argument("--analytics", action="store_true", help="Show analytics")
    parser.add_argument("--create-campaign", nargs=5, metavar=("NAME", "DESCRIPTION", "VARIANT", "SPREADSHEET_URL", "TEMPLATE"), 
                       help="Create a new campaign")
    
    args = parser.parse_args()
    
    # Initialize automation system
    automation = LinkedInAutomation()
    
    if args.init:
        if automation.initialize_system(skip_api_validation=True):
            logger.info("System initialized successfully")
        else:
            logger.error("System initialization failed")
            sys.exit(1)
    
    if args.create_campaign:
        name, description, variant, spreadsheet_url, template = args.create_campaign
        campaign_id = automation.create_campaign(name, description, variant, spreadsheet_url, template)
        logger.info(f"Created campaign with ID: {campaign_id}")
    
    if args.campaign:
        automation.run_campaign_workflow(args.campaign)
    
    if args.sync:
        synced_count = automation.sync_results()
        logger.info(f"Synced {synced_count} results")
    
    if args.followup:
        followup_count = automation.process_followups()
        logger.info(f"Processed {followup_count} follow-up messages")
    
    if args.analytics:
        analytics = automation.get_analytics()
        print("\n=== Campaign Analytics ===")
        print(f"Total Contacts: {analytics.get('total_contacts', 0)}")
        print("\nStatus Breakdown:")
        for status, count in analytics.get('status_breakdown', {}).items():
            print(f"  {status}: {count}")
        print("\nVariant Performance:")
        for variant_data in analytics.get('variant_performance', []):
            print(f"  {variant_data['variant']}: {variant_data['total']} total, "
                  f"{variant_data['replied_connection']} replied to connection, "
                  f"{variant_data['replied_followup']} replied to follow-up")
    
    # If no specific action provided, run the legacy workflow
    if not any([args.init, args.campaign, args.sync, args.followup, args.analytics, args.create_campaign]):
        if len(sys.argv) >= 3:
            # Legacy command line interface
            variant = int(sys.argv[1])
            sheet_url = sys.argv[2]
            run_legacy_workflow(variant, sheet_url)
        else:
            parser.print_help()

def run_legacy_workflow(variant: int, sheet_url: str):
    """Legacy workflow for backward compatibility"""
    logger.info(f"Running legacy workflow with variant {variant}")
    
    automation = LinkedInAutomation()
    
    # Initialize system
    if not automation.initialize_system(skip_api_validation=True):
        logger.error("System initialization failed")
        return
    
    # Create a temporary campaign
    campaign_id = automation.create_campaign(
        name=f"Legacy Campaign - Variant {variant}",
        description=f"Legacy campaign with variant {variant}",
        variant=str(variant),
        spreadsheet_url=sheet_url
    )
    
    # Run the workflow
    automation.run_campaign_workflow(campaign_id)

if __name__ == "__main__":
    main()
