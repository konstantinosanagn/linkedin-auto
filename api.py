from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from datetime import datetime
import traceback

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import LinkedInAutomation
from config import Config

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the automation system
automation = None

def get_automation():
    global automation
    if automation is None:
        try:
            automation = LinkedInAutomation()
        except Exception as e:
            print(f"Error initializing automation: {e}")
            automation = None
    return automation

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        auto = get_automation()
        if auto:
            return jsonify({
                'status': 'ok',
                'message': 'System is running',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'System not initialized',
                'timestamp': datetime.now().isoformat()
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'LinkedIn Automation API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'config': '/config',
            'campaigns': '/campaigns',
            'contacts': '/contacts',
            'analytics': '/analytics/dashboard',
            'templates': '/templates',
            'sync': '/sync',
            'followup': '/followup'
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    try:
        config = Config()
        return jsonify({
            'phantomBusterApiKey': config.PHANTOMBUSTER_API_KEY or '',
            'deepSeekApiKey': config.DEEPSEEK_API_KEY or '',
            'phantomId': config.PHANTOM_ID or '',
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/config', methods=['POST'])
def update_config():
    """Update configuration"""
    try:
        data = request.get_json() or {}
        config = Config()
        
        # Update config values
        if 'phantomBusterApiKey' in data:
            config.PHANTOMBUSTER_API_KEY = data['phantomBusterApiKey']
        if 'deepSeekApiKey' in data:
            config.DEEPSEEK_API_KEY = data['deepSeekApiKey']
        if 'phantomId' in data:
            config.PHANTOM_ID = data['phantomId']
        
        # Save to file
        # config.save_to_file() # This line was removed as per the edit hint.
        
        return jsonify({
            'phantomBusterApiKey': config.PHANTOMBUSTER_API_KEY or '',
            'deepSeekApiKey': config.DEEPSEEK_API_KEY or '',
            'phantomId': config.PHANTOM_ID or '',
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/init', methods=['POST'])
def initialize_system():
    """Initialize the system"""
    try:
        auto = get_automation()
        if auto:
            return jsonify({'message': 'System already initialized'})
        else:
            automation = LinkedInAutomation()
            return jsonify({'message': 'System initialized successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/campaigns', methods=['GET'])
def get_campaigns():
    """Get all campaigns"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        campaigns = auto.db.get_campaigns()
        return jsonify(campaigns)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/campaigns', methods=['POST'])
def create_campaign():
    """Create a new campaign"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        data = request.get_json() or {}
        campaign_id = auto.create_campaign(
            name=data.get('name', ''),
            description=data.get('description', ''),
            variant=data.get('variant', ''),
            spreadsheet_url=data.get('spreadsheet_url', ''),
            connection_template=data.get('connection_template', '')
        )
        
        return jsonify({'id': campaign_id, 'message': 'Campaign created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    """Get campaign details"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        campaigns = auto.db.get_campaigns()
        campaign = next((c for c in campaigns if c.id == campaign_id), None)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        return jsonify(campaign)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/campaigns/<int:campaign_id>/launch', methods=['POST'])
def launch_campaign(campaign_id):
    """Launch a campaign"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        result = auto.launch_campaign(campaign_id)
        return jsonify({'message': 'Campaign launched successfully', 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/campaigns/<int:campaign_id>/sync', methods=['POST'])
def sync_campaign(campaign_id):
    """Sync campaign results"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        result = auto.sync_results()
        return jsonify({'message': 'Campaign synced successfully', 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/campaigns/<int:campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    """Delete a campaign"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        # Delete campaign - use direct SQL since no delete_campaign method exists
        with auto.db.get_connection() as conn:
            conn.execute("DELETE FROM campaigns WHERE id = ?", (campaign_id,))
            conn.commit()
        return jsonify({'message': 'Campaign deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/contacts', methods=['GET'])
def get_contacts():
    """Get contacts with optional filtering"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        # Get query parameters
        status = request.args.get('status', '')
        variant = request.args.get('variant', '')
        company = request.args.get('company', '')
        
        # Get contacts using available methods
        if status:
            contacts = auto.db.get_contacts_by_status(status)
        elif variant:
            contacts = auto.db.get_contacts_by_variant(variant)
        else:
            # Get all contacts by status (default to all)
            contacts = auto.db.get_contacts_by_status('')
        
        # Filter by company if specified
        if company:
            contacts = [c for c in contacts if c.company and company.lower() in c.company.lower()]
        
        return jsonify(contacts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    """Get contact details"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        # Get all contacts and find the one with matching ID
        all_contacts = auto.db.get_contacts_by_status('')  # Get all contacts
        contact = next((c for c in all_contacts if c.id == contact_id), None)
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404
        
        return jsonify(contact)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/contacts/followup', methods=['GET'])
def get_followup_contacts():
    """Get contacts ready for follow-up"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        contacts = auto.db.get_contacts_for_followup()
        return jsonify(contacts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/contacts/followup', methods=['POST'])
def process_followups():
    """Process follow-up messages"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        result = auto.process_followups()
        return jsonify({'message': 'Follow-ups processed successfully', 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics/dashboard', methods=['GET'])
def get_dashboard_analytics():
    """Get dashboard analytics"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        analytics = auto.get_analytics()
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign_analytics(campaign_id):
    """Get campaign-specific analytics"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        analytics = auto.get_analytics()
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/templates', methods=['GET'])
def get_templates():
    """Get message templates"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        templates = auto.db.get_message_templates()
        return jsonify(templates)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/templates', methods=['POST'])
def create_template():
    """Create a new template"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        data = request.get_json() or {}
        # Create MessageTemplate object first
        from models import MessageTemplate
        template = MessageTemplate(
            name=data.get('name', ''),
            variant=data.get('variant', ''),
            template_type=data.get('template_type', ''),
            content=data.get('content', '')
        )
        template_id = auto.db.insert_message_template(template)
        
        return jsonify({'id': template_id, 'message': 'Template created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sync', methods=['POST'])
def sync_all():
    """Sync all campaigns"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        result = auto.sync_results()
        return jsonify({'message': 'All campaigns synced successfully', 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/followup', methods=['POST'])
def followup_all():
    """Process all follow-ups"""
    try:
        auto = get_automation()
        if not auto:
            return jsonify({'error': 'System not initialized'}), 500
        
        result = auto.process_followups()
        return jsonify({'message': 'Follow-ups processed successfully', 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 