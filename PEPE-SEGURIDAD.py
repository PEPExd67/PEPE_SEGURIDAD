import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# ==========================================
# 1. SERVIDOR DE MANTENIMIENTO (KEEP-ALIVE)
# ==========================================
# Render requiere un servidor web activo para no suspender el servicio gratuito.
app = Flask('')

@app.route('/')
def home():
    return "✅ SISTEMA KUSANAGI ONLINE"

def run():
    # Render asigna puertos automáticamente, pero el 8080 es el estándar
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True # Esto asegura que el hilo muera si el bot se detiene
    t.start()

# ==========================================
# 2. CONFIGURACIÓN DEL BOT
# ==========================================

# El Token se lee desde la pestaña 'Environment' de Render
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Cambiamos el estado del bot para que se vea más profesional
    await bot.change_presence(activity=discord.Game(name="Kusanagi Security 🛡️"))
    print(f'>>> SISTEMA BLINDADO ONLINE: {bot.user.name}')

# --- COMANDO DE SEGURIDAD ---
@bot.command(name="Seguridad")
@commands.is_owner() 
async def activar_seguridad(ctx):
    """Protocolo de verificación: Solo accesible por el dueño"""
    embed = discord.Embed(
        title="⛩️ PROTOCOLO DE SEGURIDAD KUSANAGI",
        description=(
            f"### 👋 ¡Hola {ctx.author.name}!\n"
            "Identidad verificada como **Dueño**. El panel de acceso está listo para los usuarios."
        ),
        color=0x00ff00
    )
    
    view = discord.ui.View(timeout=None)
    button = discord.ui.Button(
        label="VERIFICARSE", 
        style=discord.ButtonStyle.green, 
        custom_id="verify_pepe_v2"
    )
    
    async def verify_callback(interaction):
        role = discord.utils.get(interaction.guild.roles, name="Verificado")
        if not role:
            # Crea el rol automáticamente si no existe
            role = await interaction.guild.create_role(
                name="Verificado", 
                color=discord.Color.green(),
                reason="Auto-creación por comando de seguridad"
            )
        
        if role in interaction.user.roles:
            await interaction.response.send_message("⚠️ Ya cuentas con el acceso verificado.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Has sido verificado por el sistema de Pepe.", ephemeral=True)

    button.callback = verify_callback
    view.add_item(button)
    await ctx.send(embed=embed, view=view)

@activar_seguridad.error
async def seguridad_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("🚫 **ACCESO DENEGADO:** Este comando es exclusivo del creador.", delete_after=10)

# ==========================================
# 3. LANZAMIENTO DEL SISTEMA
# ==========================================
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR CRÍTICO: No se encontró la variable DISCORD_TOKEN en Render.")
    else:
        print("Iniciando servidor Flask...")
        keep_alive() 
        print("Conectando con la infraestructura de Discord...")
        bot.run(TOKEN)
