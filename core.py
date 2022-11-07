import random
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

    def get_id(self, param):
        id_list = []
        req_profile = self.vk_user.method('users.search', {'age_from': param[0], 'age_to': param[0], 'sex': param[1],
                                                           'hometown': param[2], 'status': 6, 'online': 1,
                                                           'has_photo': 1})
        for prof in req_profile['items']:
            if prof['is_closed'] is False:
                id_list.append(prof['id'])
        random.shuffle(id_list)
        return id_list

    def send_profile(self, user_id, id_profile):
        photo_list = []
        req_photo = self.vk_user.method('photos.get', {'owner_id': id_profile, 'album_id': 'profile', 'extended': 1})

        for photo in req_photo['items']:
            photo_list.append({'id': photo['id'], 'owner_id': photo['owner_id'],
                               'popularity': photo['likes']['count'] + photo['comments']['count']})
        sort_photo_list = sorted(photo_list, key=lambda photos: photos['popularity'])[::-1][:3]
        if sort_photo_list:
            self.write_msg(user_id, f'https://vk.com/id{sort_photo_list[0]["owner_id"]}')
            for i in sort_photo_list:
                self.send_photo(user_id, i['owner_id'], i['id'])

    def param(self, user_id):
        age = ''
        gender = ''
        city = ''
        self.write_msg(user_id, 'Введитe возраст:')
        for condition_age in self.longpoll.listen():
            if condition_age.type == VkEventType.MESSAGE_NEW and condition_age.to_me and condition_age.user_id == user_id:
                if condition_age.text.isdigit() and int(condition_age.text) >= 14:
                    age = condition_age.text
                    break
                elif condition_age.text.lower() == '/start' or condition_age.text.lower() == '/exit':
                    return
                else:
                    self.write_msg(user_id, 'Ошибка ввода\nВведитe возраст:')
        self.write_msg(user_id, 'Выберете пол: (женский - 1/ мужской - 2)')
        for condition_gender in self.longpoll.listen():
            if condition_gender.type == VkEventType.MESSAGE_NEW and condition_gender.to_me and condition_gender.user_id == user_id:
                if condition_gender.text.isdigit() and (condition_gender.text == '1' or condition_gender.text == '2'):
                    gender = condition_gender.text
                    break
                elif condition_gender.text.lower() == '/start' or condition_gender.text.lower() == '/exit':
                    return
                else:
                    self.write_msg(user_id, 'Ошибка ввода\nВыберете пол: (женский - 1/ мужской - 2)')
        self.write_msg(user_id, 'Введитe город:')
        for condition_city in self.longpoll.listen():
            if condition_city.type == VkEventType.MESSAGE_NEW and condition_city.to_me and condition_city.user_id == user_id:
                if condition_city.text.lower() == '/start' or condition_city.text.lower() == '/exit':
                    return
                else:
                    city = condition_city.text.capitalize()
                    break
        return [age, gender, city]
