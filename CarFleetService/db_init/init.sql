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
    location VARCHAR(50) NOT NULL,
    purchase_price INT NOT NULL,
    sub_type ENUM('subscription', 'mini-lease') DEFAULT 'subscription',
    sub_price_per_month INT NOT NULL
);

-- populate table
INSERT INTO cars (brand, model, year, license_plate, km_driven, fuel_type, status, location, purchase_price, sub_type, sub_price_per_month) 
VALUES
('Chevrolet', 'Malibu', 2021, 'BD63289', 14815, 'gasoline', 'maintenance', 'Copenhagen', 190000, 'subscription', 3500),
('Kia', 'EV6', 2022, 'CG23362', 21532, 'electric', 'available', 'Copenhagen', 330000, 'subscription', 5200),
('Volvo', 'XC40 Recharge', 2022, 'DJ77659', 19755, 'electric', 'available', 'Copenhagen', 680000, 'subscription', 8500),
('Land Rover', 'Defender', 2023, 'EM65965', 15899, 'diesel', 'rented', 'Copenhagen', 1400000, 'mini-lease', 14500),
('Porsche', 'Panamera', 2022, 'FP32859', 19404, 'gasoline', 'available', 'Copenhagen', 1609000, 'subscription', 15000),
('BMW', '320d', 2022, 'GS93193', 26185, 'diesel', 'available', 'Kolding', 617057, 'subscription', 7800),
('BMW', 'X1 xDrive25e', 2023, 'HV96519', 21808, 'hybrid', 'available', 'Aarhus', 289183, 'subscription', 4500),
('Kia', 'Niro EV', 2023, 'IY31755', 21556, 'electric', 'rented', 'Aarhus', 445246, 'subscription', 6200),
('Tesla', 'Model Y', 2023, 'JB48442', 20243, 'electric', 'available', 'Aarhus', 875167, 'mini-lease', 10500),
('Land Rover', 'Discovery', 2023, 'KE52576', 15260, 'gasoline', 'available', 'Aarhus', 1526336, 'subscription', 14800),
('Hyundai', 'Tucson', 2022, 'LH34620', 10153, 'diesel', 'available', 'Kolding', 711984, 'mini-lease', 9000),
('Porsche', 'Cayenne', 2023, 'MK21249', 10323, 'gasoline', 'available', 'Copenhagen', 1123540, 'subscription', 12500),
('Tesla', 'Model 3', 2022, 'NN46464', 16384, 'electric', 'available', 'Copenhagen', 822043, 'subscription', 10200),
('Porsche', 'Taycan', 2023, 'OQ51282', 27715, 'gasoline', 'available', 'Kolding', 1400523, 'subscription', 14000),
('Ford', 'Mustang Mach-E', 2022, 'PT71787', 15076, 'electric', 'available', 'Kolding', 939352, 'subscription', 11000);