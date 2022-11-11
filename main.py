import threading
import psycopg2
from core import *
from config import *
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

info = """Чат бот Vkinder. Данный бот подбирает аккауты по заданным условиям и выдает ссылку и 3 самых популярных фотографии подобранного аккаунта. 
Аккаунты подбираются с возрастом от 14 лет. Семейное положение: в активном поиске.  Аккаунты открытые с наличием фото и online в момент поиска.

Команды:
/start - запустить / перезапустить бота;
/next - пролистывать подобранные аккаунты;
/exit - завершить работу бота;
"""

longpoll = VkLongPoll(vk_api.VkApi(token=token_community))
bot = BotVkinder(vk_api.VkApi(token=token_community), vk_api.VkApi(token=token_user), longpoll)


def param_mode(param_event, param):
    count = 0
    if None in param:
        return
    id_list = bot.get_id(param)
    if not id_list:
        bot.write_msg(param_event.user_id, 'Анкеты не найдены')
        return
    bot.send_profile(param_event.user_id, id_list[count])
    result_bd(param_event.user_id, id_list[count])
    if len(id_list) != 1:
        count += 1
    for event_next in longpoll.listen():
        if event_next.type == VkEventType.MESSAGE_NEW and event_next.to_me and event_next.user_id == param_event.user_id:
            if event_next.text.lower() == '/next':
                bot.send_profile(event_next.user_id, id_list[count])
                result_bd(event_next.user_id, id_list[count])
                count += 1
                if count == len(id_list):
                    count = 0
            elif event_next.text.lower() == '/exit' or event_next.text.lower() == '/start':
                break


def start(start_event):
    bot.write_msg(start_event.user_id, 'Выберите режим:\nАвтоматический подбор - 1\nПодбор по параметрам - 2')
    for mode in longpoll.listen():
        if mode.type == VkEventType.MESSAGE_NEW and mode.to_me and mode.user_id == start_event.user_id:
            if mode.text.lower() == '1':
                param_mode(start_event, bot.auto_param(mode.user_id))
                break
            elif mode.text.lower() == '2':
                param_mode(start_event, [bot.age_param(mode.user_id), bot.sex_param(mode.user_id),
                                         bot.city_param(mode.user_id)])
                break
            elif mode.text.lower() == '/start' or mode.text.lower() == '/exit':
                break
            else:
                bot.write_msg(mode.user_id,
                              'Ошибка ввода\nВыберите режим:\nАвтоматический подбор - 1\nПодбор по параметрам -2')


def result_bd(id_user, id_profile):
    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name, port=port)
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO result (id_user, id_profile) VALUES ({id_user}, {id_profile});")
    connection.close()


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.text.lower() == '/start':
            bot.write_msg(event.user_id, info)
            threading.Thread(target=start, name=event.user_id, args=(event,)).start()
