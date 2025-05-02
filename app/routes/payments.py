from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models.payment import Payment
from app.models.lease import Lease
from datetime import datetime

payments = Blueprint('payments', __name__, url_prefix='/payments')

@payments.route('/')
def list_payments():
    """List all payments"""
    all_payments = Payment.get_all_payments()
    return render_template('payments/list.html', payments=all_payments)

@payments.route('/add/<int:lease_id>', methods=['GET', 'POST'])
def add_payment(lease_id):
    """Add a new payment for a lease"""
    # Get the lease details
    lease = Lease.get_lease_by_id(lease_id)
    if not lease:
        flash('Lease not found', 'danger')
        return redirect(url_for('leases.list_leases'))
    
    # Check if the lease is active
    if lease['lease_status'] != 'active':
        flash('Cannot add payment to an inactive lease', 'warning')
        return redirect(url_for('leases.view_lease', lease_id=lease_id))
    
    if request.method == 'POST':
        try:
            # Process form submission
            payment_data = {
                'lease_id': lease_id,
                'amount': float(request.form['amount']),
                'payment_method': request.form['payment_method'],
                'payment_status': request.form['payment_status'],
                'transaction_reference': request.form.get('transaction_reference', ''),
                'payment_category': request.form.get('payment_category', 'rent'),
                'payment_period': request.form.get('payment_period', ''),
                'late_fee_amount': float(request.form.get('late_fee_amount', 0)),
                'payment_verified_by': request.form.get('payment_verified_by', ''),
                'payment_verification_date': request.form.get('payment_verification_date', ''),
                'receipt_number': request.form.get('receipt_number', ''),
                'bank_transaction_id': request.form.get('bank_transaction_id', ''),
                'payment_currency': request.form.get('payment_currency', 'INR'),
                'notes': request.form.get('notes', '')
            }
            
            # Handle payment date (form returns date only, need to add time)
            payment_date = request.form['payment_date']
            payment_data['payment_date'] = f"{payment_date} {datetime.now().strftime('%H:%M:%S')}"
            
            # Add the payment to the database
            payment_id = Payment.add_payment(payment_data)
            
            if payment_id:
                flash('Payment recorded successfully', 'success')
                return redirect(url_for('leases.view_lease', lease_id=lease_id))
            else:
                flash('Error recording payment', 'danger')
        except Exception as e:
            flash(f'Error processing payment: {str(e)}', 'danger')
    
    # For GET request, show the payment form
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template('payments/add.html', lease=lease, today=today) 