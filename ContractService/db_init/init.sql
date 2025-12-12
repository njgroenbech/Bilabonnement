CREATE TABLE IF NOT EXISTS contracts (
    contract_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    car_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    sub_price_per_month INT NOT NULL,
    status ENUM('active', 'completed', 'cancelled') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Testdata
INSERT INTO contracts (customer_id, car_id, start_date, end_date, sub_price_per_month, status)
VALUES
(1, 2, '2023-11-01', '2023-12-01', 1999, 'active'),
(3, 4, '2023-10-10', '2023-10-20', 1499, 'active');