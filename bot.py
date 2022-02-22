import discord
from discord import Embed

from discord import guild

# from discord.ext import bot
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord_components import * # Button, ButtonStyle, Select, SelectOption, DiscordComponents
# from dislash import InteractionClient, ActionRow, Button, ButtonStyle, SelectMenu, SelectOption
# from PIL import Image, ImageFont, ImageDraw

import asyncio
import datetime

from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from asyncio import sleep
import random as rand

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '!', case_insensitive = True, intents = discord.Intents.all())
slash = SlashCommand(bot, sync_commands = True)

users = {}

@bot.event
async def on_ready():
    print('Бот работает!')
    DiscordComponents(bot)
    bot.ready = True
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="GTA V"))
    embed = discord.Embed(description = '**Бот работает!**')
    embed.timestamp = datetime.datetime.utcnow()
    await bot.get_channel(942828703585533984).send(embed = embed)


@bot.event
async def on_user_update(before, after):
    if before.avatar != after.avatar:
        channellog = bot.get_channel(942828703266783339)
        channel = bot.get_channel(942828702440501271)
        embed = discord.Embed(
            title ="Новая аватарка",
            color = discord.Color.from_rgb(65, 121, 78)
            )
        embed.set_author(name = f'{after.name}#{after.discriminator}', icon_url = after.avatar_url)
        embed.set_thumbnail(url = after.avatar_url)
        embed.set_footer(text = 'UnionShop Bot')
        embed.timestamp = datetime.datetime.utcnow()

        embed1 = discord.Embed(
            title = 'Рандомная аватарка',
            color = discord.Color.from_rgb(244, 127, 255)
            )
        embed1.set_image(url = after.avatar_url)
        embed1.set_footer(text = 'UnionShop Bot')
        embed1.timestamp = datetime.datetime.utcnow()

        await channellog.send(embed = embed)
        await channel.send(embed = embed1)
        await asyncio.sleep(300)

    if before.name != after.name:
        channellog = bot.get_channel(942828703266783339)
        embedname = discord.Embed(
            title = "Ник пользователя изменен",
            description = f'**Ник до изменения:** {before.name}\n**Ник после изменения:** {after.name}',
            color = discord.Color.from_rgb(65, 121, 78),
            )
        embedname.timestamp = datetime.datetime.utcnow()
        embedname.set_thumbnail(url = after.avatar_url)
        embedname.set_author(name = f'{after.name}#{after.discriminator}', icon_url = after.avatar_url)
        embedname.set_footer(text = 'UnionShop Bot')
        
        await channellog.send(embed = embedname)

    if before.discriminator != after.discriminator:
        channellog = bot.get_channel(942828703266783339)
        embedtag = Embed(
            title = "Тэг пользователя изменен",
            color = discord.Color.from_rgb(65, 121, 78),
            )
        embedtag.timestamp = datetime.datetime.utcnow()
        embedtag.set_thumbnail(url = after.avatar_url)
        embedtag.add_field(name = 'До изменения', value = before.discriminator, inline = True)
        embedtag.add_field(name = 'После изменения', value = after.discriminator, inline = True)
        embedtag.set_author(name = f'{after.name}#{after.discriminator}', icon_url = after.avatar_url)
        embedtag.set_footer(text = 'UnionShop Bot')
            
        await channellog.send(embed = embedtag)


@bot.event
async def on_member_update(before, after):
        if before.display_name != after.display_name:
            channellog = bot.get_channel(942828703266783339)
            embed = Embed(title = "Ник на сервере изменен",
                          color = discord.Color.from_rgb(65, 121, 78),
                          )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_thumbnail(url = after.avatar_url)
            embed.add_field(name = 'До изменения', value = before.display_name, inline = True)
            embed.add_field(name = 'После изменения', value = after.display_name, inline = True)
            embed.set_author(name = f'{after.name}#{after.discriminator}', icon_url = after.avatar_url)
            embed.set_footer(text = 'UnionShop Bot')

            await channellog.send(embed = embed)

        elif before.roles != after.roles:
            channellog = bot.get_channel(942828703266783339)
            embed1 = Embed(title = "Роль изменена",
                          color = discord.Color.from_rgb(65, 121, 78),
                          )
            embed1.timestamp = datetime.datetime.utcnow()
            embed1.set_thumbnail(url = after.avatar_url)
            embed1.add_field(name = 'До изменения', value = ", ".join([r.mention for r in before.roles]), inline = True)
            embed1.add_field(name = 'После изменения', value = ", ".join([r.mention for r in after.roles]), inline = True)
            embed1.set_author(name = f'{after.name}#{after.discriminator}', icon_url = after.avatar_url)
            embed1.set_footer(text = 'UnionShop Bot')

            await channellog.send(embed = embed1)


@bot.event
async def on_message_edit(before, after):
    kanal = before.channel
    time = after.created_at.strftime('%Y.%m.%d %H:%M:%S')
    embed = discord.Embed(
        title = 'Сообщение было изменено!',
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed.add_field(name = 'Сообщение до изменения:', value = before.content, inline = True)
    embed.add_field(name = 'Сообщение после изменения:', value = after.content, inline = True)
    embed.add_field(name = 'Канал:', value = kanal, inline = False)
    embed.set_footer(text = 'Cообщение отправлено: ' + time)
    channel = bot.get_channel(942828703266783339)
    if before.content == after.content:
        return
    await channel.send(embed = embed)


@bot.event
async def on_message_delete(message):
    kanal = message.channel
    time = message.created_at.strftime('%Y.%m.%d %H:%M:%S')
    embed = discord.Embed(
        title ="Сообщение было удалено!",
        description = f"__Автор:__ {message.author.mention} {message.author}",
        color = discord.Color.from_rgb(255, 0, 0)
        )
    embed.add_field(name = "Содержимое сообщения:", value = message.content)
    embed.add_field(name = 'Канал:', value = message.channel, inline = False)
    embed.set_footer(text = 'Cообщение отправлено: ' + time)
    channel = bot.get_channel(942828703266783339)
    await channel.send(embed = embed)


@bot.command(aliases = ['мут'])
@commands.has_any_role(942828699475132432, 942828699475132429, 942828699475132426)
async def mute(ctx, user: discord.Member = None, time: int = None, *, reason = None): 
    if user is None:
        await ctx.reply('Укажи пользователя, которого хочешь замутить!')
    else:
        if time is None:
            await ctx.reply('Укажи время, на которое хотите замутить пользователя!')
        elif time > 12 or time < 0:
            await ctx.reply('Время должно быть от 1 до 12 часов!')
        else:
            if reason is None:
                await ctx.reply('Укажи причину мута в виде пункта из правил!') 
            else:
                if user.top_role.position >= ctx.author.top_role.position:
                    em0 = discord.Embed(
                        title = 'Ошибка!',
                        description = 'У тебя нет прав!',
                        timestamp = datetime.datetime.utcnow()
                    )
                    em0.set_thumbnail(url = ctx.guild.icon_url)
                    em0.set_footer(text = 'UnionShop Bot')
                    
                    await ctx.reply(embed = em0)
                else:
                    role = user.guild.get_role(942828699244453975)
                    if role in user.roles:
                        em0 = discord.Embed(
                            title = 'Ошибка!',
                            description = 'Пользователь уже замучен!',
                            timestamp = datetime.datetime.utcnow()
                        )
                        em0.set_thumbnail(url = ctx.guild.icon_url)
                        em0.set_footer(text = 'UnionShops Bot')
                        await ctx.reply(embed = em0)
                    else:
                        em = discord.Embed(
                            title = 'Пользователь замучен',
                            description = f'{user.mention} получил мут\nВремя: **{time}** час/а/ов\nПричина: **{reason}**',
                            color = discord.Color.from_rgb(127,255,212)
                        )
                        em.set_footer(text = 'UnionShop Bot')
                        em.timestamp = datetime.datetime.utcnow()
                        
                        await ctx.reply(embed = em) 
                        await user.add_roles(role) 
                        await asyncio.sleep(time)
                        await user.remove_roles(role)
                        embed = discord.Embed(
                            title = 'Время мута истекло!',
                            description = f'{user.mention} пробыл в муте **{time}** часа(ов) по причине: **{reason}**',
                            color = discord.Color.from_rgb(135,206,250)
                        )
                        embed.set_footer(text = 'UnionShop Bot')
                        embed.timestamp = datetime.datetime.utcnow()
                        await ctx.send(embed = embed)


@bot.command(aliases = ['размут'])
@commands.has_any_role(942828699475132432, 942828699475132429, 942828699475132426)
async def unmute(ctx, user: discord.Member = None, *, reason = None): 
    if user is None:
        await ctx.reply('Укажи пользователя, которого хочешь размутить!')
    else:
        if reason is None:
            await ctx.reply('Укажи причину по которой следует размутить пользователя!') 
        else:
            if user.top_role.position >= ctx.author.top_role.position:
                em0 = discord.Embed(
                    title = 'Ошибка!',
                    description = 'У тебя нет прав!',
                    timestamp = datetime.datetime.utcnow()
                )
                em0.set_thumbnail(url = ctx.guild.icon_url)
                em0.set_footer(text = 'UnionShops Bot')
                
                await ctx.reply(embed = em0)
            else:
                role = user.guild.get_role(942828699244453975)
                if role not in user.roles:
                    em0 = discord.Embed(
                        title = 'Ошибка!',
                        description = 'Пользователь не был замучен!',
                        timestamp = datetime.datetime.utcnow()
                    )
                    em0.set_thumbnail(url = ctx.guild.icon_url)
                    em0.set_footer(text = 'UnionShops Bot')
                    await ctx.reply(embed = em0)
                else:
                    role1 = user.guild.get_role(942828699244453975)
                    em = discord.Embed(
                        title = 'Пользователь размучен',
                        description = f'{user.mention} размучен\nПричина: **{reason}**',
                        color = discord.Color.from_rgb(127,255,212)
                    )
                    em.set_footer(text = 'UnionShop Bot')
                    em.timestamp = datetime.datetime.utcnow()
                    
                    await user.remove_roles(role1)
                    await ctx.reply(embed = em)


@slash.slash(
    name = "мут",
    description = "Выдать мут пользователю!",
    guild_ids = [942828699244453968],
    options = [create_option(
        name = 'user',
        description = 'Выберите время мута!',
        required = True,
        option_type = 6,
    ),
        create_option(
        name = 'time',
        description = 'Выберите время мута!',
        required = True,
        option_type = 4,
        choices = [
            create_choice(
                name = '1',
                value = int('1')
            ),
            create_choice(
                name = '2',
                value = int('2')
            ),
            create_choice(
                name = '3',
                value = int('3')
            ),
            create_choice(
                name = '4',
                value = int('4')
            ),
            create_choice(
                name = '5',
                value = int('5')
            ),
            create_choice(
                name = '6',
                value = int('6')
            ),
            create_choice(
                name = '7',
                value = int('7')
            ),
            create_choice(
                name = '8',
                value = int('8')
            ),
            create_choice(
                name = '9',
                value = int('9')
            ),
            create_choice(
                name = '10',
                value = int('10')
            ),
            create_choice(
                name = '11',
                value = int('11')
            ),
            create_choice(
                name = '12',
                value = int('12')
            )
        ]
    ),
    create_option(
        name = 'reason',
        description = 'Напиши причину мута!',
        required = True,
        option_type = 3,
        )
    ]
)
async def mute(ctx: SlashContext, user: str, time: int, *, reason: str):  
    owner = ctx.guild.get_role(942828699475132432)
    admin = ctx.guild.get_role(942828699475132429)
    moder = ctx.guild.get_role(942828699475132426)
    if user is None:
        await ctx.reply('Укажи пользователя, которого хочешь замутить!')
    else:
        if time is None:
            await ctx.reply('Укажи время, на которое хотите замутить пользователя!')
        elif int(time) > 12 or int(time) < 0:
            await ctx.reply('Время должно быть от 1 до 12 часов!')
        else:
            if reason is None:
                await ctx.reply('Укажи причину мута в виде пункта из правил!') 
            else:
                if user.top_role.position >= ctx.author.top_role.position:
                    em0 = discord.Embed(
                        title = 'Ошибка!',
                        description = 'Ты не имеешь права мут пользователю с ролью как у тебя или выше!',
                        timestamp = datetime.datetime.utcnow()
                    )
                    em0.set_footer(text = 'UnionShop Bot')
                    
                    await ctx.reply(embed = em0, hidden = True)
                elif owner or moder not in ctx.author.roles is not None:
                    em1 = discord.Embed(
                        title = 'Ошибка!',
                        description = 'Ты не имеешь права использовать эту команду!',
                        timestamp = datetime.datetime.utcnow()
                    )
                    em1.set_footer(text = 'UnionShop Bot')
                    
                    await ctx.reply(embed = em1, hidden = True)
                    
                else:
                    role = user.guild.get_role(942828699244453975)

                    em = discord.Embed(
                        title = 'Пользователь замучен',
                        description = f'{user.mention} получил мут\nВремя: **{time}** час/а/ов\nПричина: **{reason}**',
                        color = discord.Color.from_rgb(127,255,212)
                    )
                    em.set_footer(text = 'UnionShop Bot')
                    em.timestamp = datetime.datetime.utcnow()
                    
                    await ctx.reply(embed = em) 
                    await user.add_roles(role) 
                    await asyncio.sleep(time)
                    await user.remove_roles(role)
                    embed = discord.Embed(
                        title = 'Время мута истекло!',
                        description = f'{user.mention} пробыл в муте **{time}** часа(ов) по причине: **{reason}**',
                        color = discord.Color.from_rgb(135,206,250)
                    )
                    embed.set_footer(text = 'UnionShop Bot')
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.reply(embed = embed)
                    

@bot.event
async def on_member_join(member):
    embed1 = discord.Embed(
        title = 'Пользователь присоединился',
        description = f'{member.mention} {len(list(member.guild.members))} по счёту на сервере\nАккаунт создан ' + f"{member.created_at.strftime('%d %B %Yг.')}",
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed1.set_author(name = f'{member}', icon_url = member.avatar_url)
    embed1.set_footer(text = f'ID: {member.id}')
    embed1.timestamp = datetime.datetime.utcnow()
    await bot.get_channel(942828703266783339).send(embed = embed1)


@bot.event
async def on_member_remove(member):
    rlist = []  
    for role in member.roles:
      if role.name != "@everyone":
        rlist.append(role.mention)

    b = ", ".join(rlist)
    embed = discord.Embed(
        title = 'Пользователь вышел с сервера',
        description = f'{member.mention} зашёл на этот сервер ' + f"{member.joined_at.strftime('%d %B %Yг.')}\n" + f"**Роли({len(rlist)}):**" + ''.join([b]),
        color = discord.Color.from_rgb(255, 0, 0)
        )
    embed.set_author(name = f'{member}', icon_url = member.avatar_url)
    embed.set_footer(text = f'ID: {member.id}')
    embed.timestamp = datetime.datetime.utcnow()
    await bot.get_channel(942828703266783339).send(embed = embed)

bot.run('OTMyNzA3ODI0ODY4NDA1MzA4.YeW52g.bHCuznd8jXPxYdHELZi4pY_xP4g')
