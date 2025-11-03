USE `fast-food_database`;

-- Új felhasználó létrehozása
DELIMITER //
CREATE PROCEDURE create_user(
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(100),
    IN p_phone VARCHAR(50),
    IN p_address TEXT,
    IN p_role ENUM('user', 'admin')
)
BEGIN
    INSERT INTO users (name, email, password, phone, address, role)
    VALUES (p_name, p_email, p_password, p_phone, p_address, p_role);
END;
//
DELIMITER ;

-- Jelszó lecserélése email cím alapján
DELIMITER //
CREATE PROCEDURE update_user_password(
    IN p_email VARCHAR(100),
    IN p_new_password VARCHAR(100)
)
BEGIN
    UPDATE USERS
    SET password = p_new_password
    WHERE email = p_email;
END;
//
DELIMITER ;

-- A felhasználó adatainak visszaadása email cím és jelszó alapján
DELIMITER //
CREATE PROCEDURE get_user(
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(100)
)
BEGIN
    SELECT id, name, password, email, phone, address, role
    FROM users
    WHERE email = p_email AND password = p_password;
END;
//
DELIMITER ;

-- A felhasználó adatainak visszaadása email alapján
DELIMITER //
CREATE PROCEDURE get_user_by_email(
    IN p_email VARCHAR(100)
)
BEGIN
    SELECT id, name, email, password, phone, address, role
    FROM users
    WHERE email = p_email;
END;
//
DELIMITER ;

-- Új étel létrehozása 
DELIMITER //
CREATE PROCEDURE create_food(
    IN p_name VARCHAR(50),
    IN p_description TEXT,
    IN p_image TEXT,
    IN p_price INT
)
BEGIN
    INSERT INTO FOODS (name, description, image, price)
    VALUES (p_name, p_description, p_image, p_price);
END;
//
DELIMITER ;


-- Étel törlése id alapján
DELIMITER //
CREATE PROCEDURE delete_food(
    IN p_id INT
)
BEGIN
    DELETE FROM FOODS WHERE id = p_id;
END;
//
DELIMITER ;

-- Étel adatainak módosítása id alapján
DELIMITER //
CREATE PROCEDURE update_food(
    IN p_id INT,
    IN p_name VARCHAR(50),
    IN p_description TEXT,
    IN p_image TEXT,
    IN p_price INT
)
BEGIN
    UPDATE FOODS
    SET name = p_name,
        description = p_description,
        image = p_image,
        price = p_price
    WHERE id = p_id;
END;
//
DELIMITER ;

-- Visszaadja egy étel összes adatát id alapján
DELIMITER //
CREATE PROCEDURE get_food(
    IN p_id INT
)
BEGIN
    SELECT id, name, description, image, price
    FROM FOODS
    WHERE id = p_id;
END;
//
DELIMITER ;

-- Visszaadja az összes étel összes adatát
DELIMITER //
CREATE PROCEDURE get_all_food()
BEGIN
    SELECT id, name, description, image, price FROM FOODS;
END;
//
DELIMITER ;

-- Rögzíti a rendelést az orders és order_items táblákba
-- Megkapja bemenetbe a felhasználó id, az ételek id és a megjegyzést
DELIMITER //
CREATE PROCEDURE create_order(
    IN p_user_id INT,
    IN p_items JSON,
    IN p_note TEXT
)
BEGIN
    DECLARE new_order_id INT;
    DECLARE i INT DEFAULT 0;
    DECLARE item_count INT;
    DECLARE total_price INT DEFAULT 0;
    DECLARE item_price INT;

    SET item_count = JSON_LENGTH(p_items);

    WHILE i < item_count DO
        SET item_price = JSON_UNQUOTE(JSON_EXTRACT(p_items, CONCAT('$[', i, '].price')));
        SET total_price = total_price + item_price;
        SET i = i + 1;
    END WHILE;

    INSERT INTO orders (user_id, order_date, status, note, price)
    VALUES (
        p_user_id,
        NOW(),
        'pending',
        p_note,
        total_price
    );

    SET new_order_id = LAST_INSERT_ID();
    SET i = 0;

    WHILE i < item_count DO
        INSERT INTO order_items (order_id, food_id, quantity, price)
        VALUES (
            new_order_id,
            JSON_UNQUOTE(JSON_EXTRACT(p_items, CONCAT('$[', i, '].food_id'))),
            JSON_UNQUOTE(JSON_EXTRACT(p_items, CONCAT('$[', i, '].quantity'))),
            JSON_UNQUOTE(JSON_EXTRACT(p_items, CONCAT('$[', i, '].price')))
        );
        SET i = i + 1;
    END WHILE;
END;
//
DELIMITER ;

-- Visszaadja az összes rendelés összes adatát
DELIMITER //
CREATE PROCEDURE get_all_orders()
BEGIN
    SELECT 
        o.id AS order_id,
        o.user_id,
        o.order_date,
        o.status,
        o.note,
        o.price AS total_price,
        oi.id AS item_id,
        oi.food_id,
        oi.quantity,
        oi.price AS item_price
    FROM orders o
    LEFT JOIN order_items oi ON o.id = oi.order_id
    ORDER BY o.order_date DESC;
END;
//
DELIMITER ;

USE `fast-food_database`;
-- Új felhasználó létrehozása
DELIMITER //
CREATE PROCEDURE create_user(
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(100),
    IN p_role ENUM('user', 'admin')
)
BEGIN
    INSERT INTO USERS (name, email, password, role)
    VALUES (p_name, p_email, p_password, p_role);
END;
//
DELIMITER ;

-- Jelszó lecserélése email cím alapján
DELIMITER //
CREATE PROCEDURE update_user_password(
    IN p_email VARCHAR(100),
    IN p_new_password VARCHAR(100)
)
BEGIN
    UPDATE USERS
    SET password = p_new_password
    WHERE email = p_email;
END;
//
DELIMITER ;

-- A felhasználó adatainak visszaadása email cím és jelszó alapján
DELIMITER //
CREATE PROCEDURE get_user(
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(100)
)
BEGIN
    SELECT id, name, password, email, role
    FROM USERS
    WHERE email = p_email AND password = p_password;
END;
//
DELIMITER ;

-- A felhasználó adatainak visszaadása email alapján
DELIMITER //
CREATE PROCEDURE get_user_by_email(
    IN p_email VARCHAR(100)
)
BEGIN
    SELECT id, name, email, password, role
    FROM USERS
    WHERE email = p_email;
END;
//
DELIMITER ;

-- Új étel létrehozása 
DELIMITER //
CREATE PROCEDURE create_food(
    IN p_name VARCHAR(50),
    IN p_image TEXT,
    IN p_price INT
)
BEGIN
    INSERT INTO FOODS (name, image, price)
    VALUES (p_name, p_image, p_price);
END;
//
DELIMITER ;

-- Étel törlése id alapján
DELIMITER //
CREATE PROCEDURE delete_food(
    IN p_id INT
)
BEGIN
    DELETE FROM FOODS WHERE id = p_id;
END;
//
DELIMITER ;

-- Étel adatainak módosítása id alapján
DELIMITER //
CREATE PROCEDURE update_food(
    IN p_id INT,
    IN p_name VARCHAR(50),
    IN p_image TEXT,
    IN p_price INT
)
BEGIN
    UPDATE FOODS
    SET name = p_name,
        image = p_image,
        price = p_price
    WHERE id = p_id;
END;
//
DELIMITER ;

-- Visszaadja egy étel összes adatát id alapján
DELIMITER //
CREATE PROCEDURE get_food(
    IN p_id INT
)
BEGIN
    SELECT id, name, image, price
    FROM FOODS
    WHERE id = p_id;
END;
//
DELIMITER ;

-- Visszaadja az összes étel összes adatát
DELIMITER //
CREATE PROCEDURE get_all_food()
BEGIN
    SELECT id, name, image, price FROM FOODS;
END;
//
DELIMITER ;

-- Rögzíti a rendelést az orders és order_items táblákba
-- Megkapja bemenetbe a felhasználó id, az ételek id és a megjegyzést
DELIMITER //
CREATE PROCEDURE create_order(
    IN p_user_id INT,
    IN p_items JSON,
    IN p_note TEXT
)
BEGIN
    DECLARE new_order_id INT;
    DECLARE i INT DEFAULT 0;
    DECLARE item_count INT;
    DECLARE total_price INT DEFAULT 0;
    DECLARE item_price INT;

    SET item_count = JSON_LENGTH(p_items);

    WHILE i < item_count DO
        SET item_price = JSON_UNQUOTE(JSON_EXTRACT(p_items, CONCAT('$[', i, '].price')));
        SET total_price = total_price + item_price;
        SET i = i + 1;
    END WHILE;

    INSERT INTO orders (user_id, order_date, status, note, price)
    VALUES (
        p_user_id,
        NOW(),
        'pending',
        p_note,
        total_price
    );

    SET new_order_id = LAST_INSERT_ID();
    SET i = 0;

    WHILE i < item_count DO
        INSERT INTO order_items (order_id, food_id, quantity, price)
        VALUES (
            new_order_id,
            JSON_UNQUOTE(JSON_EXTRACT(p_items, CONCAT('$[', i, '].food_id'))),
            JSON_UNQUOTE(JSON_EXTRACT(p_items, CONCAT('$[', i, '].quantity'))),
            JSON_UNQUOTE(JSON_EXTRACT(p_items, CONCAT('$[', i, '].price')))
        );
        SET i = i + 1;
    END WHILE;
END;
//
DELIMITER ;

-- Visszaadja az összes rendelés összes adatát
DELIMITER //
CREATE PROCEDURE get_all_orders()
BEGIN
    SELECT 
        o.id AS order_id,
        o.user_id,
        o.order_date,
        o.status,
        o.note,
        o.price AS total_price,
        oi.id AS item_id,
        oi.food_id,
        oi.quantity,
        oi.price AS item_price
    FROM orders o
    LEFT JOIN order_items oi ON o.id = oi.order_id
    ORDER BY o.order_date DESC;
END;
//
DELIMITER ;

-- Megváltoztatja a rendelés státuszát id alapján
DELIMITER //
CREATE PROCEDURE update_order_status(
    IN p_order_id INT,
    IN p_new_status ENUM('pending', 'completed', 'cancelled')
)
BEGIN
    UPDATE orders
    SET status = p_new_status
    WHERE id = p_order_id;
END;
//
DELIMITER ;
