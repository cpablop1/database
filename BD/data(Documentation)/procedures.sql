/* 
for help visit https://manuales.guebs.com/mysql-5.0/functions.html

a delimiter is necessary for MYSQL to understand where the package starts and ends
Delimiter sign, can be anytype

SET var_name := var_Value;

P R O C E D U R E S
DELIMITER //
CREATE PROCEDURE  prodeure_name(
    IN input_variable_name1 VAR_TYPE,
    IN input_variable_name2 VAR_TYPE,
    OUT output_variable_name1 VAR_TYPE,
    OUT output_variable_name2 VAR_TYPE,
    INOUT input_and_output_variable_name1 VAR_TYPE,
    INOUT input_and_output_variable_name2 VAR_TYPE
)
BEGIN
DECLARE [variable_name1] [var_type] default [default_value];
DECLARE [variable_name1] [var_type] default [default_value];
  instructios
END;
 //
DELIMITER ;

CALL prodeure_name();

F U N C I O N E S

DROP FUNCTION IF exists function_name;
 
DELIMITER //
CREATE FUNCTION function_name()
  RETURNS var_type
  DETERMINISTIC || NOT DETERMINISTIC
BEGIN
  DECLARE var_name var_type_equal_RETURNS_type;
  ********b o d y********
  RETURN var_name;
END;
 //
DELIMITER ; 

FOR TEST function USE       SELECT function_name() AS column_name;


data_need = function_name();

I F  and  E L S E
IF [condition] THEN
   [instructions]
ELSEIF [condition] THEN
   [instructions]
ELSEIF [condition] THEN
   [instructions]
ELSEIF [condition] THEN
   [instructions]
......
ELSE
   [instructions]
END IF;


*/

-- R O L     G R O U P     I N S E R T
    -- function for get id_rol from rol
DELIMITER //
CREATE OR REPLACE FUNCTION f_id_rol()
RETURNS INT
NOT DETERMINISTIC
BEGIN
DECLARE id_rol_var INT;
    SELECT MAX(id_rol) INTO id_rol_var FROM rol;
    IF id_rol_var IS NULL THEN
       RETURN 0;
    ELSE
      RETURN id_rol_var;
    END IF;
END;
//
DELIMITER ; 

    -- function for get id_group from group
DELIMITER //
CREATE OR REPLACE FUNCTION f_id_group()
RETURNS INT
NOT DETERMINISTIC
BEGIN
DECLARE id_group_var INT;
    SELECT MAX(id_group) INTO id_group_var FROM grupo;
    IF id_group_var IS NULL THEN
       RETURN 0;
    ELSE
      RETURN id_group_var;
    END IF;
END;
//
DELIMITER ; 
-- SELECT f_id_group();

    -- Procedure for INSERT into group, and rol as rol_group
DELIMITER //
CREATE OR REPLACE PROCEDURE pa_new_group_rol(
    IN nombre VARCHAR(30),
    IN monto_min DECIMAL(10, 2),
    IN monto_max DECIMAL(10, 2),
    OUT resultado VARCHAR(10)
)
BEGIN
DECLARE generar_cheque BOOLEAN DEFAULT 0;
DECLARE validar_cheque BOOLEAN DEFAULT 1;
    IF f_id_group() = 0 THEN
        SET generar_cheque := 1;
        SET validar_cheque := 0;
    END IF;
    INSERT INTO grupo(nombre, monto_min, monto_max, generar_cheque, validar_cheque)
    VALUES(nombre, monto_min, monto_max, generar_cheque, validar_cheque);
    INSERT INTO rol(id_permiso_sup,id_group)
    VALUES(NULL,f_id_group());
    SET resultado := f_id_rol();
    COMMIT;
END;
 //
DELIMITER ;
-- CALL pa_new_group_rol('Rychy group',45.3,800.50,@resultado);
-- SELECT @resultado;

-- R O L     S U P     P E R M I S I O N     I N S E R T
    -- function for get id_permiso_sup from permiso_sup
DELIMITER //
CREATE OR REPLACE FUNCTION f_id_permiso_sup()
RETURNS INT
NOT DETERMINISTIC
BEGIN
DECLARE id_permiso_sup_var INT;
    SELECT MAX(id_permiso_sup) INTO id_permiso_sup_var FROM permiso_sup;
    IF id_permiso_sup_var IS NULL THEN
       RETURN 0;
    ELSE
      RETURN id_permiso_sup_var;
    END IF;
END;
//
DELIMITER ; 
-- SELECT f_id_permiso_sup();

    -- Procedure for INSERT into permiso_sup, and a rol as rol_permiso_sup
DELIMITER //
CREATE OR REPLACE PROCEDURE pa_new_permis_sup_rol(
    IN nombre VARCHAR(30),
    IN crud_users BOOLEAN,
    IN imprimir_cheque BOOLEAN,
    IN anular_cheque BOOLEAN,
    IN modificar_cheque BOOLEAN,
    IN reporte_cheque BOOLEAN,
    IN auditar_user BOOLEAN,
    IN admin_cuenta_banc BOOLEAN,
    IN auditar_cuenta BOOLEAN,
    IN mostrar_bitacora_user BOOLEAN,
    IN mostrar_bitacora_group BOOLEAN,
    IN mostrar_bitacora_jefe BOOLEAN,
    IN jefe BOOLEAN,
    OUT resultado VARCHAR(10)
)
BEGIN
    INSERT INTO permiso_sup(
        nombre, crud_users, imprimir_cheque, anular_cheque, modificar_cheque,
        reporte_cheque, auditar_user, admin_cuenta_banc, auditar_cuenta,
        mostrar_bitacora_user, mostrar_bitacora_group, mostrar_bitacora_jefe, jefe
    )
    VALUES(
        nombre, crud_users, imprimir_cheque, anular_cheque, modificar_cheque,
        reporte_cheque, auditar_user, admin_cuenta_banc, auditar_cuenta,
        mostrar_bitacora_user, mostrar_bitacora_group, mostrar_bitacora_jefe, jefe
    ) ;
    INSERT INTO rol(id_permiso_sup,id_group)
    VALUES(f_id_permiso_sup(),NULL);
    SET resultado := f_id_rol();
    COMMIT;
END;
 //
DELIMITER ;
-- CALL pa_new_permis_sup_rol('Rychy_sup_rol',1,1,1,1,0,0,1,1,1,0,0,1,@resultado);
-- SELECT @resultado;

-- C O N T A C T A N O S     I N S E R T
    -- Procedure for INSERT into contactanos, for show pops to users
DELIMITER //
CREATE OR REPLACE PROCEDURE pa_new_contact(
    IN nombre VARCHAR(45),
    IN num_telefono INT,
    IN correo VARCHAR(30),
    IN mensaje VARCHAR(255),
    OUT resultado VARCHAR(10)
)
BEGIN
DECLARE id_custom_var INT;
-- id_user and estado, are 'NULL' and '0', until somebo
    INSERT INTO contactanos(nombre, num_telefono, correo, mensaje, estado, id_user)
    VALUES(nombre, num_telefono, correo, mensaje, 0, NULL) ;
    SELECT MAX(id_custom) INTO id_custom_var FROM contactanos;
    IF id_custom_var IS NULL THEN
        SET resultado := 0;
    END IF;
        SET resultado := id_custom_var;
    COMMIT;
END;
 //
DELIMITER ;
-- CALL pa_new_contact('Rychy_customer',45124545,'rychy@gmail.com','Hola quiero un cheque',@resultado);
-- SELECT @resultado;


-- U S U A R I O     I N S E R T
    -- function for get id_permiso_sup from permiso_sup
DELIMITER //
CREATE OR REPLACE FUNCTION f_id_user()
RETURNS INT
NOT DETERMINISTIC
BEGIN
DECLARE id_user_var INT;
    SELECT MAX(id_user) INTO id_user_var FROM usuario;
    IF id_user_var IS NULL THEN
       RETURN 0;
    ELSE
      RETURN id_user_var;
    END IF;
END;
//
DELIMITER ; 
-- SELECT f_id_user();

    -- Procedure for INSERT into contactanos, for show pops to users
DELIMITER //
CREATE OR REPLACE PROCEDURE pa_new_user(
    -- user table
    IN nombre VARCHAR(45),
    IN apellido VARCHAR(30),
    IN DPI BIGINT(15),
    IN direccion VARCHAR(20),
    IN id_rol INT,
    IN clave VARCHAR(15),
    -- email
    IN correo VARCHAR(30),
    -- phone number
    IN numero INT,
    IN compania VARCHAR(20),
    IN pais VARCHAR(30),
    OUT resultado VARCHAR(10)
)
BEGIN
DECLARE id_user_var INT;
    -- user created
    INSERT INTO usuario(nombre, apellido, DPI, direccion, id_rol, clave)
    VALUES(nombre, apellido, DPI, direccion, id_rol, clave);
    SET id_user_var := f_id_user();
    -- user email created
    INSERT INTO correo_user(correo, id_user)
    VALUES(correo, id_user_var);
    -- user email created
    INSERT INTO telefono_user(numero, compania, pais, id_user)
    VALUES(numero, compania, pais, id_user_var);

    SET resultado := id_user_var;
    COMMIT;
END;
 //
DELIMITER ;
-- CALL pa_new_user('Rychy', 'Hernández', 789456, 'sas', 1, 'micontraseña', 'rychy@gmai.com', 123456, 'tigo', 'guatemala',@resultado);
-- SELECT @resultado;
-- CALL pa_new_user('Mycat', 'Tom', 5459456, 'Clear', 7, 'catworld', 'cat@gmail.com', 6763456, 'Movistar', 'Salvador',@resultado);
-- SELECT @resultado;

-- D R O P P I N G
DROP FUNCTION IF EXISTS  f_id_rol;
DROP FUNCTION IF EXISTS  f_id_group;
DROP FUNCTION IF EXISTS  f_id_permiso_sup;
DROP FUNCTION IF EXISTS  f_id_user;

DROP PROCEDURE IF EXISTS  pa_new_group_rol;
DROP PROCEDURE IF EXISTS  pa_new_permis_sup_rol;

DROP PROCEDURE IF EXISTS  pa_new_user;


