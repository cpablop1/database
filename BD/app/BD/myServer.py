from http.server import BaseHTTPRequestHandler 
import json
 
class Server(BaseHTTPRequestHandler):
    metodo=""
    def _set_headers(self):
        self.send_response(200)
        if self.metodo == "post":
            self.send_header("Content-type", "application/json")
            # self.send_header("Access-Control-Allow-Origin", "http://localhost")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "*")
            
        else:
            self.send_header("Content-type", "text/html")
            # self.send_header("Access-Control-Allow-Origin", "http://localhost")
            self.send_header("Access-Control-Allow-Origin", "*")
            
        self.end_headers()

    def do_GET(self):
        self.metodo="get"
        self._set_headers()
        cliente = '''class Py{ constructor(url, port)
                { this.url = url; this.port=port; }
                llamar(op, ret){ fetch("http://localhost:8080", 
                {  headers: {  "Accept": "application/json",  "Content-Type": "application/json"  },  method: "POST",  body: JSON.stringify({drv: "Usuario", fnd: "hacer"}) }) .then(resp=>resp.json()) .then(data=>ret(data)) }}'''
                
        test = ''''
<h1>Tester</h1>
    <p> Controlador: <input type="text" id="drv" placeholder="clase py"> </p>
    <p> Funcion: <input type="text" id="fnd" placeholder="funcion de clase py"> </p>
    <button onclick="llamar()">Consultar</button>
    <div id="resultado"> </div>
    <script> '+ cliente +' function llamar(){
        const driver = document.getElementById(`drv`).value;
        const funcion = document.getElementById(`fnd`).value;
        const py = new Py(`localhost`, `8080`);
        op = { drv:driver, fnd:funcion };
        py.llamar(op, data=>{
            if(data.error != ``) alert(data.error);
            else { console.log(data);
                document.getElementById(`resultado`).innerHTML = JSON.stringify(data);
                }
            }); }
            </script>
'''

        self.wfile.write(bytes(test, "utf-8"))

    def do_POST(self):
        self.metodo="post"
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 

        print(post_data)

        data = json.loads(post_data)
        
        mod=__import__ (data['drv'], data['drv'])
        klass = getattr(mod, data['drv'])
        #klass = Seguridad()
                
        retorno=eval('klass.'+ data['fnd'] +'(data)')
        #retorno = klass.crearRol(data)

        self._set_headers()
        self.wfile.write(bytes(json.dumps(retorno), "utf-8")) 
