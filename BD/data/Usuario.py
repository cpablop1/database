
#from mySql import mySql
from data.mySql import mySql


maria = mySql() #objeto global de la base de datos 

class Usuario:
    #SOBRE LA LECTURA DE DATOS read_grup(), read_permiso_sup() o read_all_user
    """
    Estos metodos pueden recibir nada, o dos parametros, el primero un string (NOMBRE DEL CAMPO),
    con culquiera de los campos para cada metodo, el segundo parametro es el VALUE
    
    read_grup        = lectura de usuarios con rol de grupo
    read_permiso_sup = lectura de usuarios con rol singular
    read_all_user    = lee todos los usuarios sin importar su rol

    --si no recibe nada, devuelve todos los registros existentes
    --si recibe un string(nombre_Campo), y valor, devuelve las coincidencias con ese campo y valor
    --si no se hayan resgistros en la clave 'res' se adjunta 'No hay registros que mostrar  o en el'
    
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
    
    def read_grup(self,**kwargs):
        #campos aceptados ['id_user', 'nombre', 'apellido','DPI', 'direccion',
        #               'id_rol', 'clave', 'nombre_grupo', 'correo', 'numero', 'compania']
        
        labels = ['id_user', 'nombre', 'apellido', 'DPI', 'direccion',
                  'id_rol', 'clave', 'nombre_grupo', 'correo', 'numero', 'compania']
        vista = "v_users_rol_group"
        retorno = maria.select_vista(vista,labels,**kwargs)
        return retorno
    
    def read_permiso_sup(self,**kwargs):
        """campos aceptados ['id_user', 'nombre', 'apellido', 'DPI', 'direccion',
                         'id_rol', 'clave', 'nombre_sup_user', 'correo', 'numero', 'compania']   """
        
        labels = ['id_user', 'nombre', 'apellido', 'DPI', 'direccion',
                  'id_rol', 'clave', 'nombre_sup_user', 'correo', 'numero', 'compania']
        vista = "v_users_rol_sup"
        retorno = maria.select_vista(vista,labels,**kwargs)
        return retorno
    
    def read_all_user(self,**kwargs):
        """campos aceptados ['id_user', 'nombre', 'apellido', 'DPI', 'direccion', 'id_rol',
                          'clave', 'nombre_rol', 'correo', 'numero', 'compania']"""
        
        labels = ['id_user', 'nombre', 'apellido', 'DPI', 'direccion', 'id_rol',
                  'clave', 'nombre_rol', 'correo', 'numero', 'compania']
        vista = "v_all_users"
        retorno = maria.select_vista(vista,labels,**kwargs) 
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