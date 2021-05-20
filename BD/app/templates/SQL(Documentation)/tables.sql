--https://programacion.net/articulo/integridad_referencial_en_mysql_263/4

--Proveedor 
CREATE TABLE proveedor(
    nit INT UNSIGNED AUTO_INCREMENT,
    nombre_empresa VARCHAR(60),
    representante_name VARCHAR(40),
    representante_lastname VARCHAR(25),
    direccion VARCHAR(20),
    PRIMARY KEY (nit)
) ENGINE = INNODB;
  
CREATE TABLE correo_prov(
    correo VARCHAR(30),
    nit INT UNSIGNED,
    PRIMARY KEY (correo),
    INDEX (nit),
    FOREIGN KEY (nit) REFERENCES proveedor(nit)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

CREATE TABLE telefono_prov(
    numero INT UNSIGNED,
    compania VARCHAR(20),
    pais VARCHAR(30),
    nit INT UNSIGNED,
    PRIMARY KEY (numero),
    INDEX (nit),
    FOREIGN KEY (nit) REFERENCES proveedor(nit)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

COMMIT;

--Rol
CREATE TABLE permiso_sup(
    id_permiso_sup INT UNSIGNED AUTO_INCREMENT,
    crud_users BOOLEAN,
    imprimir_cheque BOOLEAN,
    anular_cheque BOOLEAN,
    modificar_cheque BOOLEAN,
    reporte_cheques BOOLEAN,
    auditar_usuarios BOOLEAN,
    admin_cuentas_bancaria BOOLEAN,
    auditar_cuenta BOOLEAN,
    mostrar_bitacora_user BOOLEAN,
    mostrar_bitacora_group BOOLEAN,
    mostrar_bitacora_jefe BOOLEAN,
    PRIMARY KEY (id_permiso_sup)
) ENGINE = INNODB;

CREATE TABLE grupo(
    id_group INT UNSIGNED AUTO_INCREMENT,
    nombre VARCHAR(30),
    montoMinimo DECIMAL(10,2) UNSIGNED,
    montoMaximo DECIMAL(10,2) UNSIGNED,
    nivelAutoridad INT UNSIGNED,
    generar_cheque BOOLEAN,
    llamar_jefe_Departamento BOOLEAN,
    validar_cheque BOOLEAN,
    llamar_jefe_pagos BOOLEAN,
    PRIMARY KEY (id_group)
) ENGINE = INNODB;

CREATE TABLE rol(
    id_rol INT UNSIGNED AUTO_INCREMENT,
    nombre VARCHAR(30),
    id_permiso_sup INT UNSIGNED NULL,
    id_group INT UNSIGNED NULL,
    PRIMARY KEY (id_rol),
    INDEX (id_permiso_sup),
    INDEX (id_group),
    FOREIGN KEY (id_permiso_sup) REFERENCES permiso_sup(id_permiso_sup)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_group) REFERENCES grupo(id_group)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

COMMIT;

--Usuario
CREATE TABLE usuario(
    id_user INT UNSIGNED AUTO_INCREMENT,
    nombre VARCHAR(45),
    apellido VARCHAR(30),
    DPI BIGINT(15) UNSIGNED,
    direccion VARCHAR(20),
    fecha_ingreso DATE,
    id_rol INT UNSIGNED,
    PRIMARY KEY (id_user),
    INDEX (id_rol),
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;
  
CREATE TABLE correo_user(
    correo VARCHAR(30),
    id_user INT UNSIGNED,
    PRIMARY KEY (correo),
    INDEX (id_user),
    FOREIGN KEY (id_user) REFERENCES usuario(id_user)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

CREATE TABLE telefono_user(
    numero INT UNSIGNED,
    compania VARCHAR(20),
    pais VARCHAR(30),
    id_user INT UNSIGNED,
    PRIMARY KEY (numero),
    INDEX (id_user),
    FOREIGN KEY (id_user) REFERENCES usuario(id_user)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

COMMIT;

--cuenta bancaria
CREATE TABLE cuenta_bancaria(
    num_cuenta BIGINT(16) UNSIGNED,
    nombre_banco VARCHAR(30),
    nombre_cuenta VARCHAR(30),
    fecha_creacion DATE,
    fondo DECIMAL(20,2),
    estado VARCHAR(10),
    PRIMARY KEY (num_cuenta)
) ENGINE = INNODB;

CREATE TABLE chequera(
    num_chequera INT UNSIGNED AUTO_INCREMENT,
    num_cuenta BIGINT(16) UNSIGNED,
    PRIMARY KEY (num_chequera),
    INDEX (num_cuenta),
    FOREIGN KEY (num_cuenta) REFERENCES cuenta_bancaria(num_cuenta)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

CREATE TABLE cheque(
    id_cheque INT UNSIGNED AUTO_INCREMENT,
    fecha_emision DATETIME,
    monto DECIMAL(15,2) UNSIGNED,
    lugar_emision VARCHAR(30),
    estado VARCHAR(30),
    beneficiario VARCHAR(67),
    num_cuenta BIGINT(16) UNSIGNED,
    num_chequera INT UNSIGNED,
    nit INT UNSIGNED,
    PRIMARY KEY (id_cheque),
    INDEX (num_chequera),
    INDEX (nit),
    FOREIGN KEY (num_chequera) REFERENCES chequera(num_chequera)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (nit) REFERENCES proveedor(nit)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

COMMIT;

--D R O P P I N G
DROP TABLE correo_prov;
DROP TABLE telefono_prov;
DROP TABLE proveedor;

DROP TABLE permiso_sup;
DROP TABLE grupo;
DROP TABLE rol;

DROP TABLE user;
DROP TABLE correo_user;
DROP TABLE telefono_user;

DROP TABLE cuenta_bancaria;
DROP TABLE chequera;
DROP TABLE cheque;
