CREATE TABLE IF NOT EXISTS damage_reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    contract_id INT NOT NULL,
    car_id INT NOT NULL,
    overall_status VARCHAR(50) NOT NULL,
    damage_level VARCHAR(50),
    ai_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);