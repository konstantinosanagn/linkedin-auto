#!/usr/bin/env python3
"""
Example usage of the LinkedIn Automation System
===============================================

This script demonstrates how to use the LinkedIn automation system
for creating campaigns, managing contacts, and analyzing results.
"""

import os
import sys
from datetime import datetime

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import LinkedInAutomation
from models import Contact, Campaign, MessageVariant, ContactStatus
from db import db_manager
from llm import llm
from messaging import message_manager

def example_basic_workflow():
    """Example of a basic workflow"""
    print("=== LinkedIn Automation System - Basic Workflow Example ===\n")
    
    # Initialize the automation system
    automation = LinkedInAutomation()
    
    print("1. Initializing system...")
    if not automation.initialize_system(skip_api_validation=True):
        print("❌ System initialization failed. Please check your configuration.")
        return
    
    print("✅ System initialized successfully\n")
    
    # Create a campaign
    print("2. Creating a new campaign...")
    campaign_id = automation.create_campaign(
        name="Tech Professionals Outreach",
        description="Outreach to software engineers and tech leaders",
        variant=MessageVariant.NETWORKING.value,
        spreadsheet_url="https://docs.google.com/spreadsheets/d/example",
        connection_template="Hi {first_name}, I noticed your work at {company}. Would love to connect and exchange ideas about the tech industry."
    )
    
    print(f"✅ Campaign created with ID: {campaign_id}\n")
    
    # Show analytics (empty at first)
    print("3. Current analytics:")
    analytics = automation.get_analytics()
    print(f"   Total contacts: {analytics.get('total_contacts', 0)}")
    print(f"   Status breakdown: {analytics.get('status_breakdown', {})}")
    print()

def example_message_templates():
    """Example of working with message templates"""
    print("=== Message Templates Example ===\n")
    
    # Initialize message manager
    message_mgr = message_manager
    
    print("1. Available message templates:")
    templates = message_mgr.get_message_templates()
    for template in templates:
        print(f"   - {template.name} ({template.template_type}, {template.variant})")
    print()
    
    # Create a custom template
    print("2. Creating a custom template...")
    template_id = message_mgr.save_message_template(
        name="Custom Business Outreach",
        variant=MessageVariant.BUSINESS_OPPORTUNITY.value,
        template_type="connection",
        content="Hi {first_name}, I came across your profile and was impressed by your work at {company}. I'd love to connect and explore potential business opportunities."
    )
    
    print(f"✅ Custom template created with ID: {template_id}\n")

def example_contact_management():
    """Example of contact management"""
    print("=== Contact Management Example ===\n")
    
    # Create a sample contact
    print("1. Creating a sample contact...")
    contact = Contact(
        linkedin_url="https://linkedin.com/in/johndoe",
        name="John Doe",
        first_name="John",
        last_name="Doe",
        company="Tech Corp",
        job_title="Senior Software Engineer",
        status=ContactStatus.INVITATION_SENT.value,
        variant=MessageVariant.NETWORKING.value,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    contact_id = db_manager.insert_contact(contact)
    print(f"✅ Contact created with ID: {contact_id}\n")
    
    # Retrieve the contact
    print("2. Retrieving contact...")
    retrieved_contact = db_manager.get_contact_by_url("https://linkedin.com/in/johndoe")
    if retrieved_contact:
        print(f"   Name: {retrieved_contact.name}")
        print(f"   Company: {retrieved_contact.company}")
        print(f"   Status: {retrieved_contact.status}")
        print(f"   Variant: {retrieved_contact.variant}")
    print()
    
    # Update contact status
    print("3. Updating contact status...")
    if retrieved_contact:
        retrieved_contact.status = ContactStatus.INVITATION_ACCEPTED.value
        retrieved_contact.updated_at = datetime.now()
        db_manager.update_contact(retrieved_contact)
        print("✅ Contact status updated to 'Invitation accepted'")
    print()

def example_llm_integration():
    """Example of LLM integration for message generation"""
    print("=== LLM Integration Example ===\n")
    
    # Create a sample contact for LLM testing
    contact = Contact(
        name="Jane Smith",
        first_name="Jane",
        last_name="Smith",
        company="Innovation Labs",
        job_title="Product Manager",
        variant=MessageVariant.INDUSTRY_INSIGHTS.value
    )
    
    print("1. Generating personalized connection message...")
    try:
        connection_message = llm.generate_connection_message(contact)
        print(f"   Generated message: {connection_message}")
    except Exception as e:
        print(f"   ❌ Error generating connection message: {e}")
    print()
    
    print("2. Generating personalized follow-up message...")
    try:
        followup_message = llm.generate_followup_message(contact)
        print(f"   Generated follow-up: {followup_message}")
    except Exception as e:
        print(f"   ❌ Error generating follow-up message: {e}")
    print()

def example_analytics():
    """Example of analytics and reporting"""
    print("=== Analytics Example ===\n")
    
    # Get analytics
    analytics = db_manager.get_analytics()
    
    print("1. Campaign Analytics:")
    print(f"   Total contacts: {analytics.get('total_contacts', 0)}")
    
    print("\n2. Status Breakdown:")
    status_breakdown = analytics.get('status_breakdown', {})
    for status, count in status_breakdown.items():
        print(f"   {status}: {count}")
    
    print("\n3. Variant Performance:")
    variant_performance = analytics.get('variant_performance', [])
    for variant_data in variant_performance:
        print(f"   {variant_data['variant']}:")
        print(f"     Total: {variant_data['total']}")
        print(f"     Replied to connection: {variant_data['replied_connection']}")
        print(f"     Replied to follow-up: {variant_data['replied_followup']}")
    
    print("\n4. Top Companies:")
    top_companies = analytics.get('top_companies', [])
    for company_data in top_companies[:5]:  # Show top 5
        print(f"   {company_data['company']}: {company_data['count']} contacts")
    print()

def main():
    """Run all examples"""
    print("LinkedIn Automation System - Examples\n")
    print("This script demonstrates various features of the system.\n")
    
    try:
        # Run examples
        example_basic_workflow()
        example_message_templates()
        example_contact_management()
        example_llm_integration()
        example_analytics()
        
        print("=== All examples completed successfully! ===")
        print("\nTo use the system in production:")
        print("1. Set up your API keys in environment variables")
        print("2. Create your campaigns using the CLI or programmatically")
        print("3. Run campaigns and monitor results")
        print("4. Use analytics to optimize your outreach strategy")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("\nMake sure you have:")
        print("- Set up your API keys in environment variables")
        print("- Installed all required dependencies")
        print("- Proper permissions for database operations")

if __name__ == "__main__":
    main() 