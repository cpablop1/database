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
        
    def obtener(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
        except:
            data=[]
        return data

    def query(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return 1
        except:
            return 0

    def insertar(self, sql):
        good = self.query(sql)
        respuesta = ""
        if good == 1:
            respuesta = self.query("SELECT @resultado")
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


