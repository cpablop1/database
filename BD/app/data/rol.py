from BD.app.data.mySql import mySql
#from mySql import mySql
import json
maria = mySql()
    
class Rol_grupo():
    """Esta es la clase para crear roles de grupos,
    no es para roles de usuario singular"""
    def create(self,data):
        #recibe un diccionario de la siguiente forma
        # {"nombre" : 'Name',
        # "monto_min" : number,
        # "monto_max": number}
        
        #Retorna un diccionario de la siguiente forma, 
        #---si no hay errores
        # {'Error': 'Sin errores, id del elemento insertado adjunto',
        # 'id': 'id_del_rol_grupo'}
        #---Con error
        # {'Error': 'Error!'}
        
        #El grupo 1 es de pagos, y el resto es de autoridad que validaran cheques, 
        #Mysql empieza las llaves autoincrementeas por 1
        #Solo el nivel 1, tiene True en generar cheque, y validar_cheque = 0
        #los rol_group con id_group > 1, serán lo contrario al grupo 1
        
        retorno = ""
        Data = dict(data)
        nombre = Data['nombre']
        monto_min = Data['monto_min']
        monto_max = Data['monto_max']

        sql = f"CALL pa_new_group_rol('{nombre}',{monto_min},{monto_max},@resultado);"
        retorno = maria.insertar( sql )
        return retorno
    
    def read(self,data=None):
        #Puede recibir un valor entero, que es el id_rol, o nada
        #Si recibe un id_devuelve el registro de ese id
        #si no recibe nada, devuelve todos los registros de rol_grupo
        
        #devuelve de la siguiente forma {{'error':'error o sin_error'},{'res':una_lista_de_diccionario}}
        #Si en ambos casos no encontraron registros, en 'res' es igual a 'No hay registros que mostrar
        
        #pudiendo recorerse de la siguiente forma
        """
SELECT = rol_grupo.read()
for fila in SELECT['res']:
    for campo, valor in fila.items():
            print(campo, ':', valor,end=" ")
    print('')"""
        
        retorno = {"error":"error"}
        res = {}
        if data == None:
            sql = 'SELECT * FROM v_rol_group;'
            res = maria.obtener( sql )
        else:
            sql = f"SELECT * FROM v_rol_group WHERE id_rol = {data};"
            res = maria.obtener(sql)
        if len(res['filas']) == 0:
            retorno['error'] = 'sin_errores'
            retorno['res'] = 'No hay registros que mostrar'
        else:
            retorno['res']=maria.rotular (res['filas'], ['id_rol', 'nombre', 'monto_min', 'monto_max', 'generar_cheque', 'validar_cheque'])

        return retorno
    def listar(self,data): #No funcional aun
        return {"error":"Esto es [ LISTAR ] usuarios"}
    
class Rol_permiso_sup():
    """Esta es la clase para crear roles de usuarios sigulares, cajeros, administrdores, etc 
    no, es para roles de grupo"""
    def create(self,data):
        #recibe un diccionario
        #True se representa con =  y False con 0
        #El obejeto debe estar ordenado de la siguietne forma
        #{"nombre": String(30),                   
        #"crud_users": True or False,
        #"imprimir_cheque": True or False,
        #"anular_cheque": True or False,
        #"modificar_cheque": True or False,
        #"reporte_cheque": True or False,
        #"auditar_user": True or False,
        #"admin_cuenta_banc": True or False,
        #"auditar_cuenta": True or False,
        #"mostrar_bitacora_user": True or False,
        #"mostrar_bitacora_group": True or False,
        #"mostrar_bitacora_jefe": True or False,
        #"jefe": True or False}
        
        #Retorna un diccionario, con la id_rol o error, igual que la clase Rol_grupo
        retorno = ""
        Data = dict(data)
        nombre = Data['nombre']
        crud_users = Data['crud_users']
        imprimir_cheque = Data['imprimir_cheque']
        anular_cheque = Data['anular_cheque']
        modificar_cheque = Data['modificar_cheque']
        reporte_cheque = Data['reporte_cheque']
        auditar_user = Data['auditar_user']
        admin_cuenta_banc = Data['admin_cuenta_banc']
        auditar_cuenta = Data['auditar_cuenta']
        mostrar_bitacora_user = Data['mostrar_bitacora_user']
        mostrar_bitacora_group = Data['mostrar_bitacora_group']
        mostrar_bitacora_jefe = Data['mostrar_bitacora_jefe']
        jefe = Data['jefe']

        sql = (f"CALL pa_new_permis_sup_rol('{nombre}', {crud_users}, {imprimir_cheque}"\
            f",{anular_cheque}, {modificar_cheque}, {reporte_cheque}, {auditar_user}"\
                f",{admin_cuenta_banc}, {auditar_cuenta}, {mostrar_bitacora_user}"\
                    f",{mostrar_bitacora_group}, {mostrar_bitacora_jefe}"\
                       f",{jefe},@resultado);")
        retorno = maria.insertar( sql )
        return retorno
    
    def read(self,data=None):
        #funciona igual que rol_grupo
        
        retorno = {"error":"error"}
        res = {}
        if data == None:
            sql = 'SELECT * FROM v_rol_user;'
            res = maria.obtener( sql )
        else:
            sql = f"SELECT * FROM v_rol_user WHERE id_rol = {data};"
            res = maria.obtener(sql)
        if len(res['filas']) == 0:
            retorno['error'] = 'sin_errores'
            retorno['res'] = 'No hay registros que mostrar'
        else:
            labels =  ['id_rol','nombre', 'crud_users', 'imprimir_cheque', 'anular_cheque', 'modificar_cheque',
                       'reporte_cheque', 'auditar_user', 'admin_cuenta_banc', 'auditar_cuenta',
                       'mostrar_bitacora_user', 'mostrar_bitacora_group', 'mostrar_bitacora_jefe', 'jefe']
            retorno['res']=maria.rotular (res['filas'],labels)

        return retorno
