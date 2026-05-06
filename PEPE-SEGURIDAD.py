import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# ==========================================
# 1. SERVIDOR DE MANTENIMIENTO (KEEP-ALIVE)
# ==========================================
# Render requiere una respuesta HTTP para mantener el servicio activo.
app = Flask('')

@app.route('/')
def home():
    return "✅ SISTEMA DE SEGURIDAD KUSANAGI ESTÁ OPERATIVO"

def run():
    # Render usa el puerto 8080 por defecto para servicios web.
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# ==========================================
# 2. CONFIGURACIÓN DEL BOT DE SEGURIDAD
# ==========================================

# Extrae el Token de forma segura desde las Variables de Entorno de Render.
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Estado visual para confirmar que el bot está blindado.
    await bot.change_presence(activity=discord.Game(name="Kusanagi Security 🛡️"))
    print(f'>>> [LOG] SISTEMA BLINDADO ONLINE: {bot.user.name}')

# --- COMANDO DE SEGURIDAD ---
@bot.command(name="Seguridad")
@commands.is_owner() 
async def activar_seguridad(ctx):
    """Protocolo Kusanagi: Crea un botón de verificación permanente."""
    embed = discord.Embed(
        title="⛩️ PROTOCOLO DE SEGURIDAD KUSANAGI",
        description=(
            f"### 👋 Saludos, {ctx.author.name}\n"
            "Tu identidad como **Dueño** ha sido confirmada.\n\n"
            "El botón de abajo otorgará el rol de acceso a los usuarios que lo soliciten."
        ),
        color=0x00ff00
    )
    
    # Creamos una vista persistente para el botón
    view = discord.ui.View(timeout=None)
    button = discord.ui.Button(
        label="VERIFICARSE", 
        style=discord.ButtonStyle.green, 
        custom_id="verify_pepe_global"
    )
    
    async def verify_callback(interaction):
        # Busca el rol 'Verificado' en el servidor
        role = discord.utils.get(interaction.guild.roles, name="Verificado")
        
        if not role:
            # Si el rol no existe, el bot lo crea automáticamente
            role = await interaction.guild.create_role(
                name="Verificado", 
                color=discord.Color.green(),
                reason="Auto-creación del Protocolo de Seguridad"
            )
        
        if role in interaction.user.roles:
            await interaction.response.send_message("⚠️ El acceso ya ha sido concedido anteriormente.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Has sido verificado por el sistema de Pepe. ¡Bienvenido!", ephemeral=True)

    button.callback = verify_callback
    view.add_item(button)
    await ctx.send(embed=embed, view=view)

@activar_seguridad.error
async def seguridad_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("🚫 **ACCESO DENEGADO:** Este panel de control es exclusivo de Pepe.", delete_after=10)

# ==========================================
# 3. LANZAMIENTO
# ==========================================
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR CRÍTICO: No se encontró 'DISCORD_TOKEN' en la pestaña Environment de Render.")
    else:
        # Iniciamos Flask primero para que Render vea actividad inmediata
        keep_alive() 
        print(">>> [LOG] Iniciando conexión blindada...")
        try:
            bot.run(TOKEN)
        except Exception as e:
            print(f"❌ ERROR AL INICIAR: {e}")
