import sqlite3
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

from config import Config
from models import Contact, Campaign, MessageTemplate, ContactStatus, MessageVariant

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or Config.DB_PATH
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def init_db(self):
        """Initialize database with all required tables"""
        with self.get_connection() as conn:
            # Contacts table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    linkedin_url TEXT UNIQUE NOT NULL,
                    linkedin_id TEXT,
                    name TEXT NOT NULL,
                    first_name TEXT,
                    last_name TEXT,
                    company TEXT,
                    job_title TEXT,
                    status TEXT DEFAULT 'Invitation sent',
                    variant TEXT DEFAULT 'networking',
                    replied_connection BOOLEAN DEFAULT 0,
                    replied_followup BOOLEAN DEFAULT 0,
                    followup_attempts INTEGER DEFAULT 0,
                    connection_message TEXT,
                    followup_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_followup_sent TIMESTAMP
                )
            """)
            
            # Campaigns table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS campaigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    variant TEXT DEFAULT 'networking',
                    connection_template TEXT,
                    spreadsheet_url TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Message templates table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS message_templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    variant TEXT DEFAULT 'networking',
                    template_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Campaign contacts relationship table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS campaign_contacts (
                    campaign_id INTEGER,
                    contact_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (campaign_id, contact_id),
                    FOREIGN KEY (campaign_id) REFERENCES campaigns (id),
                    FOREIGN KEY (contact_id) REFERENCES contacts (id)
                )
            """)
            
            # Create indexes for better performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_contacts_status ON contacts(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_contacts_variant ON contacts(variant)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_contacts_company ON contacts(company)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_contacts_created_at ON contacts(created_at)")
            
            conn.commit()
            logger.info("Database initialized successfully")
    
    def insert_contact(self, contact: Contact) -> int:
        """Insert a new contact and return the ID"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO contacts (
                    linkedin_url, linkedin_id, name, first_name, last_name,
                    company, job_title, status, variant, connection_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                contact.linkedin_url, contact.linkedin_id, contact.name,
                contact.first_name, contact.last_name, contact.company,
                contact.job_title, contact.status, contact.variant,
                contact.connection_message
            ))
            conn.commit()
            result = cursor.lastrowid
            if result is None:
                raise ValueError("Failed to insert contact")
            return result
    
    def update_contact(self, contact: Contact) -> bool:
        """Update an existing contact"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                UPDATE contacts SET
                    status = ?, replied_connection = ?, replied_followup = ?,
                    followup_attempts = ?, followup_message = ?,
                    last_followup_sent = ?, updated_at = CURRENT_TIMESTAMP
                WHERE linkedin_url = ?
            """, (
                contact.status, contact.replied_connection, contact.replied_followup,
                contact.followup_attempts, contact.followup_message,
                contact.last_followup_sent, contact.linkedin_url
            ))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_contact_by_url(self, linkedin_url: str) -> Optional[Contact]:
        """Get contact by LinkedIn URL"""
        with self.get_connection() as conn:
            row = conn.execute("""
                SELECT * FROM contacts WHERE linkedin_url = ?
            """, (linkedin_url,)).fetchone()
            
            if row:
                return Contact(**dict(row))
            return None
    
    def get_contacts_for_followup(self) -> List[Contact]:
        """Get contacts that need follow-up messages"""
        with self.get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM contacts 
                WHERE status = ? 
                AND replied_connection = 0 
                AND followup_attempts < ?
                AND (last_followup_sent IS NULL OR 
                     datetime(last_followup_sent) <= datetime('now', '-{} hours'))
            """.format(Config.FOLLOWUP_DELAY_HOURS), 
            (ContactStatus.INVITATION_ACCEPTED.value, Config.MAX_FOLLOWUP_ATTEMPTS)).fetchall()
            
            return [Contact(**dict(row)) for row in rows]
    
    def get_contacts_by_status(self, status: str) -> List[Contact]:
        """Get contacts by status"""
        with self.get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM contacts WHERE status = ?
                ORDER BY created_at DESC
            """, (status,)).fetchall()
            
            return [Contact(**dict(row)) for row in rows]
    
    def get_contacts_by_variant(self, variant: str) -> List[Contact]:
        """Get contacts by message variant"""
        with self.get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM contacts WHERE variant = ?
                ORDER BY created_at DESC
            """, (variant,)).fetchall()
            
            return [Contact(**dict(row)) for row in rows]
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics data for the campaign"""
        with self.get_connection() as conn:
            # Total contacts
            total = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
            
            # Status breakdown
            status_counts = conn.execute("""
                SELECT status, COUNT(*) as count 
                FROM contacts 
                GROUP BY status
            """).fetchall()
            
            # Variant performance
            variant_performance = conn.execute("""
                SELECT variant, 
                       COUNT(*) as total,
                       SUM(CASE WHEN replied_connection = 1 THEN 1 ELSE 0 END) as replied_connection,
                       SUM(CASE WHEN replied_followup = 1 THEN 1 ELSE 0 END) as replied_followup
                FROM contacts 
                GROUP BY variant
            """).fetchall()
            
            # Company breakdown
            company_counts = conn.execute("""
                SELECT company, COUNT(*) as count 
                FROM contacts 
                WHERE company IS NOT NULL AND company != ''
                GROUP BY company 
                ORDER BY count DESC 
                LIMIT 10
            """).fetchall()
            
            return {
                "total_contacts": total,
                "status_breakdown": dict(status_counts),
                "variant_performance": [dict(row) for row in variant_performance],
                "top_companies": [dict(row) for row in company_counts]
            }
    
    def insert_campaign(self, campaign: Campaign) -> int:
        """Insert a new campaign and return the ID"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO campaigns (
                    name, description, variant, connection_template, spreadsheet_url
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                campaign.name, campaign.description, campaign.variant,
                campaign.connection_template, campaign.spreadsheet_url
            ))
            conn.commit()
            result = cursor.lastrowid
            if result is None:
                raise ValueError("Failed to insert campaign")
            return result
    
    def get_campaigns(self) -> List[Campaign]:
        """Get all campaigns"""
        with self.get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM campaigns ORDER BY created_at DESC
            """).fetchall()
            
            return [Campaign(**dict(row)) for row in rows]
    
    def insert_message_template(self, template: MessageTemplate) -> int:
        """Insert a new message template and return the ID"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO message_templates (
                    name, variant, template_type, content
                ) VALUES (?, ?, ?, ?)
            """, (
                template.name, template.variant, template.template_type,
                template.content
            ))
            conn.commit()
            result = cursor.lastrowid
            if result is None:
                raise ValueError("Failed to insert message template")
            return result
    
    def get_message_templates(self, template_type: Optional[str] = None, variant: Optional[str] = None) -> List[MessageTemplate]:
        """Get message templates with optional filtering"""
        with self.get_connection() as conn:
            query = "SELECT * FROM message_templates WHERE is_active = 1"
            params = []
            
            if template_type:
                query += " AND template_type = ?"
                params.append(template_type)
            
            if variant:
                query += " AND variant = ?"
                params.append(variant)
            
            query += " ORDER BY created_at DESC"
            
            rows = conn.execute(query, params).fetchall()
            return [MessageTemplate(**dict(row)) for row in rows]

# Global database manager instance
db_manager = DatabaseManager()

def get_connection():
    """Legacy function for backward compatibility"""
    return db_manager.get_connection()

def init_db():
    """Legacy function for backward compatibility"""
    return db_manager.init_db()
