#Бот версия 0.84 Намного спокойней стал
#w1, r1, etc -переменные для сообщений которые адресованы лично для Бота
#w2, r2, etc -переменные для сообщений которые отправляет Бот автоматом
#w3, r3, etc -переменные для сообщений которые Бот отправляет после основоного сообщения
#Еще будет допиливаться и оптимизироваться

import config # наш конфиг
import telebot # ботапи
import time
import re
import random
import threading
import sqlite3
import logging as logger


#----------
#Глобальнейшие переменные!!!
#----------

bot = telebot.TeleBot(config.token) #токен
n=1# для бесконечного цикла
f=0# флаг добавочного сообщения
word=['лох', 'чмо', 'пидар', 'пидор', 'член', 'долбоеб','дурак','придурок','тупой','сука','гандон'] #оскорбления
zp=['зп','зарплату','денег','кэш']
up=['подними','повысь','дай','подыми']
vano=['Ваня', 'твой', 'выход']
dima=['Дима', 'сюда']
story=['травы','срать','пердит']
laststate1=0# последнее хеллоу
laststate2=0# последнее сообщение бота по автомату
laststate3=0# последнее добавочное автомата
laststate4=0# lastzp
dbpath='/var/tele/tarbot/db/sticker.db'


counter = 0 #счетчик оскорблений
cunter = 0 #счетчик зарплат
#------------------
# команды Бота
#------------------

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message("-227007340", "Резурекшн, ебана врот!")

@bot.message_handler(commands=["wise"])
def wise(message):
    bot.send_message("-227007340", "test")
	
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message("-227007340", "v0.84")
@bot.message_handler(commands=["cnl"])
def cnl(message):	   
    cnl = open ('/var/tele/tarbot/phrases/cnl', 'rb')	
    bot.send_document("-227007340", cnl)
    time.sleep(2)	
    bot.send_message("-227007340", "Как пофиксите, ответте всем. Только корректно")
    cnl.closed

# Ответ на скрины и фото
@bot.message_handler(content_types=["photo"])
def photo(message):
    time.sleep(1)
    ran=random.randint(0,9)
    if ran == 6:
       bot.send_message("-227007340", "отвечайте на вопрос, а не скрины кидаете")

#обращение к боту
@bot.message_handler(content_types=["text"])
def hello(message):
     
    time.sleep(1)
    result = re.search(r'тар.+[ик|ас]', message.text,re.IGNORECASE) # ищем имя и прочее в сообщении
    w1=0 #на всякий случай разные переменные cчетчика
    
    with open ('/var/tele/tarbot/phrases/hello') as f1:
     w1 = sum(1 for _ in f1)-1 #динамический словарь
    f1.closed
    
    with open ('/var/tele/tarbot/phrases/zp') as f4:
     w4 = sum(1 for _ in f4)-1 #динамический словарь zp
    f4.closed


    msg = message.text.lower()#делаем все символы сообщения маленькими, что бы найти оскорбление или зарплату

    if (result and not any (x in msg for x in word) and not any (x in msg for x in up) and not any (x in msg for x in zp) and not (message.from_user.username == "plizmol")): #если было имя, но не было оскорбления
     
     global f #детектим месагу для автоматических сообщений
     f=1
 
     #Генерация числа для сообщения
     r1 = random.randint(0,w1)

     #проверка, не последнее ли это сообщение
     global laststate1
     if r1 == laststate1:
      r1=r1+1
     

 #Отправка сообщения и запоминание статуса 
     with open ('/var/tele/tarbot/phrases/hello') as hell: # открываем фаил теперь для чтения, что бы подгружал всегда актуальную базу
      tarmsg = hell.readlines()[r1]
      bot.send_message("-227007340", tarmsg)
     #Выход вани
      if all (x in tarmsg for x in vano):
       time.sleep(1)
       sti = open('/var/tele/tarbot/phrases/sticker/vano.webp', 'rb')
       bot.send_sticker("-227007340", sti)
     #Дима сюда
      if all (x in tarmsg for x in dima):
       time.sleep(1)
       sti = open('/var/tele/tarbot/phrases/sticker/dima.webp', 'rb')
       bot.send_sticker("-227007340", sti)
   

     laststate1=r1  
     hell.closed #закрываем
       
    elif(message.from_user.username == "plizmol" and result):
        time.sleep(1)
        bot.send_message("-227007340", "Иди на бутыль садись на дрангомирова, бля пиздец!")

# Бот отвечает на оскорбления
    elif any(x in msg for x in word) and result: # если было имя и было оскорбление, то ищем оскорбление	
     mat = next((x for x in word if x in  msg), None)# определяем какое именно сокорблени
     bot.send_message("-227007340", "Сам ты "+mat)# отвечаем на оскорбление реверсом
     global counter
     counter=counter+1
     if counter == 6:
      bot.send_message("-227007340", "Все, надоели меня оскорблять тут! Весь саппорт уволен. Буду сам на сутках сидеть ")
      counter = 0
    # Зарплата 
    elif (result and any (x in msg for x in zp) and any (x in msg for x in up)):
     bot.send_message("-227007340", "...")
     global cunter
     cunter=cunter+1
     if not cunter == 6:
      r4 = random.randint(0,w4)#zp

      #проверка зп
      global laststate4
      if r4 == laststate4:
       r4+r4+1
    
      time.sleep(2)
      with open ('/var/tele/tarbot/phrases/zp') as zpf: # открываем фаил теперь для чтения, что бы подгружал всегда актуальную базу
       tarmsg = zpf.readlines()[r4]
      bot.send_message("-227007340", tarmsg)
      zpf.closed
      
     else:
      bot.send_message("-227007340","Задолбали! Поднял я вон вам бонусы всем! 3000!! Радуйтесь!")
      cunter=0

#закрываем файлы
     #l.closed
    #Выход вани 2
    if all (x.lower() in msg for x in vano):
     time.sleep(1)
     sti = open('/var/tele/tarbot/phrases/sticker/vano.webp', 'rb')
     bot.send_sticker("-227007340", sti)
    #Дима сюда 2
    if all (x.lower() in msg for x in dima):
     time.sleep(1)
     sti = open('/var/tele/tarbot/phrases/sticker/dima.webp', 'rb')
     bot.send_sticker("-227007340", sti)
	 
    if all (x.lower() in msg for x in story) and not result and (len(msg) > 50):
     time.sleep(1)
     bot.send_message("-227007340", "ух бля")
     time.sleep(1)
     bot.send_message("-227007340", "ору")
     time.sleep(1)
     bot.send_message("-227007340", "охуенная история поржал)")
    elif all (x.lower() in msg for x in story) and (len(msg) < 50):
     time.sleep(1)
     bot.send_message("-227007340", "Фу бля, дичь а не история. Проверь за щекой")


	
#---------------------
#цикл сообщений
#---------------------

def cycle(): 
 while True:
  
  w2=0
  w3=0 #на всякий случай разные переменные для размеров словарей
  
  with open ('/var/tele/tarbot/phrases/phr') as f2:
     w2 = sum(1 for _ in f2)-1 #динамический словарь для основной фразы
  

  with open ('/var/tele/tarbot/phrases/fear') as f3:
     w3 = sum(1 for _ in f3)-1 #динамический словарь для добавочной фразы
  
  #Генерация числа для сообщения 
  r2 = random.randint(0,w2) 

  #проверка, не последнее ли это сообщение 
  global laststate2 
  if r2 == laststate2: 
    r2=r2+1 
  
  #Отправка сообщения и запоминание статуса
  with open ('/var/tele/tarbot/phrases/phr') as phar: #открытие файла для актуализации базы
   tarmsg2=phar.readlines()[r2]
   bot.send_message("-227007340", tarmsg2) #Космофашисты
   global f # опускаем флаг для добавочного. Если он опущен (0) то будет ВАМ ПОВЫЛАЗИЛО?
   f=0
   phar.seek(0)
   #выход вани 3
   if all (x in tarmsg2 for x in vano):
     time.sleep(1)
     sti = open('/var/tele/tarbot/phrases/sticker/vano.webp', 'rb')
     bot.send_sticker("-227007340", sti)
   #Дима сюда 3
   if all (x in tarmsg2 for x in dima):
     time.sleep(1)
     sti = open('/var/tele/tarbot/phrases/sticker/dima.webp', 'rb')
     bot.send_sticker("-227007340", sti)
  
  laststate2=r2
  phar.closed


    
  r=random.randint(20,60) #таймер перед добавочным
  time.sleep(r)
  
  #Ловим ответ. Если есть, то пишем реагируйте!
  if f==1:
   bot.send_message("-227007340","Реагируйте быстрее в следующий раз!")
 
 #Если не было, то отправляем добавочное
  elif f==0:
   #Генерация числа для сообщения
   r3 = random.randint(0,w3)

  #проверка, не последнее ли это сообщение
   global laststate3
   if r3 == laststate3:
     r3=r3+1

  #добавочное сообщение и запоминание его статуса
   with open ('/var/tele/tarbot/phrases/fear') as evil: # опять же октрытие для актуализации базы
     bot.send_message("-227007340","Вам что повылазило там!? "+evil.readlines()[r3])
   laststate3=r3
   evil.closed

  f2.closed
  f3.closed



  
 
  #таймер паузы
  #t=1 #Test
  t=16560+random.randint(0,16560) #2,5 часа
  time.sleep(t)

#ВНЕЗАПНО  
def easter(): 
 while True:
 
  t=7*12*30*60
  time.sleep(t)
  
  id=random.randint(1,9)
  ids=str(id)
  sql = "SELECT * FROM stick WHERE id='"+ids+"'"
  conn=sqlite3.connect(dbpath)
  cdb=conn.cursor()
  cdb.execute(sql)
  records = cdb.fetchall()
  for record in records:
   stick = record[1]
  sti = open('/var/tele/tarbot/phrases/sticker/'+stick+'.webp', 'rb')
  bot.send_sticker("-227007340", sti)
   
  with open ('/var/tele/tarbot/phrases/priv') as priv: #открытие файла для актуализации базы
    wpriv = sum(1 for _ in priv)-1
    priv.seek(0)
    pr = random.randint(0,wpriv)
    time.sleep(5)
    bot.send_message("-227007340", priv.readlines()[pr]) 
  
def intro():
    bot.send_message("-227007340", "Резурекшн, ебана врот!")
  
#non crashing tarik
def polling():
  while True:

    try:
        bot.polling(none_stop=True)
    except:
        #bot.send_message("-227007340", "пошла обратная репликация меня,  через 2 секунды должно отпустить")
        logger.error('\nLost connection. Reconnect in 2 sec')
        time.sleep(2)


#----------------
#запуск потоков
#----------------
threading.Thread(target=cycle).start()
threading.Thread(target=polling).start()
threading.Thread(target=easter).start()
intro()
#threading.Thread(target=bot.polling(none_stop=True)).start()

