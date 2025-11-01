from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# INFORMACIÓN DEL CREADOR - AGREGA TU NOMBRE AQUÍ
CREATOR_INFO = {
    "nombre": "MSc. Aldo Zeas Castro",  # ⬅️ REEMPLAZA CON TU NOMBRE
    "version": "1.0",
    "fecha_creacion": "2025"
}

# Datos expandidos del bot
PERSONAJES = {
    "sandino": {
        "nombre": "Augusto C. Sandino",
        "vida": "1895-1934",
        "descripcion": "Líder guerrillero que encabezó la resistencia contra la ocupación estadounidense (1927-1933). Símbolo de soberanía nacional.",
        "cita": "Yo no vendo mi patria ni el honor de mi pueblo."
    },
    "ruben_dario": {
        "nombre": "Rubén Darío",
        "vida": "1867-1916", 
        "descripcion": "Poeta, periodista y diplomático. Padre del Modernismo literario en español.",
        "cita": "Juventud, divino tesoro, ¡ya te vas para no volver!"
    },
    "jose_dolores_estrada": {
        "nombre": "José Dolores Estrada",
        "vida": "1792-1869",
        "descripcion": "Héroe nacional de la Batalla de San Jacinto durante la Guerra Nacional contra William Walker.",
        "cita": "¡A la carga, muchachos!"
    }
}

QUIZZES = [
    {
        "pregunta": "¿En qué año se proclamó la independencia de Centroamérica?",
        "opciones": ["A) 1810", "B) 1821", "C) 1838"],
        "respuesta": "B"
    },
    {
        "pregunta": "¿Quién fundó las ciudades de Granada y León?",
        "opciones": ["A) Cristóbal Colón", "B) Francisco Hernández de Córdoba", "C) William Walker"],
        "respuesta": "B"
    },
    {
        "pregunta": "¿Qué poeta nicaragüense es considerado padre del Modernismo?",
        "opciones": ["A) Pablo Antonio Cuadra", "B) Rubén Darío", "C) Ernesto Cardenal"],
        "respuesta": "B"
    }
]

# Teclados (menús) - Agregamos botón de créditos
def main_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton("📜 Línea de Tiempo"), KeyboardButton("👤 Personajes")],
        [KeyboardButton("🧠 Quiz Histórico"), KeyboardButton("📖 Fuentes")],
        [KeyboardButton("👨‍💻 Créditos"), KeyboardButton("❓ Ayuda")]
    ], resize_keyboard=True)

def personajes_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton("Augusto Sandino"), KeyboardButton("Rubén Darío")],
        [KeyboardButton("José Dolores Estrada"), KeyboardButton("🔙 Menú Principal")]
    ], resize_keyboard=True)

# /start - Ahora incluye información del creador
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        f"🇳🇮 *¡Bienvenido a HistoriBot Nicaragua!* 🤖\n\n"
        f"Soy tu guía interactiva de historia nicaragüense. "
        f"¡Explora nuestra rica historia de forma fácil y divertida!\n\n"
        f"*¿Qué te gustaría conocer hoy?*\n\n"
        f"_Creado por {CREATOR_INFO['nombre']}_ ✨"
    )
    await update.message.reply_text(
        welcome_text, 
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# NUEVO COMANDO: /creditos - Muestra información del creador
async def creditos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    creditos_text = (
        f"👨‍💻 *Créditos y Información*\n\n"
        f"🤖 *HistoriBot Nicaragua*\n"
        f"📚 Bot educativo sobre historia nicaragüense\n\n"
        f"*Desarrollado por:* {CREATOR_INFO['nombre']}\n"
        f"*Versión:* {CREATOR_INFO['version']}\n"
        f"*Fecha de creación:* {CREATOR_INFO['fecha_creacion']}\n\n"
        f"¡Gracias por usar este bot educativo! 🇳🇮"
    )
    await update.message.reply_text(
        creditos_text,
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# /ayuda - Actualizado
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📚 *¿Cómo usar HistoriBot?*\n\n"
        "¡Es muy fácil! Solo usa los botones del menú:\n\n"
        "• *📜 Línea de Tiempo*: Historia por periodos\n"
        "• *👤 Personajes*: Biografías ilustres\n"
        "• *🧠 Quiz Histórico*: Pon a prueba tus conocimientos\n"
        "• *📖 Fuentes*: Documentos y citas históricas\n"
        "• *👨‍💻 Créditos*: Información del creador\n\n"
        "También puedes escribir preguntas libres.\n\n"
        f"_Bot desarrollado por {CREATOR_INFO['nombre']}_"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# Manejar mensajes de botones - Agregamos manejo de "Créditos"
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    
    if user_choice == "📜 Línea de Tiempo":
        await linea_tiempo_interactive(update, context)
    elif user_choice == "👤 Personajes":
        await update.message.reply_text(
            "👥 *Personajes Históricos*\n\nSelecciona un personage:",
            reply_markup=personajes_menu(),
            parse_mode="Markdown"
        )
    elif user_choice == "🧠 Quiz Histórico":
        await actividad_interactive(update, context)
    elif user_choice == "📖 Fuentes":
        await fuente_interactive(update, context)
    elif user_choice == "👨‍💻 Créditos":  # NUEVO BOTÓN
        await creditos(update, context)
    elif user_choice == "❓ Ayuda":
        await ayuda(update, context)
    elif user_choice == "🔙 Menú Principal":
        await start(update, context)
    elif user_choice in ["Augusto Sandino", "Rubén Darío", "José Dolores Estrada"]:
        await mostrar_personaje(update, context, user_choice)
    else:
        await handle_general_question(update, context)

# El resto del código se mantiene igual...
async def linea_tiempo_interactive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    eventos = [
        "🟢 *Época Precolombina (hasta 1502)*\nPueblos originarios: Nicaraos, Chorotegas, Matagalpas",
        "🔵 *Conquista y Colonia (1502-1821)*\n1524: Fundación de Granada y León",
        "🟡 *Independencia (1821-1850)*\n1821: Independencia de Centroamérica",
        "🔴 *Siglo XIX (1850-1900)*\n1856: Guerra Nacional contra William Walker",
        "🟣 *Siglo XX (1900-2000)*\n1979: Triunfo de la Revolución Sandinista"
    ]
    
    texto = "🕰️ *Línea de Tiempo de Nicaragua*\n\n" + "\n\n".join(eventos)
    await update.message.reply_text(
        texto, 
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

async def actividad_interactive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quiz = random.choice(QUIZZES)
    
    quiz_keyboard = ReplyKeyboardMarkup([
        [KeyboardButton("A"), KeyboardButton("B"), KeyboardButton("C")],
        [KeyboardButton("🔙 Menú Principal")]
    ], resize_keyboard=True)
    
    texto = (
        f"🧠 *Quiz Histórico*\n\n"
        f"{quiz['pregunta']}\n\n"
        f"{chr(10).join(quiz['opciones'])}"
    )
    
    context.user_data['quiz_respuesta'] = quiz['respuesta']
    context.user_data['quiz_activo'] = True
    
    await update.message.reply_text(
        texto, 
        reply_markup=quiz_keyboard,
        parse_mode="Markdown"
    )

async def mostrar_personaje(update: Update, context: ContextTypes.DEFAULT_TYPE, nombre: str):
    if "Sandino" in nombre:
        key = "sandino"
    elif "Darío" in nombre:
        key = "ruben_dario"
    elif "Estrada" in nombre:
        key = "jose_dolores_estrada"
    else:
        key = "sandino"
    
    p = PERSONAJES[key]
    
    texto = (
        f"👤 *{p['nombre']}* ({p['vida']})\n\n"
        f"{p['descripcion']}\n\n"
        f"*Cita célebre:* \"{p['cita']}\""
    )
    
    await update.message.reply_text(
        texto,
        reply_markup=personajes_menu(),
        parse_mode="Markdown"
    )

async def fuente_interactive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fuentes = [
        "📜 *Acta de Independencia* (1821)\n\"La independencia del gobierno español...\"",
        "📖 *Rubén Darío*\n\"Si pequeña es la Patria, uno grande la sueña.\"",
        "⚔️ *Augusto C. Sandino*\n\"Yo no vendo mi patria ni el honor de mi pueblo.\"",
        "🎯 *Carlos Fonseca*\n\"Y también enséñenles a leer sobre la gloria y el honor de Nicaragua.\""
    ]
    
    await update.message.reply_text(
        random.choice(fuentes),
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

async def handle_quiz_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('quiz_activo'):
        respuesta_usuario = update.message.text.upper().strip()
        respuesta_correcta = context.user_data.get('quiz_respuesta')
        
        if respuesta_usuario == respuesta_correcta:
            mensaje = "✅ *¡Correcto!* ¡Excelente conocimiento histórico! 🎉"
        elif respuesta_usuario in ['A', 'B', 'C']:
            mensaje = f"❌ *Incorrecto*. La respuesta correcta era {respuesta_correcta}."
        else:
            mensaje = "Por favor selecciona A, B o C usando los botones."
            
        context.user_data['quiz_activo'] = False
        await update.message.reply_text(
            mensaje,
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
    else:
        await handle_general_question(update, context)

async def handle_general_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pregunta = update.message.text.lower()
    
    if any(palabra in pregunta for palabra in ["hola", "hi", "hello", "buenas"]):
        await start(update, context)
    elif "gracias" in pregunta:
        await update.message.reply_text(
            f"¡De nada! ¿En qué más puedo ayudarte? 😊\n\n_— {CREATOR_INFO['nombre']}_",
            reply_markup=main_menu()
        )
    elif any(palabra in pregunta for palabra in ["quien te creo", "creador", "desarrollador"]):
        await creditos(update, context)
    else:
        await update.message.reply_text(
            "🤔 Interesante pregunta. Por ahora puedo ayudarte mejor con los menús temáticos.\n\n"
            "¿Qué te gustaría explorar?",
            reply_markup=main_menu()
        )

# Inicializar la aplicación
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Comandos básicos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("creditos", creditos))  # NUEVO COMANDO
    
    # Manejar mensajes de texto (selecciones de menú)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))
    
    print(f"🤖 HistoriBot Nicaragua v{CREATOR_INFO['version']} está en marcha...")
    print(f"👨‍💻 Desarrollado por: {CREATOR_INFO['nombre']}")
    app.run_polling()

if __name__ == "__main__":
    main()