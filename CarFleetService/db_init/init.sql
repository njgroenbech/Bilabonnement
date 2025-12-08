-- create cars table
CREATE TABLE IF NOT EXISTS cars (
    car_id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    km_driven INT DEFAULT 0,
    fuel_type ENUM('gasoline', 'diesel', 'electric', 'hybrid') NOT NULL,
    status ENUM('available', 'rented', 'maintenance') DEFAULT 'available',
    purchase_price INT NOT NULL,
    location VARCHAR(50) NOT NULL
);

-- populate table
INSERT INTO cars (brand, model, year, license_plate, km_driven, fuel_type, status, purchase_price, location) VALUES
('Chevrolet', 'Standard', 2021, 'BD63289', 14815, 'gasoline', 'maintenance', 190000, 'Copenhagen'),
('Kia', 'Standard', 2022, 'CG23362', 21532, 'electric', 'available', 330000, 'Copenhagen'),
('Volvo', 'Standard', 2022, 'DJ77659', 19755, 'electric', 'available', 680000, 'Copenhagen'),
('Land', 'Rover', 2023, 'EM65965', 15899, 'diesel', 'rented', 1400000, 'Copenhagen'),
('Porsche', 'Panamera', 2022, 'FP32859', 19404, 'gasoline', 'available', 1609000, 'Copenhagen'),
('BMW', 'Standard', 2022, 'GS93193', 26185, 'diesel', 'available', 617057, 'Kolding'),
('BMW', 'Standard', 2023, 'HV96519', 21808, 'hybrid', 'available', 289183, 'Aarhus'),
('Kia', 'Standard', 2023, 'IY31755', 21556, 'electric', 'rented', 445246, 'Aarhus'),
('Tesla', 'Standard', 2023, 'JB48442', 20243, 'electric', 'available', 875167, 'Aarhus'),
('Land', 'Rover', 2023, 'KE52576', 15260, 'gasoline', 'available', 1526336, 'Aarhus'),
('Hyundai', 'Standard', 2022, 'LH34620', 10153, 'diesel', 'available', 711984, 'Kolding'),
('Porsche', 'Panamera', 2023, 'MK21249', 10323, 'gasoline', 'available', 1123540, 'Copenhagen'),
('Tesla', 'Standard', 2022, 'NN46464', 16384, 'electric', 'available', 822043, 'Copenhagen'),
('Porsche', 'Panamera', 2023, 'OQ51282', 27715, 'gasoline', 'available', 1400523, 'Kolding'),
('Ford', 'Standard', 2022, 'PT71787', 15076, 'electric', 'available', 939352, 'Kolding');