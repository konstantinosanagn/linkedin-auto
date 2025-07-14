#!/usr/bin/env python3
"""
Test Setup Script
=================

This script tests the basic setup and database initialization
without requiring API keys.
"""

import sys
import os
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import LinkedInAutomation
from models import Contact, Campaign, MessageVariant, ContactStatus
from db import db_manager

def test_database_initialization():
    """Test database initialization"""
    print("=== Testing Database Initialization ===")
    
    try:
        # Initialize the automation system
        automation = LinkedInAutomation()
        success = automation.initialize_system(skip_api_validation=True)
        
        if success:
            print("✅ Database initialized successfully")
            return True
        else:
            print("❌ Database initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during database initialization: {e}")
        return False

def test_campaign_creation():
    """Test campaign creation"""
    print("\n=== Testing Campaign Creation ===")
    
    try:
        # Create a test campaign
        campaign = Campaign(
            name="Test Campaign",
            description="Test campaign for validation",
            variant=MessageVariant.NETWORKING.value,
            connection_template="Hi {first_name}, test message",
            spreadsheet_url="https://example.com/test",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        campaign_id = db_manager.insert_campaign(campaign)
        print(f"✅ Campaign created with ID: {campaign_id}")
        
        # Retrieve campaigns
        campaigns = db_manager.get_campaigns()
        print(f"✅ Retrieved {len(campaigns)} campaigns")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during campaign creation: {e}")
        return False

def test_contact_creation():
    """Test contact creation"""
    print("\n=== Testing Contact Creation ===")
    
    try:
        # Create a test contact
        contact = Contact(
            linkedin_url="https://linkedin.com/in/testuser",
            name="Test User",
            first_name="Test",
            last_name="User",
            company="Test Company",
            job_title="Test Position",
            status=ContactStatus.INVITATION_SENT.value,
            variant=MessageVariant.NETWORKING.value,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        contact_id = db_manager.insert_contact(contact)
        print(f"✅ Contact created with ID: {contact_id}")
        
        # Retrieve the contact
        retrieved_contact = db_manager.get_contact_by_url("https://linkedin.com/in/testuser")
        if retrieved_contact:
            print(f"✅ Contact retrieved: {retrieved_contact.name} at {retrieved_contact.company}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during contact creation: {e}")
        return False

def test_analytics():
    """Test analytics functionality"""
    print("\n=== Testing Analytics ===")
    
    try:
        analytics = db_manager.get_analytics()
        
        print(f"✅ Analytics retrieved:")
        print(f"   Total contacts: {analytics.get('total_contacts', 0)}")
        print(f"   Status breakdown: {analytics.get('status_breakdown', {})}")
        print(f"   Variant performance: {len(analytics.get('variant_performance', []))} variants")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during analytics test: {e}")
        return False

def test_message_templates():
    """Test message template functionality"""
    print("\n=== Testing Message Templates ===")
    
    try:
        from messaging import message_manager
        
        # Get templates
        templates = message_manager.get_message_templates()
        print(f"✅ Retrieved {len(templates)} message templates")
        
        # Create a test template
        template_id = message_manager.save_message_template(
            name="Test Template",
            variant=MessageVariant.NETWORKING.value,
            template_type="connection",
            content="Hi {first_name}, this is a test template."
        )
        
        print(f"✅ Test template created with ID: {template_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during message template test: {e}")
        return False

def main():
    """Run all tests"""
    print("LinkedIn Automation System - Setup Test\n")
    
    tests = [
        test_database_initialization,
        test_campaign_creation,
        test_contact_creation,
        test_analytics,
        test_message_templates
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\nNext steps:")
        print("1. Set up your API keys in a .env file")
        print("2. Run: python main.py --init")
        print("3. Create campaigns and start automation")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 