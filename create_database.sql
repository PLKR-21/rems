-- Create the database
CREATE DATABASE real_estate_management;
USE real_estate_management;

-- Enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Create Owners table
CREATE TABLE Owners (
    owner_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    join_date DATE NOT NULL
);

-- Create Properties table
CREATE TABLE Properties (
    property_id INT AUTO_INCREMENT PRIMARY KEY,
    property_type ENUM('house', 'apartment', 'commercial', 'land') NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(50) NOT NULL DEFAULT 'USA',
    size_sqft DECIMAL(10,2) NOT NULL,
    num_bedrooms INT,
    num_bathrooms DECIMAL(3,1),
    year_built YEAR,
    description TEXT,
    listing_status ENUM('available', 'leased', 'sold') NOT NULL DEFAULT 'available',
    listing_price DECIMAL(12,2),
    owner_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES Owners(owner_id) ON DELETE RESTRICT
);

-- Create Tenants table
CREATE TABLE Tenants (
    tenant_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    date_of_birth DATE,
    identification_number VARCHAR(50) UNIQUE,
    occupation VARCHAR(100),
    registration_date DATE NOT NULL
);

-- Create Leases table
CREATE TABLE Leases (
    lease_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    tenant_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    monthly_rent DECIMAL(10,2) NOT NULL,
    security_deposit DECIMAL(10,2) NOT NULL,
    lease_status ENUM('active', 'expired', 'terminated') NOT NULL DEFAULT 'active',
    payment_due_day TINYINT NOT NULL DEFAULT 1,
    FOREIGN KEY (property_id) REFERENCES Properties(property_id) ON DELETE RESTRICT,
    FOREIGN KEY (tenant_id) REFERENCES Tenants(tenant_id) ON DELETE RESTRICT,
    CHECK (end_date > start_date),
    CHECK (payment_due_day BETWEEN 1 AND 31)
);

-- Create Payments table
CREATE TABLE Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    lease_id INT NOT NULL,
    payment_date DATETIME NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('cash', 'check', 'credit_card', 'bank_transfer', 'online') NOT NULL,
    payment_status ENUM('pending', 'completed', 'failed') NOT NULL DEFAULT 'pending',
    transaction_reference VARCHAR(100),
    payment_category ENUM('rent', 'security_deposit', 'late_fee', 'maintenance', 'other') NOT NULL DEFAULT 'rent',
    payment_period VARCHAR(20),
    late_fee_amount DECIMAL(10,2) DEFAULT 0,
    payment_verified_by VARCHAR(100),
    payment_verification_date DATETIME,
    receipt_number VARCHAR(50),
    bank_transaction_id VARCHAR(100),
    payment_currency VARCHAR(3) DEFAULT 'INR',
    notes TEXT,
    FOREIGN KEY (lease_id) REFERENCES Leases(lease_id) ON DELETE RESTRICT
); 