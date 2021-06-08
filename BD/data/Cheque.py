
#from mySql import mySql
from data.mySql import mySql

maria = mySql()

#SOBRE LA LECTURA DE DATOS DENTRO DE LAS CLASES, metodos read*
"""
    Estos metodos pueden recibir nada, o dos parametros, el primero unNOMBRE DEL CAMPO,
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

class Cheque():
    """
        Clase para generar los cheques, y leer los cheques
    """
    
    def create(self,data):
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
        
        el id_user_genero, será el id del usuario con
        sesion abierta
        
        #---Retorna un diccionario de la siguiente forma, 
        ---si no hay errores, o ERRORES dectados en la BD
         {'Error': 'Sin errores, id del elemento insertado adjunto',
         'id': id_cheque'}
        
        #---posibles valores para 'id'
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

    def read_cheque_modificado(self,**kwargs):
        """  ---campos aceptados
        
        ['id_cheque', 'num_cheque', 'fecha_emision', 'monto', 'lugar_emision',
        'estado', 'num_cuenta', 'num_chequera', 'id_user_genero', 'id_mod',
        'fecha_modificacion', 'monto_antes', 'monto_post', 'benef_antes',
        'benef_post', 'id_user_modifico']
        
        """
        
        labels = ['id_cheque', 'num_cheque', 'fecha_emision', 'monto', 'lugar_emision',
        'estado', 'num_cuenta', 'num_chequera', 'id_user_genero', 'id_mod',
        'fecha_modificacion', 'monto_antes', 'monto_post', 'benef_antes',
        'benef_post', 'id_user_modifico']
    
        vista = "v_b_cheq_modif"
        retorno = maria.select_vista(vista,labels,**kwargs)
        return retorno
    
    def read_cheque_liberado(self,**kwargs):
        """  ---campos aceptados
        ['id_cheque', 'num_cheque', 'fecha_emision', 'monto', 'lugar_emision',
        'estado', 'beneficiario', 'num_cuenta', 'num_chequera', 'nit', 'id_user_genero',
        'id_liberacion', 'fecha_liberacion', 'id_grupo', 'id_user_libero']

        """
        labels = ['id_cheque', 'num_cheque', 'fecha_emision', 'monto', 'lugar_emision',
        'estado', 'beneficiario', 'num_cuenta', 'num_chequera', 'nit', 'id_user_genero',
        'id_liberacion', 'fecha_liberacion', 'id_grupo', 'id_user_libero']
        vista = "v_b_cheq_liberado"
        retorno = maria.select_vista(vista,labels,**kwargs)
        return retorno
    
    def read_cheque_fallido(self,**kwargs):
        """  ---campos aceptados 
        ['id_cheque', 'num_cheque', 'fecha_emision', 'monto', 'lugar_emision',
        'estado', 'beneficiario', 'num_cuenta', 'num_chequera', 'nit',
        'id_user_genero', 'id_fallo', 'fecha_fallo', 'cod_error', 'id_user_fallo']
        
        """
        labels = ['id_cheque', 'num_cheque', 'fecha_emision', 'monto', 'lugar_emision',
        'estado', 'beneficiario', 'num_cuenta', 'num_chequera', 'nit',
        'id_user_genero', 'id_fallo', 'fecha_fallo', 'cod_error', 'id_user_fallo']
        
        vista = "v_b_cheq_fallido"
        retorno = maria.select_vista(vista,labels,**kwargs)
        return retorno

    def read_cheque_emitido(self,**kwargs):
        """  ---campos aceptados 
        ['id_cheque','num_cheque', 'fecha_emision', 'monto', 'lugar_emision',
        'estado','beneficiario','num_cuenta','num_chequera','nit',
        'id_user_genero','id_emision','fecha_entrega','nombre_cajero','id_user_emitio']

        """
        labels = ['id_cheque','num_cheque', 'fecha_emision', 'monto', 'lugar_emision',
        'estado','beneficiario','num_cuenta','num_chequera','nit',
        'id_user_genero','id_emision','fecha_entrega','nombre_cajero','id_user_emitio']

        vista = "v_b_cheq_emitido"
        retorno = maria.select_vista(vista,labels,**kwargs)
        return retorno
    
    def read_cheque_eliminado(self,**kwargs):
        """  ---campos aceptados
        ['id_cheque', 'num_cheque', 'fecha_emision', 'monto', 'lugar_emision',
        'estado', 'beneficiario', 'num_cuenta', 'num_chequera', 'nit', 'id_user_genero', 'id_mod',
        'fecha_mod', 'monto_antes', 'monto_post', 'benef_antes', 'benef_post', 'id_user_modifico']
        """
        
        labels = ['id_cheque', 'num_cheque', 'fecha_emision', 'monto', 'lugar_emision',
            'estado', 'beneficiario', 'num_cuenta', 'num_chequera', 'nit', 'id_user_genero', 'id_mod',
            'fecha_mod', 'monto_antes', 'monto_post', 'benef_antes', 'benef_post', 'id_user_modifico']

        vista = "v_b_cheq_eliminado"
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
