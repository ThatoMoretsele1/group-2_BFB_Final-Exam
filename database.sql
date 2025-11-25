


CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    USER_NAME TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    Last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    password TEXT NOT NULL,
    Comfirm_password TEXT NOT NULL,
    date_created TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 
CREATE TABLE IF NOT EXISTS Driver_reg (
    driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    Last_name TEXT NOT NULL,
    number_plate TEXT NOT NULL UNIQUE,
    Vehicle_color TEXT NOT NULL,
    phone TEXT,
    password TEXT NOT NULL,
    Comfirm_password TEXT NOT NULL,
    date_created TEXT NOT NULL DEFAULT (datetime('now'))
);




CREATE TABLE IF NOT EXISTS user_login (
    login_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    last_login TEXT DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    pickup_location TEXT NOT NULL,
    dropoff_location TEXT NOT NULL,
    pickup_time TEXT,
    booking_date TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);




CREATE TABLE IF NOT EXISTS dropoff_location (
    dropoff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_id INTEGER NOT NULL,
    location_name TEXT NOT NULL,
    dropoff_time TEXT NOT NULL,
    FOREIGN KEY (driver_id) REFERENCES Driver_reg(driver_id) ON DELETE CASCADE
);






CREATE TABLE IF NOT EXISTS routes_locations (
    route_name TEXT NOT NULL,
    location_name TEXT NOT NULL
);



BEGIN TRANSACTION;

-- USERS
INSERT INTO routes_locations (route_name, location_name) VALUES
('Mamelodi - CBD', 'Mamelodi East'),
('Mamelodi - CBD', 'Mamelodi West'),
('Mamelodi - CBD', 'Silverton'),
('Mamelodi - CBD', 'Koedoespoort'),
('Mamelodi - CBD', 'Pretoria Station'),
('Mamelodi - CBD', 'Bosman Taxi Rank');


INSERT INTO routes_locations (route_name, location_name) VALUES
('Soshanguve - CBD', 'Soshanguve Block L'),
('Soshanguve - CBD', 'Soshanguve Block H'),
('Soshanguve - CBD', 'Mabopane Station'),
('Soshanguve - CBD', 'Pretoria North'),
('Soshanguve - CBD', 'Marabastad'),
('Soshanguve - CBD', 'Bosman Taxi Rank');


INSERT INTO routes_locations (route_name, location_name) VALUES
('Atteridgeville - CBD', 'Atteridgeville'),
('Atteridgeville - CBD', 'Saulsville'),
('Atteridgeville - CBD', 'Pretoria West'),
('Atteridgeville - CBD', 'Marabastad'),
('Atteridgeville - CBD', 'Bosman Taxi Rank');


INSERT INTO routes_locations (route_name, location_name) VALUES
('Centurion - CBD', 'Centurion Mall'),
('Centurion - CBD', 'Jean Avenue'),
('Centurion - CBD', 'Fountains Valley'),
('Centurion - CBD', 'Pretoria Station'),
('Centurion - CBD', 'Bosman Taxi Rank');

INSERT INTO routes_locations (route_name, location_name) VALUES
('Hammanskraal - CBD', 'Hammanskraal'),
('Hammanskraal - CBD', 'Temba'),
('Hammanskraal - CBD', 'Waltloo'),
('Hammanskraal - CBD', 'Marabastad'),
('Hammanskraal - CBD', 'Pretoria Station');


INSERT INTO routes_locations (route_name, location_name) VALUES
('Ga-Rankuwa - CBD', 'Ga-Rankuwa Zone 1'),
('Ga-Rankuwa - CBD', 'Ga-Rankuwa Hospital'),
('Ga-Rankuwa - CBD', 'Mabopane Station'),
('Ga-Rankuwa - CBD', 'Pretoria North'),
('Ga-Rankuwa - CBD', 'Bosman Taxi Rank');


INSERT INTO routes_locations (route_name, location_name) VALUES
('Eersterust - Menlyn', 'Eersterust'),
('Eersterust - Menlyn', 'Silverton'),
('Eersterust - Menlyn', 'Pretoria Botanical Garden'),
('Eersterust - Menlyn', 'Lynnwood Road'),
('Eersterust - Menlyn', 'Menlyn Mall');


INSERT INTO routes_locations (route_name, location_name) VALUES
('Mamelodi - Hatfield', 'Mamelodi East'),
('Mamelodi - Hatfield', 'Mamelodi West'),
('Mamelodi - Hatfield', 'Pretoria CBD'),
('Mamelodi - Hatfield', 'Arcadia'),
('Mamelodi - Hatfield', 'Hatfield Gautrain Station');

COMMIT;
