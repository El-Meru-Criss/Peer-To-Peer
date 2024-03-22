import socket #Importa las funciones del socket
import threading #Importa las funciones de los hilos/tareas para la comunicacion de los participantes
import time #Importa la funcion que se utiliza para la latencia

def handle_client(client_socket, client_address): #Esto sirve para la mensajeria y el uso de comandos internos
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"El cliente {client_address} se ha desconectado de forma inesperada.") # Mensaje de desconexión
                break
            message = data.decode('utf-8')

            if message.lower() == "--co":
                continue
            elif message.lower() == "--name":
                client_socket.send("Criss".encode('utf-8'))  # Envía el nombre del servidor al cliente
                continue

            
            print(f"Mensaje recibido de {client_address}: {message}")

            broadcast(message, client_socket)

    except ConnectionResetError:
        print(f"El cliente {client_address} se ha desconectado.")
    except Exception as e:
        print(f"Error al manejar cliente {client_address}: {e}")

    finally:
        # Cerrar el socket y eliminarlo de la lista de clientes
        try:
            clients.remove(client_socket)
            client_socket.close()
        except ValueError:
            pass  # Si el socket no está en la lista, no hacer nada

def is_client_connected(client_socket): #Esto sirve para saber si los clientes siguen conectados
    try:
        # Envía un mensaje de latido al cliente y espera una respuesta
        client_socket.send("--hb".encode('utf-8'))
        client_socket.settimeout(5)  # Espera 5 segundos para recibir la respuesta de latido
        response = client_socket.recv(1024)
        if response.decode('utf-8') == "--hb":
            return True
        else:
            return False
    except socket.timeout:
        return False

def broadcast(message, sender_socket):# Difunde los mensajes
    for client in clients:
        if client != sender_socket:
            client.send(message.encode('utf-8'))

def start_server(): #Inicia el servidor
    HOST = '192.168.2.121' # Se utiliza la ip del dispositivo
    PORT = 9999 # Se utiliza el puerto escrito

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Servidor escuchando en {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        print(f"Conexión establecida desde {client_address}")
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

def connect_to_server(): #Conecta los servidores
    clients = []  # Lista para almacenar los sockets de los clientes
    error_clients = set()  # Conjunto para registrar los clientes que causaron un error

    while True:
        try:
            HOST = input("Ip:")
            port_input = input("Puerto:")
            if not port_input.isdigit():
                print("El puerto debe ser un número entero.")
                continue
            PORT = int(port_input)

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            clients.append(client)  # Agregar el socket del cliente a la lista
        except (socket.gaierror, TimeoutError, ValueError) as e:
            print(f"No se pudo conectar al servidor: {e}")
            continue  # Intentar la conexión nuevamente

        try:
            while True:
                message = input("Ingrese un mensaje: ")

                # Comprobar si el mensaje es un comando especial
                if message.lower() == "--ex":
                    break  # Salir del bucle si el usuario quiere salir
                elif message.lower() == "--ch":
                    try:
                        HOST = input("Ip:")
                        port_input = input("Puerto:")
                        if not port_input.isdigit():
                            print("El puerto debe ser un número entero.")
                            continue
                        PORT = int(port_input)

                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client.connect((HOST, PORT))
                        clients.append(client)  # Agregar el socket del cliente a la lista
                    except (socket.gaierror, TimeoutError, ValueError) as e:
                        print(f"No se pudo conectar al servidor: {e}")
                        continue  # Intentar la conexión nuevamente

                # Enviar el mensaje a todos los clientes en la lista
                for client_socket in clients:
                    try:
                        client_socket.send(message.encode('utf-8'))
                    except Exception as e:
                        # Verificar si el cliente ya ha causado un error antes
                        if client_socket not in error_clients:
                            error_clients.add(client_socket)
                            print(f"Error al enviar el mensaje a {client_socket.getpeername()}: {e}")

                time.sleep(2)  # Esperar antes de enviar el próximo mensaje
            
        except KeyboardInterrupt:
            break  # Salir del bucle si se presiona Ctrl+C

    # Cerrar todas las conexiones de los clientes
    for client_socket in clients:
        client_socket.close()
        
def detect_servers(): # Función para detectar en un rango de servidores
    start_ip = '192.168.2.' #Ip inicial para la detección
    start_port = 9990 #Puerto inicial para la detección
    end_port = 10005 #Puerto final para la detección

    active_servers = []

    for i in range(121, 160): # Rango del ultimo tramo de las Ips
        ip = start_ip + str(i)
        for port in range(start_port, end_port + 1):
            server_address = (ip, port)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            result = s.connect_ex(server_address)
            if result == 0:
                # Establecer conexión exitosa, ahora intenta obtener el nombre del servidor
                # Solicitar el nombre del servidor
                s.send("--name".encode('utf-8'))
                # Recibir el nombre del servidor
                
                try:
                    name = s.recv(1024).decode('utf-8')
                except socket.timeout:
                    name = "Anonimo"
                active_servers.append((ip, port, name))  # Agregar dirección IP, puerto y nombre a la lista
            s.close()

    return active_servers



def main(): #Menu principal
    choice = 0

    while choice != 1: #ciclo para la elección de funciones
        print("Presione 1 para conectarse. 0 para buscar")
        choice = input("Ingrese su elección: ")

        if choice == "1":
            connect_to_server() #Ejecuta la conexión del servidor
        elif choice == "0":
            print("Buscando servidores peer-to-peer activos en la red local...")
            active_servers = detect_servers() #Ejecuta la detección de los servidores

            if active_servers:
                print("Servidores activos encontrados:")
                for server in active_servers:
                    print(f"{server[2]} - {server[0]}:{server[1]}")

            else:
                print("No se encontraron servidores activos en la red local.")

        else:
            print("Opción no válida. Saliendo del programa.")

if __name__ == "__main__":
    clients = []

    server_thread = threading.Thread(target=start_server) #esto ayuda a la ejecución del servidor en segundo plano
    server_thread.start() #esto ayuda a la ejecución del servidor en segundo plano

    main()
