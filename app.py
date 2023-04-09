import asyncio
import websockets

# Lista de conexiones
connections = set()

async def handler(websocket, path):
    # Agregar la nueva conexión a la lista
    connections.add(websocket)
    print("****************")
    # Conecciones actuales
    # print(connections)

    # typo de dato (class 'set')
    # print(type(connections))

    # Numero de usuario conectados
    numero_usuario_conectados = len(connections)
    print(numero_usuario_conectados)

    # # Convertir el set en una lista
    mi_lista = list(connections)

    # Acceder al primer elemento de la lista (primer valor del set)
    # set_lista = mi_lista[0]
    # ruta_cliente_py= str(set_lista)
    # print(ruta_cliente_py)
    # print(type(ruta_cliente_py))


    # Permitir la conexión solo para los primeros dos clientes
    if numero_usuario_conectados <= 2: 
        try:
            # Recibir y enviar mensajes a los clientes conectados
            async for message in websocket:
                for connection in connections:

                    # si deja de resivir mensaje en menos de 10 segundos cierra sección
                    await asyncio.wait_for(connection.send(message), timeout=10)
        finally:
            # Eliminar la conexión de la lista
            print("inicio 1")
            connections.remove(websocket)
            await websocket.close()
            print("fin 1")


            # # se resta -1 para darle espacio al siguiente cliente
            # numero_usuario_conectados=numero_usuario_conectados
    else:
        
        print("******************************")
        print(numero_usuario_conectados)
        print("*******************************")

        print("Se ha alcanzado el límite máximo de clientes")
        # Eliminar la conexión de la lista
        connections.remove(websocket)
        await websocket.close()
        

# Iniciar el servidor websockets
start_server = websockets.serve(handler, "localhost", 8001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()