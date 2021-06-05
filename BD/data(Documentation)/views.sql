/*
CREATE VIEW view_name as
  SELECT BODY

 SELECT * FROM view_name;

CREATE VIEW view_name as
  SELECT BODY

  FROM other_View
  WHERE;


*/

    -- view for SELECT rol_group
CREATE OR REPLACE VIEW v_rol_group AS
    SELECT r.id_rol, g.nombre, g.monto_min, g.monto_max, g.generar_cheque, g.validar_cheque
    FROM rol AS r
    JOIN  grupo AS g
    on r.id_group = g.id_group
    ORDER BY id_rol;
-- SELECT * FROM v_rol_group;

    -- view for SELECT show sup users
CREATE OR REPLACE VIEW v_rol_user AS
    SELECT r.id_rol,
           p.nombre,
           p.crud_users,
           p.imprimir_cheque,
           p.anular_cheque,
           p.modificar_cheque,
           p.reporte_cheque,
           p.auditar_user,
           p.admin_cuenta_banc,
           p.auditar_cuenta,
           p.mostrar_bitacora_user,
           p.mostrar_bitacora_group,
           p.mostrar_bitacora_jefe,
           p.jefe
    FROM rol AS r
    JOIN  permiso_sup AS p
    on r.id_permiso_sup = p.id_permiso_sup
    ORDER BY id_rol;
-- SELECT * FROM v_rol_user;

    -- view for SELECT rol_group
CREATE OR REPLACE VIEW v_all_rol AS
    SELECT 
    id_rol,
    nombre as nombre_rol
    FROM v_rol_group
    UNION 
    SELECT 
    id_rol,
    nombre as nombre_rol
    FROM v_rol_user
    ORDER BY id_rol
    ;
-- SELECT * FROM v_all_rol;



    -- view for SELECT contactos no atendidos
CREATE OR REPLACE VIEW v_contactanos_no AS
    SELECT c.nombre, c.num_telefono, c.correo, c.mensaje
    FROM contactanos AS c
    WHERE c.estado = 0
    ORDER BY nombre
    ;
-- SELECT * FROM v_contactanos_no;

-- view for SELECT contactos si atendidos
CREATE OR REPLACE VIEW v_contactanos_si AS
    SELECT c.nombre, c.num_telefono, c.correo, c.mensaje, u.nombre as user_name, u.apellido, u.id_user
    FROM contactanos AS c
    JOIN  usuario AS u
    on u.id_user = c.id_user
    where c.estado = 1
    ORDER BY id_user
    ;

-- SELECT * FROM v_contactanos_si;

-- view for SELECT usuarios de grupo
CREATE OR REPLACE VIEW v_users_rol_group AS
    SELECT
        u.id_user,
        u.nombre,
        u.apellido,
        u.DPI,
        u.direccion,
        u.id_rol,
        u.clave,
        g.nombre as nombre_grupo,
        cu.correo,
        tfu.numero,
        tfu.compania
    FROM
        usuario AS u
    JOIN rol AS r
    ON u.id_rol = r.id_rol
    JOIN grupo AS g
    ON r.id_group = g.id_group
    JOIN correo_user AS cu
    ON u.id_user = cu.id_user
    JOIN telefono_user AS tfu
    ON u.id_user = tfu.id_user
    ORDER BY id_user
    ;
-- SELECT * FROM v_users_rol_group;

-- view for SELECT usuarios con permiso sup
CREATE OR REPLACE VIEW v_users_rol_sup AS
    SELECT
        u.id_user,
        u.nombre,
        u.apellido,
        u.DPI,
        u.direccion,
        u.id_rol,
        u.clave,
        ps.nombre as nombre_sup_user,
        cu.correo,
        tfu.numero,
        tfu.compania
    FROM
        usuario AS u
    JOIN rol AS r
    ON u.id_rol = r.id_rol
    JOIN permiso_sup AS ps
    ON r.id_permiso_sup = ps.id_permiso_sup
    JOIN correo_user AS cu
    ON u.id_user = cu.id_user
    JOIN telefono_user AS tfu
    ON u.id_user = tfu.id_user
    ORDER BY id_user
    ;
-- SELECT * FROM v_users_rol_sup;

-- view for SELECT all users
CREATE OR REPLACE VIEW v_all_users
 AS
    SELECT
        id_user,
        nombre,
        apellido,
        DPI,
        direccion,
        id_rol,
        clave,
        nombre_sup_user as nombre_rol,
        correo,
        numero,
        compania
    FROM
        v_users_rol_sup AS v_r_sup
    UNION
    SELECT
        id_user,
        nombre,
        apellido,
        DPI,
        direccion,
        id_rol,
        clave,
        nombre_grupo as nombre_rol,
        correo,
        numero,
        compania
    FROM
        v_users_rol_group AS v_r_grp
    ORDER BY id_user
    ;  
    
-- SELECT * FROM v_all_users;

-- view for SELECT usuarios con permiso sup
CREATE OR REPLACE VIEW v_proveedor AS
    SELECT
        p.nit,
        p.nombre_empresa,
        p.prov_name,
        p.prov_lastname,
        p.direccion,
        p.estado,
        cp.correo,
        tfp.numero,
        tfp.compania
    FROM
        proveedor AS p
    JOIN correo_prov AS cp
    ON p.nit = cp.nit
    JOIN telefono_prov AS tfp
    ON p.nit = tfp.nit
    ORDER BY nit
    ;
-- SELECT * FROM v_proveedor;


-- view for SELECT movimiento cuenta
CREATE OR REPLACE VIEW v_mov_cuenta AS
        SELECT
    bm.monto_movido,
    bm.fondo_resultante,
    bm.num_cuenta,
    bm.no_deposito,
    bm.id_emision,
    IF(bm.no_deposito IS NULL, 
       (SELECT bce.fecha_entrega
       FROM bitacora_cheque_emitido AS bce
       WHERE bce.id_emision = bm.id_emision),
       (SELECT bd.fecha_deposito
       FROM bitacora_deposito AS bd
       WHERE bd.no_deposito = bm.no_deposito)
       ) AS fecha
    FROM
        bitacora_movimiento_cuenta AS bm
    ORDER BY fecha
    ;
-- SELECT * FROM mov_cuenta;

-- view for SELECT cheques eliminados
CREATE OR REPLACE VIEW v_b_cheq_emitido AS
    SELECT
    
    chq.id_cheque,
    chq.num_cheque,
    chq.fecha_emision,
    chq.monto,
    chq.lugar_emision,
    chq.estado,
    chq.beneficiario,
    chq.num_cuenta,
    chq.num_chequera,
    chq.nit,
    chq.id_user_genero,
    bce.id_emision,
    bce.fecha_entrega,
    bce.nombre_cajero,
    bce.id_user AS id_user_emitio

    FROM
        cheque AS chq
    JOIN bitacora_cheque_emitido AS bce
    ON chq.id_cheque = bce.id_cheque
    ORDER BY fecha_entrega
    ;
-- SELECT * FROM v_b_cheq_emitido;

-- view for SELECT cheques eliminados o anulados
CREATE OR REPLACE VIEW v_b_cheq_eliminado AS
    SELECT
    
    chq.id_cheque,
    chq.num_cheque,
    chq.fecha_emision,
    chq.monto,
    chq.lugar_emision,
    chq.estado,
    chq.beneficiario,
    chq.num_cuenta,
    chq.num_chequera,
    chq.nit,
    chq.id_user_genero,
    
    bce.id_eliminado,
    bce.fecha_anulacion,
    bce.id_user AS id_user_elimino

    FROM
        cheque AS chq
    JOIN bitacora_cheque_eliminado AS bce
    ON chq.id_cheque = bce.id_cheque
    ORDER BY fecha_anulacion
    ;
-- SELECT * FROM v_b_cheq_eliminado;

-- view for SELECT cheques fallidos
CREATE OR REPLACE VIEW v_b_cheq_fallido AS
    SELECT
    
    chq.id_cheque,
    chq.num_cheque,
    chq.fecha_emision,
    chq.monto,
    chq.lugar_emision,
    chq.estado,
    chq.beneficiario,
    chq.num_cuenta,
    chq.num_chequera,
    chq.nit,
    chq.id_user_genero,
    
    cf.id_fallo,
    cf.fecha_fallo,
    cf.cod_error,
    cf.id_user AS id_user_fallo

    FROM
        cheque AS chq
    JOIN bitacora_cheque_fallido AS cf
    ON chq.id_cheque = cf.id_cheque
    ORDER BY fecha_fallo
    ;
-- SELECT * FROM v_b_cheq_eliminado;

-- view for SELECT cheques liberados
CREATE OR REPLACE VIEW v_b_cheq_liberado AS
    SELECT
    
    chq.id_cheque,
    chq.num_cheque,
    chq.fecha_emision,
    chq.monto,
    chq.lugar_emision,
    chq.estado,
    chq.beneficiario,
    chq.num_cuenta,
    chq.num_chequera,
    chq.nit,
    chq.id_user_genero,
    
    bcl.id_liberacion,
    bcl.fecha_liberacion,
    bcl.id_grupo,
    bcl.id_user AS id_user_libero

    FROM
        cheque AS chq
    JOIN bitacora_cheque_liberado AS bcl
    ON chq.id_cheque = bcl.id_cheque
    ORDER BY fecha_liberacion
    ;
-- SELECT * FROM v_b_cheq_liberado;

-- view for SELECT cheques en buffer pendientes
CREATE OR REPLACE VIEW v_chq_pendient_valid AS
    SELECT
    
    chq.id_cheque,
    bcpa.id_pendencia,
    chq.fecha_emision,
    chq.monto,
    chq.estado,
    chq.beneficiario,
    chq.num_cuenta,
    bcpa.id_group
    
    FROM
        cheque AS chq
    JOIN buffer_cheque_pendiente_autorizacion AS bcpa
    ON chq.id_cheque = bcpa.id_cheque
    ORDER BY bcpa.id_pendencia
    ;
-- SELECT * FROM v_chq_pendient_valid;


-- view for SELECT cheques modificados
CREATE OR REPLACE VIEW v_chq_dispon AS
    SELECT
    
    chq.id_cheque,
    bcds.id_disponible,
    chq.fecha_emision,
    chq.monto,
    chq.estado,
    chq.beneficiario,
    chq.num_cuenta,
    bcds.id_group
    
    FROM
        cheque AS chq
    JOIN buffer_cheque_disponible AS bcds
    ON chq.id_cheque = bcds.id_cheque
    ORDER BY bcpa.id_pendencia
    ;
-- SELECT * FROM v_chq_pendient_valid;




-- D R O P P I N G
DROP VIEW IF EXISTS v_rol_group;
DROP VIEW IF EXISTS v_rol_user;
DROP VIEW IF EXISTS v_all_rol;

DROP VIEW IF EXISTS v_contactanos_no;
DROP VIEW IF EXISTS v_contactanos_si;

DROP VIEW IF EXISTS v_users_rol_group;
DROP VIEW IF EXISTS v_users_rol_sup;
DROP VIEW IF EXISTS v_all_users;

DROP VIEW IF EXISTS v_proveedor;
DROP VIEW IF EXISTS v_mov_cuenta;

DROP VIEW IF EXISTS v_b_cheq_emitido;
DROP VIEW IF EXISTS v_b_cheq_eliminado;

DROP VIEW IF EXISTS v_b_cheq_fallido;
DROP VIEW IF EXISTS v_b_cheq_liberado;
DROP VIEW IF EXISTS v_b_cheq_modif;

DROP VIEW IF EXISTS v_chq_pendient_valid;
DROP VIEW IF EXISTS v_chq_dispon;