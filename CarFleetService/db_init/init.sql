-- Create cars table
CREATE TABLE IF NOT EXISTS cars (
    car_id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    color VARCHAR(30),
    mileage INT DEFAULT 0,
    status ENUM('available', 'rented', 'maintenance') DEFAULT 'available',
    daily_rate DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert some test data
INSERT INTO cars (brand, model, year, license_plate, color, mileage, status, daily_rate) VALUES
('Toyota', 'Corolla', 2022, 'AB12345', 'White', 15000, 'available', 299.99),
('Honda', 'Civic', 2023, 'CD67890', 'Black', 8000, 'available', 349.99),
('Ford', 'Focus', 2021, 'EF23456', 'Blue', 25000, 'rented', 279.99),
('Tesla', 'Model 3', 2023, 'GH78901', 'Red', 5000, 'available', 599.99),
('BMW', '3 Series', 2022, 'IJ34567', 'Silver', 12000, 'maintenance', 499.99);