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
