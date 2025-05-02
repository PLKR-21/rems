from app.models.db import get_db_connection, execute_query

class Property:
    @staticmethod
    def get_all_properties():
        """Get all properties from database"""
        connection = get_db_connection()
        if connection:
            query = """
            SELECT p.*, o.first_name, o.last_name 
            FROM Properties p
            JOIN Owners o ON p.owner_id = o.owner_id
            """
            properties = execute_query(connection, query)
            connection.close()
            return properties
        return []
    
    @staticmethod
    def get_property_by_id(property_id):
        """Get a property by ID"""
        connection = get_db_connection()
        if connection:
            query = """
            SELECT p.*, o.first_name, o.last_name 
            FROM Properties p
            JOIN Owners o ON p.owner_id = o.owner_id
            WHERE p.property_id = %s
            """
            properties = execute_query(connection, query, (property_id,))
            connection.close()
            return properties[0] if properties else None
        return None
    
    @staticmethod
    def add_property(property_data):
        """Add a new property"""
        connection = get_db_connection()
        if connection:
            query = """
            INSERT INTO Properties (
                property_type, address, city, state, postal_code, country,
                size_sqft, num_bedrooms, num_bathrooms, year_built,
                description, listing_status, listing_price, owner_id
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            params = (
                property_data['property_type'], property_data['address'],
                property_data['city'], property_data['state'],
                property_data['postal_code'], property_data.get('country', 'USA'),
                property_data['size_sqft'], property_data.get('num_bedrooms'),
                property_data.get('num_bathrooms'), property_data.get('year_built'),
                property_data.get('description'), property_data.get('listing_status', 'available'),
                property_data.get('listing_price'), property_data['owner_id']
            )
            property_id = execute_query(connection, query, params)
            connection.close()
            return property_id
        return None
    
    @staticmethod
    def update_property(property_id, property_data):
        """Update an existing property"""
        connection = get_db_connection()
        if connection:
            query = """
            UPDATE Properties SET
                property_type = %s, address = %s, city = %s, state = %s,
                postal_code = %s, country = %s, size_sqft = %s, num_bedrooms = %s,
                num_bathrooms = %s, year_built = %s, description = %s,
                listing_status = %s, listing_price = %s, owner_id = %s
            WHERE property_id = %s
            """
            params = (
                property_data['property_type'], property_data['address'],
                property_data['city'], property_data['state'],
                property_data['postal_code'], property_data.get('country', 'USA'),
                property_data['size_sqft'], property_data.get('num_bedrooms'),
                property_data.get('num_bathrooms'), property_data.get('year_built'),
                property_data.get('description'), property_data.get('listing_status', 'available'),
                property_data.get('listing_price'), property_data['owner_id'],
                property_id
            )
            result = execute_query(connection, query, params)
            connection.close()
            return result is not None
        return False
    
    @staticmethod
    def delete_property(property_id):
        """Delete a property"""
        connection = get_db_connection()
        if connection:
            query = "DELETE FROM Properties WHERE property_id = %s"
            result = execute_query(connection, query, (property_id,))
            connection.close()
            return result is not None
        return False 