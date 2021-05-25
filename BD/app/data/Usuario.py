from BD.app.data.mySql import mySql #Importamos la libreria para usar la base de datos
maria = mySql() #objeto global de la base de datos 

class Usuario:  #Driver de usuarios
    def nuevo(data):
        return {"error":"Esto es [ CREAR ] nuevo usuario"}
    
    def hacer(data): #Funcion o metodo
        retorno = {"error":""}
        sql = 'SELECT * FROM urol'
        res = maria.obtener( sql )

        if len(res) == 0:
            retorno['error'] = 'NO hay registros que mostrar'
        else:
            retorno['res']=maria.rotular (res, ['Contenido_id', 'Leccion_id', 'Nombre', 'Direccion', 'tipo', 'primeracceso', 'ultimoacceso'])

        return retorno #Retorno de la API
    def listar(data):
        return {"error":"Esto es [ LISTAR ] usuarios"}





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