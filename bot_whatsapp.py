import os
import logging
from neonize.client import NewClient

# Configuración básica de rutas locales
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_SESION = os.path.join(RUTA_BASE, "sesion_bot.sqlite3")

logging.basicConfig(level=logging.INFO)

client = NewClient(ARCHIVO_SESION)

@client.event
def on_message(client_instance: NewClient, message):
    # Esto imprimirá ABSOLUTAMENTE TODO lo que pase por el chat (textos, audios, multimedia)
    print(f"🔥 ¡EVENTO DETECTADO EN VIVO! 🔥")
    print(message)

if __name__ == "__main__":
    print("🚀 Iniciando bot en modo ultra-simple...")
    client.connect()