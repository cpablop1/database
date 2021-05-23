import pymysql #conexion a myslq y MariaDb 

class mySql:
    conn=0
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host='localhost',
                user='root',
                password='admin',
                db='aula',
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
        if good == 1:
            res = self.query('SELECT LAST_INSERT_ID()')
            good = res[0][0]
        
    def rotular(self, res, label):
        retorno=[]
        for x in res:
            fila = {}
            i = 0
            for c in x:
                fila[ label[i] ] = c
                i = i + 1
            retorno.append(fila)
        return retorno


intento = Usuario.insertar('Willy',7445654,'asdfsdf')
if intento == True:
    levantar_alerta()
else:
    levantar_error()
    
