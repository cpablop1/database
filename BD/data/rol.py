#from mySql import mySql
from data.mySql import mySql

maria = mySql()


def sql_builder(procedure, labels, data):

    sql = f"CALL {procedure}("

    for label in labels:
        if type(data[label]) != type('str'):
            sql += f"{data[label]},"
        else:
            text = str(data[label])
            sql += f"'{text}',"

    sql += "@resultado);"

    return sql


class Rol_all():
    """Esta es clase para funciones que abarcan todo
    todos los roles sin importar si son de grupo o user_sup"""
    def read_all(self, **kwargs):
        """
        funciona igual que el metod read de la clase Rol_grupo
         Siendo los campos posibles 
         ['id_rol', 'nombre_rol']
        """

        labels = ['id_rol', 'nombre_rol']
        vista = "v_all_rol"
        retorno = maria.select_vista(vista, labels, **kwargs)
        return retorno


class Rol_grupo():
    """Esta es la clase para crear roles de grupos,
    no es para roles de usuario singular"""
    def create(self, data):
        """
        recibe un diccionario de la siguiente forma
        {"nombre" : 'Name', "monto_min" : number, "monto_max": number}
        
        RETORNO
        un diccionario de la siguiente forma
        #---si no hay errores
        {'Error': 'Sin errores, id del elemento insertado adjunto',
         'id': 'id_del_rol_grupo'}
        #---Con error
         {'Error': 'Error!'}
        
        #El grupo 1 es de pagos, y el resto es de autoridad que validaran cheques, 
        #Mysql empieza las llaves autoincrementeas por 1
        #Solo el nivel 1, tiene True en generar cheque, y validar_cheque = 0
        #los rol_group con id_group > 1, serán lo contrario al grupo 1
        """
        procedure = 'pa_new_group_rol'
        labels = ['nombre', 'monto_min', 'monto_max']
        sql = sql_builder(procedure, labels, data)
        retorno = maria.insertar(sql)
        return retorno

    def read(self, **kwargs):
        """
        Puede recibir cualquier campo o serie de campos, con su valor, 
        
        ejemplo *read*.(campo1=valor1, campo2=valor2... campon=valorn)
        
        siendo todos los campos posibles 
        ['id_rol', 'nombre', 'monto_min', 'monto_max','generar_cheque', 'validar_cheque']
        
        #Si recibe campos, hace busquedas de acuerdo a los campos
        #si no recibe nada, devuelve todos los registros de rol_grupo
        
        --RETORNO
        devuelve de la siguiente forma:
        {{'error':'error o sin_error'},{'res':una_lista_de_diccionario}}
        #Si en ambos casos no encontraron registros, en 'res' es igual a 'No hay registros que mostrar
        """
        #pudiendo recorerse de la siguiente forma
        #SELECT = rol_grupo.read()
        #for fila in SELECT['res']:
        #    for campo, valor in fila.items():
        #            print(campo, ':', valor,end=" ")
        #    print('')

        labels = [
            'id_rol', 'nombre', 'monto_min', 'monto_max', 'generar_cheque',
            'validar_cheque'
        ]
        vista = "v_rol_group"
        retorno = maria.select_vista(vista, labels, **kwargs)
        return retorno


class Rol_permiso_sup():
    """Esta es la clase para crear roles de usuarios sigulares, cajeros, administrdores, etc 
    no, es para roles de grupo"""
    def create(self, data):
        """
        Recibe un diccionario
        True se representa con =  y False con 0
        El objeto debe estar ordenado de la siguietne forma
        
        {"nombre": String(30),                   
        "crud_users": True or False,
        "imprimir_cheque": True or False,
        "anular_cheque": True or False,
        "modificar_cheque": True or False,
        "reporte_cheque": True or False,
        "auditar_user": True or False,
        "admin_cuenta_banc": True or False,
        "auditar_cuenta": True or False,
        "mostrar_bitacora_user": True or False,
        "mostrar_bitacora_group": True or False,
        "mostrar_bitacora_jefe": True or False,
        "jefe": True or False}
        
        RETORNO
        Retorna igual que el metodo create de la clase Rol_grupo
        """

        labels = [
            'nombre', 'crud_users', 'imprimir_cheque', 'anular_cheque',
            'modificar_cheque', 'reporte_cheque', 'auditar_user',
            'admin_cuenta_banc', 'auditar_cuenta', 'mostrar_bitacora_user',
            'mostrar_bitacora_group', 'mostrar_bitacora_jefe', 'jefe'
        ]
        procedure = 'pa_new_permis_sup_rol'
        sql = sql_builder(procedure, labels, data)

        retorno = maria.insertar(sql)
        return retorno

    def read(self, **kwargs):
        """Funciona igual que el metodo create, de la clase Rol_grupo
        siendo los campos posibles
        ['id_rol','nombre', 'crud_users', 'imprimir_cheque', 'anular_cheque', 'modificar_cheque',
         'reporte_cheque', 'auditar_user', 'admin_cuenta_banc', 'auditar_cuenta',
         'mostrar_bitacora_user', 'mostrar_bitacora_group', 'mostrar_bitacora_jefe', 'jefe']
        """

        labels = [
            'id_rol', 'nombre', 'crud_users', 'imprimir_cheque',
            'anular_cheque', 'modificar_cheque', 'reporte_cheque',
            'auditar_user', 'admin_cuenta_banc', 'auditar_cuenta',
            'mostrar_bitacora_user', 'mostrar_bitacora_group',
            'mostrar_bitacora_jefe', 'jefe'
        ]
        vista = "v_rol_user"
        retorno = maria.select_vista(vista, labels, **kwargs)
        return retorno
