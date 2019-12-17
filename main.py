import json
import vk_api
import os
import random

from vk_api.longpoll import VkLongPoll, VkEventType


keylist = ['Меню заказов' , 'О нас' , 'Помочь денюшкой' , 'Вернуться' , 'Холодец-молодец' , 'Просто харкнуть в суп' , 'Состав' , 'Заказать' , 'Гусь в кровавом кляре' , 'Предыстория']

def check(vk):
    answer = {}
    longpoll = VkLongPoll(vk)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.from_user:
                answer['id'] = event.user_id
                answer['message'] = event.text
                return answer

vk_key = 'df7aaa4a744209d0f29fee90106d56e6bd0201ab0509f7b7df9f63ca818b553a9b0cc00d0aaa8f7c96cf4'

main_keyboard = {
    'one_time': False,
    'buttons': [
        [{'color': 'primary', 'action': {'type': 'text' , 'label': 'Меню заказов'}}],
        [{'color': 'primary', 'action': {'type': 'text' , 'label': 'О нас'}}],
        [{'color': 'primary', 'action': {'type': 'text' , 'label': 'Помочь денюшкой'}}],
        [{'color': 'primary', 'action': {'type': 'text' , 'label': 'Вернуться'}}]
    ]
}

menu_keyboard = {
    'one_time': False,
    'buttons': [
        [{'color': 'positive' , 'action': {'type': 'text' , 'label': 'Холодец-молодец'}}],
        [{'color': 'positive' , 'action': {'type': 'text' , 'label': 'Просто харкнуть в суп'}}],
        [{'color': 'positive' , 'action': {'type': 'text' , 'label': 'Гусь в кровавом кляре'}}],
        [{'color': 'primary'  , 'action': {'type': 'text' , 'label': 'Вернуться'}}],
    ]
}

holodec = {
    'one_time': False,
    'buttons': [
        [{'color': 'positive' , 'action': {'type': 'text' , 'label': 'Состав'}}],
        [{'color': 'positive' , 'action': {'type': 'text' , 'label': 'Заказать'}}],
        [{'color': 'primary'  , 'action': {'type': 'text' , 'label': 'Вернуться'}}],
    ]
}

soup = {
    'one_time': False,
    'buttons': [
        [{'color': 'positive' , 'action': {'type': 'text' , 'label': 'Состав'}}],
        [{'color': 'positive' , 'action': {'type': 'text' , 'label': 'Заказать'}}],
        [{'color': 'primary'  , 'action': {'type': 'text' , 'label': 'Вернуться'}}],
    ]
}

gus = {
    'one_time': False,
    'buttons': [
        [{'color': 'positive' , 'action': {'type': 'text' , 'label': 'Состав'}}],
        [{'color': 'positive' , 'action': {'type': 'text' , 'label': 'Предыстория'}}],
        [{'color': 'positive' , 'action': {'type': 'text' , 'label': 'Заказать'}}],
        [{'color': 'primary'  , 'action': {'type': 'text' , 'label': 'Вернуться'}}],
    ]
}
holod_sostav = 'Холодец из рыбы, оливок, молока, изюма и бульона, настоенный в погребе целое десятилетие'
soup_sostav  = 'Ну незнаю даже'
gus_sostav   = 'Кровь девственного гуся, с печенью того же гуся, все это ещё и в кляре'
pred_gus     = 'Предыстория сего блюда достойна отдельного упоминания. Давным давном в Мексике, Майа верили в то что если поднести жертвоприношению богам молодости, а потом испить кровь гуся, можно собсна получить молодость. В качестве даров обычно выступала, туша гуся. Вобщем типа, мы все это собрали,завернули в пищевую пленку, и кинули во фритюр'

about_us = """Мы маленькая но быстро развивающаяся забегаловка.
Пока вы не знаете о нас, но в ближайшем будущем, о нас узнает весь мир.
Сегодня холодец, а завтра весь мир.
"""
def set_random_id():
    return random.randint(0 , 2147483647)

def auth():
    vk = vk_api.VkApi(token=vk_key)
    return vk

def send_message(user_id , message , keyboard):
    vk = auth()
    vk.method('messages.send' , {'user_id': user_id , 'random_id': set_random_id() , 'message': message , 'keyboard': json.dumps(keyboard)})

def back_to_menu(user_id):
    send_message(user_id , 'Выбирайте' , main_keyboard)

def last_message(user_id):
    vk = auth()
    chat = vk.method('messages.getHistory' , {'user_id': user_id})
    if chat['count'] == 0:
        return None
    else:
        last_message = ''
        for item in chat['items'][1:]:
            if item['from_id'] == user_id:
                last_message = item['text']
                break
        return last_message

def main():
    print('| Server started |')
    vk = auth()
    while True:
        lp = check(vk)
        if lp['message'] not in keylist or lp['message'] == 'Вернуться':            
            back_to_menu(lp['id'])
        else:
            if lp['message'] == 'Меню заказов':
                send_message(lp['id'] , 'Вот наше меню' , menu_keyboard)
            elif lp['message'] == 'Холодец-молодец':
                send_message(lp['id'] , 'Хороший выбор' , holodec)
            elif lp['message'] == 'Просто харкнуть в суп':
                send_message(lp['id'] , 'Хороший выбор' , soup)
            elif lp['message'] == 'Гусь в кровавом кляре':
                send_message(lp['id'] , 'Хороший выбор' , gus)
            elif lp['message'] == 'О нас':
                send_message(lp['id'] , about_us , main_keyboard)
            elif lp['message'] == 'Помочь денюшкой':
                send_message(lp['id'] , 'Пока рано' , main_keyboard)
            elif lp['message'] == 'Заказать':
                send_message(lp['id'] , 'Извините, но мы пока не открылись' , main_keyboard)
            elif lp['message'] == 'Предыстория':
                send_message(lp['id'] , pred_gus , gus)

            elif lp['message'] == 'Состав':
                last_user_message = last_message(lp['id'])
                if last_user_message == 'Холодец-молодец':
                    send_message(lp['id'] , 'Вот состав холодца-молодца: {0}'.format(holod_sostav) , holodec)
                elif last_user_message == 'Просто харкнуть в суп':
                    send_message(lp['id'] , '{0}'.format(soup_sostav) , soup)
                elif last_user_message == 'Гусь в кровавом кляре':
                    send_message(lp['id'] , '{0}'.format(gus_sostav) , gus)
                else:
                    send_message(lp['id'] , 'Извините, но я вас не понял' , main_keyboard)
if __name__ == '__main__':
    main()