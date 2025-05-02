from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models.property import Property
from app.models.owner import Owner
from datetime import datetime

properties = Blueprint('properties', __name__, url_prefix='/properties')

@properties.route('/')
def list_properties():
    """List all properties"""
    props = Property.get_all_properties()
    return render_template('properties/list.html', properties=props)

@properties.route('/<int:property_id>')
def view_property(property_id):
    """View a single property"""
    prop = Property.get_property_by_id(property_id)
    if not prop:
        flash('Property not found', 'danger')
        return redirect(url_for('properties.list_properties'))
    return render_template('properties/view.html', property=prop)

@properties.route('/add', methods=['GET', 'POST'])
def add_property():
    """Add a new property"""
    if request.method == 'POST':
        property_data = {
            'property_type': request.form['property_type'],
            'address': request.form['address'],
            'city': request.form['city'],
            'state': request.form['state'],
            'postal_code': request.form['postal_code'],
            'country': request.form.get('country', 'USA'),
            'size_sqft': request.form['size_sqft'],
            'num_bedrooms': request.form.get('num_bedrooms') or None,
            'num_bathrooms': request.form.get('num_bathrooms') or None,
            'year_built': request.form.get('year_built') or None,
            'description': request.form.get('description'),
            'listing_status': request.form.get('listing_status', 'available'),
            'listing_price': request.form.get('listing_price') or None,
            'owner_id': request.form['owner_id']
        }
        
        property_id = Property.add_property(property_data)
        if property_id:
            flash('Property added successfully', 'success')
            return redirect(url_for('properties.view_property', property_id=property_id))
        else:
            flash('Error adding property', 'danger')
    
    # Get all owners for the dropdown
    owners = Owner.get_all_owners()
    return render_template('properties/add.html', owners=owners)

@properties.route('/<int:property_id>/edit', methods=['GET', 'POST'])
def edit_property(property_id):
    """Edit an existing property"""
    prop = Property.get_property_by_id(property_id)
    if not prop:
        flash('Property not found', 'danger')
        return redirect(url_for('properties.list_properties'))
    
    if request.method == 'POST':
        property_data = {
            'property_type': request.form['property_type'],
            'address': request.form['address'],
            'city': request.form['city'],
            'state': request.form['state'],
            'postal_code': request.form['postal_code'],
            'country': request.form.get('country', 'USA'),
            'size_sqft': request.form['size_sqft'],
            'num_bedrooms': request.form.get('num_bedrooms') or None,
            'num_bathrooms': request.form.get('num_bathrooms') or None,
            'year_built': request.form.get('year_built') or None,
            'description': request.form.get('description'),
            'listing_status': request.form.get('listing_status', 'available'),
            'listing_price': request.form.get('listing_price') or None,
            'owner_id': request.form['owner_id']
        }
        
        success = Property.update_property(property_id, property_data)
        if success:
            flash('Property updated successfully', 'success')
            return redirect(url_for('properties.view_property', property_id=property_id))
        else:
            flash('Error updating property', 'danger')
    
    # Get all owners for the dropdown
    owners = Owner.get_all_owners()
    return render_template('properties/edit.html', property=prop, owners=owners)

@properties.route('/<int:property_id>/delete', methods=['POST'])
def delete_property(property_id):
    """Delete a property"""
    success = Property.delete_property(property_id)
    if success:
        flash('Property deleted successfully', 'success')
    else:
        flash('Error deleting property', 'danger')
    return redirect(url_for('properties.list_properties')) 