import discord
import discord.ext

def swear_detection(message, swear_words):
    for word in swear_words:
        if word in message.content.lower():
            return True
        else:
            return False

