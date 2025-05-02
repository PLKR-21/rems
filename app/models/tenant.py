from app.models.db import get_db_connection, execute_query

class Tenant:
    @staticmethod
    def get_all_tenants():
        """Get all tenants from database"""
        connection = get_db_connection()
        if connection:
            query = "SELECT * FROM Tenants"
            tenants = execute_query(connection, query)
            connection.close()
            return tenants
        return []
    
    @staticmethod
    def get_tenant_by_id(tenant_id):
        """Get a tenant by ID"""
        connection = get_db_connection()
        if connection:
            query = "SELECT * FROM Tenants WHERE tenant_id = %s"
            tenants = execute_query(connection, query, (tenant_id,))
            connection.close()
            return tenants[0] if tenants else None
        return None
    
    @staticmethod
    def add_tenant(tenant_data):
        """Add a new tenant"""
        connection = get_db_connection()
        if connection:
            query = """
            INSERT INTO Tenants (
                first_name, last_name, email, phone, date_of_birth,
                identification_number, occupation, registration_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                tenant_data['first_name'], tenant_data['last_name'],
                tenant_data['email'], tenant_data['phone'],
                tenant_data.get('date_of_birth'), tenant_data.get('identification_number'),
                tenant_data.get('occupation'), tenant_data['registration_date']
            )
            tenant_id = execute_query(connection, query, params)
            connection.close()
            return tenant_id
        return None
    
    @staticmethod
    def update_tenant(tenant_id, tenant_data):
        """Update an existing tenant"""
        connection = get_db_connection()
        if connection:
            query = """
            UPDATE Tenants SET
                first_name = %s, last_name = %s, email = %s, phone = %s,
                date_of_birth = %s, identification_number = %s,
                occupation = %s, registration_date = %s
            WHERE tenant_id = %s
            """
            params = (
                tenant_data['first_name'], tenant_data['last_name'],
                tenant_data['email'], tenant_data['phone'],
                tenant_data.get('date_of_birth'), tenant_data.get('identification_number'),
                tenant_data.get('occupation'), tenant_data['registration_date'],
                tenant_id
            )
            result = execute_query(connection, query, params)
            connection.close()
            return result is not None
        return False
    
    @staticmethod
    def delete_tenant(tenant_id):
        """Delete a tenant"""
        connection = get_db_connection()
        if connection:
            # Check if tenant has active leases
            check_query = """
            SELECT COUNT(*) as count FROM Leases 
            WHERE tenant_id = %s AND lease_status = 'active'
            """
            result = execute_query(connection, check_query, (tenant_id,))
            if result and result[0]['count'] > 0:
                connection.close()
                return False  # Cannot delete tenant with active leases
            
            # Delete the tenant
            query = "DELETE FROM Tenants WHERE tenant_id = %s"
            result = execute_query(connection, query, (tenant_id,))
            connection.close()
            return result is not None
        return False
    
    @staticmethod
    def get_tenant_leases(tenant_id):
        """Get all leases for a tenant"""
        connection = get_db_connection()
        if connection:
            query = """
            SELECT l.*, p.address, p.property_type
            FROM Leases l
            JOIN Properties p ON l.property_id = p.property_id
            WHERE l.tenant_id = %s
            """
            leases = execute_query(connection, query, (tenant_id,))
            connection.close()
            return leases
        return [] 