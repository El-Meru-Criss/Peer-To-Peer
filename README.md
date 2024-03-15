

<center> 

  <H1> TUTORIAL PA SUBIR COSAS A ESTE GIT</H1>
  <ol>
    <li>El admin debe añadirlo como colaborador</li>
    <li>debe solicitar su propio Token de Acceso al admin</li>
    <li>reconfigure su URL de push usando el Token y la direccion del repositorio, de la siguiente forma:</li>
  </ol>
  <br>
  git remote set-url origin https://<b>-Tu Id De Token Personal-</b>@github.com/<b>-La URL de tu repositorio en GIT-</b>

</center>

def connect_to_server():
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
