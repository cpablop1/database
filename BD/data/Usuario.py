
#from mySql import mySql
from data.mySql import mySql

maria = mySql() #objeto global de la base de datos 

class Usuario: 
    def create(self,data):
        ##### MUCHO CUIDADO CON METER correos o telefonos iguales, da error en la base,
        # comprobar que no existan antes
        
        #recibe un diccionario de la siguiente forma
        #   -- user table
        #{"nombre" : string,
        # "apellido" : string,
        # "DPI" : integer,
        # "direccion" : string,
        # "id_rol" : integer,
        # "clave" : string,
        # "correo" : string,
        # "numero" : integer,
        # "compania" : string,
        # "pais" : string}
        
        #Retorna un diccionario de la siguiente forma, 
        #---si no hay errores
        # {'Error': 'Sin errores, id del elemento insertado adjunto',
        # 'id': 'id_del_usuario'}
        #---Con error
        # {'Error': 'Error!'}

        retorno = ""
        Data = dict(data)
        nombre = Data['nombre']
        apellido = Data['apellido']
        DPI = Data['DPI']
        direccion = Data['direccion']
        id_rol = Data['id_rol']
        clave = Data['clave']
        correo = Data['correo']
        numero = Data['numero']
        compania = Data['compania']
        pais = Data['pais']
           
        sql = (f"CALL pa_new_user('{nombre}', '{apellido}', {DPI}"\
            f",'{direccion}', {id_rol}, '{clave}', '{correo}', {numero}"\
                f",'{compania}', '{pais}',@resultado);")
                
        retorno = maria.insertar( sql )
        return retorno
    
    def read_grup(self,data=None):
        #Puede recibir un valor entero, que es el id_user, o nada
        #Si recibe un id_ devuelve el registro de ese id
        #si no recibe nada, devuelve todos los registros de rol_grupo
        
        #devuelve de la siguiente forma {{'error':'error o sin_error'},{'res':una_lista_de_diccionario}}
        #Si en ambos casos no encontraron registros, en 'res' es igual a 'No hay registros que mostrar

        retorno = {"error":"error"}
        res = {}
        if data == None:
            sql = 'SELECT * FROM v_users_rol_group'
            res = maria.obtener( sql )
        else:
            sql = f"SELECT * FROM v_users_rol_group WHERE id_user = {data};"
            res = maria.obtener(sql)
        if len(res['filas']) == 0:
            retorno['error'] = 'sin_errores'
            retorno['res'] = 'No hay registros que mostrar'
        else:
            labels = ['id_user',
                      'nombre',
                      'apellido',
                      'DPI',
                      'direccion',
                      'id_rol',
                      'clave',
                      'nombre_grupo',
                      'correo',
                      'numero',
                      'compania']
            retorno['res']=maria.rotular (res['filas'],labels)

        return retorno
    
    def read_permiso_sup(self,data=None):
        #Puede recibir un valor entero, que es el id_user, o nada
        #Si recibe un id_ devuelve el registro de ese id
        #si no recibe nada, devuelve todos los registros de rol_grupo
        
        #devuelve de la siguiente forma {{'error':'error o sin_error'},{'res':una_lista_de_diccionario}}
        #Si en ambos casos no encontraron registros, en 'res' es igual a 'No hay registros que mostrar

        retorno = {"error":"error"}
        res = {}
        if data == None:
            sql = 'SELECT * FROM v_users_rol_sup'
            res = maria.obtener( sql )
        else:
            sql = f"SELECT * FROM v_users_rol_sup WHERE id_user = {data};"
            res = maria.obtener(sql)
        if len(res['filas']) == 0:
            retorno['error'] = 'sin_errores'
            retorno['res'] = 'No hay registros que mostrar'
        else:
            labels = ['id_user',
                      'nombre',
                      'apellido',
                      'DPI',
                      'direccion',
                      'id_rol',
                      'clave',
                      'nombre_grupo',
                      'correo',
                      'numero',
                      'compania']
            retorno['res']=maria.rotular (res['filas'],labels)

        return retorno
    
    def read_all_user(self,data=None):
        #Puede recibir un valor entero, que es el id_user, o nada
        #Si recibe un id_ devuelve el registro de ese id
        #si no recibe nada, devuelve todos los registros de rol_grupo
        
        #devuelve de la siguiente forma {{'error':'error o sin_error'},{'res':una_lista_de_diccionario}}
        #Si en ambos casos no encontraron registros, en 'res' es igual a 'No hay registros que mostrar

        retorno = {"error":"error"}
        res = {}
        if data == None:
            sql = 'SELECT * FROM v_all_users'
            res = maria.obtener( sql )
        else:
            sql = f"SELECT * FROM v_all_users WHERE id_user = {data};"
            res = maria.obtener(sql)
        if len(res['filas']) == 0:
            retorno['error'] = 'sin_errores'
            retorno['res'] = 'No hay registros que mostrar'
        else:
            labels = ['id_user',
                      'nombre',
                      'apellido',
                      'DPI',
                      'direccion',
                      'id_rol',
                      'clave',
                      'nombre_rol',
                      'correo',
                      'numero',
                      'compania']
        
            retorno['res']=maria.rotular (res['filas'],labels)

        return retorno
             


# Documentacion Libreria mySql

# Metodos:
# query (sql)
#     Parametros
#     sql = consulta a la base de datos

#     Retorno
#     0 en caso de fallo
#     1 en caso de error

# obtener (sql)
#     Parametros
#     sql = consulta a la base de datos (solamente consultas select)

#     Retorno
#     arreglo (array) de registros
#     arreglo vacio en caso de error


# insertar (sql)
#     Parametros
#     sql = consulta a la base de datos (solamente consultas INSERT INTO)

#     Retorno
#     numero entero positivo con el ID del último registro creado

# rotular (resultado, etiquetas)
#     Parametros
#     1. resultado = un resultado devuelto de obtener
#     2. etiquetas = un arreglo (array) con los nombres de cada uno de los campos del resultado

#     Retorno
#     arreglo (array) de registros tipo lista con llave=>valor 

#     Ejemplo:
#     datos = maria.obtener("SELECT nombre, apellido, edad FROM usuario")
#     resultado = maria.rotular(datos, ['Nombre', 'Apellido', 'Edad'])

#     Nota: 
#     Datos regresara algo como Esto
#         [
#             ['Jesus', 'Laynes', 42],
#             ['Mario', 'Cabrera', 18],
#             ['Willy', 'Morales', 23]
#         ]

#     Y resultado tendría algo asi
#         [
#             {'Nombre':'Jesus', 'Apellido':'Laynes', 'Edad':42},
#             {'Nombre':'Mario', 'Apellido':'Cabrera', 'Edad':18},
#             {'Nombre':'Willy', 'Apellido':'Morales', 'Edad':23}
#         ]

#     Resultado tiene un formato mas cómodo de trabajar ya que podrá usarse de la siguiente manera
#       Primer Registro
#         resultado[0].Nombre    
#         resultado[0].Apellido  
#         resultado[0].Edad

#       Segundo registro
#         resultado[1].Nombre
#         resultado[1].Apellido
#         resultado[1].Edad