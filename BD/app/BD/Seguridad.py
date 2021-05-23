from mySql import mySql #Importamos la libreria para usar la base de datos
maria = mySql() #objeto global de la base de datos 

class Seguridad:  #Driver de seguridad
    def validarCheque(self, data):
        retorno = {"error":""}
        retorno["saludo"] = "Estamos validando el cheque " + data['cheque_id']
        return retorno ## esto le llega a Willy

    def usuarioRol(data):
        retorno = {"error":""}
        res = maria.obtener("SELECT * FROM urol")
        if len(res) == 0:
            retorno['error'] = 'No existen resultados.'
        else:
            retorno['registros'] = maria.rotular(res, ['rol', 'id','credencial','Nombre', 'Apellido'])
        return retorno ## esto le llega a Willy

    def crearRol(data):
        retorno = {"error":""}
        form = data["formulario"]
        sql = "INSERT INTO usuario (nombre, apellido) VALUES ('"+ form['nombre'] +"','"+ form['apellido'] +"')"
        sepudo = maria.insertar(sql)
        if sepudo==0:
            retorno["error"] = "No se pudo crear el registro"
        else:
            retorno["usuario_id"] = sepudo
        return retorno



