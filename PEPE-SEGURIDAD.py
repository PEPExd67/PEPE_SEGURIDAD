import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# ==========================================
# 1. SERVIDOR WEB (PARA MANTENER RENDER VIVO)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "✅ SISTEMA KUSANAGI ONLINE"

def run():
    # Render usa el puerto 8080 por defecto
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ==========================================
# 2. CONFIGURACIÓN DEL BOT
# ==========================================

# --- AGREGA TU TOKEN AQUÍ ---
# Si prefieres seguridad total, usa: TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = 'MTUwMTQ1OTY0ODQ2Nzk2Mzk0NA.G3kEgC.r3-Y5wXFU8C9LiiwsoxvAIJmfnuWDL7e3DQplU' 

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'>>> SISTEMA BLINDADO ONLINE: {bot.user.name}')

# --- COMANDO DE SEGURIDAD ---
@bot.command(name="Seguridad")
@commands.is_owner() 
async def activar_seguridad(ctx):
    """Solo Pepe puede activar este protocolo"""
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
            # Crea el rol si no existe
            role = await interaction.guild.create_role(name="Verificado", color=discord.Color.green())
        
        await interaction.user.add_roles(role)
        await interaction.response.send_message("✅ Has sido verificado por el sistema de Pepe.", ephemeral=True)

    button.callback = verify_callback
    view.add_item(button)
    await ctx.send(embed=embed, view=view)

@activar_seguridad.error
async def seguridad_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("🚫 **ERROR DE SEGURIDAD:** Solo el dueño del bot tiene acceso a este comando.", delete_after=10)

# ==========================================
# 3. EJECUCIÓN DEL SISTEMA
# ==========================================
if __name__ == "__main__":
    print("Iniciando servidor de mantenimiento...")
    keep_alive()  # Lanza Flask en un hilo separado
    print("Conectando con Discord...")
    bot.run(TOKEN)
