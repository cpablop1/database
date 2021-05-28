#from mySql import mySql
from data.mySql import mySql
maria = mySql()
    
class Contacto():
    """Esta es la clase para quienes desean contactarnos,
    no es para proveedores/clientes"""
    def create(self,data):
        #recibe un diccionario de la siguiente forma
        # {"nombre" : string,
        # "num_telefono" : integer,
        # "correo" : string,
        # "mensaje": string}
        
        #Retorna un diccionario de la siguiente forma, 
        #---si no hay errores
        # {'Error': 'Sin errores, id adjunto',
        # 'id': 'id_customer'}
        #---Con error
        # {'Error': 'Error!'}
            
        retorno = ""
        Data = dict(data)
        nombre = Data['nombre']
        num_telefono = Data['num_telefono']
        correo = Data['correo']
        mensaje = Data['mensaje']

        sql = f"CALL pa_new_contact('{nombre}',{num_telefono},'{correo}','{mensaje}',@resultado);"
        retorno = maria.insertar( sql )
        return retorno
    
    def read(self,option='no_atendido',id_user=None):
        #Pueden leerso todos lo no atendidos, se ase por defecto
        #o todos los atendidos, para lo que se tiene que pasar un string = 'atendido'
        #o pueden leerse los atendidos por un usuario, pasando un string = 'atendido', y un id_user = INT,
        #           obteniendo solo los registros que ese usuario atendio
        
        #devuelve de la siguiente forma {{'error':'error o sin_error'},{'res':una_lista_de_diccionario}}
        #Si en ambos casos no encontraron registros, en 'res' es igual a 'No hay registros que mostrar      
        #pudiendo recorerse de la siguiente forma
        #no atendidos dict contiene nombre_cliente, num_telefono_cliente, correo_cliente, mensaje_cliente
        #atendidos dict contiene nombre_cliente, num_telefono_cliente, correo_cliente, mensaje_cliente, nombre_user_atendio, apellido_user_atendio

        
        def no_atendido():
            retorno = {"error":"error"}
            res = {}
            sql = 'SELECT * FROM v_contactanos_no;'
            res = maria.obtener( sql )

            if len(res['filas']) == 0:
                retorno['error'] = 'sin_errores'
                retorno['res'] = 'No hay registros que mostrar'
            else:
                labels = ['nombre_cliente',
                          'num_telefono_cliente',
                          'correo_cliente',
                          'mensaje_cliente']
                retorno['res']=maria.rotular (res['filas'], labels)
            return retorno
        
        def atendido(id_user):
            retorno = {"error":"error"}
            res = {}
            if id_user == None:
                sql = 'SELECT * FROM v_contactanos_si;'
                res = maria.obtener( sql )
            else:
                sql = f"SELECT * FROM v_contactanos_si WHERE id_user = {id_user};"
                res = maria.obtener( sql )

            if len(res['filas']) == 0:
                retorno['error'] = 'sin_errores'
                retorno['res'] = 'No hay registros que mostrar'
            else:
                labels = ['nombre',
                          'num_telefono',
                          'correo',
                          'mensaje',
                          'user_name',
                          'user_apellido',
                          'id_user_atendio']
                retorno['res']=maria.rotular (res['filas'], labels)
            return retorno
        
        if option == 'no_atendido':
            retorno = no_atendido()
        else:
            retorno = atendido(id_user)
            
        return retorno
    