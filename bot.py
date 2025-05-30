import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from datetime import datetime

# تحميل المتغيرات البيئية
load_dotenv()

# إعداد البوت مع كافة الصلاحيات
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# معرف قناة التسجيل (ستحتاج لتغييره لاحقاً)
LOG_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID', 0))

@bot.event
async def on_ready():
    print('============================')
    print(f'تم تسجيل الدخول كـ {bot.user}')
    print(f'معرف البوت: {bot.user.id}')
    print(f'عدد السيرفرات: {len(bot.guilds)}')
    print('قائمة السيرفرات:')
    for guild in bot.guilds:
        print(f'- {guild.name} (ID: {guild.id})')
    print('============================')
    
    # التحقق من قناة السجلات
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        print(f'تم العثور على قناة السجلات: {log_channel.name}')
        try:
            await log_channel.send('✅ تم تشغيل البوت بنجاح!')
        except discord.errors.Forbidden:
            print('❌ لا يمكن للبوت الكتابة في قناة السجلات')
    else:
        print('❌ لم يتم العثور على قناة السجلات')

    # تسجيل الأوامر
    try:
        synced = await bot.tree.sync()
        print(f'تم تسجيل {len(synced)} من الأوامر')
    except Exception as e:
        print(f'حدث خطأ في تسجيل الأوامر: {e}')

# أمر لعرض معلومات القناة
@bot.tree.command(name="channel-info", description="عرض معلومات عن القناة الحالية")
async def channel_info(interaction: discord.Interaction):
    channel = interaction.channel
    embed = discord.Embed(
        title=f"معلومات القناة: {channel.name}",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="المعرف", value=channel.id, inline=True)
    embed.add_field(name="النوع", value=str(channel.type), inline=True)
    embed.add_field(name="تاريخ الإنشاء", value=channel.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    await interaction.response.send_message(embed=embed)

# أمر لعرض إحصائيات السيرفر
@bot.tree.command(name="server-stats", description="عرض إحصائيات السيرفر")
async def server_stats(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(
        title=f"إحصائيات سيرفر {guild.name}",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="عدد الأعضاء", value=guild.member_count, inline=True)
    embed.add_field(name="تاريخ الإنشاء", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="عدد القنوات", value=len(guild.channels), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await interaction.response.send_message(embed=embed)

# أمر لتغيير قناة السجلات
@bot.tree.command(name="set-log-channel", description="تعيين قناة السجلات")
@app_commands.checks.has_permissions(administrator=True)
async def set_log_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    global LOG_CHANNEL_ID
    LOG_CHANNEL_ID = channel.id
    embed = discord.Embed(
        title="✅ تم تعيين قناة السجلات",
        description=f"تم تعيين {channel.mention} كقناة للسجلات",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    await interaction.response.send_message(embed=embed)

# تسجيل حذف الرسائل
@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="✂️ تم حذف رسالة",
            description=f"تم حذف رسالة من {message.author.mention} في {message.channel.mention}",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="محتوى الرسالة", value=message.content or "لا يوجد محتوى", inline=False)
        await log_channel.send(embed=embed)

# تسجيل تعديل الرسائل
@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    
    if before.content == after.content:
        return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="📝 تم تعديل رسالة",
            description=f"تم تعديل رسالة من {before.author.mention} في {before.channel.mention}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="قبل التعديل", value=before.content, inline=False)
        embed.add_field(name="بعد التعديل", value=after.content, inline=False)
        await log_channel.send(embed=embed)

# تسجيل انضمام الأعضاء
@bot.event
async def on_member_join(member):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="👋 عضو جديد",
            description=f"{member.mention} انضم إلى السيرفر",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="تاريخ إنشاء الحساب", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        await log_channel.send(embed=embed)

# تسجيل مغادرة الأعضاء
@bot.event
async def on_member_remove(member):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="👋 مغادرة عضو",
            description=f"{member.mention} غادر السيرفر",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await log_channel.send(embed=embed)

# تسجيل نشاط القنوات الصوتية
@bot.event
async def on_voice_state_update(member, before, after):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        if before.channel != after.channel:
            if after.channel:
                embed = discord.Embed(
                    title="🎤 دخول قناة صوتية",
                    description=f"{member.mention} دخل إلى {after.channel.name}",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
            else:
                embed = discord.Embed(
                    title="🎤 خروج من قناة صوتية",
                    description=f"{member.mention} خرج من {before.channel.name}",
                    color=discord.Color.red(),
                    timestamp=datetime.utcnow()
                )
            await log_channel.send(embed=embed)

# تشغيل البوت
try:
    token = os.getenv('TOKEN')
    if not token:
        raise ValueError("لم يتم العثور على توكن البوت. تأكد من وجود ملف .env وتعبئته بشكل صحيح")
    
    channel_id = os.getenv('LOG_CHANNEL_ID')
    if not channel_id:
        raise ValueError("لم يتم العثور على معرف قناة السجلات. تأكد من وجود LOG_CHANNEL_ID في ملف .env")
    
    # التحقق من أن معرف القناة رقم صحيح
    try:
        LOG_CHANNEL_ID = int(channel_id)
    except ValueError:
        raise ValueError(f"معرف القناة غير صالح: {channel_id}. يجب أن يكون رقماً")

    print("جاري تشغيل البوت...")
    bot.run(token)
except Exception as e:
    print(f"حدث خطأ: {str(e)}")
