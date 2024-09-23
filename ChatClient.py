import asyncio
import socket
from reactpy import component, html, use_state, use_effect
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
import uvicorn

class AsyncChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        self.connected = asyncio.Event()

    async def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            await asyncio.get_event_loop().sock_connect(self.sock, (self.host, self.port)) # espera a la conexion
            self.connected.set()
        except Exception as e:
            print(f"Error de conexión: {e}")
            self.sock = None

    async def enviar_mensaje(self, message):
        if self.sock:
            await asyncio.get_event_loop().sock_sendall(self.sock, message.encode())

    async def recibir_mensaje(self):
        if self.sock:
            return (await asyncio.get_event_loop().sock_recv(self.sock, 1024)).decode()
        return None