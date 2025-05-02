from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models.tenant import Tenant
from datetime import datetime

tenants = Blueprint('tenants', __name__, url_prefix='/tenants')

@tenants.route('/')
def list_tenants():
    """List all tenants"""
    all_tenants = Tenant.get_all_tenants()
    return render_template('tenants/list.html', tenants=all_tenants)

@tenants.route('/<int:tenant_id>')
def view_tenant(tenant_id):
    """View a single tenant and their leases"""
    tenant = Tenant.get_tenant_by_id(tenant_id)
    if not tenant:
        flash('Tenant not found', 'danger')
        return redirect(url_for('tenants.list_tenants'))
    
    leases = Tenant.get_tenant_leases(tenant_id)
    return render_template('tenants/view.html', tenant=tenant, leases=leases)

@tenants.route('/add', methods=['GET', 'POST'])
def add_tenant():
    """Add a new tenant"""
    if request.method == 'POST':
        tenant_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'date_of_birth': request.form.get('date_of_birth') or None,
            'identification_number': request.form.get('identification_number') or None,
            'occupation': request.form.get('occupation') or None,
            'registration_date': request.form['registration_date']
        }
        
        tenant_id = Tenant.add_tenant(tenant_data)
        if tenant_id:
            flash('Tenant added successfully', 'success')
            return redirect(url_for('tenants.view_tenant', tenant_id=tenant_id))
        else:
            flash('Error adding tenant', 'danger')
    
    # Set default registration date to today
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template('tenants/add.html', today=today)

@tenants.route('/<int:tenant_id>/edit', methods=['GET', 'POST'])
def edit_tenant(tenant_id):
    """Edit an existing tenant"""
    tenant = Tenant.get_tenant_by_id(tenant_id)
    if not tenant:
        flash('Tenant not found', 'danger')
        return redirect(url_for('tenants.list_tenants'))
    
    if request.method == 'POST':
        tenant_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'date_of_birth': request.form.get('date_of_birth') or None,
            'identification_number': request.form.get('identification_number') or None,
            'occupation': request.form.get('occupation') or None,
            'registration_date': request.form['registration_date']
        }
        
        success = Tenant.update_tenant(tenant_id, tenant_data)
        if success:
            flash('Tenant updated successfully', 'success')
            return redirect(url_for('tenants.view_tenant', tenant_id=tenant_id))
        else:
            flash('Error updating tenant', 'danger')
    
    return render_template('tenants/edit.html', tenant=tenant)

@tenants.route('/<int:tenant_id>/delete', methods=['POST'])
def delete_tenant(tenant_id):
    """Delete a tenant"""
    success = Tenant.delete_tenant(tenant_id)
    if success:
        flash('Tenant deleted successfully', 'success')
    else:
        flash('Cannot delete tenant with active leases', 'danger')
    return redirect(url_for('tenants.list_tenants')) 