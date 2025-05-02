from app.models.db import get_db_connection, execute_query
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Payment:
    @staticmethod
    def add_payment(payment_data):
        """Add a new payment to the database"""
        connection = get_db_connection()
        if not connection:
            logger.error("Failed to establish database connection")
            return None

        try:
            query = """
            INSERT INTO Payments (
                lease_id, payment_date, amount, payment_method, 
                payment_status, transaction_reference
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                payment_data['lease_id'],
                payment_data.get('payment_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                payment_data['amount'],
                payment_data['payment_method'],
                payment_data.get('payment_status', 'completed'),
                payment_data.get('transaction_reference', '')
            )
            
            logger.debug(f"Attempting to add payment with data: {payment_data}")
            payment_id = execute_query(connection, query, params)
            
            if payment_id:
                logger.info(f"Successfully added payment with ID: {payment_id}")
                return payment_id
            else:
                logger.error("Failed to add payment - no ID returned")
                return None
                
        except Exception as e:
            logger.error(f"Error adding payment: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    def get_payment_by_id(payment_id):
        """Get a payment by ID"""
        connection = get_db_connection()
        if not connection:
            logger.error("Failed to establish database connection")
            return None

        try:
            query = "SELECT * FROM Payments WHERE payment_id = %s"
            payments = execute_query(connection, query, (payment_id,))
            return payments[0] if payments else None
        except Exception as e:
            logger.error(f"Error getting payment by ID: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
        
    @staticmethod
    def get_all_payments():
        """Get all payments with lease and property information"""
        connection = get_db_connection()
        if not connection:
            logger.error("Failed to establish database connection")
            return []

        try:
            query = """
            SELECT p.*, l.lease_id, l.monthly_rent, 
                   pr.address, pr.property_id,
                   t.first_name as tenant_first_name, t.last_name as tenant_last_name, t.tenant_id
            FROM Payments p
            JOIN Leases l ON p.lease_id = l.lease_id
            JOIN Properties pr ON l.property_id = pr.property_id
            JOIN Tenants t ON l.tenant_id = t.tenant_id
            ORDER BY p.payment_date DESC
            """
            payments = execute_query(connection, query)
            return payments
        except Exception as e:
            logger.error(f"Error getting all payments: {str(e)}")
            raise
        finally:
            if connection:
                connection.close() 