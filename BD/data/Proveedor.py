#metodos para crear proveedores

#from mySql import mySql
from data.mySql import mySql


maria = mySql() #objeto global de la base de datos 
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

class Proveedor:
    #SOBRE LA LECTURA DE DATOS read_prov()
    """
    Estos metodos pueden recibir nada, o dos parametros, el primero un string (NOMBRE DEL CAMPO),
    con culquiera de los campos para cada metodo, el segundo parametro es el VALUE

    --si no recibe nada, devuelve todos los registros existentes
    --si recibe un nombre_Campo, y valor, devuelve las coincidencias con ese campo y valor
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
        """ MUCHO CUIDADO CON METER correos o telefonos iguales, da error en la base,
        devuelve comprobacion igual que usuario
        nit INT,
        
        #recibe un diccionario de la siguiente forma
        {"nit":number,
        "nombre_empresa" : string,
        "prov_name" : string,
        "prov_lastname" : string,
        "direccion" : string,
        "correo" : string,
        "numero" : integer,
        "compania" : string,
        "pais" : string}
 
        #Retorna un diccionario de la siguiente forma, 
        #---si no hay errores
        # {'Error': 'Sin errores, id del elemento insertado adjunto',
        # 'id': 'id_del_prov'}
        #---Con error
        # {'Error': 'Error!'}
        """
        retorno = ""
        labels = ['nit','nombre_empresa', 'prov_name', 'prov_lastname',
                  'direccion', 'correo', 'numero', 'compania', 'pais']
        procedure = 'pa_new_proveedor'
        sql = sql_builder(procedure,labels,data)
        retorno = maria.insertar( sql )
        return retorno
    
    def read(self,**kwargs):
        #campos aceptados ['nit','nombre_empresa', 'prov_name', 'prov_lastname',
        #          'direccion', 'correo', 'numero', 'compania', 'pais']
        
        labels = ['nit','nombre_empresa', 'prov_name', 'prov_lastname',
                  'direccion', 'estado', 'correo', 'numero', 'compania']
        vista = "v_proveedor"
        retorno = maria.select_vista(vista,labels,**kwargs)
        return retorno