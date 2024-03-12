import socket
import threading
import time

def handle_client(client_socket, client_address):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"El cliente {client_address} se ha desconectado de forma inesperada.")
                break
            message = data.decode('utf-8')
            print(f"Mensaje recibido de {client_address}: {message}")

            if message.lower() == "--co":
                continue

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

def is_client_connected(client_socket):
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

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message.encode('utf-8'))

def start_server():
    HOST = '192.168.2.135'
    PORT = 9997

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

def connect_to_server():
    while True:
        try:
            HOST = input("Ip:")
            PORT = int(input("Puerto:"))

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            break  # Si la conexión tiene éxito, salimos del bucle y continuamos con el flujo normal
        except socket.gaierror:
            print("La dirección IP no es válida o no se puede alcanzar. Inténtelo de nuevo.")
        except TimeoutError:
            print("El puerto no está disponible o la conexión se ha agotado. Inténtelo de nuevo.")

    ExisCleinte = True
    ExisCleinte2 = False

    try:
        while True:
            message = input("Ingrese un mensaje: ")
            if message.lower() == "--ch":
                while True:
                    try:
                        HOST = input("Ip:")
                        PORT = int(input("Puerto:"))

                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client.connect((HOST, PORT))
                        break  # Si la conexión tiene éxito, salimos del bucle y continuamos con el flujo normal
                    except socket.gaierror:
                        print("La dirección IP no es válida o no se puede alcanzar. Inténtelo de nuevo.")
                    except TimeoutError:
                        print("El puerto no está disponible o la conexión se ha agotado. Inténtelo de nuevo.")
                ExisCleinte = True

            if message.lower() == "--co":
                while True:
                    try:
                        HOST = input("Ip:")
                        PORT = int(input("Puerto:"))

                        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client2.connect((HOST, PORT))
                        break  # Si la conexión tiene éxito, salimos del bucle y continuamos con el flujo normal
                    except socket.gaierror:
                        print("La dirección IP no es válida o no se puede alcanzar. Inténtelo de nuevo.")
                    except TimeoutError:
                        print("El puerto no está disponible o la conexión se ha agotado. Inténtelo de nuevo.")
                ExisCleinte2 = True

            if message.lower() == "--ex":
                break

            if ExisCleinte == True:
                try:
                    client.send(message.encode('utf-8'))
                except ConnectionResetError:
                    print("La conexión fue restablecida por el host remoto.")
                    client.close
                    ExisCleinte = False
                    
                except ConnectionAbortedError:
                    print("La conexión fue abortada.")
                    client.close
                    ExisCleinte = False

            if ExisCleinte2 == True:
                try:
                    client2.send(message.encode('utf-8'))
                except ConnectionResetError:
                    print("La conexión fue restablecida por el host remoto.")
                    client2.close
                    ExisCleinte2 = False
                except ConnectionAbortedError:
                    print("La conexión fue abortada.")
                    client2.close
                    ExisCleinte2 = False

            time.sleep(2)  # Espera antes de enviar el próximo mensaje

    finally:
        # Cerrar la conexión del cliente
        client.close()
        
def detect_servers():
    start_ip = '192.168.2.'
    start_port = 9990
    end_port = 10005

    active_servers = []

    for i in range(135, 159):  # Supongamos que quieres generar direcciones IP del 192.168.100.10 al 192.168.100.19
        ip = start_ip + str(i)
        for port in range(start_port, end_port + 1):
            server_address = (ip, port)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            result = s.connect_ex(server_address)
            if result == 0:
                active_servers.append(server_address)
            s.close()

    return active_servers


def main():
    choice = 0

    while choice != 1:
        print("Presione 1 para conectarse. 0 para buscar")
        choice = input("Ingrese su elección: ")

        if choice == "1":
            connect_to_server()
        elif choice == "0":
            print("Buscando servidores peer-to-peer activos en la red local...")
            active_servers = detect_servers()

            if active_servers:
                print("Servidores activos encontrados:")
                for server in active_servers:
                    print(f"- {server[0]}:{server[1]}")

            else:
                print("No se encontraron servidores activos en la red local.")

        else:
            print("Opción no válida. Saliendo del programa.")

if __name__ == "__main__":
    clients = []

    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    main()