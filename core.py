import random
import re
import datetime
from datetime import datetime
from random import randrange
from vk_api.longpoll import VkEventType


class BotVkinder:
    def __init__(self, vk_community, vk_user, longpoll):
        self.vk_community = vk_community
        self.vk_user = vk_user
        self.longpoll = longpoll

    def write_msg(self, user_id, message):
        self.vk_community.method('messages.send', {'user_id': user_id, 'message': message,
                                                   'random_id': randrange(2 ** 31)})

    def send_photo(self, user_id, owner_id, media_id):
        self.vk_community.method('messages.send', {'user_id': user_id, 'random_id': randrange(2 ** 31),
                                                   'attachment': f'photo{owner_id}_{media_id}'})

    def age_param(self, user_id):
        self.write_msg(user_id, 'Введитe возраст:')
        for condition_age in self.longpoll.listen():
            if condition_age.type == VkEventType.MESSAGE_NEW and condition_age.to_me and condition_age.user_id == user_id:
                if condition_age.text.isdigit() and int(condition_age.text) >= 14:
                    age = condition_age.text
                    return age
                elif condition_age.text.lower() == '/start' or condition_age.text.lower() == '/exit':
                    break
                else:
                    self.write_msg(user_id, 'Ошибка ввода\nВведитe возраст:')

    def sex_param(self, user_id):
        self.write_msg(user_id, 'Выберете пол: (женский - 1/ мужской - 2)')
        for condition_gender in self.longpoll.listen():
            if condition_gender.type == VkEventType.MESSAGE_NEW and condition_gender.to_me and condition_gender.user_id == user_id:
                if condition_gender.text.isdigit() and (condition_gender.text == '1' or condition_gender.text == '2'):
                    gender = condition_gender.text
                    return gender
                elif condition_gender.text.lower() == '/start' or condition_gender.text.lower() == '/exit':
                    break
                else:
                    self.write_msg(user_id, 'Ошибка ввода\nВыберете пол: (женский - 1/ мужской - 2)')

    def city_param(self, user_id):
        self.write_msg(user_id, 'Введитe город:')
        for condition_city in self.longpoll.listen():
            if condition_city.type == VkEventType.MESSAGE_NEW and condition_city.to_me and condition_city.user_id == user_id:
                if condition_city.text.lower() == '/start' or condition_city.text.lower() == '/exit':
                    break
                else:
                    city = condition_city.text.capitalize()
                    return city

    def get_id(self, param):
        id_list = []
        req_profile = self.vk_user.method('users.search', {'age_from': param[0], 'age_to': param[0], 'sex': param[1],
                                                           'hometown': param[2], 'status': 6, 'online': 1,
                                                           'has_photo': 1})
        if 'items' in req_profile:
            for prof in req_profile['items']:
                if prof['is_closed'] is False:
                    id_list.append(prof['id'])
            random.shuffle(id_list)
            return id_list
        else:
            return id_list

    def send_profile(self, user_id, id_profile):
        photo_list = []
        req_photo = self.vk_user.method('photos.get', {'owner_id': id_profile, 'album_id': 'profile', 'extended': 1})
        if 'items' in req_photo:
            for photo in req_photo['items']:
                photo_list.append({'id': photo['id'], 'owner_id': photo['owner_id'],
                                   'popularity': photo['likes']['count'] + photo['comments']['count']})
            sort_photo_list = sorted(photo_list, key=lambda photos: photos['popularity'])[::-1][:3]
            if sort_photo_list:
                self.write_msg(user_id, f'https://vk.com/id{sort_photo_list[0]["owner_id"]}')
                for i in sort_photo_list:
                    self.send_photo(user_id, i['owner_id'], i['id'])
        else:
            self.write_msg(user_id, 'Нет фото')

    def auto_param(self, user_id):
        param = self.vk_community.method('users.get', {'user_id': user_id, 'fields': 'bdate, sex, city'})
        if param:
            if 'bdate' in param[0] and re.search(r'\d*\.\d*\.\d*', param[0]['bdate']) is not None:
                age = ((datetime.today() - datetime.strptime(param[0]['bdate'], '%d.%m.%Y')) / 365).days
            else:
                age = self.age_param(user_id)
                if age is None:
                    return [None]
            if param[0]['sex'] == 1:
                gender = 2
            else:
                gender = 1
            if 'city' in param[0]:
                city = param[0]['city']['title']
            else:
                city = self.city_param(user_id)
                if city is None:
                    return [None]
            return [age, gender, city]
        else:
            age = self.age_param(user_id)
            if age is None:
                return [None]
            gender = self.sex_param(user_id)
            if gender is None:
                return [None]
            city = self.city_param(user_id)
            if city is None:
                return [None]
            return [age, gender, city]
