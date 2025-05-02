from flask import Blueprint, render_template, redirect, url_for
from app.models.property import Property
from app.models.tenant import Tenant
from app.models.owner import Owner
from app.models.lease import Lease
from app.models.payment import Payment

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Homepage with dashboard"""
    properties = Property.get_all_properties()
    tenants = Tenant.get_all_tenants()
    owners = Owner.get_all_owners()
    leases = Lease.get_all_leases()
    payments = Payment.get_all_payments()
    
    # Calculate some stats
    available_properties = sum(1 for p in properties if p['listing_status'] == 'available')
    leased_properties = sum(1 for p in properties if p['listing_status'] == 'leased')
    active_leases = sum(1 for l in leases if l['lease_status'] == 'active')
    
    return render_template('index.html', 
                          property_count=len(properties),
                          tenant_count=len(tenants),
                          owner_count=len(owners),
                          lease_count=len(leases),
                          payment_count=len(payments),
                          available_properties=available_properties,
                          leased_properties=leased_properties,
                          active_leases=active_leases) 