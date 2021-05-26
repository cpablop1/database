/*
CREATE VIEW view_name as
  SELECT BODY

 SELECT * FROM view_name;
*/

    -- view for SELECT rol_group
CREATE VIEW v_rol_group AS
    SELECT r.id_rol, g.nombre, g.monto_min, g.monto_max, g.generar_cheque, g.validar_cheque
    FROM rol AS r
    JOIN  grupo AS g
    on r.id_group = g.id_group;

-- SELECT * FROM v_rol_user;
CREATE VIEW v_rol_user AS
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
    on r.id_permiso_sup = p.id_permiso_sup;

-- D R O P P I N G
DROP VIEW IF EXISTS v_rol_group;
    