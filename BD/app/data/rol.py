from BD.app.data.mySql import mySql
import json
maria = mySql()

# JSON to Python -> x = json.loads(var1)
# Python to JSON -> y = json.dumps(var2)

class Rol_grupo():
    def nuevo(self,data):
        #recibe un objeto json de la siguiente forma
        # ({'nombre' : 'Name',
        # 'monto_min' : number,
        # 'monto_max' number})
        # retorna un mensaje '1' si todo esta bien, o '' si ocurrio un error
        
        #El grupo 1 es de pagos, y el resto es de autoridad que validaran cheques, 
        #Mysql empieza las llaves autoincrementeas por 1
        #Solo el nivel 1, tiene True en generar cheque, y validar_cheque = 0
        #los rol_group con id_group > 1, serán lo contrario al grupo 1
        
        #-- CALL pa_new_group_rol('Rychy group',45.3,800.50,@resultado);
        retorno = ""
        Data = dict(json.loads(data))
        nombre = Data['nombre']
        monto_min = Data['monto_min']
        monto_max = Data['monto_max']

        sql = f"CALL pa_new_group_rol('{nombre}',{monto_min},{monto_max},@resultado)"
        retorno = maria.insertar( sql )
        return retorno
        #IGNORENSE TODAS LAS LINEAS HASTA LA 42, pero no las borren jsjsj
        #data = {"nombre": "User1", "monto_min": 43.45,"monto_max":452.41}
        #data = json.dumps(data)
        #rol_grupo.nuevo(data)
    
    #from rol import Rol_grupo
    #import json
    #data = {"nombre": "User1", "monto_min": 43.45,"monto_max":452.41}
    #data = json.dumps(data)
    #rol_grupo = Rol_grupo()
    #rol_grupo.nuevo(data)
    
    def hacer(self,data): #no funcional aun
        retorno = {"error":""}
        sql = 'SELECT * FROM urol'
        res = maria.obtener( sql )

        if len(res) == 0:
            retorno['error'] = 'NO hay registros que mostrar'
        else:
            retorno['res']=maria.rotular (res, ['Contenido_id', 'Leccion_id', 'Nombre', 'Direccion', 'tipo', 'primeracceso', 'ultimoacceso'])

        return retorno
    def listar(self,data): #No funcional aun
        return {"error":"Esto es [ LISTAR ] usuarios"}