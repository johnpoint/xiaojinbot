#!/bin/python3

import telebot
#from telebot import types

import config

TOKEN = config.TOKEN
botname = config.name
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new(message):
    if message.chat.id == -1001376188698:
        try:
            username = message.new_chat_members[0].username
            bot.send_message(message.chat.id,'@%s 欢迎加入津津乐道听友的大家庭~\n在这里你可以尽情的与主播以及其他听友进行交流，但是要注意不要发广告哦！'%username)
            bot.send_message(message.chat.id,'很高兴认识你，我是群内的小助手，点击\n--> /help <--\n试试吧')
        except AttributeError:
            bot.send_message(message.chat.id,'欢迎加入津津乐道听友的大家庭~\n在这里你可以尽情的与主播以及其他听友进行交流，但是要注意不要发广告哦！')
            bot.send_message(message.chat.id,'很高兴认识你，我是群内的小助手，点击\n--> /help <--\n试试吧')
        bot.delete_message(message.chat.id,message.message_id)
    else:
        pass

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,'HI，终于等到你，我是小津！\n/help 获取帮助信息')

@bot.message_handler(commands=['help'])
def send_help_info(message):
    bot.send_message(message.chat.id,'/new - 获取最新一期节目\n/get [关键词] - 通过节目标题搜索节目')

#TODO
#@bot.message_handler(commands=['get'])
def send_info(message):
    text = message.text
    text = text.lstrip('/get').lstrip('@'+botname).lstrip()
