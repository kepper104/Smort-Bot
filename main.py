import lightbulb
import hikari
from mytoken import TOKEN
import datetime as dt
from deck_game_checker import get_app_id, get_deck_game_status

PREFIX = '!'
bot = lightbulb.BotApp(token=TOKEN, prefix=PREFIX,
                       default_enabled_guilds=(405058933603041280, 737291852763365419))

pref = lightbulb.PrefixCommand
slash = lightbulb.SlashCommand
group = lightbulb.SlashCommandGroup
sub = lightbulb.SlashSubCommand


@bot.listen(hikari.GuildMessageCreateEvent)
async def on_message(event):
    with open('log.txt', 'a') as file:
        file.write(
            f"{event.author} said '{event.content}' in '{event.get_channel()}' (id: {event.channel_id}) at {dt.datetime.today()}")
        print(
            f"{event.author} said '{event.content}' in '{event.get_channel()}' (id: {event.channel_id}) at {dt.datetime.today()}")


@bot.listen(hikari.StartedEvent)
async def on_start(event):
    print("Bot started!")


@bot.command
@lightbulb.command('ping', 'returns pong')
@lightbulb.implements(slash, pref)
async def ping(ctx):
    await ctx.respond("pong!")
    # embed = (
    #     hikari.Embed(
    #         title=f"BRUH",
    #         description=f"HAH",
    #         colour=0x3B9DFF,
    #         # timestamp=datetime.now().astimezone(),
    #     )
    #     .set_footer(
    #         "KEK"
    #     )
    #     # .set_thumbnail()
    #     .add_field(
    #         "LOL", "JFLD"
    #     )
    # )
    # await ctx.respond(embed)


@bot.command
@lightbulb.command('group', 'this is a group')
@lightbulb.implements(group)
async def on_group(ctx):
    pass


@on_group.child
@lightbulb.command('subcommand', 'you know')
@lightbulb.implements(sub)
async def subcommand(ctx):
    await ctx.respond('i am subcommand')


@bot.command
@lightbulb.option('num2', 'the first number', type=int)
@lightbulb.option('num1', 'the second number', type=int)
@lightbulb.command("add", 'adds two numbers together')
@lightbulb.implements(pref)
async def add(ctx):
    print(f"Adding {ctx.options.num1} and {ctx.options.num2}")
    await ctx.respond(ctx.options.num1 + ctx.options.num2)


@bot.command
@lightbulb.option('name', 'Game`s name', type=str)
@lightbulb.command('deck', 'Get game`s steam deck avalibibilitily')
@lightbulb.implements(slash, pref)
async def deck(ctx):
    # real_name = " ".join(ctx.options.name)
    real_name = ctx.options.name
    app_id = get_app_id(real_name)
    if app_id:
        print(f"Found id for {real_name}: {app_id}")
        result = get_deck_game_status(int(app_id))
        if result:
            embed = hikari.Embed(
                title=result[0], url=f"https://steamdb.info/app/{app_id}", description=f"Current status for {real_name.capitalize()} is {result[0]}", color=0x008000)
            value = ''
            for i in result[1:]:
                value += f"{i[0]}: {i[1]}\n"
            embed.add_field(name="Additional notes:", value=value)
            embed.set_thumbnail(
                f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg")
            await ctx.respond(embed=embed)
        else:
            embed = hikari.Embed(
                title="Unsupported", url=f"https://steamdb.info/app/{app_id}", description=f"Current status for {real_name.capitalize()} is Unsupported", color=0x008000)
            # value = ''
            # for i in result[1:]:
            #     value += f"{i[0]}: {i[1]}\n"
            # embed.add_field(name="Additional notes:", value=value)
            embed.set_thumbnail(
                f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg")
            await ctx.respond(embed)
            # await ctx.respond("I got error when processing this request")
    else:
        await ctx.respond(f"I couldn't find any game called '{real_name}'")

bot.run()
