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
-- CALL pa_new_group_rol('Grupo pago',0,4999.00,@resultado);
-- SELECT @resultado;
-- CALL pa_new_group_rol('Grupo Auditoria',5000,24999.00,@resultado);
-- SELECT @resultado;
-- CALL pa_new_group_rol('Grupo Gerencia',25000,100000.00,@resultado);
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
-- CALL pa_new_permis_sup_rol('Jefe De pagos', 0, 0, 1, 1, 1, 0, 0, 0, 0,0,0,1,@resultado);
-- SELECT @resultado;
-- CALL pa_new_permis_sup_rol('Jefe De Departamento', 0, 0, 1, 1, 1, 1, 0, 0, 1, 1,0,1,@resultado);
-- SELECT @resultado;
-- CALL pa_new_permis_sup_rol('Gerente', 1, 1, 0, 0, 1, 1, 1, 1, 1, 1,1,0,@resultado);
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
    OUT resultado VARCHAR(33)
)
BEGIN
DECLARE id_user_var INT;
DECLARE id_rol_var VARCHAR(30);
DECLARE correo_var VARCHAR(30);
DECLARE numero_var INT;
DECLARE res_var VARCHAR(33);

    SELECT r.id_rol INTO id_rol_var FROM  rol AS r WHERE id_rol = r.id_rol;
    IF id_rol_var IS NOT NULL THEN
        SELECT cu.correo INTO correo_var FROM  correo_user AS cu WHERE correo = cu.correo;
        IF correo_var IS NULL THEN
            SELECT tu.numero INTO numero_var FROM  telefono_user AS tu WHERE numero = tu.numero;
            IF numero_var IS NULL THEN
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

                SET res_var := id_user_var;
                COMMIT;
            ELSE
                SET res_var := "Numero de telefono, ya existente";
            END IF;
        ELSE
            SET res_var := "Correo, ya existente";
        END IF;
    ELSE
        SET res_var := "Id_rol, invalido!";
    END IF;
    SET resultado := res_var;
END;
 //
DELIMITER ;
-- CALL pa_new_user('Rych', 'Jefe pago', 23323, 'sas', 6, 'micontraseña', 'ry23y@gmai.com', 23232, 'tigo', 'guatemala',@resultado);
-- SELECT @resultado;
-- CALL pa_new_user('Rych', 'Jefe Dep', 32323, 'sas', 7, 'micontraseña', 'ry2y@gmasi.com', 213231, 'tigo', 'guatemala',@resultado);
-- SELECT @resultado;
-- CALL pa_new_user('Rych', 'Gerente', 32323, 'sas', 8, 'micontraseña', 'r2y23y@gmasi.com', 41323, 'tigo', 'guatemala',@resultado);
-- SELECT @resultado;
-- CALL pa_new_user('Rychy', 'Hernández', 789456, 'sas', 1, 'micontraseña', 'rychy@gmai.com', 123456, 'tigo', 'guatemala',@resultado);
-- SELECT @resultado;
-- CALL pa_new_user('Mycat', 'Tom', 5459456, 'Clear', 2, 'catworld', 'cat@gmail.com', 6763456, 'Movistar', 'Salvador',@resultado);
-- SELECT @resultado;



--P R O V E E D O R
    -- Procedure for insert into proveedor
DELIMITER //
CREATE OR REPLACE PROCEDURE pa_new_proveedor(
    -- prov table
    IN nit INT,
    IN nombre_empresa VARCHAR(60),
    IN prov_name VARCHAR(40),
    IN prov_lastname VARCHAR(25),
    IN direccion VARCHAR(20),
    -- email
    IN correo VARCHAR(30),
    -- phone number
    IN numero INT,
    IN compania VARCHAR(20),
    IN pais VARCHAR(30),
    OUT resultado VARCHAR(33)
)
BEGIN
DECLARE nit_var INT;
DECLARE correo_var VARCHAR(30);
DECLARE numero_var INT;
DECLARE res_var VARCHAR(33);

    SELECT prov.nit INTO nit_var FROM  proveedor AS prov WHERE nit = prov.nit;
    IF nit_var IS NULL THEN
        SELECT cp.correo INTO correo_var FROM  correo_prov AS cp WHERE correo = cp.correo;
        IF correo_var IS NULL THEN
            SELECT tp.numero INTO numero_var FROM  telefono_prov AS tp WHERE numero = tp.numero;
            IF numero_var IS NULL THEN
                -- user created
                INSERT INTO
                proveedor(nit, nombre_empresa, prov_name, prov_lastname, direccion, estado)
                VALUES
                (nit, nombre_empresa, prov_name, prov_lastname, direccion, 'activo');
                -- user email created
                INSERT INTO correo_prov(correo, nit)
                VALUES(correo, nit);
                -- user telefone_prov created
                INSERT INTO telefono_prov(numero, compania, pais, nit)
                VALUES(numero, compania, pais, nit);
                SET res_var := nit;
                COMMIT;
            ELSE
                SET res_var := "Numero de telefono, ya existente";
            END IF;
        ELSE
            SET res_var := "Correo, ya existente";
        END IF;
    ELSE
        SET res_var := "Nit, ya existente";
    END IF;
    SET resultado := res_var;

END;
 //
DELIMITER ;
-- CALL pa_new_proveedor(465456,'RychyInc', 'Rychy', 'Hernandez', 'sas', 'incrych@gmail.com', 78894512, 'lact enterprise', 'salvador',@resultado);
-- SELECT @resultado;
-- CALL pa_new_proveedor(426556,'RychyInc', 'Rychy', 'Hernandez', 'sas', 'incr2yc2h@gmail.com', 787894512, 'lact enterprise', 'salvador',@resultado);
-- SELECT @resultado;

-- this function ist just for a test over nit from proveedor, don't carry
DELIMITER //
CREATE OR REPLACE FUNCTION _prueva_nit()
RETURNS INT
NOT DETERMINISTIC
BEGIN
DECLARE nit_var INT;
    SELECT prov.nit INTO nit_var FROM  proveedor AS prov WHERE 12 = prov.nit;
    RETURN nit_var;
END;
//
DELIMITER ; 
-- SELECT _prueva_nit();

-- N E W     C U E N T A     B A N C A R I A
/*SELECT CURRENT_TIME;      || SELECT CURRENT_DATE;
  SELECT CURRENT_TIMESTAMP; || SELECT CURRENT_USER;*/

    -- Procedure to insert into Cuenta_bancaria
DELIMITER //
CREATE OR REPLACE PROCEDURE pa_new_cuenta_bancaria(
    IN num_cuenta BIGINT(16),
    IN nombre_banco VARCHAR(30),
    IN nombre_cuenta VARCHAR(30),
    IN fondo DECIMAL(20, 2),
    
    OUT resultado VARCHAR(33)
)
BEGIN
DECLARE num_cuenta_var INT;
DECLARE num_chequera_var INT;
DECLARE res_var VARCHAR(33);

    SELECT cb.num_cuenta INTO num_cuenta_var 
    FROM  cuenta_bancaria AS cb
    WHERE num_cuenta = cb.num_cuenta;
    IF num_cuenta_var IS NULL THEN
        IF fondo >= 0 THEN
            -- Cuenta creating
            INSERT INTO
            cuenta_bancaria(num_cuenta, nombre_banco, nombre_cuenta, fecha_creacion, fondo, estado)
            VALUES (num_cuenta, nombre_banco, nombre_cuenta, CURRENT_DATE, fondo, 'activo');
            SET res_var := num_cuenta;
            SET num_chequera_var := f_num_chequera() + 1;
            CALL pa_new_chequera(num_chequera_var,num_cuenta,10,@resultado);

            COMMIT;
        ELSE
            SET res_var := "Fondo, no puede ser negativo";
        END IF;
    ELSE
        SET res_var := "Numero de cuenta, ya existente";
    END IF;
    SET resultado := res_var;
END;
 //
DELIMITER ;

-- CALL  pa_new_cuenta_bancaria(465456, 'Banrural','Nueva Verapaz',789.45,@resultado);
-- SELECT @resultado;
-- CALL  pa_new_cuenta_bancaria(426556, 'Banco Industrial','Nueva Verapaz',1000.45,@resultado);
-- SELECT @resultado;

-- N E W     C H E Q U E R A
    -- function for get num_chequera from chequera
DELIMITER //
CREATE OR REPLACE FUNCTION f_num_chequera()
RETURNS INT
NOT DETERMINISTIC
BEGIN
DECLARE num_chequera_var INT;
    SELECT MAX(num_chequera) INTO num_chequera_var FROM chequera;
    IF num_chequera_var IS NULL THEN
       RETURN 0;
    ELSE
      RETURN num_chequera_var;
    END IF;
END;
//
DELIMITER ; 
-- SELECT f_num_chequera();

    -- Procedure to insert into chequera
DELIMITER //
CREATE OR REPLACE PROCEDURE pa_new_chequera(
    IN num_chequera INT,
    IN num_cuenta BIGINT(16),
    IN num_cheque_dispo INT,
    OUT resultado VARCHAR(33)
)
BEGIN
DECLARE num_chequera_var INT;
DECLARE num_cuenta_var BIGINT(16);
DECLARE res_var VARCHAR(33);

    SELECT chq.num_chequera INTO num_chequera_var
    FROM chequera AS chq
    WHERE num_chequera = chq.num_chequera;
    IF num_chequera_var IS NULL THEN
        SELECT cb.num_cuenta INTO num_cuenta_var
        FROM cuenta_bancaria AS cb
        WHERE num_cuenta = cb.num_cuenta;
        IF num_cuenta_var IS NOT NULL THEN
            -- Cuenta creating
            INSERT INTO chequera
                (num_chequera, num_cuenta, num_cheque_dispo,estado)
            VALUES
                (num_chequera, num_cuenta, num_cheque_dispo,'activo');
            SET res_var := num_chequera;
            COMMIT;
        ELSE
            SET res_var := "Numero de cuenta, no existente";
        END IF;
    ELSE
        SET res_var := "Numero de chequera, ya existente";
    END IF;
    SET resultado := res_var;
END;
 //
DELIMITER ;

-- CALL pa_new_chequera(1,465456,10,@resultado);
-- SELECT @resultado;
-- CALL pa_new_chequera(1,715648992,10,@resultado);
-- SELECT @resultado;

    -- S O U R C E    F O R    C H E Q U E
        -- function to get next num_cheque from cheque
DELIMITER //
CREATE OR REPLACE FUNCTION f_get_num_cheque(
        num_chequera INT
    )
    RETURNS INT
    NOT DETERMINISTIC
    BEGIN
    DECLARE num_cheque_var INT;
    DECLARE res_iner_var INT;
        SELECT MAX(cq.num_cheque) INTO num_cheque_var
        FROM cheque AS cq
        WHERE num_chequera = cq.num_chequera;
        IF num_cheque_var IS NULL THEN
           SET res_iner_var := 1;
        ELSE
           SET res_iner_var := num_cheque_var + 1;
        END IF;
        RETURN res_iner_var;
    END;
    //
DELIMITER ; 
-- SELECT f_get_num_cheque(45);

        -- function get beneficiary for cheque from proveedor
DELIMITER //
CREATE OR REPLACE FUNCTION f_get_benef_prov(
        nit INT
    )
    RETURNS VARCHAR(67)
    NOT DETERMINISTIC
    BEGIN
    DECLARE benef_var VARCHAR(67);
    DECLARE res_iner_var VARCHAR(67);
    -- CONCAT it's for concatenate the select result
        SELECT CONCAT (p.prov_name,' ',p.prov_lastname) INTO benef_var
        FROM proveedor AS p
        WHERE p.nit = nit;
        IF benef_var IS NULL THEN
           SET res_iner_var := CONCAT('Error whit nit : ',NIT);
        ELSE
           SET res_iner_var := benef_var;
        END IF;
        RETURN res_iner_var;
END;
//
DELIMITER ; 
-- SELECT f_get_benef_prov(426556);

        -- function get id_cheque from grupo cheque
DELIMITER //
CREATE OR REPLACE FUNCTION f_id_cheque()
RETURNS INT
NOT DETERMINISTIC
BEGIN
DECLARE id_cheque_var INT;
    SELECT MAX(id_cheque) INTO id_cheque_var FROM cheque;
    RETURN id_cheque_var;
END;
//
DELIMITER ; 
-- SELECT f_id_cheque();

        -- function get fondo from cuenta_bancaria
DELIMITER //
CREATE OR REPLACE FUNCTION f_fondo_cuenta(
    num_cuenta BIGINT(16)
)
RETURNS DECIMAL(20, 2)
NOT DETERMINISTIC
BEGIN
DECLARE fondo_var DECIMAL(20, 2);
    SELECT fondo INTO fondo_var 
    FROM cuenta_bancaria AS cb
    WHERE cb.num_cuenta = num_cuenta;
    RETURN fondo_var;
END;
//
DELIMITER ; 
-- SELECT f_fondo_cuenta(465456);


-- Procedure to insert into cheque
DELIMITER //
CREATE OR REPLACE PROCEDURE pa_new_cheque(
    IN monto DECIMAL(15, 2),
    IN lugar_emision VARCHAR(30),
    IN num_cuenta BIGINT(16),
    IN num_chequera INT,
    IN nit INT,
    IN id_user_genero INT,
    
    OUT resultado VARCHAR(56)
)
BEGIN
  DECLARE num_cheque_var INT;
  DECLARE estado_var VARCHAR(30);
  DECLARE beneficiario VARCHAR(67);
  DECLARE monto_var DECIMAL(15, 2);
  DECLARE num_cuenta_var BIGINT(16);
  DECLARE num_chequera_var INT;
  DECLARE nit_var INT;
  DECLARE id_user_genero_var INT;
  DECLARE num_cheque_dispo_var INT;
  DECLARE res_var VARCHAR(63);

    SELECT cb.num_cuenta INTO num_cuenta_var
    FROM cuenta_bancaria AS cb
    WHERE num_cuenta = cb.num_cuenta;

  IF monto >= 0 THEN
    IF num_cuenta_var IS NOT NULL THEN 
      SELECT chq.num_chequera INTO num_chequera_var
      FROM chequera AS chq
      WHERE chq.num_chequera = num_chequera;

        IF num_chequera_var IS NOT NULL THEN

          SELECT pr.nit INTO nit_var
          FROM proveedor AS pr
          WHERE pr.nit = nit;

            IF nit_var IS NOT NULL THEN

              SELECT us.id_user INTO id_user_genero_var
              FROM usuario AS us
              INNER JOIN rol
              ON rol.id_rol = us.id_rol
              INNER JOIN grupo
              ON grupo.id_group = rol.id_group
              AND grupo.generar_cheque = 1
              WHERE us.id_user = id_user_genero;
                
                IF id_user_genero_var IS NOT NULL THEN
                  IF (f_fondo_cuenta(num_cuenta)-monto) >= 0 THEN
                    -- Cheque genereting
                    SET num_cheque_var := f_get_num_cheque(num_chequera);
                    SET beneficiario := f_get_benef_prov(nit);
                    
                    SELECT monto_max INTO monto_var
                    FROM grupo
                    WHERE grupo.id_group = 1;
  
                    IF monto_var < monto THEN 
                      SET estado_var := "Pendiente autorizacion";
                    ELSE
                      SET estado_var := "Disponible para impresion";
                    END IF;
  
                    INSERT INTO cheque
                        (num_cheque, fecha_emision, monto, lugar_emision, estado,
                         beneficiario, num_cuenta, num_chequera, nit, id_user_genero)
                    VALUES
                        (num_cheque_var, CURRENT_TIMESTAMP, monto, lugar_emision, estado_var,
                         beneficiario, num_cuenta, num_chequera, nit, id_user_genero);

                    SELECT MAX(num_cheque_dispo) INTO num_cheque_dispo_var
                    FROM chequera AS cheq
                    WHERE num_chequera = cheq.num_chequera;
                    IF num_cheque_dispo_var IS NULL THEN
                        SET num_chequera_var := 1;
                    END IF;
                    SET num_cheque_dispo_var := num_cheque_dispo_var-1;

                    UPDATE chequera SET num_cheque_dispo = num_cheque_dispo_var
                    WHERE num_chequera = chequera.num_chequera;

                    SET res_var := f_id_cheque();
                    COMMIT;
                  ELSE
                    SET res_var := "Cuenta con saldo insuficiente";
                  END IF;
                    
                ELSE
                    SET res_var := "Solo un usuario de grupo de pagos, puede generar cheques";
                END IF;
            ELSE
                SET res_var := "Numero de NIT, no existente";
            END IF;
        ELSE
            SET res_var := "Numero de chequera, no existente";
        END IF;
    ELSE
        SET res_var := "Numero de cuenta, no existente";
    END IF;
  ELSE
      SET res_var := "El monto no puede ser negativo";
  END IF;
  SET resultado := res_var;
END;
 //
DELIMITER ;

-- CALL pa_new_cheque(45,'Sas',465456,1,426556,1,@resultado);
-- SELECT @resultado;
-- CALL pa_new_cheque(45,'SAS',465456,2,426556,3,@resultado);
-- SELECT @resultado;
-- monto, lugar_emision, num_cuenta, num_chequera, nit, id_user_genero

-- D R O P P I N G
DROP FUNCTION IF EXISTS f_id_rol;
DROP FUNCTION IF EXISTS f_id_group;
DROP FUNCTION IF EXISTS f_id_permiso_sup;
DROP FUNCTION IF EXISTS f_id_user;
DROP FUNCTION IF EXISTS _prueva_nit;

DROP FUNCTION IF EXISTS f_num_chequera;
DROP FUNCTION IF EXISTS f_get_num_cheque;
DROP FUNCTION IF EXISTS f_get_benef_prov;

DROP FUNCTION IF EXISTS f_id_cheque;
DROP FUNCTION IF EXISTS f_fondo_cuenta;

DROP PROCEDURE IF EXISTS pa_new_group_rol;
DROP PROCEDURE IF EXISTS pa_new_permis_sup_rol;

DROP PROCEDURE IF EXISTS pa_new_user;
DROP PROCEDURE IF EXISTS pa_new_proveedor;
DROP PROCEDURE IF EXISTS pa_new_contact;

DROP PROCEDURE IF EXISTS pa_new_cuenta_bancaria;
DROP PROCEDURE IF EXISTS pa_new_chequera;
DROP PROCEDURE IF EXISTS pa_new_cheque;


