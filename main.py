import time
import json
import telebot

##TOKEN DETAILS
TOKEN = "KUPON"

BOT_TOKEN = "5861126009:AAFqHO50PoX96CMAMj-VNt-jmwWG6xLcQ2o"
PAYMENT_CHANNEL = "@Jjnjjjgh" #add payment channel here including the '@' sign
OWNER_ID = 5716083446 #write owner's user id here.. get it from @MissRose_Bot by /id
CHANNELS = ["@heyterbaruu"] #add channels to be checked here in the format - ["Channel 1", "Channel 2"] 
              #you can add as many channels here and also add the '@' sign before channel username
Daily_bonus = 500 #Put daily bonus amount here!
Mini_Withdraw = 100  #remove 0 and add the minimum withdraw u want to set
Per_Refer = 1000 #add per refer bonus here

bot = telebot.TeleBot(BOT_TOKEN)

def check(id):
    for i in CHANNELS:
        check = bot.get_chat_member(i, id)
        if check.status != 'left':
            pass
        else:
            return False
    return True
bonus = {}

def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('π CEK SALDO')
    keyboard.row('ππ» Undang', 'π Bonus', 'πΈ Tukar Kupon')
    keyboard.row('π§Ύ VERIFIKASI', 'πJumlah Teman')
    bot.send_message(id, "*π‘ Home*", parse_mode="Markdown",
                     reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
   try:
    user = message.chat.id
    msg = message.text
    if msg == '/start':
        user = str(user)
        data = json.load(open('users.json', 'r'))
        if user not in data['referred']:
            data['referred'][user] = 0
            data['total'] = data['total'] + 1
        if user not in data['referby']:
            data['referby'][user] = user
        if user not in data['checkin']:
            data['checkin'][user] = 0
        if user not in data['DailyQuiz']:
            data['DailyQuiz'][user] = "0"
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = "none"
        if user not in data['withd']:
            data['withd'][user] = 0
        if user not in data['id']:
            data['id'][user] = data['total']+1
        json.dump(data, open('users.json', 'w'))
        print(data)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(
           text='π€ΌββοΈ Masuk', callback_data='check'))
        msg_start = "*β₯οΈ Untuk masuk kesini silahkan join dulu π - "
        for i in CHANNELS:
            msg_start += f"\nβ‘οΈ {i}\n"
        msg_start += "*"
        bot.send_message(user, msg_start,
                         parse_mode="Markdown", reply_markup=markup)
    else:

        data = json.load(open('users.json', 'r'))
        user = message.chat.id
        user = str(user)
        refid = message.text.split()[1]
        if user not in data['referred']:
            data['referred'][user] = 0
            data['total'] = data['total'] + 1
        if user not in data['referby']:
            data['referby'][user] = refid
        if user not in data['checkin']:
            data['checkin'][user] = 0
        if user not in data['DailyQuiz']:
            data['DailyQuiz'][user] = 0
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = "none"
        if user not in data['withd']:
            data['withd'][user] = 0
        if user not in data['id']:
            data['id'][user] = data['total']+1
        json.dump(data, open('users.json', 'w'))
        print(data)
        markups = telebot.types.InlineKeyboardMarkup()
        markups.add(telebot.types.InlineKeyboardButton(
            text='π€ΌββοΈ Masuk', callback_data='check'))
        msg_start = "*β₯οΈ Untuk masuk kesini silahkan join dulu π - \nβ‘οΈ @heyterbaruu*"
        bot.send_message(user, msg_start,
                         parse_mode="Markdown", reply_markup=markups)
   except:
        bot.send_message(message.chat.id, "This command having error pls wait for ficing the glitch by admin")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: "+message.text)
        return

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
   try:
    ch = check(call.message.chat.id)
    if call.data == 'check':
        if ch == True:
            data = json.load(open('users.json', 'r'))
            user_id = call.message.chat.id
            user = str(user_id)
            bot.answer_callback_query(
                callback_query_id=call.id, text='β Segera Masuk Sekarang')
            bot.delete_message(call.message.chat.id, call.message.message_id)
            if user not in data['refer']:
                data['refer'][user] = True

                if user not in data['referby']:
                    data['referby'][user] = user
                    json.dump(data, open('users.json', 'w'))
                if int(data['referby'][user]) != user_id:
                    ref_id = data['referby'][user]
                    ref = str(ref_id)
                    if ref not in data['balance']:
                        data['balance'][ref] = 0
                    if ref not in data['referred']:
                        data['referred'][ref] = 0
                    json.dump(data, open('users.json', 'w'))
                    data['balance'][ref] += Per_Refer
                    data['referred'][ref] += 1
                    bot.send_message(
                        ref_id, f"*πΉ Undangan kamu  masuk Level 1, semangat : +{Per_Refer} {TOKEN}*", parse_mode="Markdown")
                    json.dump(data, open('users.json', 'w'))
                    return menu(call.message.chat.id)

                else:
                    json.dump(data, open('users.json', 'w'))
                    return menu(call.message.chat.id)

            else:
                json.dump(data, open('users.json', 'w'))
                menu(call.message.chat.id)

        else:
            bot.answer_callback_query(
                callback_query_id=call.id, text='β Kamu belum Join silahkan join dulu ya ..agar bisa masuk')
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text='π€ΌββοΈ Joined', callback_data='check'))
            msg_start = "*β₯οΈ Untuk masuk kesini silahkan join dulu  - \nβ‘οΈ @heyterbaruu*"
            bot.send_message(call.message.chat.id, msg_start,
                             parse_mode="Markdown", reply_markup=markup)
   except:
        bot.send_message(call.message.chat.id, "This command having error pls wait for ficing the glitch by admin")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: "+call.data)
        return

@bot.message_handler(content_types=['text'])
def send_text(message):
   try:
    if message.text == 'π CEK SALDO':
        data = json.load(open('users.json', 'r'))
        accmsg = '*π? User : {}\n\nβοΈ Wallet : *`{}`*\n\nπΈ Kupon : *`{}`* {}*'
        user_id = message.chat.id
        user = str(user_id)

        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = "none"

        json.dump(data, open('users.json', 'w'))

        balance = data['balance'][user]
        wallet = data['wallet'][user]
        msg = accmsg.format(message.from_user.first_name,
                            wallet, balance, TOKEN)
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    if message.text == 'ππ» Undang':
        data = json.load(open('users.json', 'r'))
        ref_msg = "*β―οΈ Total Undang : {} Users\n\nπ₯ Undangan System\n\n1 Level:\nπ₯ LevelΒ°1 - {} {}\n\nπ Undang Link β¬οΈ\n{}*"

        bot_name = bot.get_me().username
        user_id = message.chat.id
        user = str(user_id)

        if user not in data['referred']:
            data['referred'][user] = 0
        json.dump(data, open('users.json', 'w'))

        ref_count = data['referred'][user]
        ref_link = 'https://telegram.me/{}?start={}'.format(
            bot_name, message.chat.id)
        msg = ref_msg.format(ref_count, Per_Refer, TOKEN, ref_link)
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    if message.text == "π§Ύ VERIFIKASI":
        user_id = message.chat.id
        user = str(user_id)

        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('π« Cancel')
        send = bot.send_message(message.chat.id, "_β οΈSilahkan Ketik  YES untuk mengisi Data._",
                                parse_mode="Markdown", reply_markup=keyboard)
        # Next message will call the name_handler function
        bot.register_next_step_handler(message, trx_address)
    if message.text == "π Bonus":
        user_id = message.chat.id
        user = str(user_id)
        cur_time = int((time.time()))
        data = json.load(open('users.json', 'r'))
        #bot.send_message(user_id, "*π Bonus Button is Under Maintainance*", parse_mode="Markdown")
        if (user_id not in bonus.keys()) or (cur_time - bonus[user_id] > 60*60*24):
            data['balance'][(user)] += Daily_bonus
            bot.send_message(
                user_id, f"Kamu dapat menukarkan Kupon mu 100 Kupon !!!\n\n Bagikan ke Group Agar banyak mendapatkan Kupon agar bisa ditukarkan ...!!!\n\nπ Penukaran Secara Otomatis, Jika Sudah Sesuai Maka link Vip akan dikirim kan  \n\n \n\nSelamat anda mendapatkan Bonus  {Daily_bonus} {TOKEN}")
            bonus[user_id] = cur_time
            json.dump(data, open('users.json', 'w'))
        else:
            bot.send_message(
                message.chat.id, "*Kamu dapat menukarkan Kupon mu  100 Kupon !!!\n\n Bagikan ke Group Agar banyak mendapatkan Kupon agar bisa ditukarkan ...!!!\n\nπ Penukaran Secara Otomatis, Jika Sudah Sesuai Maka link Vip akan dikirim kan   \n\nβ Yah bonus sudah habis, Silakhan besok lagi*",parse_mode="markdown")
        return

    if message.text == "πJumlah Teman":
        user_id = message.chat.id
        user = str(user_id)
        data = json.load(open('users.json', 'r'))
        msg = "*π Total Teman : {} Users\n\nπ₯ Total sukses penukaran : {} {}*"
        msg = msg.format(data['total'], data['totalwith'], TOKEN)
        bot.send_message(user_id, msg, parse_mode="Markdown")
        return

    if message.text == "πΈ Tukar Kupon":
        user_id = message.chat.id
        user = str(user_id)

        data = json.load(open('users.json', 'r'))
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = "none"
        json.dump(data, open('users.json', 'w'))

        bal = data['balance'][user]
        wall = data['wallet'][user]
        if wall == "none":
            bot.send_message(user_id, "_β VERIFIKASI Dulu di menu π π§ΎVerivikasi_",
                             parse_mode="Markdown")
            return
        if bal >= Mini_Withdraw:
            bot.send_message(user_id, "_Masukan dan Kirim jumlah Kupon _",
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, amo_with)
        else:
            bot.send_message(
                user_id, f"_β Kupon anda tidak cukup undang sebanyak Agar bisa di tukarkan!! Minimal π {Mini_Withdraw} {TOKEN} to Withdraw_", parse_mode="Markdown")
            return
   except:
        bot.send_message(message.chat.id, "This command having error pls wait for ficing the glitch by admin")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: "+message.text)
        return

def trx_address(message):
   try:
    if message.text == "π« Cancel":
        return menu(message.chat.id)
    if len(message.text) == 3:
        user_id = message.chat.id
        user = str(user_id)
        data = json.load(open('users.json', 'r'))
        data['wallet'][user] = message.text

        bot.send_message(message.chat.id, "*β Data mu sudah tersimpan Silahkan Tukarkan " +
                         data['wallet'][user]+"*", parse_mode="Markdown")
        json.dump(data, open('users.json', 'w'))
        return menu(message.chat.id)
    else:
        bot.send_message(
            message.chat.id, "*β οΈ Silahkan Ketik  YES untuk mengisi Data*", parse_mode="Markdown")
        return menu(message.chat.id)
   except:
        bot.send_message(message.chat.id, "This command having error pls wait for ficing the glitch by admin")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: "+message.text)
        return

def amo_with(message):
   try:
    user_id = message.chat.id
    amo = message.text
    user = str(user_id)
    data = json.load(open('users.json', 'r'))
    if user not in data['balance']:
        data['balance'][user] = 0
    if user not in data['wallet']:
        data['wallet'][user] = "none"
    json.dump(data, open('users.json', 'w'))

    bal = data['balance'][user]
    wall = data['wallet'][user]
    msg = message.text
    if msg.isdigit() == False:
        bot.send_message(
            user_id, "_π Tidak boleh ada Huruf Titik koma!! Semua angka Sesuai minimal penukaran_", parse_mode="Markdown")
        return
    if int(message.text) < Mini_Withdraw:
        bot.send_message(
            user_id, f"_βKupon anda tidak cukup undang sebanyak  Agar bisa di tukarkan!! Minimal {Mini_Withdraw} {TOKEN}_", parse_mode="Markdown")
        return
    if int(message.text) > bal:
        bot.send_message(
            user_id, "_βKupon anda tidak cukup undang sebanyak Agar bisa di tukarkan!! Minimal_", parse_mode="Markdown")
        return
    amo = int(amo)
    data['balance'][user] -= int(amo)
    data['totalwith'] += int(amo)
    bot_name = bot.get_me().username
    json.dump(data, open('users.json', 'w'))
    bot.send_message(user_id, "β* Selamat Kupon Berhasil Ditukarkan Secara Otomatis\n\nπΉ Channel Vip :- "+PAYMENT_CHANNEL +"*", parse_mode="Markdown")

    markupp = telebot.types.InlineKeyboardMarkup()
    markupp.add(telebot.types.InlineKeyboardButton(text='π BOT LINK', url=f'https://telegram.me/{bot_name}?start={OWNER_ID}'))

    send = bot.send_message(PAYMENT_CHANNEL,  "β* New Withdraw\n\nβ­ Amount - "+str(amo)+f" {TOKEN}\nπ¦ User - @"+message.from_user.username+"\nπ  Wallet* - `"+data['wallet'][user]+"`\nβοΈ *User Referrals = "+str(
        data['referred'][user])+"\n\nπ Bot Link - @"+bot_name+"\nβ© Please wait our owner will confrim it*", parse_mode="Markdown", disable_web_page_preview=True, reply_markup=markupp)
   except:
        bot.send_message(message.chat.id, "This command having error pls wait for ficing the glitch by admin")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: "+message.text)
        return

if __name__ == '__main__':
    bot.polling(none_stop=True)
