import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# ==========================================
# 1. SERVIDOR MANTENIMIENTO (FLASK)
# ==========================================
# Esto engaña a Render para que crea que es una web y no apague el bot
app = Flask('')

@app.route('/')
def home():
    return "✅ SISTEMA KUSANAGI ESTÁ OPERATIVO"

def run():
    # Render usa el puerto 8080 por defecto
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# ==========================================
# 2. CONFIGURACIÓN DEL BOT
# ==========================================

# Aquí el código busca la variable que configuraste en Render
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
    embed = discord.Embed(
        title="⛩️ PROTOCOLO DE SEGURIDAD KUSANAGI",
        description=(
            f"### 👋 ¡Hola {ctx.author.name}!\n"
            "Identidad verificada como **Dueño**. El panel de acceso está listo."
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
            await interaction.response.send_message("✅ Verificado por el sistema de Pepe.", ephemeral=True)

    button.callback = verify_callback
    view.add_item(button)
    await ctx.send(embed=embed, view=view)

@activar_seguridad.error
async def seguridad_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("🚫 **ACCESO DENEGADO:** Solo el dueño tiene permisos.", delete_after=10)

# ==========================================
# 3. LANZAMIENTO
# ==========================================
if __name__ == "__main__":
    if TOKEN is None:
        print("❌ ERROR: No se encontró DISCORD_TOKEN en la pestaña Environment de Render.")
    else:
        keep_alive() # Inicia la "web" para Render
        print("Conectando con Discord...")
        bot.run(TOKEN)
