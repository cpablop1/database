
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

class Cuenta_bancaria():
    #SOBRE LA LECTURA DE DATOS read_prov()
    """
    Estos metodos pueden recibir nada, o dos parametros, el primero un string (NOMBRE DEL CAMPO),
    con cualquiera de los campos para cada metodo, el segundo parametro es el VALUE

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
    
    def create(self,data):

        """ MUCHO CUIDADO CON METER Fondo negativo, 
        o numeros de cuenta iguales, da error en la base,
        devuelve comprobacion en 'id'
                
        #recibe un diccionario de la siguiente forma
        {"num_cuenta":integer,
        "nombre_banco" : string,
        "nombre_cuenta" : string,
        "fondo" : float}
 
       
        
        #Retorna un diccionario de la siguiente forma, 
        #---si no hay errores, o errore en datos dectados en la BD
        # {'Error': 'Sin errores, id del elemento insertado adjunto',
        # 'id': 'id_del_prov'}
        
        posibles valores para 'id'
        1- "Numero de cuenta, ya existente";    (dato no insertado)
        2- "Fondo, no puede ser negativo";      (dato no insertado)
        2-  num_cuenta;                         (dato insertado)
        
        #---Con error interno
        # {'Error': 'Error!'}
        
        
        """
        

        labels = ['num_cuenta','nombre_banco','nombre_cuenta','fondo']
        
        procedure = 'pa_new_cuenta_bancaria'
        sql = sql_builder(procedure,labels,data)
        retorno = maria.insertar( sql )
        return retorno
    
    def read(self,**kwargs):
        """  campos aceptados 
        ['num_cuenta', 'nombre_banco', 'nombre_cuenta',
         'fecha_creacion', 'fondo', 'estado ',]
        """
        labels = ['num_cuenta', 'nombre_banco', 'nombre_cuenta',
                  'fecha_creacion', 'fondo', 'estado ',]
        
        vista = "v_proveedor"
        retorno = maria.select_vista(vista,labels,**kwargs)
        return retorno
    
    def read(self,**kwargs):
        #campos aceptados ['nit','nombre_empresa', 'prov_name', 'prov_lastname',
        #          'direccion', 'correo', 'numero', 'compania', 'pais']
        
        labels = ['nit','nombre_empresa', 'prov_name', 'prov_lastname',
                  'direccion', 'estado', 'correo', 'numero', 'compania']
        vista = "v_proveedor"
        retorno = maria.select_vista(vista,labels,**kwargs)
        return retorno

"""
    pa_new_chequera

    IN num_chequera INT,
    IN num_cuenta BIGINT(16),
    IN num_cheque_dispo INT,
    
    SET res_var := num_chequera;
    SET res_var := "Numero de chequera, ya existente";
    SET res_var := "Numero de cuenta, no existente";
    
"""

"""
    pa_resgistrar_deposito
    
    IN no_deposito INT,
    IN monto DECIMAL(15, 2),
    IN num_cuenta BIGINT(16),
    
    SET resultado := 'Cuenta no existente';
    SET resultado := 'Monto invalido';
    SET resultado := CONCAT('Nol. ',no_deposito,' YA existente');
    SET resultado := CONCAT('Deposito ',no_deposito,' registrado');
"""