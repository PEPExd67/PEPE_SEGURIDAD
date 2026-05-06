import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# ==========================================
# 1. SERVIDOR WEB (PARA MANTENER RENDER VIVO)
# ==========================================
# Render apaga los proyectos si no detecta una web. Esto lo mantiene activo.
app = Flask('')

@app.route('/')
def home():
    return "✅ SISTEMA KUSANAGI OPERATIVO 24/7"

def run():
    # Render usa el puerto 8080 por defecto para servicios web
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# ==========================================
# 2. CONFIGURACIÓN DEL BOT (SEGURIDAD)
# ==========================================

# Aquí el código busca la variable 'DISCORD_TOKEN' que pusiste en Render
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'>>> SISTEMA BLINDADO ONLINE: {bot.user.name}')

# --- COMANDO DE SEGURIDAD ---
@bot.command(name="Seguridad")
@commands.is_owner() 
async def activar_seguridad(ctx):
    """Protocolo Kusanagi: Solo Pepe puede usarlo"""
    embed = discord.Embed(
        title="⛩️ PROTOCOLO DE SEGURIDAD KUSANAGI",
        description=(
            f"### 👋 ¡Hola {ctx.author.name}!\n"
            "El sistema ha verificado tu identidad como **Dueño del Servidor**.\n\n"
            "El panel de verificación para los usuarios ya está listo abajo."
        ),
        color=0x00ff00
    )
    
    view = discord.ui.View(timeout=None)
    button = discord.ui.Button(label="VERIFICARSE", style=discord.ButtonStyle.green, custom_id="verify_pepe")
    
    async def verify_callback(interaction):
        role = discord.utils.get(interaction.guild.roles, name="Verificado")
        if not role:
            role = await interaction.guild.create_role(name="Verificado", color=discord.Color.green())
        
        if role in interaction.user.roles:
            await interaction.response.send_message("⚠️ Ya estás verificado.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Has sido verificado por el sistema de Pepe.", ephemeral=True)

    button.callback = verify_callback
    view.add_item(button)
    await ctx.send(embed=embed, view=view)

@activar_seguridad.error
async def seguridad_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("🚫 **ERROR DE SEGURIDAD:** Solo el dueño tiene acceso.", delete_after=10)

# ==========================================
# 3. EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: No se encontró la variable DISCORD_TOKEN en Render.")
    else:
        keep_alive()  # Inicia el servidor web
        print("Iniciando conexión con Discord...")
        bot.run(TOKEN)
