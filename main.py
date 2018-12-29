#!/bin/python3

import telebot
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler

import config
import getinfo

TOKEN = config.TOKEN
botname = config.NAME
chatid = config.CHATID
bot = telebot.TeleBot(TOKEN)

print('bot 正在运行...')

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new(message):
    if message.chat.id == chatid :
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

@bot.message_handler(commands=['get'])
def send_info(message):
    if ' ' not in message.text :
        bot.send_message(message.chat.id,'昂？你好像啥都没有说，找啥呀...')
    else:
        text = message.text
        text = text.lstrip('/get').lstrip('@'+botname).lstrip()
        num,data = getinfo.get_url(text)
        if data == 404:
            bot.send_message(message.chat.id,'没有你想要的节目哦，选个别的关键词吧~')
        else:
            if num  > 5:
                num = 5
            else:
                num = num
            num = int(num)
            markup = types.InlineKeyboardMarkup()
            text = '找到如下节目:'
            for i in range(num):
                btn = types.InlineKeyboardButton(data[i]["title"], url='%s'%data[i]["url"])
                markup.add(btn)
            bot.reply_to(message, text, reply_markup=markup)

@bot.message_handler(commands=['new'])
def send_new(message):
    num,data=getinfo.get_url('.')
    if data == 404:
        bot.send_message(message.chat.id,'API貌似出现了一些问题，稍后试试吧！')
    else:
        i = int(num)
        text='最新一期的节目在这:'
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(data[i-1]["title"], url='%s'%data[i-1]["url"])
        markup.add(btn)
        bot.reply_to(message, text, reply_markup=markup)

def send_rss():
	f = open('new','r')
	l = f.read()
	f.close()
	num,data=getinfo.get_url('.')
    if l+1 == num:
        i = int(num)
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(data[i-1]["title"], url='%s'%data[i-1]["url"])
        markup.add(btn)
        bot.send_message(chatid, '有新的节目更新！', reply_markup=markup)
    else:
        pass

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_rss,'interval', minutes=2)
    scheduler.start()
    bot.polling()
