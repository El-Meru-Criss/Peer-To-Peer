

<center> 

  <H1> SISTEMA PEER TO PEER DE MENSAJERIA</H1>
    Esto es un proyecto sobre servidores peer to peer de mensajeria(tipo chat).
    Este cuenta con un menu principal con 2 funciones:
    <H2>OPCION 0</H2>
    Al colocar la opción 0 se ejecuta la busqueda de los servidores en un rango de Ips y en un rango de puertos.

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

  <H2>OPCION 1</H2>
    la función 1 es para realizar la conexión con los otros servidores(nodo), ingresando la Ip y el puerto del servidor deseado previamente encontrado con la función 0.

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

</center>
