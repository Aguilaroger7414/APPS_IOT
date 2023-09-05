from http.server import BaseHTTPRequestHandler, HTTPServer
import json

#Aqui tenemos nuestro valor con el cual inicia nuestro servidor
contador = 20

# Aqui definimos nuestra clase la cual es la encargada de manejar las solicitudes http
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    # Mediante este metodo es por el cual configuramos las respuestas http
    def _set_response(self, content_type=""):
        self.send_response(200)  # Enviamos un código de respuesta 200 (éxito)
        self.send_header("Content-type", content_type)
        self.end_headers()

    # Método para manejar las solicitudes GET
    def do_GET(self):
        self._set_response()  # Configuramos la respuesta
        respuesta = {"valor": contador}  # Creamos un objeto JSON con el valor del contador
        self.wfile.write(json.dumps(respuesta).encode())  # Enviamos la respuesta JSON

    # Método para manejar las solicitudes POST
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])  # Obtenemos la longitud del cuerpo de la solicitud
        post_data = self.rfile.read(content_length)  

        body_json = json.loads(post_data.decode())  

        global contador  # Declaramos la variable contador como global para modificarla

        # Verificamos si la solicitud POST contiene las claves 'action' y 'quantity'
        if 'action' in body_json and 'quantity' in body_json:
            action = body_json['action']  # Obtenemos el valor de 'action'
            quantity = body_json['quantity']  # Obtenemos el valor de 'quantity'

            # Actualizamos el contador según la acción especificada
            if action == 'asc':
                contador += quantity  # Aqui incrementamos el contador
            elif action == 'desc':
                contador -= quantity  # Aqui restamos el contador

            # Creamos una respuesta JSON indicando que el contador se actualizó correctamente
            response_data = json.dumps({"Mensaje": "Contador actualizado", "contador": contador})
            self._set_response("application/json")  # Configuramos la respuesta como JSON
            self.wfile.write(response_data.encode())  # Enviamos la respuesta JSON
        else:
            # Si la solicitud POST no cumple con el formato esperado, enviamos una respuesta de error
            response_data = json.dumps({"error": "solicitud no incorrecta"})
            self._set_response("aplicacion de json")  # Configuramos la respuesta de json
            self.wfile.write(response_data.encode())  # Enviamos respuesta de error

# Con esta funcion ejecutamos el server
def run_server(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=7800):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server iniciado {port}...")  # Con esta linea mandamos un mensaje para saber que nuestro servidor esta corriendo
    httpd.serve_forever()  


if __name__ == "__main__":
    run_server() 
