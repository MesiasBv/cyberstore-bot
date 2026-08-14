import os
import logging
import mysql.connector
from neonize.client import NewClient

# Rutas locales
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_SESION = os.path.join(RUTA_BASE, "sesion_bot.sqlite3")

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')

# Conexión directa a tu XAMPP local para la prueba
def verificar_grupo_local(chat_id):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sistema_ventas" # Cambia esto si tu BD local tiene otro nombre
        )
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bot_grupos_autorizados WHERE grupo_id = %s", (chat_id,))
        resultado = cursor.fetchone()
        cursor.close()
        db.close()
        return resultado is not None
    except Exception as e:
        print(f"Error conectando a la BD local: {e}")
        return False

client = NewClient(ARCHIVO_SESION)

@client.event
def on_message(client_instance: NewClient, message):
    print("🔥 ¡EVENTO RECIBIDO DE WHATSAPP! 🔥")
    try:
        chat = message.info.chat
        grupo_id = f"{chat.user}@{chat.server}"
        print(f"📩 Grupo ID: {grupo_id}")

        # Validar texto del mensaje
        texto = ""
        if hasattr(message.message, 'conversation') and message.message.conversation:
            texto = message.message.conversation
        elif hasattr(message.message, 'extendedTextMessage') and message.message.extendedTextMessage:
            texto = message.message.extendedTextMessage.text
        
        print(f"💬 Texto: '{texto}'")

        if texto.strip().lower() == "/ping":
            # Si quieres probar sin validar la BD primero para ver si responde rápido, 
            # puedes comentar la línea de abajo. Si ya tienes el grupo en tu BD local, déjala.
            if verificar_grupo_local(grupo_id):
                client_instance.send_message(chat, "🤖 ¡Pong! CyberStore local activo.")
                print("✅ ¡Respondido /ping con éxito!")
            else:
                print(f"❌ Este grupo ({grupo_id}) no está registrado en tu tabla bot_grupos_autorizados local.")

    except Exception as e:
        print(f"⚠️ Error procesando mensaje: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando bot en entorno local...")
    client.connect()
