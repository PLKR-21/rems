from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models.owner import Owner
from datetime import datetime

owners = Blueprint('owners', __name__, url_prefix='/owners')

@owners.route('/')
def list_owners():
    """List all owners"""
    all_owners = Owner.get_all_owners()
    return render_template('owners/list.html', owners=all_owners)

@owners.route('/<int:owner_id>')
def view_owner(owner_id):
    """View a single owner and their properties"""
    owner = Owner.get_owner_by_id(owner_id)
    if not owner:
        flash('Owner not found', 'danger')
        return redirect(url_for('owners.list_owners'))
    
    properties = Owner.get_owner_properties(owner_id)
    return render_template('owners/view.html', owner=owner, properties=properties)

@owners.route('/add', methods=['GET', 'POST'])
def add_owner():
    """Add a new owner"""
    if request.method == 'POST':
        owner_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'address': request.form['address'],
            'join_date': request.form['join_date']
        }
        
        owner_id = Owner.add_owner(owner_data)
        if owner_id:
            flash('Owner added successfully', 'success')
            return redirect(url_for('owners.view_owner', owner_id=owner_id))
        else:
            flash('Error adding owner', 'danger')
    
    # Set default join date to today
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template('owners/add.html', today=today)

@owners.route('/<int:owner_id>/edit', methods=['GET', 'POST'])
def edit_owner(owner_id):
    """Edit an existing owner"""
    owner = Owner.get_owner_by_id(owner_id)
    if not owner:
        flash('Owner not found', 'danger')
        return redirect(url_for('owners.list_owners'))
    
    if request.method == 'POST':
        owner_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'address': request.form['address'],
            'join_date': request.form['join_date']
        }
        
        success = Owner.update_owner(owner_id, owner_data)
        if success:
            flash('Owner updated successfully', 'success')
            return redirect(url_for('owners.view_owner', owner_id=owner_id))
        else:
            flash('Error updating owner', 'danger')
    
    return render_template('owners/edit.html', owner=owner)

@owners.route('/<int:owner_id>/delete', methods=['POST'])
def delete_owner(owner_id):
    """Delete an owner"""
    success = Owner.delete_owner(owner_id)
    if success:
        flash('Owner deleted successfully', 'success')
    else:
        flash('Cannot delete owner with properties', 'danger')
    return redirect(url_for('owners.list_owners')) 