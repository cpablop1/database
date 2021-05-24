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
    -- function for get id_group from group
DELIMITER //
CREATE OR REPLACE FUNCTION f_id_group()
RETURNS INT
DETERMINISTIC
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
DECLARE id_group INT;
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
    SET resultado := 'Ingresado exitosamente';
    COMMIT;   
END;
 //
DELIMITER ;
-- CALL pa_new_group_rol('Rychy group',45.3,800.50,@resultado);
-- SELECT @resultado;

-- R O L     G R O U P     I N S E R T
