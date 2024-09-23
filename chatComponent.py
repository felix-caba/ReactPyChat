from reactpy import component, html, use_state, use_effect
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
import uvicorn
import webview
import threading
import ChatClient as AsyncChatClient
import asyncio




# Create Client Thread


client = AsyncChatClient.AsyncChatClient("172.28.255.7", 5000)

@component
def Aplicacion():
    messages, set_messages = use_state([])
    input_message, set_input_message = use_state("")
    connection_status, set_connection_status = use_state("Conectando...")

    async def handle_send_message(): # funcion asincrona, para enviar mensajes al servidor sin que se pare la app
        if input_message.strip():
            await client.enviar_mensaje(input_message) # se espera este hiilo a que el mensaje sea enviado
            set_messages(lambda m: m + [f"Yo: {input_message}"]) 

            # POR QUE USO LAMBDA? 

            # SEGUN REACTPY, EL ESTADO DE ESTE COMPONENTE SIN LAMBDA (USANDO MESSAGES, NO SE ACTUALIZA, SE USA DIRECTAMENTE)
            #SI USAS LA LAMBDA, EN EL MOMENTO DE ACTUALIZAR EL ESTADO SE EJECUTA LA FUNCION QUE COGE M que es la lista

            # se agrega el mensaje al chat. a message se le suman todos los mensajes anteriores (lambda)
            # m es el estado actual de los mensajes, y se le agrega el mensaje que se acaba de enviar
            set_input_message("")

    def handle_input_change(event):
        set_input_message(event['target']['value'])

    def handle_key_press(event):
        if event['key'] == 'Enter':
            asyncio.create_task(handle_send_message()) # se crea un hilo para enviar el mensaje async

    @use_effect
    async def setup_connection(): #se hace setup de la conexion al user effect, osea, al iniciar el cliente
        await client.connect() # espera a la conexion pa seguir
        if client.sock:
            set_connection_status("Conectado")
            while True:
                message = await client.recibir_mensaje()
                if message:
                    set_messages(lambda m: m + [message])

        else:
            set_connection_status("Error de conexión")


    return html.div(
        html.h1("PyChat"),
        html.p(connection_status),
        html.div(
            [html.p(message) for message in messages]
        ),
        html.input({
            "type": "text", 
            "value": input_message, 
            "onChange": handle_input_change, 
            "onKeyPress": handle_key_press
        }),
        html.button({"onClick": lambda event: asyncio.create_task(handle_send_message())}, "Enviar")
    )

