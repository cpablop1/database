
#from mySql import mySql
from data.mySql import mySql

maria = mySql()

#SOBRE LA LECTURA DE DATOS DENTRO DE LAS CLASES, metodos read*
"""
    Estos metodos pueden recibir nada, o dos parametros, el primero un NOMBRE DEL CAMPO,
    con cualquiera de los campos para cada metodo, el segundo parametro es el VALUE
    
    ejemplo *read*.(campo1=valor1, campo2=valor2... campon=valorn)
    los campos posibles aparecen con cada metodo read* de las clases
    
    --si no recibe nada, devuelve todos los registros existentes
    --si recibe un nombre_Campo, y valor, devuelve las coincidencias con ese campo y valor
    --si no se hayan resgistros en la clave 'res' se adjunta 'No hay registros que mostrar'
    
    estructura del retorno
    dict = {
        'error':'error_type, or no_error'
        'res' : list{
            fila1= dict{'field1':value, 'field2':value, ... 'fieldn':value}
            fila2= dict{'field1':value, 'field2':value, ... 'fieldn':value}
            ...
            filan= dict{'field1':value, 'field2':value, ... 'fieldn':value}
        }
    }
"""
class buffer_chq_pendt_autorizacion():
    """Acciones sobre el Buffer Cheques pendientes de autorizacion     
    """
    
    def read(self,**kwargs):
        """ ---campos aceptados 
        ['id_cheque', 'id_pendencia', 'fecha_emision', 'monto',
        'estado', 'beneficiario', 'num_cuenta', 'id_group']
    
        """
        labels = ['id_cheque', 'id_pendencia', 'fecha_emision', 'monto',
                  'estado', 'beneficiario', 'num_cuenta', 'id_group']
        
        vista = "v_chq_pendient_valid"
        retorno = maria.select_vista(vista,labels,**kwargs)
        return retorno

    def validar(self,data):
        """
        #---Aca un usuario de grupo valida los cheques
        dependiendo el nivel del grupo, le aparecera los cheques
        que estan dentro del monto permitido para su grupo
                
        #---recibe un diccionario de la siguiente forma
        {'id_pendencia':integer,
        'id_user':integer}
        
        el id_user, será del que ha iniciado sesion
        
        #---Retorna un diccionario de la siguiente forma, 
        ---si no hay errores, o ERRORES dectados en la BD
         {'Error': 'Sin errores, id del elemento insertado adjunto',
         'id': id_liberacion'}
        
        #---posibles valores para 'id'
        1 - 0                          (dato no insertado, error en el id_pendencia o id_user)
        2 - id_liberacion              (dato INSERTADO)
        
        recuerdese que nigun id puede se 0, si hay un cero es "error!"
        
        #---Con error interno, error interno se refiere a algun modulo python
            {'Error': 'Error!'}
        """
         

        labels = ['id_pendencia', 'id_user']
        procedure = 'pa_validar_cheque_grupo'
        sql = sql_builder(procedure,labels,data)
        retorno = maria.insertar( sql )
        return retorno
    
    def solicitar_modificar_elim(self,data):
        """               
        #---recibe un diccionario de la siguiente forma
        {'id_pendencia': integer}
        
        #---Retorna un diccionario de la siguiente forma, 
        ---si no hay errores, o ERRORES dectados en la BD
         {'Error': 'Sin errores, id del elemento insertado adjunto',
         'id': id_llamada'}
        
        #---posibles valores para 'id'
        1 - 0                      (dato no insertado, error en el id_pendencia)
        2 - id_llamada             (dato INSERTADO)
        
        #---Con error interno
            {'Error': 'Error!'}
        """
         
                
        labels = ['id_pendencia']
        procedure = 'pa_solicitar_modificar_elimi'
        sql = sql_builder(procedure,labels,data)
        retorno = maria.insertar( sql )
        return retorno

class buffer_chq_disponible():
    """Acciones sobre el Buffer Cheques disponibles
    
    DROP PROCEDURE IF EXISTS pa_emitir_cheque;
    """
    
    def imprimir(self,data):
        """
        #---MUCHO CUIDADO CON METER numero de chequera ya existente,
        o numero de cuenta no existe devuelve comprobacion en 'id'
        SOLO LOS USUARIOS QUE PERTENECEN AL GRUPO DE PAGOS PUEDEN
        GENERAR CHEQUES
                
        #---recibe un diccionario de la siguiente forma
        {'id_disponible':integer,
         'id_user':integer}
     
        id_user, es del usuario que tiene activa la sesion
        
        #---Retorna un diccionario de la siguiente forma, 
        ---si no hay errores, o ERRORES dectados en la BD
         {'Error': 'Sin errores, id del elemento insertado adjunto',
         'id': id_emision'}

        
        #---posibles valores para 'id'
        1 - 0                       (dato no insertado, error en el id_user o en el id_disponible)
        7 - "Retorna el id_emision " (dato INSERTADO)
        
        #---Con error interno
            {'Error': 'Error!'}
        """
         
                
        labels = ['id_disponible', 'id_user']
        procedure = 'pa_emitir_cheque'
        sql = sql_builder(procedure,labels,data)
        retorno = maria.insertar( sql )
        return retorno
    
    def read_all(self,**kwargs):
        """ ---campos aceptados 
        ['id_cheque', 'num_cheque', 'fecha_emision', 'monto',
        'lugar_emision', 'estado', 'beneficiario', 'num_cuenta',
        'num_chequera', 'nit', 'id_user_genero']
        """
        labels = ['id_cheque', 'num_cheque', 'fecha_emision', 'monto',
        'lugar_emision', 'estado', 'beneficiario', 'num_cuenta',
        'num_chequera', 'nit', 'id_user_genero']
        
        vista = "cheque"
        retorno = maria.select_vista(vista,labels,**kwargs)
        return retorno

class buffer_llam_jefe():
    """
        Acciones sobre el Buffer llamados de jefe
DROP PROCEDURE IF EXISTS pa_validar_cheque_jefe;
DROP PROCEDURE IF EXISTS pa_modificar_cheque;
DROP PROCEDURE IF EXISTS pa_eliminar_cheque_jefe;
    """
    
    def validar(self,data):
        """
        #---MUCHO CUIDADO CON METER numero de chequera ya existente,
        o numero de cuenta no existe devuelve comprobacion en 'id'
        SOLO LOS USUARIOS QUE PERTENECEN AL GRUPO DE PAGOS PUEDEN
        GENERAR CHEQUES
                
        #---recibe un diccionario de la siguiente forma
        {'monto': float,
        'lugar_emision':string,
        'num_cuenta': integer,
        'num_chequera': integer,
        'nit': integer,
        'id_user_genero': integer}
        
        #---Retorna un diccionario de la siguiente forma, 
        ---si no hay errores, o ERRORES dectados en la BD
         {'Error': 'Sin errores, id del elemento insertado adjunto',
         'id': id_cheque'}
        
        #---posibles valores para 'id'                                          (dato no insertado)
        1 - "Cuenta con saldo insuficiente";                                (dato no insertado)
        2 - "Solo un usuario de grupo de pagos, puede generar cheques";     (dato no insertado)
        3 - "Numero de NIT, no existente";                                  (dato no insertado)
        4 - "Numero de chequera, no existente";                             (dato no insertado)
        5 - "Numero de cuenta, no existente";                               (dato no insertado)
        6 - "El monto no puede ser negativo";                               (dato no insertado)
        7 - "Retorna el id_cheque "                                         (dato INSERTADO)
        
        #---Con error interno
            {'Error': 'Error!'}
        """
         
                
        labels = ['monto', 'lugar_emision', 'num_cuenta', 
        'num_chequera', 'nit', 'id_user_genero']
        procedure = 'pa_new_cheque'
        sql = sql_builder(procedure,labels,data)
        retorno = maria.insertar( sql )
        return retorno
    
    def modificar(self,data):
        """
        #---MUCHO CUIDADO CON METER numero de chequera ya existente,
        o numero de cuenta no existe devuelve comprobacion en 'id'
        SOLO LOS USUARIOS QUE PERTENECEN AL GRUPO DE PAGOS PUEDEN
        GENERAR CHEQUES
                
        #---recibe un diccionario de la siguiente forma
        {'monto': float,
        'lugar_emision':string,
        'num_cuenta': integer,
        'num_chequera': integer,
        'nit': integer,
        'id_user_genero': integer}
        
        #---Retorna un diccionario de la siguiente forma, 
        ---si no hay errores, o ERRORES dectados en la BD
         {'Error': 'Sin errores, id del elemento insertado adjunto',
         'id': id_cheque'}
        
        #---posibles valores para 'id'                                          (dato no insertado)
        1 - "Cuenta con saldo insuficiente";                                (dato no insertado)
        2 - "Solo un usuario de grupo de pagos, puede generar cheques";     (dato no insertado)
        3 - "Numero de NIT, no existente";                                  (dato no insertado)
        4 - "Numero de chequera, no existente";                             (dato no insertado)
        5 - "Numero de cuenta, no existente";                               (dato no insertado)
        6 - "El monto no puede ser negativo";                               (dato no insertado)
        7 - "Retorna el id_cheque "                                         (dato INSERTADO)
        
        #---Con error interno
            {'Error': 'Error!'}
        """
         
                
        labels = ['monto', 'lugar_emision', 'num_cuenta', 
        'num_chequera', 'nit', 'id_user_genero']
        procedure = 'pa_new_cheque'
        sql = sql_builder(procedure,labels,data)
        retorno = maria.insertar( sql )
        return retorno
    
    def anular(self,data):
        """
        #---MUCHO CUIDADO CON METER numero de chequera ya existente,
        o numero de cuenta no existe devuelve comprobacion en 'id'
        SOLO LOS USUARIOS QUE PERTENECEN AL GRUPO DE PAGOS PUEDEN
        GENERAR CHEQUES
                
        #---recibe un diccionario de la siguiente forma
        {'monto': float,
        'lugar_emision':string,
        'num_cuenta': integer,
        'num_chequera': integer,
        'nit': integer,
        'id_user_genero': integer}
        
        #---Retorna un diccionario de la siguiente forma, 
        ---si no hay errores, o ERRORES dectados en la BD
         {'Error': 'Sin errores, id del elemento insertado adjunto',
         'id': id_cheque'}
        
        #---posibles valores para 'id'                                          (dato no insertado)
        1 - "Cuenta con saldo insuficiente";                                (dato no insertado)
        2 - "Solo un usuario de grupo de pagos, puede generar cheques";     (dato no insertado)
        3 - "Numero de NIT, no existente";                                  (dato no insertado)
        4 - "Numero de chequera, no existente";                             (dato no insertado)
        5 - "Numero de cuenta, no existente";                               (dato no insertado)
        6 - "El monto no puede ser negativo";                               (dato no insertado)
        7 - "Retorna el id_cheque "                                         (dato INSERTADO)
        
        #---Con error interno
            {'Error': 'Error!'}
        """
         
                
        labels = ['monto', 'lugar_emision', 'num_cuenta', 
        'num_chequera', 'nit', 'id_user_genero']
        procedure = 'pa_new_cheque'
        sql = sql_builder(procedure,labels,data)
        retorno = maria.insertar( sql )
        return retorno
    
    def read_all(self,**kwargs):
        """ ---campos aceptados 
        ['id_cheque', 'num_cheque', 'fecha_emision', 'monto',
        'lugar_emision', 'estado', 'beneficiario', 'num_cuenta',
        'num_chequera', 'nit', 'id_user_genero']
        """
        labels = ['id_cheque', 'num_cheque', 'fecha_emision', 'monto',
        'lugar_emision', 'estado', 'beneficiario', 'num_cuenta',
        'num_chequera', 'nit', 'id_user_genero']
        
        vista = "cheque"
        retorno = maria.select_vista(vista,labels,**kwargs)
        return retorno

def sql_builder(procedure,labels,data):
        
    sql = f"CALL {procedure}("

    for label in labels:
        if type(data[label]) != type('str'):
            sql += f"{data[label]},"
        else:
            text = str(data[label])
            sql += f"'{text}',"

    sql += "@resultado);"

    return sql
