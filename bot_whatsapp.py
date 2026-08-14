import os
import threading
from flask import Flask
import mysql.connector
from neonize.client import NewClient

# 1. Servidor web falso para que Render detecte un puerto abierto
app = Flask(__name__)

@app.route("/")
def home():
    return "CyberStore Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# 2. Tu código del Bot de WhatsApp
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_SESION = os.path.join(RUTA_BASE, "sesion_bot.sqlite3")

client = NewClient(ARCHIVO_SESION)

@client.event
def on_message(client_instance: NewClient, message):
    print("🔥 ¡EVENTO RECIBIDO DE WHATSAPP! 🔥")
    try:
        chat = message.info.chat
        texto = ""
        if hasattr(message.message, 'conversation') and message.message.conversation:
            texto = message.message.conversation
        
        if texto.strip().lower() == "/ping":
            client_instance.send_message(chat, "🤖 ¡Pong! CyberStore en la nube activo.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Arrancar Flask en un hilo secundario para que Render abra el puerto
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    print("🚀 Iniciando bot de WhatsApp en Render...")
    client.connect()
