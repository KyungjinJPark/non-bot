async def respond(ctx, msg):
    '''send a message'''
    await ctx.send(msg)

DELETE_DELAY = 5
async def temp_send(ctx, msg: str):
    await ctx.send(msg, delete_after=DELETE_DELAY)
async def temp_reply(orig, msg: str, mention: bool):
    await orig.reply(msg, mention_author=mention, delete_after=DELETE_DELAY)