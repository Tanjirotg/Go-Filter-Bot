import re
from pymongo import MongoClient
from bson.regex import Regex
from utils import GetAdmins

Admins = GetAdmins()

def GFilter(bot, ctx):
    update = ctx.message
    chat_id = 0
    message_id = update.message_id
    chat_type = update.chat.type

    if chat_type == "private":
        chat_id = DB.GetConnection(update.from_user.id)
        if chat_id is None:
            return
    elif chat_type == "supergroup" or chat_type == "group":
        chat_id = update.chat.id
    else:
        return

    res = DB.GetMfilters(globalNumber)
    stopped = DB.GetCachedSetting(chat_id).Stopped

    for f in res:
        key = f.get("text")
        text = f"(?i)( |^|[^\w]){re.escape(key)}( |$|[^\w])"
        pattern = re.compile(text)
        m = pattern.findall(update.text)
        
        if m:
            isStopped = any(k == key for k in stopped)
            if isStopped:
                continue
            filter = DB.GetFilter(f)
            sendFilter(filter, bot, update, chat_id, message_id)

    return

def StartGlobal(bot, ctx):
    update = ctx.message
    c, v = customfilters.Verify(bot, ctx)
    if not v:
        return
    
    if c == 0:
        c = ctx.message.chat.id
    
    split = update.text.split(" ", 2)
    
    if len(split) < 2:
        bot.send_message(update.chat.id, "Bad Usage No Keyword Provided :(")
    else:
        key = split[1]
        if not DB.GetMfilter(globalNumber, key):
            bot.send_message(update.chat.id, f"No Global Filter For {key} Was Found To Restart !")
        else:
            stopped_filters = DB.GetCachedSetting(c).Stopped
            if key in stopped_filters:
                DB.StartGfilter(c, key)
                bot.send_message(update.chat.id, f"Restarted Global Filter For {key} Successfully !", parse_mode="HTML")
            else:
                bot.send_message(update.chat.id, f"You Havent Stopped Any Global Filter For {key} :(")

    return

def Gfilters(bot, ctx):
    text = DB.StringMfilter(globalNumber)
    bot.send_message(ctx.message.chat.id, "All filters saved for global usage:\n"+text, parse_mode="HTML")
    return
