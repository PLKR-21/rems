from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models.lease import Lease
from app.models.property import Property
from app.models.tenant import Tenant
from datetime import datetime

leases = Blueprint('leases', __name__, url_prefix='/leases')

@leases.route('/')
def list_leases():
    """List all leases"""
    all_leases = Lease.get_all_leases()
    return render_template('leases/list.html', leases=all_leases)

@leases.route('/<int:lease_id>')
def view_lease(lease_id):
    """View a single lease"""
    lease = Lease.get_lease_by_id(lease_id)
    if not lease:
        flash('Lease not found', 'danger')
        return redirect(url_for('leases.list_leases'))
    
    payments = Lease.get_lease_payments(lease_id)
    return render_template('leases/view.html', lease=lease, payments=payments)

@leases.route('/<int:lease_id>/print')
def print_lease(lease_id):
    """Generate a printable lease document"""
    lease = Lease.get_lease_by_id(lease_id)
    if not lease:
        flash('Lease not found', 'danger')
        return redirect(url_for('leases.list_leases'))
    
    return render_template('leases/print.html', lease=lease)

@leases.route('/add', methods=['GET', 'POST'])
def add_lease():
    """Add a new lease"""
    if request.method == 'POST':
        lease_data = {
            'property_id': int(request.form['property_id']),
            'tenant_id': int(request.form['tenant_id']),
            'start_date': request.form['start_date'],
            'end_date': request.form['end_date'],
            'monthly_rent': float(request.form['monthly_rent']),
            'security_deposit': float(request.form['security_deposit']),
            'lease_status': request.form.get('lease_status', 'active'),
            'payment_due_day': int(request.form.get('payment_due_day', 1))
        }
        
        lease_id = Lease.add_lease(lease_data)
        if lease_id:
            flash('Lease added successfully', 'success')
            return redirect(url_for('leases.view_lease', lease_id=lease_id))
        else:
            flash('Error adding lease. Property may not be available.', 'danger')
    
    # Get available properties and tenants for dropdowns
    properties = Property.get_all_properties()
    available_properties = [p for p in properties if p['listing_status'] == 'available']
    tenants = Tenant.get_all_tenants()
    
    # Set default dates
    today = datetime.today().strftime('%Y-%m-%d')
    next_year = datetime.today().replace(year=datetime.today().year + 1).strftime('%Y-%m-%d')
    
    return render_template('leases/add.html', 
                           properties=available_properties, 
                           tenants=tenants, 
                           today=today, 
                           next_year=next_year)

@leases.route('/<int:lease_id>/edit', methods=['GET', 'POST'])
def edit_lease(lease_id):
    """Edit an existing lease"""
    lease = Lease.get_lease_by_id(lease_id)
    if not lease:
        flash('Lease not found', 'danger')
        return redirect(url_for('leases.list_leases'))
    
    if request.method == 'POST':
        lease_data = {
            'start_date': request.form['start_date'],
            'end_date': request.form['end_date'],
            'monthly_rent': float(request.form['monthly_rent']),
            'security_deposit': float(request.form['security_deposit']),
            'lease_status': request.form['lease_status'],
            'payment_due_day': int(request.form.get('payment_due_day', 1))
        }
        
        success = Lease.update_lease(lease_id, lease_data)
        if success:
            flash('Lease updated successfully', 'success')
            return redirect(url_for('leases.view_lease', lease_id=lease_id))
        else:
            flash('Error updating lease', 'danger')
    
    return render_template('leases/edit.html', lease=lease)

@leases.route('/<int:lease_id>/terminate', methods=['POST'])
def terminate_lease(lease_id):
    """Terminate a lease"""
    success = Lease.terminate_lease(lease_id)
    if success:
        flash('Lease terminated successfully', 'success')
    else:
        flash('Error terminating lease', 'danger')
    return redirect(url_for('leases.view_lease', lease_id=lease_id)) 