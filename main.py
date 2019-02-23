#!/bin/python3

import telebot
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
import time
import datetime

import config
import getinfo

TOKEN = config.TOKEN
botname = config.NAME
chatid = config.CHATID
bot = telebot.TeleBot(TOKEN)

print('[Info] bot running...')
print('[Info] set time point')
start_time = datetime.datetime.now()

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new(message):
    print('[Info] new members')
    print(str(message.chat.id))
    if str(message.chat.id) == chatid:
        username = message.new_chat_members[0].username
        if username == None:
            try:
                userfirstname = message.new_chat_members[0].first_name
                userlastname = message.new_chat_members[0].last_name
                if userlastname == None:
                    userlastname = ''
                msg1 = bot.reply_to(
                    message, '%s %s 欢迎加入津津乐道听友的大家庭~\n在这里你可以尽情的与主播以及其他听友进行交流，但是要注意不要发广告哦！\nhttps://t.me/htnpodcast/44627' % (userfirstname,userlastname)).message_id
                msg2 = bot.reply_to(
                    message, '很高兴认识你，我是群内的小助手，点击\n--> /help <--\n试试吧').message_id
            except AttributeError:
                msg1 = bot.reply_to(
                    message, '欢迎加入津津乐道听友的大家庭~\n在这里你可以尽情的与主播以及其他听友进行交流，但是要注意不要发广告哦！\nhttps://t.me/htnpodcast/44627').message_id
                msg2 = bot.reply_to(
                    message, '很高兴认识你，我是群内的小助手，点击\n--> /help <--\n试试吧').message_id
        else:
            msg1 = bot.send_message(
                message.chat.id, '@%s 欢迎加入津津乐道听友的大家庭~\n在这里你可以尽情的与主播以及其他听友进行交流，但是要注意不要发广告哦！\nhttps://t.me/htnpodcast/44627' % username).message_id
            msg2 = bot.send_message(
                message.chat.id, '很高兴认识你，我是群内的小助手，点击\n--> /help <--\n试试吧\n点击--> /verify --<\n完成入群验证').message_id
            bot.delete_message(message.chat.id, message.message_id)
        time.sleep(20)
        bot.delete_message(message.chat.id, msg1)
        bot.delete_message(message.chat.id, msg2)
    else:
        pass

@bot.message_handler(commands=['verify'])
def send_verify(message):
    print('[Info] send reply for /verify')
    msg = bot.send_message(message.chat.id, '验证成功!欢迎加入~').message_id
    bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print('[Info] send reply for /start')
    bot.send_message(message.chat.id, 'HI，终于等到你，我是小津！\n/help 获取帮助信息')

@bot.message_handler(commands=['help'])
def send_help_info(message):
    print('[Info] send reply for /help')
    bot.send_message(
        message.chat.id, '/new - 获取最新一期节目\n/get [关键词] - 通过节目标题搜索节目')


@bot.message_handler(commands=['get'])
def send_info(message):
    print('[Info] send reply for /get')
    if ' ' not in message.text:
        bot.send_message(message.chat.id, '昂？你好像啥都没有说，找啥呀...')
    else:
        msg = bot.send_message(message.chat.id,'查询中...').message_id
        text = message.text
        text = text.lstrip('/get').lstrip('@'+botname).lstrip()
        num, data = getinfo.get_url(text)
        bot.delete_message(message.chat.id,msg)
        if data == 404:
            bot.send_message(message.chat.id, '没有你想要的节目哦，选个别的关键词吧~')
        else:
            if num > 5:
                num = 5
            else:
                num = num
            num = int(num)
            markup = types.InlineKeyboardMarkup()
            text = '找到如下节目:'
            for i in range(num):
                btn = types.InlineKeyboardButton(
                    data[i]["title"], url='%s' % data[i]["url"])
                markup.add(btn)
            bot.reply_to(message, text, reply_markup=markup)


@bot.message_handler(commands=['new'])
def send_new(message):
    msg = bot.send_message(message.chat.id,'查询中...').message_id
    num, data = getinfo.get_url('.')
    bot.delete_message(message.chat.id,msg)
    if data == 404:
        print('[Error] API error')
        bot.send_message(message.chat.id, 'API貌似出现了一些问题，稍后试试吧！')
    else:
        print('[Info] send reply for /new')
        i = int(num)
        text = '最新一期的节目在这:'
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(
            data[i-1]["title"], url='%s' % data[i-1]["url"])
        markup.add(btn)
        bot.reply_to(message, text, reply_markup=markup)

@bot.message_handler(commands=['ping'])
def send_pong(message):
    print('[Info] send reply for /ping')
    nowtime = datetime.datetime.now()
    uptime = (nowtime - start_time)
    bot.send_message(message.chat.id,'pong! uptime: %s'%uptime)

def send_rss():
    print('[Info] RUN rss!')
    print('[Info:RSS] read file...')
    f = open(config.newfile,'r')
    l = f.read()
    f.close()
    num,data=getinfo.get_url('.')
    if int(l)+1 == num:
        print('[Info:RSS] send RSS')
        i = int(num)
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(data[i-1]["title"], url='%s'%data[i-1]["url"])
        markup.add(btn)
        bot.send_message(-1001376188698, '有新的节目更新！', reply_markup=markup)
        l = int(l)
        newnum = l + 1
        newnum = str(newnum)
        f = open(config.newfile,'w')
        f.write(newnum)
        f.close
    else:
        pass

if __name__ == '__main__':
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_rss,'interval', minutes=1)
        scheduler.start()
        print('[Info] start scheduler jobs...')
        bot.polling()
