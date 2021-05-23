from django.db import models
from django.contrib.auth.models import User

"""
class Bitacora_personal(models.Model):
    id_user = models.PositiveIntegerField(default=0)
    nombre = models.TextField()
    apellido = models.TextField()
    dpi = models.CharField(max_length=13)
    direccion = models.TextField()
    id_rol = models.PositiveIntegerField(default=0)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_egreso = models.DateTimeField(auto_now=True)
    
class Bitacora_cuenta(models.Model):
    num_cuenta = models.CharField(max_length=10)
    nombre_banco = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_eliminacion = models.DateTimeField(auto_now=True)
    fondo = models.FloatField(default=0)

class Bitacora_cheque_generado(models.Model):
    fecha_emision = models.DateTimeField(auto_now_add=True)
    monto = models.FloatField(default=0)
    lugar_emision = models.TextField()
    num_cheque = models.PositiveIntegerField(default=0)
    num_cuenta = models.CharField(max_length=10)
    num_chequera = models.PositiveIntegerField(default=0)
    id_cheque = models.PositiveIntegerField(default=0)
    beneficiario = models.TextField()
    id_user = models.PositiveIntegerField(default=0)

class Bitacora_cheque_modificado(models.Model):
    fecha_modificacion = models.DateTimeField(auto_now=True)
    monto_antes = models.FloatField(default=0)
    monto_post = models.FloatField(default=0)
    beneficiario_antes = models.TextField()
    beneficiario_post = models.TextField()
    id_user = models.PositiveIntegerField(default=0)
    id_cheque = models.PositiveIntegerField(default=0)

class Bitacora_cheque_liberado(models.Model):
    fecha_liberacion = models.DateTimeField(auto_now_add=True)
    id_grupo = models.PositiveIntegerField(default=0)
    id_user = models.PositiveIntegerField(default=0)
    id_cheque = models.PositiveIntegerField(default=0)

class Bitacora_cheque_fallido(models.Model):
    fecha_fallo = models.DateTimeField(auto_now_add=True)
    cuasa = models.TextField()
    id_cheque = models.PositiveIntegerField(default=0)
    id_user = models.PositiveIntegerField(default=0)

class Permiso_superior(models.Model):
    crud_users = models.PositiveIntegerField(default=0)
    imprimir_cheque = models.PositiveIntegerField(default=0)
    anular_cheque = models.PositiveIntegerField(default=0)
    modificar_cheque = models.PositiveIntegerField(default=0)
    reporte_cheques = models.PositiveIntegerField(default=0)
    auditar_usuarios = models.PositiveIntegerField(default=0)
    administrar_cuentas_bancarias = models.PositiveIntegerField(default=0)
    auditar_cuenta = models.PositiveIntegerField(default=0)
    mostrar_bitacora_usuario = models.PositiveIntegerField(default=0)
    mostrar_bitacora_grupo = models.PositiveIntegerField(default=0)
    mostrar_bitacura_jefe = models.PositiveIntegerField(default=0)

class Grupo(models.Model):
    nombre = models.TextField()
    monto_minimo = models.FloatField(default=0)
    manto_maximo = models.FloatField(default=0)
    nivel_autoridad = models.PositiveIntegerField(default=0)
    generar_cheque = models.PositiveIntegerField(default=0)
    llamar_jefe_departamento = models.PositiveIntegerField(default=0)
    validar_cheque = models.PositiveIntegerField(default=0)
    llamar_jefe_pagos = models.PositiveIntegerField(default=0)

class Rol(models.Model):
    nombre = models.TextField()
    id_permiso_sup = models.ForeignKey(Permiso_superior, on_delete=models.PROTECT)
    id_grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dpi = models.CharField(max_length=13)
    direccion = models.TextField()
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.PROTECT)

class Telefono_user(models.Model):
    numero = models.CharField(max_length=8)
    compania = models.TextField()
    pais = models.TextField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)

class Correo_user(models.Model):
    correo = models.TextField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)

class Proveedor(models.Model):
    nit = models.CharField(primary_key=True, max_length=8)
    nombre_empresa = models.TextField()
    representante_nombre = models.TextField()
    representante_apellido = models.TextField()
    direccion = models.TextField()

class Correo_prov(models.Model):
    correo = models.TextField()
    nit = models.ForeignKey(Proveedor, on_delete=models.PROTECT)

class Telefono_prov(models.Model):
    numero = models.CharField(max_length=8)
    compania = models.TextField()
    pais = models.TextField()
    nit = models.ForeignKey(Proveedor, on_delete=models.PROTECT)

class Cuenta_bancaria(models.Model):
    num_cuenta = models.CharField(primary_key=True, max_length=10)
    nombre_banco = models.TextField()
    nombre_cuenta = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fondo = models.FloatField(default=0)
    estado = models.TextField()

class Chequera(models.Model):
    num_chequera = models.CharField(primary_key=True, max_length=15)
    num_cuenta = models.ForeignKey(Cuenta_bancaria, on_delete=models.PROTECT)

class Cheque(models.Model):
    num_cheque = models.CharField(max_length=15)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    monto = models.FloatField(default=0)
    lugar_emision = models.TextField()
    estado = models.TextField()
    beneficiario = models.TextField()
    num_cuenta = models.CharField(max_length=10)
    num_chequera = models.ForeignKey(Chequera, on_delete=models.PROTECT)
    nit = models.ForeignKey(Proveedor, on_delete=models.PROTECT)

class Buffer_cheque_disponible(models.Model):
    atendido = models.PositiveIntegerField(default=0)
    id_cheque = models.ForeignKey(Cheque, on_delete=models.PROTECT)

class Buffer_cheque_pendiente_autorizacion(models.Model):
    atendido = models.PositiveIntegerField(default=0)
    id_grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)
    id_cheque = models.ForeignKey(Cheque, on_delete=models.PROTECT)

class Bitacora_cheque_emitido(models.Model):
    fecha_entrega = models.DateTimeField(auto_now_add=True)
    nombre_cajero = models.TextField()
    id_user = models.CharField(max_length=3)
    id_cheque = models.ForeignKey(Cheque, on_delete=models.PROTECT)

class Bitacora_deposito(models.Model):
    fecha_deposito = models.DateTimeField(auto_now_add=True)
    monto = models.FloatField(default=0)
    num_cuenta = models.CharField(max_length=10)

class Bitacora_movimiento_cuenta(models.Model):
    no_deposito = models.ForeignKey(Bitacora_deposito, on_delete=models.PROTECT)
    id_emision = models.ForeignKey(Bitacora_cheque_emitido, on_delete=models.PROTECT)

class Bitacora_cheque_eliminado(models.Model):
    fecha_eliminacion = models.DateTimeField(auto_now_add=True)
    id_user = models.CharField(max_length=3)
    id_cheque = models.ForeignKey(Cheque, on_delete=models.PROTECT)
"""