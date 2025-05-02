from app.models.db import get_db_connection, execute_query

class Owner:
    @staticmethod
    def get_all_owners():
        """Get all owners from database"""
        connection = get_db_connection()
        if connection:
            # Join with Properties to count properties for each owner
            query = """
            SELECT o.*, COUNT(p.property_id) as properties_count 
            FROM Owners o
            LEFT JOIN Properties p ON o.owner_id = p.owner_id
            GROUP BY o.owner_id
            """
            owners = execute_query(connection, query)
            connection.close()
            return owners
        return []
    
    @staticmethod
    def get_owner_by_id(owner_id):
        """Get an owner by ID"""
        connection = get_db_connection()
        if connection:
            # Also get property count
            query = """
            SELECT o.*, COUNT(p.property_id) as properties_count 
            FROM Owners o
            LEFT JOIN Properties p ON o.owner_id = p.owner_id
            WHERE o.owner_id = %s
            GROUP BY o.owner_id
            """
            owners = execute_query(connection, query, (owner_id,))
            connection.close()
            return owners[0] if owners else None
        return None
    
    @staticmethod
    def add_owner(owner_data):
        """Add a new owner"""
        connection = get_db_connection()
        if connection:
            query = """
            INSERT INTO Owners (
                first_name, last_name, email, phone, address, join_date
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                owner_data['first_name'], owner_data['last_name'],
                owner_data['email'], owner_data['phone'],
                owner_data['address'], owner_data['join_date']
            )
            owner_id = execute_query(connection, query, params)
            connection.close()
            return owner_id
        return None
    
    @staticmethod
    def update_owner(owner_id, owner_data):
        """Update an existing owner"""
        connection = get_db_connection()
        if connection:
            query = """
            UPDATE Owners SET
                first_name = %s, last_name = %s, email = %s,
                phone = %s, address = %s, join_date = %s
            WHERE owner_id = %s
            """
            params = (
                owner_data['first_name'], owner_data['last_name'],
                owner_data['email'], owner_data['phone'],
                owner_data['address'], owner_data['join_date'],
                owner_id
            )
            result = execute_query(connection, query, params)
            connection.close()
            return result is not None
        return False
    
    @staticmethod
    def delete_owner(owner_id):
        """Delete an owner"""
        connection = get_db_connection()
        if connection:
            # Check if owner has properties
            check_query = "SELECT COUNT(*) as count FROM Properties WHERE owner_id = %s"
            result = execute_query(connection, check_query, (owner_id,))
            if result and result[0]['count'] > 0:
                connection.close()
                return False  # Cannot delete owner with properties
            
            # Delete the owner
            query = "DELETE FROM Owners WHERE owner_id = %s"
            result = execute_query(connection, query, (owner_id,))
            connection.close()
            return result is not None
        return False
    
    @staticmethod
    def get_owner_properties(owner_id):
        """Get all properties belonging to an owner"""
        connection = get_db_connection()
        if connection:
            query = "SELECT * FROM Properties WHERE owner_id = %s"
            properties = execute_query(connection, query, (owner_id,))
            connection.close()
            return properties
        return [] 