/*
CREATE [OR REPLACE]
    [DEFINER = { user | CURRENT_USER | role | CURRENT_ROLE }]
    TRIGGER [IF NOT EXISTS] trigger_name trigger_time trigger_event
    ON tbl_name FOR EACH ROW
   [{ FOLLOWS | PRECEDES } other_trigger_name ]
   trigger_stmt;


CREATE OR REPLACE TRIGGER trigger_name
    [BEFORE/AFTER] [INSERT/DELETE/UPDATE]
    ON table_name
    FOR EACH ROW
BEGIN
    sql-instructions;
END


*/

-- T R I G G E R    F O R    B I T A C O R A    P E R S O N A L

    -- Trigger for insert into bitacora_personal
DELIMITER //
CREATE OR REPLACE TRIGGER after_insert_user
    AFTER INSERT
    ON usuario FOR EACH ROW
    BEGIN
        INSERT INTO bitacora_personal        
        (id_user, nombre, apellido, DPI, direccion, id_rol, fecha_ingreso, fecha_egreso)
        VALUES
        (new.id_user, new.nombre, new.apellido, new.DPI, new.direccion, new.id_rol, CURRENT_DATE, NULL);
    END;
    //
DELIMITER; 


-- T R I G G E R    F O R    C U E N T A    B A N C A R I A

    -- Trigger for insert into bitacora_cuenta
DELIMITER //
CREATE OR REPLACE TRIGGER after_insert_bit_cntban
    AFTER INSERT
    ON cuenta_bancaria FOR EACH ROW
    BEGIN
    -- num_cuenta, nombre_banco, nombre_cuenta, fecha_creacion, fondo, estado
        INSERT INTO bitacora_cuenta
        (num_cuenta, nombre_banco, nombre_cuenta, fecha_creacion, fecha_eliminacion, fondo)
        VALUES
        (new.num_cuenta, new.nombre_banco, new.nombre_cuenta, new.fecha_creacion, NULL, new.fondo);
    END;
    //
DELIMITER ; 


-- T R I G G E R    F O R    C H E Q U E

    -- Trigger for insert into bitacora_cuenta
                    --  SET estado_var := "Pendiente autorizacion";
                    --  SET estado_var := "Disponible para impresion";
                    -- restar cuenta bancaria
/*
INSERT INTO cheque
    (num_cheque, fecha_emision, monto, lugar_emision, estado,
    beneficiario, num_cuenta, num_chequera, nit, id_user_genero)
VALUES
    (num_cheque_var, CURRENT_TIMESTAMP, monto, lugar_emision, estado,
    beneficiario, num_cuenta, num_chequera, nit, id_user_genero);
*/
DELIMITER //
CREATE OR REPLACE TRIGGER after_insert_cheque
    AFTER INSERT
    ON cheque FOR EACH ROW
    BEGIN
    DECLARE fondo_var DECIMAL(20, 2);
    DECLARE id_group_var INT;
    DECLARE id_user_var INT;
    
    IF new.estado = "Pendiente autorizacion" THEN
    -- recordar restar el monto en caso de que se valide el cheque
        SELECT gr.id_group INTO id_group_var
        FROM grupo AS gr
        WHERE gr.monto_max =(
	        SELECT MIN(gd.monto_max)
	        FROM grupo AS gd
	        WHERE gd.monto_max >= new.monto);
        
        INSERT INTO bitacora_cheque_fallido
            (fecha_fallo, cod_error, id_user, id_cheque)
        VALUES
            (CURRENT_TIMESTAMP, 'Monto no permito para usuario generador',
            new.id_user_genero, new.id_cheque);

        IF id_group_var IS NULL THEN
            SELECT MAX(us.id_user) INTO id_user_var
            FROM usuario AS us
            WHERE us.id_rol = (
                SELECT MIN(r.id_rol)
            	FROM rol AS r
            	WHERE r.id_permiso_sup = (
            		SELECT MIN(id_permiso_sup)
            		FROM permiso_sup AS ps
            		WHERE ps.nombre REGEXP'pago+')
                     );

            INSERT INTO buffer_llamados_jefe
                (atendido, id_user, id_cheque)
            VALUES (0, id_user_var, new.id_cheque);

        ELSE
            INSERT INTO buffer_cheque_pendiente_autorizacion    
              (atendido, id_cheque, id_group)
            VALUES
              (0, new.id_cheque, id_group_var);
        END IF;
    ELSE
        SET fondo_var := f_fondo_cuenta(new.num_cuenta);
        SET fondo_var := fondo_var - new.monto;
        UPDATE cuenta_bancaria SET fondo=fondo_var WHERE num_cuenta = new.num_cuenta;
        
        INSERT INTO buffer_cheque_disponible
        (atendido, id_cheque)
        VALUES
        (0, new.id_cheque);

    END IF;
    END;
    //
DELIMITER ; 




-- D R O P P I N G
-- DROP TRIGGER [IF EXISTS] [schema_name.]trigger_name
DROP TRIGGER IF EXISTS after_insert_bit_cntban;
DROP TRIGGER IF EXISTS after_insert_user;

DROP TRIGGER IF EXISTS after_insert_cheque;