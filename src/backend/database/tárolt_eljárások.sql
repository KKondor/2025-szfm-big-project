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
