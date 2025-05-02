from app.models.db import get_db_connection, execute_query

class Lease:
    @staticmethod
    def get_all_leases():
        """Get all leases from database"""
        connection = get_db_connection()
        if connection:
            query = """
            SELECT l.*, p.address, p.property_type, 
                   t.first_name as tenant_first_name, t.last_name as tenant_last_name
            FROM Leases l
            JOIN Properties p ON l.property_id = p.property_id
            JOIN Tenants t ON l.tenant_id = t.tenant_id
            """
            leases = execute_query(connection, query)
            connection.close()
            return leases
        return []
    
    @staticmethod
    def get_lease_by_id(lease_id):
        """Get a lease by ID"""
        connection = get_db_connection()
        if connection:
            query = """
            SELECT l.*, p.address, p.property_type, 
                   t.first_name as tenant_first_name, t.last_name as tenant_last_name
            FROM Leases l
            JOIN Properties p ON l.property_id = p.property_id
            JOIN Tenants t ON l.tenant_id = t.tenant_id
            WHERE l.lease_id = %s
            """
            leases = execute_query(connection, query, (lease_id,))
            connection.close()
            return leases[0] if leases else None
        return None
    
    @staticmethod
    def add_lease(lease_data):
        """Add a new lease"""
        connection = get_db_connection()
        if connection:
            # Check if property is available
            check_query = """
            SELECT listing_status FROM Properties 
            WHERE property_id = %s
            """
            result = execute_query(connection, check_query, (lease_data['property_id'],))
            
            if not result or result[0]['listing_status'] != 'available':
                connection.close()
                return None  # Property not available
            
            # Add the lease
            query = """
            INSERT INTO Leases (
                property_id, tenant_id, start_date, end_date,
                monthly_rent, security_deposit, lease_status, payment_due_day
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                lease_data['property_id'], lease_data['tenant_id'],
                lease_data['start_date'], lease_data['end_date'],
                lease_data['monthly_rent'], lease_data['security_deposit'],
                lease_data.get('lease_status', 'active'), 
                lease_data.get('payment_due_day', 1)
            )
            lease_id = execute_query(connection, query, params)
            
            if lease_id:
                # Update property status to leased
                update_query = """
                UPDATE Properties SET listing_status = 'leased'
                WHERE property_id = %s
                """
                execute_query(connection, update_query, (lease_data['property_id'],))
            
            connection.close()
            return lease_id
        return None
    
    @staticmethod
    def update_lease(lease_id, lease_data):
        """Update an existing lease"""
        connection = get_db_connection()
        if connection:
            query = """
            UPDATE Leases SET
                start_date = %s, end_date = %s, monthly_rent = %s,
                security_deposit = %s, lease_status = %s, payment_due_day = %s
            WHERE lease_id = %s
            """
            params = (
                lease_data['start_date'], lease_data['end_date'],
                lease_data['monthly_rent'], lease_data['security_deposit'],
                lease_data['lease_status'], lease_data.get('payment_due_day', 1),
                lease_id
            )
            result = execute_query(connection, query, params)
            
            # If lease is terminated, update property status
            if lease_data['lease_status'] != 'active':
                get_property_query = "SELECT property_id FROM Leases WHERE lease_id = %s"
                property_result = execute_query(connection, get_property_query, (lease_id,))
                
                if property_result:
                    update_query = """
                    UPDATE Properties SET listing_status = 'available'
                    WHERE property_id = %s
                    """
                    execute_query(connection, update_query, (property_result[0]['property_id'],))
            
            connection.close()
            return result is not None
        return False
    
    @staticmethod
    def terminate_lease(lease_id):
        """Terminate a lease"""
        connection = get_db_connection()
        if connection:
            # Get property_id first
            get_property_query = "SELECT property_id FROM Leases WHERE lease_id = %s"
            property_result = execute_query(connection, get_property_query, (lease_id,))
            
            if not property_result:
                connection.close()
                return False
                
            # Update lease status
            query = """
            UPDATE Leases SET lease_status = 'terminated'
            WHERE lease_id = %s
            """
            result = execute_query(connection, query, (lease_id,))
            
            if result:
                # Update property status to available
                update_query = """
                UPDATE Properties SET listing_status = 'available'
                WHERE property_id = %s
                """
                execute_query(connection, update_query, (property_result[0]['property_id'],))
            
            connection.close()
            return result is not None
        return False
    
    @staticmethod
    def get_lease_payments(lease_id):
        """Get all payments for a lease"""
        connection = get_db_connection()
        if connection:
            query = "SELECT * FROM Payments WHERE lease_id = %s ORDER BY payment_date DESC"
            payments = execute_query(connection, query, (lease_id,))
            connection.close()
            return payments
        return [] 