import openai
from twitchio.ext import commands

# set OpenAI API key
openai.api_key = 'YOUR OPENAI API KEY'

# initialize the bot with Twitch credentials and prefix
bot = commands.Bot(
    token='oauth:YOUR_TWITCH_OAUTH_TOKEN',
    client_id='YOUR_TWITCH_CLIENT_ID',
    nick='YOUR_TWITCH_NICK',
    prefix='!',
    initial_channels=['#YOUR_TWITCH_CHANNEL'] # enter the channel name here
)

# handle messages sent in the channel
@bot.event
async def event_message(message):
    await bot.handle_commands(message)

# create a custom command for the bot
@bot.command(name="Grisha")
async def grisha_command(ctx):
    t = ctx.message.content.replace('!Grisha', '').strip()
    if t == "":
        await ctx.send("You must enter text after the Grisha command")
        return

    print(t)

    try:
        # generate an AI response using OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "assistant", "content": t},
            ]
        )
        answer = response.choices[0].message['content']
        if len(answer) > 128:
            await ctx.send("The response text is too long, please try a different query")
            return

        await ctx.send(f"{answer}")

    except Exception as e:
        print(f"Error: {e}")
        await ctx.send("An error occurred while executing the command.")

if __name__ == '__main__':
    bot.run()
