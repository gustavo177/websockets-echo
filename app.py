import asyncio
import http
import signal

import websockets

# Lista de conexiones
connections = set()

async def echo(websocket):
    # Agregar la nueva conexión a la lista
    connections.add(websocket)
    # print("****************")
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
            # print("inicio 1")
            connections.remove(websocket)
            await websocket.close()
            # print("fin 1")


            # # se resta -1 para darle espacio al siguiente cliente
            # numero_usuario_conectados=numero_usuario_conectados
    else:
        
        # print("******************************")
        # print(numero_usuario_conectados)
        # print("*******************************")

        # print("Se ha alcanzado el límite máximo de clientes")
        # Eliminar la conexión de la lista
        connections.remove(websocket)
        await websocket.close()


async def health_check(path, request_headers):
    if path == "/healthz":
        return http.HTTPStatus.OK, [], b"OK\n"


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        echo,
        host="",
        port=8080,
        process_request=health_check,
    ):
        await stop


if __name__ == "__main__":
    asyncio.run(main())