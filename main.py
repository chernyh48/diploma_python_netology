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


def start(start_event):
    count = 0
    param = bot.param(start_event.user_id)
    if param is None:
        return
    id_list = bot.get_id(param)
    if not id_list:
        bot.write_msg(start_event.user_id, 'Смените параметры поиска')
        return
    bot.send_profile(start_event.user_id, id_list[count])
    result_bd(start_event.user_id, id_list[count])
    if len(id_list) != 1:
        count += 1
    for event_next in longpoll.listen():
        if event_next.type == VkEventType.MESSAGE_NEW and event_next.to_me and event_next.user_id == start_event.user_id:
            if event_next.text.lower() == '/next':
                bot.send_profile(event_next.user_id, id_list[count])
                result_bd(event_next.user_id, id_list[count])
                count += 1
                if count == len(id_list):
                    count = 0
            elif event_next.text.lower() == '/exit' or event_next.text.lower() == '/start':
                break


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
