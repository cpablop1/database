import pymysql

class mySql():
    conn=0
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host='localhost',
                port = 3306,
                user='adminman',
                password='hi!',
                db='ourData',
                charset='utf8mb4'
            )
        except:
            print ("ERROR:!! No fue posible acceder al a Base de datos!!!")

    def query(self, sql):
        data = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            cursor.execute('SELECT @resultado;')
            var = cursor.fetchall()
            data.append(var[0][0])
        except:
            data.append('error')
        return data
    
    def select(self, sql):
        data = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            var = cursor.fetchall()
            data.append(var)
        except:
            data.append('error')
        return data
            
    def insertar(self, sql):
        respuesta = {'error':''}
        good = self.query(sql)
        if good[0] != 'error':
            respuesta['id'] = good[0]
            respuesta['error']='Sin errores, id del elemento insertado adjunto'
        else:
            respuesta['error'] = 'Fallo en la conexion servidor'
        return respuesta

    def obtener(self, sql):
        respuesta = {'error':''}
        good = self.select(sql)
        if good[0] != 'error':
            respuesta['filas'] = good[0]
            respuesta['error']='Sin error, Ejecutado exitosamente'
        else:
            respuesta['error'] = 'Fallo en la conexion al servidor'
        return respuesta
    
    def rotular(self, res, label):
        retorno=[]
        for registro in res:
            fila = {}
            i = 0
            for valor in registro:
                fila[ label[i] ] = valor
                i = i + 1
            retorno.append(fila)
        return retorno


