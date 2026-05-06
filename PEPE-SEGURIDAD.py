import discord
from discord.ext import commands
import os

# --- CONFIGURACIÓN CRÍTICA ---
TOKEN = 'MTUwMTQ1OTY0ODQ2Nzk2Mzk0NA.G3kEgC.r3-Y5wXFU8C9LiiwsoxvAIJmfnuWDL7e3DQplU'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'>>> SISTEMA BLINDADO ONLINE: {bot.user.name}')
    # El bot detectará automáticamente que tú eres el dueño legal del token
    await bot.application_info() 

# --- CAPA DE SEGURIDAD ABSOLUTA ---
@bot.command(name="Seguridad")
@commands.is_owner() # <--- CLAVE: Solo tú (Pepe) puedes ejecutar esto
async def activar_seguridad(ctx):
    """Despliega el panel de seguridad que solo el dueño puede iniciar"""
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
        # Crea el rol si no existe y lo asigna al usuario que presione el botón
        role = discord.utils.get(interaction.guild.roles, name="Verificado")
        if not role:
            role = await interaction.guild.create_role(name="Verificado", color=discord.Color.green())
        
        await interaction.user.add_roles(role)
        await interaction.response.send_message("✅ Has sido verificado por el sistema de Pepe.", ephemeral=True)

    button.callback = verify_callback
    view.add_item(button)
    await ctx.send(embed=embed, view=view)

# Manejo de error si alguien más intenta usarlo
@activar_seguridad.error
async def seguridad_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("🚫 **ERROR DE SEGURIDAD:** Solo el dueño del bot tiene acceso a este comando.", delete_after=10)

bot.run(TOKEN)