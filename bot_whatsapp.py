import os
import threading
from flask import Flask
import mysql.connector
from neonize.client import NewClient

app = Flask(__name__)

@app.route("/")
def home():
    return "CyberStore Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_SESION = os.path.join(RUTA_BASE, "sesion_bot.sqlite3")

client = NewClient(ARCHIVO_SESION)

@client.event
def on_message(client_instance: NewClient, message):
    # Imprimir en los logs que CUALQUIER evento de mensaje entró al sistema
    print(f"🔔 EVENTO CAPTURADO: {message}")
    try:
        chat = message.info.chat
        
        texto = ""
        msg_content = message.message
        if msg_content.conversation:
            texto = msg_content.conversation
        elif msg_content.extendedTextMessage and msg_content.extendedTextMessage.text:
            texto = msg_content.extendedTextMessage.text
        
        print(f"💬 Texto extraído: '{texto}'")

        if texto.strip().lower() == "/ping":
            client_instance.send_message(chat, "🤖 ¡Pong! CyberStore en la nube activo.")
            print("✅ ¡Respondido /ping con éxito!")
            
    except Exception as e:
        print(f"⚠️ Error procesando mensaje: {e}")

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    print("🚀 Iniciando cliente de WhatsApp...")
    client.connect()
