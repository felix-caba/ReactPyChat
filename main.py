from reactpy import component, html, use_effect
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
from chatComponent import Aplicacion
import uvicorn
import webview
import threading
import ChatClient


app = FastAPI()


def run_server():
    uvicorn.run(app, host="127.0.0.1", port=2511)



if __name__ == "__main__":

    # Inicia el servidor en un hilo separado

    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Crea y muestra la ventana de la aplicación
    configure(app, Aplicacion)
    webview.create_window("PyChat Server (Admin)", "http://127.0.0.1:2511")
    #webview.settings(width=800, height=600, resizable=False)
    webview.start()


