
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
class Buffer_chq_pendt_autorizacion():
    """Acciones sobre el Buffer Cheques pendientes de autorizacion     
    """
    
    def read(self,**kwargs):
        """ ---campos aceptados 
        ['id_cheque', 'id_pendencia', 'fecha_emision', 'monto',
        'estado', 'beneficiario', 'num_cuenta', 'id_group', 'nombre']
    
        """

        labels = ['id_cheque', 'id_pendencia', 'fecha_emision', 'monto',
                  'estado', 'beneficiario', 'num_cuenta', 'id_group', 'nombre']

        
        vista = "v_chq_pendient_valid"
        retorno = maria.select_vista(vista,labels,**kwargs)
        return retorno

    def validar(self,data):
        """
        #---Aca un usuario de grupo validar los cheques
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

class Buffer_chq_disponible():
    """Acciones sobre el Buffer Cheques disponibles
    """
    
    def imprimir(self,data):
        """                
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
        7 - "Retorna el id_emision" (dato INSERTADO)
        
        #---Con error interno, error interno se refiere a fuera de la base de datos, internamente en modulos Py
            {'Error': 'Error!'}
        """     
        labels = ['id_disponible', 'id_user']
        procedure = 'pa_emitir_cheque'
        sql = sql_builder(procedure,labels,data)
        retorno = maria.insertar( sql )
        return retorno
    
    def read(self,**kwargs):
        """ ---campos aceptados
        
        ['id_cheque', 'id_disponible', 'fecha_emision',
        'monto', 'estado', 'beneficiario', 'num_cuenta ']
        """
        labels = ['id_cheque', 'id_disponible', 'fecha_emision',
                  'monto', 'estado', 'beneficiario', 'num_cuenta ']
        
        vista = "v_chq_dispon"
        retorno = maria.select_vista(vista,labels,**kwargs)
        return retorno

class Buffer_llam_jefe():
    """
        Acciones sobre el Buffer llamados de jefe
    """
    
    def validar(self,data):
        """     
        #---recibe un diccionario de la siguiente forma
        {'id_llamada':integer,
        'id_user':integer}
        
        #---Retorna un diccionario de la siguiente forma, 
        ---si no hay errores, o ERRORES dectados en la BD
         {'Error': 'Sin errores, id del elemento insertado adjunto',
         'id': id_liberacion'}
        
        #---posibles valores para 'id'
        1 - 0                          (dato no insertado, error en el id_user o el id_llamada)
        2 - "Retorna el id_liberacion" (dato INSERTADO)
        
        #---Con error interno
            {'Error': 'Error!'}
        """
         
                
        labels = ['id_llamada', 'id_user']
        procedure = 'pa_validar_cheque_jefe'
        sql = sql_builder(procedure,labels,data)
        retorno = maria.insertar( sql )
        return retorno
    
    def modificar(self,data):
        """   
        #---recibe un diccionario de la siguiente forma
        {'id_llamada':integer,
        'monto_post':float,
        'nit_post':integer,
        'id_user_modifico':integer}
        
        #---Retorna un diccionario de la siguiente forma, 
        ---si no hay errores, o ERRORES dectados en la BD
         {'Error': 'Sin errores, id del elemento insertado adjunto',
         'id': mensaje'}
        
        #---posibles valores para 'id'        
        1 - 'Monto no puede ser negativo';                           (dato no INSERTADO)
        2 - 'id_llamada invalido'                                    (dato no INSERTADO)
        3 - 'Chequera : num_chequera ,Cheque: num_cheque modificado' (dato INSERTADO)
        
        #---Con error interno
            {'Error': 'Error!'}
        """
        labels = ['id_llamada', 'monto_post', 'nit_post', 'id_user_modifico']
        procedure = 'pa_modificar_cheque'
        sql = sql_builder(procedure,labels,data)
        retorno = maria.insertar( sql )
        return retorno
    
    def anular(self,data):
        """        
        #---recibe un diccionario de la siguiente forma
        {'id_llamada':integer,
        'id_user':integer}
        
        #---Retorna un diccionario de la siguiente forma, 
        ---si no hay errores, o ERRORES dectados en la BD
         {'Error': 'Sin errores, id del elemento insertado adjunto',
         'id': id_eliminado'}
        
        #---posibles valores para 'id'
        1 - 0                (dato no insertado, id_llamada o id_user, invalido)
        2 - el id_eliminado  (dato INSERTADO)
        
        #---Con error interno
            {'Error': 'Error!'}
        """       
        labels = ['id_llamada', 'id_user']
        procedure = 'pa_eliminar_cheque_jefe'
        sql = sql_builder(procedure,labels,data)
        retorno = maria.insertar( sql )
        return retorno
    
    def read(self,**kwargs):
        """ ---campos aceptados 
        ['id_cheque', 'id_llamada', 'fecha_emision', 'monto',
        'estado', 'beneficiario', 'num_cuenta']

        """
        labels = ['id_cheque', 'id_llamada', 'fecha_emision', 'monto',
                  'estado', 'beneficiario', 'num_cuenta']
        
        vista = "v_llamada_jefe"
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
