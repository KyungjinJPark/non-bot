import os
import psycopg2

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

cur.execute("SELECT * FROM guilds;")
guild_ids = []
for record in cur:
  guild_ids.append(record[2])


async def respond(ctx, msg):
    '''send a message'''
    await ctx.send(msg)


DELETE_DELAY = 5
async def temp_send(ctx, msg: str):
    await ctx.send(msg, delete_after=DELETE_DELAY)
async def temp_reply(orig, msg: str, mention: bool):
    await orig.reply(msg, mention_author=mention, delete_after=DELETE_DELAY)