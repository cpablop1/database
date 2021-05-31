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
    /*
        SET fondo_var := f_fondo_cuenta(new.num_cuenta);
        SET fondo_var := fondo_var - new.monto;
        UPDATE cuenta_bancaria SET fondo=fondo_var WHERE num_cuenta = new.num_cuenta;
    */
        INSERT INTO buffer_cheque_disponible
        (atendido, id_cheque)
        VALUES
        (0, new.id_cheque);

    END IF;
    END;
    //
DELIMITER ; 

-- UPDATE ON CHEQUE
DELIMITER //
CREATE OR REPLACE TRIGGER after_up_cheque
    AFTER UPDATE
    ON cheque FOR EACH ROW
    BEGIN 

    INSERT INTO bitacora_cheque_modificado
        (fecha_mod, monto_antes, monto_post, benef_antes, benef_post, id_user, id_cheque)
    VALUES
        (CURRENT_TIMESTAMP, old.monto,new.monto, old.beneficiario, new.beneficiario,
        old.id_user_genero,old.id_cheque);
    END;

    //
DELIMITER ; 

-- T R I G G E R    F O R    i n s e r t    O N   bitacora_cheque_emitido

    -- Trigger for insert into bitacora_cuenta
DELIMITER //
CREATE OR REPLACE TRIGGER after_in_emit_cheque
    AFTER INSERT
    ON bitacora_cheque_emitido FOR EACH ROW
    BEGIN
    DECLARE fondo_var DECIMAL(20, 2);
    DECLARE fondo_res_var DECIMAL(20, 2);
    DECLARE monto_var DECIMAL(20, 2);
    DECLARE num_cuenta_var BIGINT(16);
    
        SELECT ch.num_cuenta
         INTO num_cuenta_var
         FROM cheque AS ch
        WHERE ch.id_cheque = new.id_cheque;

        SELECT fdc.fondo
          INTO fondo_var
          FROM cuenta_bancaria AS fdc
         WHERE fdc.num_cuenta = num_cuenta_var;
            
        SELECT ch.monto
          INTO monto_var
          FROM cheque AS ch
         WHERE ch.id_cheque = new.id_cheque;

        SET fondo_res_var := fondo_var - monto_var;
        UPDATE cuenta_bancaria SET fondo=fondo_res_var
        WHERE cuenta_bancaria.num_cuenta = num_cuenta_var;

        SET monto_var := monto_var *-1;
        INSERT INTO bitacora_movimiento_cuenta
          (monto_movido, fondo_resultante, num_cuenta, no_deposito, id_emision)
        VALUES
          (monto_var, fondo_res_var, num_cuenta_var, NULL, new.id_emision);

    END;
    //
DELIMITER ;


-- T R I G G E R    F O R    i n s e r t    O N   bitacora_cheque_liberado

    -- Trigger for insert into bitacora_cuenta
/* DELIMITER //
CREATE OR REPLACE TRIGGER after_in_liberar_cheque
    AFTER INSERT
    ON bitacora_cheque_liberado FOR EACH ROW
    BEGIN
    DECLARE fondo_var DECIMAL(20, 2);
    DECLARE monto_var DECIMAL(20, 2);
    DECLARE num_cuenta_var BIGINT(16);
    
        SELECT ch.num_cuenta
         INTO num_cuenta_var
         FROM cheque AS ch
        WHERE ch.id_cheque = new.id_cheque;

        SELECT fdc.fondo
          INTO fondo_var
          FROM cuenta_bancaria AS fdc
         WHERE num_cuenta = num_cuenta_var;
            
        SELECT ch.monto
          INTO monto_var
          FROM cheque AS ch
         WHERE ch.id_cheque = new.id_cheque;

        SET fondo_var := fondo_var - monto_var;
        UPDATE cuenta_bancaria SET fondo=fondo_var WHERE num_cuenta = num_cuenta_var;

    END;
    //
DELIMITER ; */

-- D R O P P I N G
-- DROP TRIGGER [IF EXISTS] [schema_name.]trigger_name
DROP TRIGGER IF EXISTS after_insert_bit_cntban;
DROP TRIGGER IF EXISTS after_insert_user;

DROP TRIGGER IF EXISTS after_insert_cheque;
DROP TRIGGER IF EXISTS after_in_emit_cheque;

/* DROP TRIGGER IF EXISTS after_in_liberar_cheque; */