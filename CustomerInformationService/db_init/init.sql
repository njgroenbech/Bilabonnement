-- create customer information table
-- Todo: change cpr_number, registration_number and account_number to VARBINARY and possible encryption? using cryptography library
CREATE TABLE IF NOT EXISTS customer_info (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    address VARCHAR(255) NOT NULL,
    postal_code CHAR(4) NOT NULL,
    city VARCHAR(20) NOT NULL,
    email VARCHAR(60) UNIQUE NOT NULL,
    cpr_number VARCHAR(11) UNIQUE NOT NULL,
    registration_number VARCHAR(20) UNIQUE NOT NULL,
    account_number VARCHAR(30) UNIQUE NOT NULL,
    comments TEXT
);

-- insert data
INSERT INTO customer_info (name, last_name, address, postal_code, city, email, cpr_number, registration_number, account_number, comments) VALUES
('Anders', 'Nielsen', 'Vestergade 45, 2. tv', '1000', 'København', 'anders.nielsen@email.dk', '150678-2341', 1234, 1234567, 'Preferred customer'),
('Mette', 'Jensen', 'Nørregade 12, 1. th', '8000', 'Aarhus', 'mette.jensen@email.dk', '230891-5678', 2345, 2345678, 'VIP client'),
('Lars', 'Hansen', 'Østergade 78, 3. mf', '5000', 'Odense', 'lars.hansen@email.dk', '101265-8912', 3456, 3456789, 'Requires invoice by email'),
('Anne', 'Pedersen', 'Søndergade 23, 4. tv', '9000', 'Aalborg', 'anne.pedersen@email.dk', '050580-3456', 4567, 4567890, 'Contact before 3 PM'),
('Peter', 'Andersen', 'Hovedgaden 56, 1. th', '6700', 'Esbjerg', 'peter.andersen@email.dk', '180772-7890', 5678, 5678901, NULL),
('Sofie', 'Christensen', 'Kongensgade 89, 2. tv', '8900', 'Randers', 'sofie.christensen@email.dk', '270394-1234', 6789, 6789012, 'Long-standing customer'),
('Michael', 'Larsen', 'Strandvejen 34, 3. th', '6000', 'Kolding', 'michael.larsen@email.dk', '111058-5678', 7890, 7890123, NULL),
('Emma', 'Sørensen', 'Kirkevej 67, 1. mf', '8700', 'Horsens', 'emma.soerensen@email.dk', '190886-9012', 8901, 8901234, 'New customer'),
('Jens', 'Rasmussen', 'Skolegade 91, 4. tv', '7100', 'Vejle', 'jens.rasmussen@email.dk', '080470-3456', 9012, 9012345, 'Corporate account'),
('Marie', 'Jørgensen', 'Parkvej 15, 2. th', '4000', 'Roskilde', 'marie.joergensen@email.dk', '140595-7890', 9123, 9123456, 'Sensitive to pricing');