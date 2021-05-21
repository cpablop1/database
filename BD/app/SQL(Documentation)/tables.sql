-- https://programacion.net/articulo/integridad_referencial_en_mysql_263/4

-- Proveedor
CREATE TABLE proveedor(
    nit INT UNSIGNED AUTO_INCREMENT,
    nombre_empresa VARCHAR(60),
    prov_name VARCHAR(40),
    prov_lastname VARCHAR(25),
    direccion VARCHAR(20),
    estado VARCHAR(10),
    PRIMARY KEY(nit)
) ENGINE = INNODB;

CREATE TABLE correo_prov(
    correo VARCHAR(30),
    nit INT UNSIGNED,
    PRIMARY KEY(correo),
    INDEX(nit),
    FOREIGN KEY(nit) REFERENCES proveedor(nit) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

CREATE TABLE telefono_prov(
    numero INT UNSIGNED,
    compania VARCHAR(20),
    pais VARCHAR(30),
    nit INT UNSIGNED,
    PRIMARY KEY(numero),
    INDEX(nit),
    FOREIGN KEY(nit) REFERENCES proveedor(nit) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB; 

-- Rol
CREATE TABLE permiso_sup(
    id_permiso_sup INT UNSIGNED AUTO_INCREMENT,
    nombre VARCHAR(30),
    crud_users BOOLEAN,
    imprimir_cheque BOOLEAN,
    anular_cheque BOOLEAN,
    modificar_cheque BOOLEAN,
    reporte_cheque BOOLEAN,
    auditar_user BOOLEAN,
    admin_cuenta_banc BOOLEAN,
    auditar_cuenta BOOLEAN,
    mostrar_bitacora_user BOOLEAN,
    mostrar_bitacora_group BOOLEAN,
    mostrar_bitacora_jefe BOOLEAN,
    PRIMARY KEY(id_permiso_sup)
) ENGINE = INNODB;

CREATE TABLE grupo(
    id_group INT UNSIGNED AUTO_INCREMENT,
    nombre VARCHAR(30),
    monto_min DECIMAL(10, 2) UNSIGNED,
    monto_max DECIMAL(10, 2) UNSIGNED,
    nivel_autoridad INT UNSIGNED,
    generar_cheque BOOLEAN,
    llamar_jefe_dep BOOLEAN,
    validar_cheque BOOLEAN,
    llamar_jefe_pagos BOOLEAN,
    PRIMARY KEY(id_group)
) ENGINE = INNODB;

CREATE TABLE rol(
    id_rol INT UNSIGNED AUTO_INCREMENT,
    id_permiso_sup INT UNSIGNED NULL,
    id_group INT UNSIGNED NULL,
    PRIMARY KEY(id_rol),
    INDEX(id_permiso_sup),
    INDEX(id_group),
    FOREIGN KEY(id_permiso_sup) REFERENCES permiso_sup(id_permiso_sup) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(id_group) REFERENCES grupo(id_group) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB; 

-- Usuario
CREATE TABLE usuario(
    id_user INT UNSIGNED AUTO_INCREMENT,
    nombre VARCHAR(45),
    apellido VARCHAR(30),
    DPI BIGINT(15) UNSIGNED,
    direccion VARCHAR(20),
    id_rol INT UNSIGNED,
    PRIMARY KEY(id_user),
    INDEX(id_rol),
    FOREIGN KEY(id_rol) REFERENCES rol(id_rol) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

CREATE TABLE correo_user(
    correo VARCHAR(30),
    id_user INT UNSIGNED,
    PRIMARY KEY(correo),
    INDEX(id_user),
    FOREIGN KEY(id_user) REFERENCES usuario(id_user) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

CREATE TABLE telefono_user(
    numero INT UNSIGNED,
    compania VARCHAR(20),
    pais VARCHAR(30),
    id_user INT UNSIGNED,
    PRIMARY KEY(numero),
    INDEX(id_user),
    FOREIGN KEY(id_user) REFERENCES usuario(id_user) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

-- cuenta bancaria
CREATE TABLE cuenta_bancaria(
    num_cuenta BIGINT(16) UNSIGNED,
    nombre_banco VARCHAR(30),
    nombre_cuenta VARCHAR(30),
    fecha_creacion DATE,
    fondo DECIMAL(20, 2) UNSIGNED,
    estado VARCHAR(10),
    PRIMARY KEY(num_cuenta)
) ENGINE = INNODB;

CREATE TABLE chequera(
    num_chequera INT UNSIGNED AUTO_INCREMENT,
    num_cuenta BIGINT(16) UNSIGNED,
    PRIMARY KEY(num_chequera),
    INDEX(num_cuenta),
    FOREIGN KEY(num_cuenta) REFERENCES cuenta_bancaria(num_cuenta) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

CREATE TABLE cheque(
    id_cheque INT UNSIGNED AUTO_INCREMENT,
    fecha_emision DATETIME,
    monto DECIMAL(15, 2) UNSIGNED,
    lugar_emision VARCHAR(30),
    estado VARCHAR(30),
    beneficiario VARCHAR(67),
    num_cuenta BIGINT(16) UNSIGNED,
    num_chequera INT UNSIGNED,
    nit INT UNSIGNED,
    PRIMARY KEY(id_cheque),
    INDEX(num_chequera),
    INDEX(nit),
    FOREIGN KEY(num_chequera) REFERENCES chequera(num_chequera) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(nit) REFERENCES proveedor(nit) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

-- Buffers
CREATE TABLE buffer_cheque_pendiente_autorizacion(
    id_pendencia INT UNSIGNED AUTO_INCREMENT,
    atendido BOOLEAN,
    id_cheque INT UNSIGNED,
    id_group INT UNSIGNED,
    PRIMARY KEY(id_pendencia),
    INDEX(id_cheque),
    INDEX(id_group),
    FOREIGN KEY(id_cheque) REFERENCES cheque(id_cheque) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(id_group) REFERENCES grupo(id_group) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

CREATE TABLE buffer_cheque_disponible(
    id_disponible INT UNSIGNED AUTO_INCREMENT,
    atendido BOOLEAN,
    id_cheque INT UNSIGNED,
    PRIMARY KEY(id_disponible),
    INDEX(id_cheque),
    FOREIGN KEY(id_cheque) REFERENCES cheque(id_cheque) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

-- Bitacoras relacionados
CREATE TABLE bitacora_cheque_eliminado(
    id_eliminado INT UNSIGNED AUTO_INCREMENT,
    fecha_anulacion DATETIME,
    id_user INT UNSIGNED,
    id_cheque INT UNSIGNED,
    PRIMARY KEY(id_eliminado),
    INDEX(id_user),
    INDEX(id_cheque),
    FOREIGN KEY(id_user) REFERENCES usuario(id_user) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(id_cheque) REFERENCES cheque(id_cheque) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

CREATE TABLE bitacora_movimiento_cuenta(
    num_movimiento INT UNSIGNED AUTO_INCREMENT,
    monto_movido DECIMAL(15, 2),
    fondo_resultante DECIMAL(20, 2) UNSIGNED,
    num_cuenta BIGINT(16) UNSIGNED,
    PRIMARY KEY(num_movimiento),
    INDEX(num_cuenta),
    FOREIGN KEY(num_cuenta) REFERENCES cuenta_bancaria(num_cuenta) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

CREATE TABLE bitacora_cheque_emitido(
    id_emision INT UNSIGNED AUTO_INCREMENT,
    fecha_entrega DATETIME,
    nombre_cajero VARCHAR(75),
    id_user INT UNSIGNED,
    id_cheque INT UNSIGNED,
    num_movimiento INT UNSIGNED,
    PRIMARY KEY(id_emision),
    INDEX(id_user),
    INDEX(num_movimiento),
    FOREIGN KEY(num_movimiento) REFERENCES bitacora_movimiento_cuenta(num_movimiento)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(id_cheque) REFERENCES cheque(id_cheque) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

CREATE TABLE bitacora_deposito(
    no_deposito INT UNSIGNED AUTO_INCREMENT,
    fecha_deposito DATETIME,
    monto DECIMAL(15, 2) UNSIGNED,
    num_cuenta BIGINT(16) UNSIGNED,
    num_movimiento INT UNSIGNED,
    PRIMARY KEY(no_deposito),
    INDEX(num_cuenta),
    INDEX(num_movimiento),
    FOREIGN KEY(num_cuenta) REFERENCES cuenta_bancaria(num_cuenta) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(num_movimiento) REFERENCES bitacora_movimiento_cuenta(num_movimiento) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

-- Bitacoras huerfanas
CREATE TABLE bitacora_personal(
    id_b_personal INT UNSIGNED AUTO_INCREMENT,
    id_user INT UNSIGNED,
    nombre VARCHAR(45),
    apellido VARCHAR(30),
    DPI BIGINT(15) UNSIGNED,
    direccion VARCHAR(20),
    id_rol INT UNSIGNED,
    fecha_ingreso DATE,
    fecha_egreso DATE NULL,
    PRIMARY KEY(id_b_personal)
) ENGINE = INNODB; 

CREATE TABLE bitacora_cuenta(
    id_b_cuenta INT UNSIGNED AUTO_INCREMENT,
    num_cuenta BIGINT(16) UNSIGNED,
    nombre_banco VARCHAR(30),
    nombre_cuenta VARCHAR(30),
    fecha_creacion DATE,
    fecha_eliminacion DATE NULL,
    fondo DECIMAL(20, 2) UNSIGNED NULL,
    PRIMARY KEY(id_b_cuenta)
) ENGINE = INNODB;

CREATE TABLE bitacora_cheque_fallido(
    id_fallo INT UNSIGNED AUTO_INCREMENT,
    fecha_fallo DATETIME,
    cod_error VARCHAR(50),
    id_user INT UNSIGNED,
    id_cheque INT UNSIGNED,
    PRIMARY KEY(id_fallo)
) ENGINE = INNODB;

CREATE TABLE bitacora_cheque_modificado(
    id_mod INT UNSIGNED AUTO_INCREMENT,
    fecha_mod DATETIME,
    monto_antes DECIMAL(15, 2) UNSIGNED,
    monto_post DECIMAL(15, 2) UNSIGNED,
    benef_antes VARCHAR(67),
    benef_post VARCHAR(67),
    id_user INT UNSIGNED,
    id_cheque INT UNSIGNED,
    PRIMARY KEY(id_mod)
) ENGINE = INNODB;

CREATE TABLE bitacora_cheque_liberado(
    id_liberacion INT UNSIGNED AUTO_INCREMENT,
    fecha_liberacion DATETIME,
    id_grupo INT UNSIGNED,
    id_user INT UNSIGNED,
    id_cheque INT UNSIGNED,
    PRIMARY KEY(id_liberacion)
) ENGINE = INNODB;

CREATE TABLE bitacora_cheque_generado(
    id_b_cheque INT UNSIGNED AUTO_INCREMENT,
    fecha_gen DATETIME,
    monto DECIMAL(15, 2) UNSIGNED,
    lugar_gen VARCHAR(30),
    beneficiario VARCHAR(67),
    num_chequera INT UNSIGNED,
    num_cuenta BIGINT(16) UNSIGNED,
    id_user INT UNSIGNED,
    id_cheque INT UNSIGNED,
    PRIMARY KEY(id_b_cheque)
) ENGINE = INNODB;

-- Contactanos
CREATE TABLE contactanos(
    id_custom INT UNSIGNED AUTO_INCREMENT,
    nombre VARCHAR(45),
    num_telefono INT UNSIGNED,
    correo VARCHAR(30),
    mensaje VARCHAR(255),
    estado BOOLEAN,
    id_user INT UNSIGNED,
    PRIMARY KEY(id_custom),
    INDEX(id_user),
    FOREIGN KEY(id_user) REFERENCES usuario(id_user) ON DELETE CASCADE ON UPDATE CASCADE
);

COMMIT;

-- D R O P P I N G
DROP TABLE contactanos;

DROP TABLE bitacora_personal;
DROP TABLE bitacora_cuenta;
DROP TABLE bitacora_cheque_fallido;
DROP TABLE bitacora_cheque_modificado;
DROP TABLE bitacora_cheque_liberado;
DROP TABLE bitacora_cheque_generado;

DROP TABLE bitacora_deposito;
DROP TABLE bitacora_cheque_emitido;
DROP TABLE bitacora_movimiento_cuenta;
DROP TABLE bitacora_cheque_eliminado;

DROP TABLE buffer_cheque_pendiente_autorizacion;
DROP TABLE buffer_cheque_disponible;

DROP TABLE cheque;
DROP TABLE chequera;
DROP TABLE cuenta_bancaria;

DROP TABLE correo_user;
DROP TABLE telefono_user;
DROP TABLE usuario;

DROP TABLE rol;
DROP TABLE grupo;
DROP TABLE permiso_sup;

DROP TABLE correo_prov;
DROP TABLE telefono_prov;
DROP TABLE proveedor;
COMMIT;