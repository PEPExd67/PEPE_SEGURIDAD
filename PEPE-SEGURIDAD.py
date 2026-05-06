import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# ==========================================
# 1. SERVIDOR DE MANTENIMIENTO (ANTI-SUSPENSIÓN)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "✅ SISTEMA DE SEGURIDAD KUSANAGI ONLINE"

def run():
    # Usamos el puerto 8080 para que Render lo reconozca de inmediato
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# ==========================================
# 2. CONFIGURACIÓN DEL BOT
# ==========================================
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Kusanagi Security 🛡️"))
    print(f'>>> [LOG] SEGURIDAD ACTIVADA: {bot.user.name}')

@bot.command(name="Seguridad")
@commands.is_owner() 
async def activar_seguridad(ctx):
    embed = discord.Embed(
        title="⛩️ PROTOCOLO DE SEGURIDAD KUSANAGI",
        description=f"### 👋 Saludos, {ctx.author.name}\nIdentidad confirmada. El botón de acceso está listo.",
        color=0x00ff00
    )
    
    view = discord.ui.View(timeout=None)
    button = discord.ui.Button(label="VERIFICARSE", style=discord.ButtonStyle.green, custom_id="verify_pepe_global")
    
    async def verify_callback(interaction):
        role = discord.utils.get(interaction.guild.roles, name="Verificado")
        if not role:
            role = await interaction.guild.create_role(name="Verificado", color=discord.Color.green())
        
        if role in interaction.user.roles:
            await interaction.response.send_message("⚠️ Ya estás verificado.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Verificación completada.", ephemeral=True)

    button.callback = verify_callback
    view.add_item(button)
    await ctx.send(embed=embed, view=view)

if __name__ == "__main__":
    if TOKEN:
        keep_alive() 
        bot.run(TOKEN)
