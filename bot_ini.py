import telebot
from config import TOKEN
import db_operations as db
import dt_def as dt
import datetime
import Gcalendar
import math
bot = telebot.TeleBot(TOKEN)

class Workers:
    """Класс работников салона"""

    def __init__(self, call):
        self.call = call

    def get_workers_menu(self):
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)  # наша клавиатура
        key_add_worker = telebot.types.InlineKeyboardButton(text='Добавить сотрудника ✅',
                                                            callback_data='add_worker')
        key_edit_worker = telebot.types.InlineKeyboardButton(text='Удалить сотрудника ❌',
                                                             callback_data='edit_worker')
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
                                                         callback_data='admin_mode')
        keyboard.add(key_add_worker)  # добавляем кнопку в клавиатуру
        keyboard.add(key_edit_worker)
        keyboard.add(key_go_back)
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        bot.edit_message_text('🙎🏻‍♂🙍🏻‍♀ Раздел сотрудники:', self.call.message.chat.id, self.call.message.message_id,
                              reply_markup=keyboard)

    def add_worker_name(self):
        bot.edit_message_text('🙎🏻‍♂🙍🏻‍♀ Введите ФИО сотрудника:' , self.call.message.chat.id,
                              self.call.message.message_id)
        bot.register_next_step_handler(self.call.message, self.add_worker)

    def add_worker(self, message):
        worker_name = message.text
        if (worker_name != ''):
            res = db.add_worker(worker_name)
        else:
            bot.send_message(self.call.message.chat.id, 'Вы не ввели ФИО сотрудника!')

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура
        key_add_worker = telebot.types.InlineKeyboardButton(text='✅ Добавить',
                                                            callback_data='add_worker')
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
                                                         callback_data='workers')
        key_go_main_menu = telebot.types.InlineKeyboardButton(text='↩️ На главную',
                                                         callback_data='start/2')
        buttons = []
        buttons.append(key_go_back)
        buttons.append(key_add_worker)
        buttons.append(key_go_main_menu)
        keyboard.add(*buttons)

        bot.delete_message(message.chat.id, message.message_id)
        bot.edit_message_text(res + '\nВыберете пункт:', self.call.message.chat.id,
                              self.call.message.message_id, reply_markup=keyboard)

    def edit_worker(self):
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        userid = -1
        res = db.get_workers(userid)
        bot.edit_message_text('Список сотрудников:', self.call.message.chat.id, self.call.message.message_id)
        for id, name in res:
            buttons = []
            keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
            key_delete = telebot.types.InlineKeyboardButton(text=str('Удалить ❌'),
                                                            callback_data='wrk_delete' + '/' + str(id))
            buttons.append(key_delete)
            keyboard.add(*buttons)
            sending_message = bot.send_message(self.call.message.chat.id, '👩🏻‍💼 ' + str(name), reply_markup=keyboard)

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
                                                         callback_data='workers')
        keyboard.add(key_go_back)
        bot.send_message(self.call.message.chat.id, 'Вернуться назад:', reply_markup=keyboard)

    def delete_worker(self):
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        userid = self.call.data.split('/', 1)[1]
        db.del_worker(userid)
        bot.answer_callback_query(callback_query_id=self.call.id, show_alert=True, text="Запись успешно удалена!")
        bot.edit_message_text(str(self.call.message.text) + '❌', self.call.message.chat.id, self.call.message.message_id)


class Services:
    """Класс услуг предоставляемых в салоне"""

    def __init__(self, call):
        self.call = call

    def get_services_menu(self):
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)  # наша клавиатура
        key_add_services = telebot.types.InlineKeyboardButton(text='Добавить услугу ✅',
                                                              callback_data='add_services')
        key_delete_services = telebot.types.InlineKeyboardButton(text='Удалить услугу ❌',
                                                                 callback_data='edit_services')
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
                                                         callback_data='admin_mode')
        keyboard.add(key_add_services)  # добавляем кнопку в клавиатуру
        keyboard.add(key_delete_services)
        keyboard.add(key_go_back)
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        bot.edit_message_text('🛍 Раздел услуги:', self.call.message.chat.id, self.call.message.message_id,
                              reply_markup=keyboard)

    def add_services(self):
        bot.edit_message_text('🛍 Введите наименование услуги:', self.call.message.chat.id, self.call.message.message_id)
        bot.register_next_step_handler(self.call.message, self.add_services_name)

    def add_services_name(self, message):
        service_name = message.text
        if (service_name != ''):
            #answers = []
            #first_answer = service_name
            #answers.append(first_answer)
            res = db.add_services(service_name)
            bot.delete_message(message.chat.id, message.message_id)
            keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура
            key_add_service = telebot.types.InlineKeyboardButton(text='✅ Добавить',
                                                                 callback_data='add_services')
            key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
                                                             callback_data='services')
            key_go_main_menu = telebot.types.InlineKeyboardButton(text='↩️ На главную',
                                                                  callback_data='start/2')
            buttons = []
            buttons.append(key_go_back)
            buttons.append(key_add_service)
            buttons.append(key_go_main_menu)
            keyboard.add(*buttons)
            #bot.delete_message(message.chat.id, message.message_id)
            bot.edit_message_text(res + '\nВыберете пункт:', self.call.message.chat.id,
                                  self.call.message.message_id, reply_markup=keyboard)
            #bot.edit_message_text('🛍 '+str(service_name)+ '\n💵 Введите сторимость в руб.:', self.call.message.chat.id,
            #                      self.call.message.message_id)
            #bot.register_next_step_handler(self.call.message, self.add_services_cost, answers)

    # def add_services_cost(self, message, answers): #пока не используется!
    #     service_cost = message.text
    #
    #     if (service_cost != ''):
    #         two_answer = service_cost
    #         answers.append(two_answer)
    #     res = db.add_services(answers)
    #
    #     keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура
    #     key_add_service = telebot.types.InlineKeyboardButton(text='✅ Добавить',
    #                                                          callback_data='add_services')
    #     key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
    #                                                      callback_data='services')
    #     key_go_main_menu = telebot.types.InlineKeyboardButton(text='↩️ На главную',
    #                                                      callback_data='start/2')
    #     buttons = []
    #     buttons.append(key_go_back)
    #     buttons.append(key_add_service)
    #     buttons.append(key_go_main_menu)
    #     keyboard.add(*buttons)
    #     bot.delete_message(message.chat.id, message.message_id)
    #     bot.edit_message_text(res + '\nВыберете пункт:', self.call.message.chat.id,
    #                           self.call.message.message_id, reply_markup=keyboard)
    #     #bot.send_message(self.call.message.chat.id, res)
    #     #bot.send_message(self.call.message.chat.id, 'Выберете пункт:', reply_markup=keyboard)

    def edit_services(self):
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        serviceid = -1
        res = db.get_services(serviceid)
        bot.edit_message_text('Список услуг:', self.call.message.chat.id, self.call.message.message_id)
        for id, name, cost in res:
            buttons = []
            keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
            key_delete = telebot.types.InlineKeyboardButton(text=str('Удалить ❌'),
                                                            callback_data='service_delete' + '/' + str(id))
            buttons.append(key_delete)
            keyboard.add(*buttons)
            bot.send_message(self.call.message.chat.id, '💅🏻 ' + str(name) , reply_markup=keyboard)

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
                                                         callback_data='services')
        keyboard.add(key_go_back)
        bot.send_message(self.call.message.chat.id, 'Вернуться назад:', reply_markup=keyboard)

    def delete_services(self):
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        serviceid = self.call.data.split('/', 1)[1]

        res = db.get_services(serviceid)
        name = res[0][1]
        cost = res[0][2]
        db.del_service(serviceid)
        bot.answer_callback_query(callback_query_id=self.call.id, show_alert=True, text="Запись успешно удалена!")
        bot.edit_message_text('💅🏻' + str(name) + '❌', self.call.message.chat.id,
                              self.call.message.message_id)

class Shedule:
    """Класс расписания сотрудников салона"""

    def __init__(self, call):
        self.call = call

    def get_shedules_menu(self):
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)  # наша клавиатура
        key_add_shedule = telebot.types.InlineKeyboardButton(text='Добавить расписание ✅',
                                                             callback_data='add_shedule')
        key_delete_shedule = telebot.types.InlineKeyboardButton(text='Удалить расписание ❌',
                                                                callback_data='edit_shedule')
        key_show_shedule = telebot.types.InlineKeyboardButton(text='Просмотреть расписание 🗓',
                                                                callback_data='show_shedule')
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
                                                         callback_data='admin_mode')
        keyboard.add(key_add_shedule)  # добавляем кнопку в клавиатуру
        keyboard.add(key_delete_shedule)
        keyboard.add(key_show_shedule)
        keyboard.add(key_go_back)
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        bot.edit_message_text('🗓 Раздел расписание:', self.call.message.chat.id, self.call.message.message_id,
                              reply_markup=keyboard)

    def add_shedule_select_worker(self):
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
        res = db.get_workers(-1)
        for id, name in res:
            key_s = telebot.types.InlineKeyboardButton(text=str(name),
                                                       callback_data='select_shedule_worker_id' + '/' + str(id))
            keyboard.add(key_s)
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад', callback_data='shedule')
        keyboard.add(key_go_back)
        bot.edit_message_text('👩🏻‍💼 Выберете сотрудника:', self.call.message.chat.id, self.call.message.message_id,
                              reply_markup=keyboard)
        #bot.send_message(self.call.message.chat.id, 'Выберете сотрудника:', reply_markup=keyboard)
        bot.answer_callback_query(callback_query_id=self.call.id, show_alert=False, text="Выберете сотрудника:")

    def add_shedule_select_service(self, callbackstr):
        bot.answer_callback_query(callback_query_id=self.call.id, show_alert=False, text="Выберете услугу:")
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
        res = db.get_services(-1)
        for id, name, cost in res:
            key_s = telebot.types.InlineKeyboardButton(text=str(name) ,#+ '(' + str(cost) + ' руб.)',
                                                       callback_data='select_shedule_service/' + str(
                                                           callbackstr) + '/' + str(id))
            keyboard.add(key_s)
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад', callback_data='add_shedule')
        keyboard.add(key_go_back)
        bot.edit_message_text('💅🏻 Выберете услугу:', self.call.message.chat.id, self.call.message.message_id, reply_markup=keyboard)

    def add_shedule_select_shiftdate(self, callbackstr, enddate):

        bot.answer_callback_query(callback_query_id=self.call.id, show_alert=False, text="Выберете дату:")
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
        if enddate == 0:
            now = dt.Current_Now_Str()
        else:
            now = enddate
        i = 0
        buttons = []
        pg_buttons = []
        while i < 16:
            date = datetime.datetime.strftime(now + datetime.timedelta(i), '%d.%m.%Y')
            key_s = telebot.types.InlineKeyboardButton(text=str(date),
                                                       callback_data='select_shiftdate/' + str(callbackstr) + '/' + str(
                                                           date))
            buttons.append(key_s)
            i += 1
            if i == 15:
                enddate = date

        keyboard.add(*buttons)
        key_back = telebot.types.InlineKeyboardButton(text='⬅️️',
                                                      callback_data='add_shedule_select_shiftdate_back/' + str(
                                                          callbackstr) + '/' + str(enddate))
        pg_buttons.append(key_back)
        key_next = telebot.types.InlineKeyboardButton(text='➡️',
                                                      callback_data='add_shedule_select_shiftdate_next/' + str(
                                                          callbackstr) + '/' + str(enddate))
        pg_buttons.append(key_next)
        keyboard.add(*pg_buttons)
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
                                                         callback_data='select_shedule_worker_id/' + str(callbackstr))
        keyboard.add(key_go_back)
        bot.edit_message_text('📅 Выберете дату:', self.call.message.chat.id, self.call.message.message_id, reply_markup=keyboard)

    def add_shedule_select_begintime(self, callbackstr):
        bot.answer_callback_query(callback_query_id=self.call.id, show_alert=False, text="Выберете время начала:")
        userid, serviceid, shiftdate = callbackstr.split('/')[:]
        sh = dt.DateStrToFloat(shiftdate)
        shstr = ''
        res = db.get_shedule(userid, sh, -1)
        i = 1

        for id, name, service, shdate, begintime, endtime in res:
            if shstr == '':
                shstr = '📅 На дату [' + dt.DateToStr(shdate, 1) + ']' + '\nУ мастера: ' + str(
                    name) + ' есть расписание!\n\n🗓' + str(i) + '. [' + dt.IntToTimeStr(
                    begintime) + ' - ' + dt.IntToTimeStr(
                    endtime) + '].\nУслуга: ' + str(
                    service)  # + '\n❌Для удаления нажмите: '  + '/del_sh_' + str(id) + '\n'
            else:
                shstr = shstr + '\n🗓' + str(i) + '. [' + dt.IntToTimeStr(begintime) + ' - ' + dt.IntToTimeStr(
                    endtime) + '].\nУслуга: ' + str(
                    service)  # + '\n❌Для удаления нажмите: ' + '/del_sh_' + str(id)+ '\n'
            i += 1

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=5)
        buttons = []
        format = '%H:%M'
        tm = datetime.datetime.strptime('07:00', format)

        i = 0

        while i < 15:
            t = datetime.datetime.strftime(tm + datetime.timedelta(hours=i), '%H:%M')
            key_s = telebot.types.InlineKeyboardButton(text=str(t), callback_data='select_begintime/'
                                                                                  + str(callbackstr) + '/' + str(t))
            buttons.append(key_s)
            i += 1
        keyboard.add(*buttons)

        if shstr == '':
            shstr = '\n🕓 Выберете время начала работы: '
        else:
            shstr = shstr + '\n\n🕓 Выберете время начала работы не пересекающиеся с имеющимся расписанием: '

        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
                                                         callback_data='select_shedule_worker_id/' + str(callbackstr))
        keyboard.add(key_go_back)
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        bot.edit_message_text(shstr, self.call.message.chat.id, self.call.message.message_id,
                              reply_markup=keyboard)

    def add_shedule_select_endtime(self, callbackstr):
        bot.answer_callback_query(callback_query_id=self.call.id, show_alert=False, text="Выберете время окончания:")

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=5)
        buttons = []
        format = '%H:%M'
        tm = datetime.datetime.strptime('07:00', format)
        i = 0

        while i < 15:
            t = datetime.datetime.strftime(tm + datetime.timedelta(hours=i), '%H:%M')
            key_s = telebot.types.InlineKeyboardButton(text=str(t), callback_data='select_endtime/'
                                                                                  + str(callbackstr) + '/' + str(t))
            buttons.append(key_s)
            i += 1
        keyboard.add(*buttons)
        userid, serviceid, shiftdate, begintime = callbackstr.split('/')[:]
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
                                                         callback_data='select_shiftdate/' + str(userid)+'/'+str(serviceid)+'/'+str(shiftdate))
        keyboard.add(key_go_back)
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        bot.edit_message_text('🕓 Выберете время окончания работы:', self.call.message.chat.id, self.call.message.message_id,
                              reply_markup=keyboard)

    def add_shedule_select_step(self, callbackstr):
        bot.answer_callback_query(callback_query_id=self.call.id, show_alert=False,
                                  text="Выберете продолжительность 1 процедуры(в мин.):")
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
        buttons = []
        step = 30
        i = 0
        while i < 180:
            i += step
            key_s = telebot.types.InlineKeyboardButton(text=str(i),
                                                       callback_data='select_step/' + str(callbackstr) + '/' + str(i))
            buttons.append(key_s)
        keyboard.add(*buttons)
        userid, serviceid, shiftdate, begintime, endtime = callbackstr.split('/')[:]
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
                                                         callback_data='select_begintime/' + str(userid) + '/' + str(
                                                             serviceid) + '/' + str(shiftdate) + '/' +str(begintime))
        keyboard.add(key_go_back)
        bot.edit_message_text('🕓 Выберете время одной процедуры\n(в мин.):', self.call.message.chat.id,
                              self.call.message.message_id,
                              reply_markup=keyboard)

    # def add_shedule_select_cost(self, callbackstr ):
    #
    #     bot.answer_callback_query(callback_query_id=self.call.id, show_alert=False,
    #                               text="Укажите стоимость услуги:")
    #     #bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
    #     bot.edit_message_text('💵 Укажите стоимость услуги:', self.call.message.chat.id,
    #                           self.call.message.message_id)
    #     bot.register_next_step_handler(self.call.message, self.add_shedule, callbackstr)


    def add_shedule(self, callbackstr):


        userid, serviceid, shiftdate, begintime, endtime, step = callbackstr.split('/')[:]
        st = dt.TimeStrToInt(begintime)
        et = dt.TimeStrToInt(endtime)
        crdate = dt.Current_Now()
        sh = dt.DateStrToFloat(shiftdate)

        shdata = []
        tldata = []

        shdata.append((userid, serviceid, crdate, sh, st, et))
        while st < et:
            tldata.append([crdate, st, st + int(step)])
            st += int(step)

        res = db.add_user_shedule(shdata, tldata)
        gc_dict = []
        if len(res) > 0:
            for gcalendarid, talonid, shiftdate, begintime, endtime in res:
                start = dt.DateToDateIsoformat(shiftdate + (begintime / 1440))
                end = dt.DateToDateIsoformat(shiftdate + (endtime / 1440))
                event = {
                    "summary": 'Свободное время',
                    "description": '',
                    "start": {"dateTime": start, "timeZone": 'Europe/Moscow'},
                    "end": {"dateTime": end, "timeZone": 'Europe/Moscow'},
                    "colorId": '2',
                    "source": {
                        "url": 'https://t.me/llllllallllll_bot',
                        "title": talonid
                    },
                }
                gc_dict.append((gcalendarid, event))

            events_info = Gcalendar.add_event(gc_dict)
            if len(events_info) > 0:
                db.upd_talon_event(events_info)
            res = 'Запись успешно добавлена! ✅'

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура
        key_add_worker = telebot.types.InlineKeyboardButton(text='✅ Добавить',
                                                            callback_data='add_shedule')
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад', callback_data='shedule')
        key_go_main_menu = telebot.types.InlineKeyboardButton(text='↩️ На главную',
                                                              callback_data='start/2')
        buttons = []
        buttons.append(key_go_back)
        buttons.append(key_add_worker)
        buttons.append(key_go_main_menu)
        keyboard.add(*buttons)
        bot.edit_message_text(res + '\nВыберете пункт:', self.call.message.chat.id, self.call.message.message_id, reply_markup=keyboard)
        #bot.send_message(self.call.message.chat.id, res)
        #bot.send_message(self.call.message.chat.id, 'Выберете пункт:', reply_markup=keyboard)

    def edit_shedule(self):
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        shiftdate = -1
        userid = -1
        res = db.get_shedule(userid, shiftdate, -1)
        bot.edit_message_text('Первые 20 расписаний от текущей даты:', self.call.message.chat.id, self.call.message.message_id)
        for id, username, servicename, shiftdate, begintime, endtime, cost in res:
            buttons = []
            keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
            key_delete = telebot.types.InlineKeyboardButton(text=str('Удалить ❌'),
                                                            callback_data='shedule_delete' + '/' + str(id))
            buttons.append(key_delete)
            keyboard.add(*buttons)
            bot.send_message(self.call.message.chat.id, '🗓 Расписание: \n\n📅  Дата: ' + dt.DateToStr(shiftdate, 1) +
                             '\n🕓  Время: [' + dt.IntToTimeStr(begintime) + ' - ' + dt.IntToTimeStr(endtime) + ']' +
                             '\n👩🏻‍💼  Мастер: ' + str(username) +
                             '\n💅🏻  Услуга: ' + str(servicename), reply_markup=keyboard)

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
                                                         callback_data='shedule')
        keyboard.add(key_go_back)
        bot.send_message(self.call.message.chat.id, 'Вернуться назад:', reply_markup=keyboard)

    def delete_shedule(self):
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        sheduleid = self.call.data.split('/', 1)[1]

        res = db.get_shedule(-1, -1, sheduleid)
        username    = res[0][1]
        servicename = res[0][2]
        shiftdate   = res[0][3]
        begintime   = res[0][4]
        endtime     = res[0][5]
        cost        = res[0][6]

        db.del_shedule(sheduleid)

        bot.answer_callback_query(callback_query_id=self.call.id, show_alert=True, text="Запись успешно удалена!")
        bot.edit_message_text('🗓 Расписание: \n\n📅  Дата: ' + dt.DateToStr(shiftdate, 1) +
                             '\n🕓  Время: [' + dt.IntToTimeStr(begintime) + ' - ' + dt.IntToTimeStr(endtime) + ']' +
                             '\n👩🏻‍💼  Мастер: ' + str(username) +
                             '\n💅🏻  Услуга: ' + str(servicename) +
                             '❌', self.call.message.chat.id, self.call.message.message_id)

        events = db.get_talons(sheduleid)
        for calendarId, eventid in events:
            Gcalendar.delete_event(calendarId, eventid)

    def show_shedule(self):
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        res = db.get_shedules_days()

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
        buttons = []
        for shiftdate in res:
            key = telebot.types.InlineKeyboardButton(text=str(dt.DateToStr(shiftdate[0], 1)),
                                                     callback_data='show_shedule_day/' + str(shiftdate[0]))
            buttons.append(key)

        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
                                                         callback_data='shedule')
        keyboard.add(*buttons)
        keyboard.add(key_go_back)
        bot.edit_message_text('Первые 30 дней  в которых есть расписание:', self.call.message.chat.id,
                              self.call.message.message_id, reply_markup=keyboard)

    def show_shedule_day(self, shiftdate):
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        res = db.get_shedule(-1, shiftdate, -1)

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        buttons = []
        msg = '📅 Дата: ' + dt.DateToStr(int(shiftdate), 1)
        old_user_name = ''
        old_user_service = ''

        for shid, user_name, servie_name, shiftdate, begintime, endtime, client_name, phone, cost in res:
           if old_user_name == user_name:
               if old_user_service == servie_name:
                   msg = msg + '\n🕗' + str(dt.IntToTimeStr(begintime)) + ' ' + str(client_name or '') + ' ' + str(phone or '')
               else:
                   msg = msg + '\n' + '\n💅🏻Услуга: ' + str(servie_name) + '\n🕗' + str(
                       dt.IntToTimeStr(begintime)) + ' ' + str(client_name or '') + ' ' + str(phone or '')
           else:
               msg = msg + '\n' + '\n👩🏻‍💼 Мастер:' + str(user_name)
               if old_user_service == servie_name:
                   msg = msg + '\n🕗' + str(dt.IntToTimeStr(begintime)) + ' ' + str(client_name or '') + ' ' + str(phone or '')
               else:
                   msg = msg + '\n' + '\n💅🏻Услуга: ' + str(servie_name) + '\n🕗' + str(
                       dt.IntToTimeStr(begintime)) + ' ' + str(client_name or '') + ' ' + str(phone or '')

           old_user_service = servie_name
           old_user_name = user_name



        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад', callback_data='show_shedule')
        keyboard.add(key_go_back)
        keyboard.add(*buttons)
        bot.edit_message_text(msg, self.call.message.chat.id, self.call.message.message_id, reply_markup=keyboard)

class Registration:
    """Класс записи по услуги"""

    def __init__(self, call):
        self.call = call

    def reg_select_service(self):
        bot.answer_callback_query(callback_query_id=self.call.id, show_alert=False, text="Выберете услугу:")
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
        res = db.get_services(-1)
        for id, name, cost in res:
            key_s = telebot.types.InlineKeyboardButton(text='💅🏻 ' + str(name) ,
                                                       callback_data='reg_select_service/' + str(id))
            keyboard.add(key_s)
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад', callback_data='start/2')
        keyboard.add(key_go_back)
        bot.edit_message_text('🛍 Выберете услугу:', self.call.message.chat.id, self.call.message.message_id,
                              reply_markup=keyboard)

    def reg_check_pat_employed_talons(self, callbackstr):
        res = db.get_clients_booked_talons(self.call.message.chat.id, callbackstr)
        if len(res) == 0:
            self.reg_select_date(callbackstr)
        else:
            bot.answer_callback_query(callback_query_id=self.call.id, show_alert=True,
                                      text="У вас уже есть запись на данную услугу, сперва отмените старую запись:")
            for talonid, shiftdate, begintime, endtime, username, serviceid, servicename, cost in res:
                sendingmsg = '📅 Дата: ' + dt.DateToStr(shiftdate, 1) + ' в ' + dt.IntToTimeStr(
                    begintime) + '\n💅🏻 Услуга: ' + str(servicename)  + '\n👩🏻‍💼 Ваш мастер: ' + str(username)
                keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
                key_del_tln = telebot.types.InlineKeyboardButton(text='Отменить запись ❌',
                                                                 callback_data='del_talon' + '/' + str(talonid))
                key_del_msg = telebot.types.InlineKeyboardButton(text='Удалить сообщение 🗑',
                                                                 callback_data='del_msg')
                keyboard.add(key_del_tln)
                keyboard.add(key_del_msg)
                bot.send_message(self.call.message.chat.id, sendingmsg, reply_markup=keyboard)

    def reg_select_date(self, callbackstr):

        serviceid = callbackstr
        res = db.get_shiftdays_with_free_time(serviceid)
        if len(res) == 0:
            bot.answer_callback_query(callback_query_id=self.call.id, show_alert=True,
                                      text="К сожалению, на ближайшие 30 дней нет свободного времени😔\nВыберете другую услугу либо попробуйте позже")
        else:
            bot.answer_callback_query(callback_query_id=self.call.id, show_alert=False, text="Выберете дату:")
            bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
            keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
            buttons = []
            key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад', callback_data='registration')
            for shiftdate in res:
                key = telebot.types.InlineKeyboardButton(text=str(dt.DateToStr(shiftdate[0], 1)),
                                                         callback_data='reg_select_date/' + str(
                                                             serviceid) + '/' + str(shiftdate[0]))
                buttons.append(key)

            keyboard.add(*buttons)
            keyboard.add(key_go_back)
            bot.edit_message_text('Ниже приведены даты в которых есть свободные места для записи:\n\n📅 Выберете дату:',
                                  self.call.message.chat.id, self.call.message.message_id, reply_markup=keyboard)

    def reg_select_time(self, callbackstr):
        serviceid, shiftdate = callbackstr.split('/')[:]
        servicename = db.get_services(serviceid)
        msgstr = '📅 Дата: ' + dt.DateToStr(int(shiftdate), 1) + '\n' + '💅🏻 Услуга: ' + str(
            servicename[0][1]) + '\n\n' + 'Выберете удобное время:'
        bot.answer_callback_query(callback_query_id=self.call.id, show_alert=False, text='Выберете удобное время:')
        bot.edit_message_reply_markup(self.call.message.chat.id, self.call.message.message_id)
        res = db.get_free_shedule_intervals(serviceid, shiftdate)
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        buttons = []
        for id, begintime, endtime, username, cost in res:
            button_text = '🕓 ' + dt.IntToTimeStr(begintime) + ' 👩🏻‍💼 ' + str(username)
            key = telebot.types.InlineKeyboardButton(text=button_text, callback_data='reg_select_time' + '/' + str(id))
            buttons.append(key)
        keyboard.add(*buttons)
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад', callback_data='reg_select_service/' + str(serviceid))

        keyboard.add(key_go_back)
        bot.edit_message_text(msgstr, self.call.message.chat.id, self.call.message.message_id, reply_markup=keyboard)

    def reg_get_patient_phone(self, callbackstr, msg):
        talonid = callbackstr
        taloninfo = db.get_talon(talonid)
        (talonid, shiftdate, begintime, endtime, username, serviceid, servicename, cost, eventid, gcalendarid,
         client_name, phone, tlg_client_name) = taloninfo
        res = db.add_booked_talon(talonid)

        if msg > 0:
            bot.delete_message(self.call.message.chat.id, msg)
        else:
            bot.answer_callback_query(callback_query_id=self.call.id, show_alert=True,
                                      text="Для завершения записи поделитесь\nсвоим номером нажав клавишу ниже\nЕсли не зевершить запись\nв течении 5 минут, данное время станет\nдоступно другим клиентам")
            bot.delete_message(self.call.message.chat.id, self.call.message.message_id)

        # if not res:
        #     bot.answer_callback_query(callback_query_id=self.call.id, show_alert=True,
        #                               text="К сожалению, данное время только что успели занять 😔\nВыберете, другое свободное время🕗")
        #     callback = str(serviceid) + '/' + str(shiftdate)
        #     self.reg_select_time(callback)
        # else:
            #bot.answer_callback_query(callback_query_id=self.call.id, show_alert=True,
            #                          text="Для завершения записи\nподелитесь своим номером\nнажав клавишу ниже\nЕсли не зевершить запись\nв течении 5 минут, данное время станет\nдоступно другим клиентам")

        sendmsg = '📅  Дата: ' + dt.DateToStr(shiftdate, 1) + '\n' + '🕗  Время: ' + dt.IntToTimeStr(
            begintime) + ' - ' + dt.IntToTimeStr(endtime) + '\n💅🏻  Услуга: ' + str(
            servicename) + '\n' + '👩🏻‍💼  Мастер: ' + str(username) + '\n\n📱 Поделитесь вашим номером телефона:'

        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button_phone = telebot.types.KeyboardButton(text="Поделиться номером телефона ✅", request_contact=True)
        keyboard.add(button_phone)
        send = bot.send_message(self.call.message.chat.id, sendmsg, reply_markup=keyboard)
        old_message = send.message_id
        bot.register_next_step_handler(send, self.reg_book_talon, talonid, old_message, self.call.id) #, self.call.id)

    def reg_book_talon(self, message, talonid, old_message, callid):

        try:
            message.contact.phone_number.isdigit()
            talon_status = db.get_talon_status(talonid)
            if talon_status:
                phone = str(message.contact.phone_number)
                if phone[0] == '+':
                    phone = '8' + str(message.contact.phone_number)[2:12]
                else:
                    phone = '8' + str(message.contact.phone_number)[1:11]

                chatid = message.chat.id
                tlg_clientid = message.from_user.id
                client_name = message.from_user.first_name
                tlg_client_name = message.from_user.username
                res = db.add_client_talon(talonid, chatid, tlg_clientid, client_name, tlg_client_name, phone)
                if res:
                    taloninfo = db.get_talon(talonid)
                    (talonid, shiftdate, begintime, endtime, username, serviceid, servicename, cost, eventid,
                     gcalendarid, client_name, phone, tlg_client_name) = taloninfo
                    event_star = dt.DateToDateIsoformat(shiftdate + (begintime / 1440))
                    event_end = dt.DateToDateIsoformat(shiftdate + (endtime / 1440))
                    colorId = 4
                    Gcalendar.update_event(gcalendarid, eventid, event_star, event_end, talonid, client_name, phone, str('https://t.me/'+tlg_client_name),
                                           colorId)
                    sendingmsg = '✅ Время забронировано!\n\n📅 Дата: ' + dt.DateToStr(shiftdate,
                                                                                      1) + ' в ' + dt.IntToTimeStr(
                        begintime) + '\n💅🏻 Услуга: ' + str(servicename) + '\n👩🏻‍💼 Ваш мастер: ' + str(username)
                    buttons = []
                    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
                    key_del_tln = telebot.types.InlineKeyboardButton(text='Отменить запись ❌',
                                                                     callback_data='del_talon' + '/' + str(talonid))
                    key_del_msg = telebot.types.InlineKeyboardButton(text='Удалить сообщение 🗑',
                                                                     callback_data='del_msg')
                    keyboard.add(key_del_tln)
                    keyboard.add(key_del_msg)

                    keyboard.add(*buttons)
                    bot.delete_message(self.call.message.chat.id, message.message_id)
                    bot.delete_message(self.call.message.chat.id, old_message)
                    bot.send_message(self.call.message.chat.id, sendingmsg, reply_markup=keyboard)

                    ftalons = db.get_free_talons(serviceid, shiftdate, begintime, self.call.message.chat.id)

                    for talonid, shiftdate, begintime, endtime, username, serviceid, servicename, cost in ftalons:
                        sendingmsg = 'В это же время можно\nзаписаться на другую услугу\nНе хотите забронировать?\nЕсли в течении 5 минут\nВы не займете данное время,\nоно станет доступно для других людей\n\n📅  Дата: ' + dt.DateToStr(
                            shiftdate, 1) + '\n' + '🕗  Время: ' + dt.IntToTimeStr(
                            begintime) + '\n💅🏻  Услуга: ' + str(
                            servicename) + '\n' + '👩🏻‍💼  Мастер: ' + str(username)
                        keyboard2 = telebot.types.InlineKeyboardMarkup(row_width=3)
                        key_bk = telebot.types.InlineKeyboardButton(text='Да ✅',
                                                                    callback_data='booking_additional_talon/' + str(
                                                                        talonid))
                        key_bkn = telebot.types.InlineKeyboardButton(text='Нет ❌',
                                                                     callback_data='pass_additional_talon/' + str(
                                                                         talonid))
                        buttons = []
                        buttons.append(key_bk)
                        buttons.append(key_bkn)
                        keyboard2.add(*buttons)
                        bot.send_message(self.call.message.chat.id, sendingmsg, reply_markup=keyboard2)
                        db.add_booked_talon(talonid)

                    keyboard3 = telebot.types.InlineKeyboardMarkup(row_width=1)
                    key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Главное меню',
                                                                     callback_data='start/2')
                    keyboard3.add(key_go_back)
                    bot.send_message(self.call.message.chat.id, 'Вернуться в главное меню:', reply_markup=keyboard3)
            else:
                bot.delete_message(self.call.message.chat.id, message.message_id)
                bot.delete_message(self.call.message.chat.id, old_message)
                keyboard3 = telebot.types.InlineKeyboardMarkup(row_width=1)
                key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Главное меню',
                                                                 callback_data='start/2')
                keyboard3.add(key_go_back)
                bot.send_message(self.call.message.chat.id,
                                 'К сожалению, данное время уже занято😔\nт.к. вы не подтвердили его в течении 5 минут. \nВернуться в главное меню:',
                                 reply_markup=keyboard3)
        except Exception as ex:
            self.reg_get_patient_phone(talonid, old_message)


    def booking_additional_talon(self, talonid):

        talon_status = db.get_talon_status(talonid)

        if talon_status:

            chatid = self.call.message.json['chat']['id']
            tlg_clientid = self.call.from_user.id
            cl_name = self.call.from_user.first_name
            tlg_client_name = self.call.from_user.username

            taloninfo = db.get_talon(talonid)
            serviceid = taloninfo[5]
            res = db.get_clients_booked_talons(self.call.message.chat.id, serviceid)

            if len(res) == 0:
                set_talon = db.add_client_talon(talonid, chatid, tlg_clientid, cl_name, tlg_client_name, '')
                if set_talon:
                    taloninfo = db.get_talon(talonid)
                    (talonid, shiftdate, begintime, endtime, username, serviceid, servicename, cost, eventid, gcalendarid,
                    client_name, phone, tlg_client_name) = taloninfo
                    event_star = dt.DateToDateIsoformat(shiftdate + (begintime / 1440))
                    event_end = dt.DateToDateIsoformat(shiftdate + (endtime / 1440))
                    colorId = 4
                    Gcalendar.update_event(gcalendarid, eventid, event_star, event_end, talonid, client_name, phone, str('https://t.me/' + tlg_client_name), colorId)
                    msgstr = '✅ Время забронировано!\n\n📅 Дата: ' + dt.DateToStr(shiftdate, 1) + ' в ' + dt.IntToTimeStr(
                        begintime) + '\n💅🏻 Услуга: ' + str(servicename) + '\n👩🏻‍💼 Ваш мастер: ' + str(
                       username)
                    buttons = []
                    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
                    key_del_tln = telebot.types.InlineKeyboardButton(text='Отменить запись ❌',
                                                                     callback_data='del_talon' + '/' + str(talonid))
                    key_del_msg = telebot.types.InlineKeyboardButton(text='Удалить сообщение 🗑',
                                                                     callback_data='del_msg')
                    keyboard.add(key_del_tln)
                    keyboard.add(key_del_msg)
                    keyboard.add(*buttons)
                    bot.answer_callback_query(callback_query_id=self.call.id, show_alert=True,
                                              text="Время забронировано! ✅")
                    bot.edit_message_text(msgstr, self.call.message.chat.id, self.call.message.message_id,
                                          reply_markup=keyboard)
            else:
                bot.answer_callback_query(callback_query_id=self.call.id, show_alert=True,
                                          text="У вас уже есть запись на данную услугу, сперва отмените старую запись:")
                for talonid, shiftdate, begintime, endtime, username, serviceid, servicename, cost in res:
                    sendingmsg = '📅 Дата: ' + dt.DateToStr(shiftdate, 1) + ' в ' + dt.IntToTimeStr(
                        begintime) + '\n💅🏻 Услуга: ' + str(servicename) + '\n👩🏻‍💼 Ваш мастер: ' + str(username)
                    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
                    key_del_tln = telebot.types.InlineKeyboardButton(text='Отменить запись ❌',
                                                                     callback_data='del_talon' + '/' + str(talonid))
                    key_del_msg = telebot.types.InlineKeyboardButton(text='Удалить сообщение 🗑',
                                                                     callback_data='del_msg')
                    keyboard.add(key_del_tln)
                    keyboard.add(key_del_msg)
                    bot.send_message(self.call.message.chat.id, sendingmsg, reply_markup=keyboard)
        else:
            bot.answer_callback_query(callback_query_id=self.call.id, show_alert=True,
                                      text="Данное время уже занято😔 т.к. вы не подтвердили запись в течении 5 минут ")
            bot.delete_message(self.call.message.chat.id, self.call.message.message_id)

    def del_talon(self, talonid):
        taloninfo = db.get_talon(talonid)
        (talonid, shiftdate, begintime, endtime, username, serviceid, servicename, cost, eventid, gcalendarid,
         client_name, phone, tlg_client_name) = taloninfo
        currdt = math.floor(dt.Current_Now())
        if shiftdate >= currdt:
            res = db.del_talon(talonid)
        else:
            res = False
        if res:
            sendingmsg = 'Запись отменена ❌\n\n📅 Дата: ' + dt.DateToStr(shiftdate, 1) + ' в ' + dt.IntToTimeStr(
                begintime) + '\n💅🏻 Услуга: ' + str(servicename) + '\n👩🏻‍💼 Ваш мастер: ' + str(username)
            bot.edit_message_text(sendingmsg, self.call.message.chat.id, self.call.message.message_id)
            bot.delete_message(self.call.message.chat.id, self.call.message.message_id)
            bot.answer_callback_query(callback_query_id=self.call.id, show_alert=True,
                                      text="Запись отменена ❌")
            event_star = dt.DateToDateIsoformat(shiftdate + (begintime / 1440))
            event_end = dt.DateToDateIsoformat(shiftdate + (endtime / 1440))
            colorId = 2
            Gcalendar.update_event(gcalendarid, eventid, event_star, event_end, talonid, 'Свободное время', '', '', colorId)
        else:
            bot.answer_callback_query(callback_query_id=self.call.id, show_alert=True,
                                      text="Дата талона уже прошла\nЕсли сообщение вам мешает, нажните на кнопку 'Удалить сообщение'")




@bot.message_handler(commands=['start'])
def start_message(message):
    get_main_menu(message, message.from_user.id, message.chat.id, 1)

@bot.callback_query_handler(func=lambda call: True)
def callback_bot(call):


    if 'start' in call.data:  # call.data это callback_data, которую мы указали при объявлении кнопки
        type = call.data.split('/', 1)[1]
        #if int(type) == 2:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        get_main_menu(call, call.from_user.id, call.message.chat.id, type)

    if call.data == 'admin_mode':  # call.data это callback_data, которую мы указали при объявлении кнопки
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы вошли в меню администратора!")
        #bot.delete_message(call.message.chat.id, call.message.message_id)
        get_admin_menu(call)

    if call.data == 'location':  # call.data это callback_data, которую мы указали при объявлении кнопки

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад', callback_data='start/1')
        keyboard.add(key_go_back)
        bot.send_location(call.message.chat.id, 53.518775, 49.314679, reply_markup=keyboard)
        bot.edit_message_text('Наше расположение на карте: 📍', call.message.chat.id, call.message.message_id)

    if call.data == 'information':  # call.data это callback_data, которую мы указали при объявлении кнопки

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад', callback_data='start/2')
        keyboard.add(key_go_back)
        bot.edit_message_text('💅🏻 Салон: TN Studio \n📍 Адрес: г. Тольятти, ТЦ "Арбат", 40 лет\n      победы 65б, офис 302/4\n📲 Телефон: 8(927)218-42-31', call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    if call.data == 'workers':
        worker = Workers(call)
        worker.get_workers_menu()

    if call.data == 'add_worker':
        worker = Workers(call)
        worker.add_worker_name()

    if call.data == 'edit_worker':
        worker = Workers(call)
        worker.edit_worker()

    if 'wrk_delete' in call.data:
        worker = Workers(call)
        worker.delete_worker()

    if call.data == 'services':
        services = Services(call)
        services.get_services_menu()

    if call.data == 'del_msg':
        bot.delete_message(call.message.chat.id, call.message.message_id)


    if call.data == 'add_services':
        services = Services(call)
        services.add_services()

    if 'edit_services' in call.data:
        services = Services(call)
        services.edit_services()

    if 'service_delete' in call.data:  # call.data это callback_data, которую мы указали при объявлении кнопки
        services = Services(call)
        services.delete_services()

    if call.data == 'shedule':
        shedule = Shedule(call)
        shedule.get_shedules_menu()

    elif call.data == 'add_shedule':
        shedule = Shedule(call)
        shedule.add_shedule_select_worker()

    elif 'select_shedule_worker_id' in call.data:
        callbackstr = call.data.split('/')[1]
        shedule = Shedule(call)
        shedule.add_shedule_select_service(callbackstr)

    elif 'select_shedule_service' in call.data:
        callbackstr = call.data.split('/', 1)[1]
        shedule = Shedule(call)
        shedule.add_shedule_select_shiftdate(callbackstr, 0)

    elif 'add_shedule_select_shiftdate_next' in call.data:
        callbackstr = call.data.split('/', 1)[1]
        userid, serviceid, enddate = callbackstr.split('/')[:]
        enddate = datetime.datetime.strptime(enddate, '%d.%m.%Y') + datetime.timedelta(2)
        shedule = Shedule(call)
        shedule.add_shedule_select_shiftdate(str(userid)+'/'+str(serviceid), enddate)

    elif 'add_shedule_select_shiftdate_back' in call.data:
        callbackstr = call.data.split('/', 1)[1]
        userid, serviceid, enddate = callbackstr.split('/')[:]
        shedule = Shedule(call)
        enddate = datetime.datetime.strptime(enddate, '%d.%m.%Y') - datetime.timedelta(30)
        shedule.add_shedule_select_shiftdate(str(userid) + '/' + str(serviceid), enddate)

    elif 'select_shiftdate' in call.data:
        callbackstr = call.data.split('/', 1)[1]
        shedule = Shedule(call)
        shedule.add_shedule_select_begintime(callbackstr)

    elif 'select_begintime' in call.data:
        callbackstr = call.data.split('/', 1)[1]
        shedule = Shedule(call)
        shedule.add_shedule_select_endtime(callbackstr)

    elif 'select_endtime' in call.data:
        callbackstr = call.data.split('/', 1)[1]
        shedule = Shedule(call)
        shedule.add_shedule_select_step(callbackstr)

    elif 'select_step' in call.data:
        callbackstr = call.data.split('/', 1)[1]
        shedule = Shedule(call)
        shedule.add_shedule(callbackstr)

    elif call.data == 'edit_shedule':
        shedule = Shedule(call)
        shedule.edit_shedule()

    elif call.data == 'show_shedule':
        shedule = Shedule(call)
        shedule.show_shedule()

    elif 'show_shedule_day'in call.data:
        callbackstr = call.data.split('/', 1)[1]
        shedule = Shedule(call)
        shedule.show_shedule_day(callbackstr)

    elif 'shedule_delete' in call.data:  # call.data это callback_data, которую мы указали при объявлении кнопки
        shedule = Shedule(call)
        shedule.delete_shedule()

    elif 'registration' in call.data:
        reg = Registration(call)
        reg.reg_select_service()

    elif 'reg_select_service/' in call.data:
        callbackstr = call.data.split('/')[1]
        reg = Registration(call)
        reg.reg_check_pat_employed_talons(callbackstr)
        #reg.reg_select_date(callbackstr)

    elif 'reg_select_date/' in call.data:
        callbackstr = call.data.split('/', 1)[1]
        reg = Registration(call)
        reg.reg_select_time(callbackstr)

    elif 'reg_select_time/' in call.data:
        callbackstr = call.data.split('/', 1)[1]
        reg = Registration(call)
        reg.reg_get_patient_phone(callbackstr, 0)

    elif 'booking_additional_talon/' in call.data:

        callbackstr = call.data.split('/', 1)[1]
        reg = Registration(call)
        reg.booking_additional_talon(callbackstr)

    elif 'pass_additional_talon/' in call.data:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif 'del_talon/' in call.data:
        callbackstr = call.data.split('/', 1)[1]
        reg = Registration(call)
        reg.del_talon(callbackstr)




def get_main_menu(call, userid, chatid, type):
    print(userid)
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)  # наша клавиатура
    key_inf = telebot.types.InlineKeyboardButton(text='Информация о нас ⚒', callback_data='information')
    keyboard.add(key_inf)  # добавляем кнопку в клавиатуру
    key_location = telebot.types.InlineKeyboardButton(text='Как проехать 🚘', callback_data='location')
    keyboard.add(key_location)
    key_url = telebot.types.InlineKeyboardButton(text='Посмотреть работы 💅🏻',
                                                 url='https://instagram.com/nadezhda.nogotok?igshid=1uees69ae5wdj')
    keyboard.add(key_url)
    key_inst = telebot.types.InlineKeyboardButton(text='', callback_data='inst')
    keyboard.add(key_inst)
    key_reg = telebot.types.InlineKeyboardButton(text='Записаться на услугу 💅🏻', callback_data='registration')
    keyboard.add(key_reg)

    if userid == 754897644 or userid == 636283883:
        key_admin_mode = telebot.types.InlineKeyboardButton(text='Настройки ⚙️', callback_data='admin_mode')
        keyboard.add(key_admin_mode)

    if int(type) == 1:
        bot.send_message(chatid,
                         'Выберите интересующий пункт:',
                         reply_markup=keyboard)
    else:
        bot.edit_message_text(
            'Выберите интересующий пункт:'
            , chatid, call.message.message_id, reply_markup=keyboard)

def get_admin_menu(call):

    if call.from_user.id == 754897644 or call.from_user.id == 636283883:

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)  # наша клавиатура
        key_workers = telebot.types.InlineKeyboardButton(text='Сотрудники 💅🏻',
                                                     callback_data='workers')
        key_services = telebot.types.InlineKeyboardButton(text='Услуги 🛍',
                                                      callback_data='services')
        key_shedule = telebot.types.InlineKeyboardButton(text='Расписание 🗓',
                                                     callback_data='shedule')
        key_go_back = telebot.types.InlineKeyboardButton(text='⬅ Назад',
                                                         callback_data='start/2')
        keyboard.add(key_workers)  # добавляем кнопку в клавиатуру
        keyboard.add(key_services)
        keyboard.add(key_shedule)
        keyboard.add(key_go_back)
        bot.edit_message_text('Вы вошли в меню администратора:', call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    else:
        bot.send_message(call.message.chat.id, 'Вы не являетесь администратором бота!')



if __name__ == '__main__':

    bot.skip_pending = True
    bot.polling(none_stop=True, interval=1)



