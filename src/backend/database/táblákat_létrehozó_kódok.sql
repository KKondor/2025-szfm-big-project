USE `fast-food_database`;

-- user tábla létrehozása
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(100) NOT NULL,
  phone VARCHAR(50),
  address TEXT NOT NULL,
  role ENUM('user', 'admin') NOT NULL
);

-- foods tábla létrehozása
CREATE TABLE foods (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  description TEXT,
  image TEXT,
  price INT NOT NULL,
  category VARCHAR(50)
);

-- orders tábla létrehozása
CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status ENUM('pending', 'completed', 'cancelled') NOT NULL DEFAULT 'pending',
  note TEXT,
  price INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- order_items tábla létrehozása
CREATE TABLE order_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  food_id INT NOT NULL,
  quantity INT NOT NULL,
  price INT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (food_id) REFERENCES foods(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
