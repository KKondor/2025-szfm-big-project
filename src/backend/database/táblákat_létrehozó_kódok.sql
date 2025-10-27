USE `fast-food_database`;

-- user tábla létrehozása
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(100) NOT NULL,
  role ENUM('user', 'admin') NOT NULL
);

-- foods tábla létrehozása
CREATE TABLE foods (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  image TEXT,
  price INT NOT NULL
);
