import asyncio

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js

chat_msgs = []
"""Задаём параметр в котором будут наши онлайн пользователи"""
online_users = set()

MAX_MESSAGES_COUNT = 100

async def main():
    """
    Задаём структуру нашего чата
    Создаём интерфейс видимый пользователю
    -----------------------------------------------------------------
    Ввод имени пользователя и проверка на его индивидуальность

    nickname = await input("Войти в чат", required=True, placeholder="Ваше имя",
                           validate=lambda n: "Такой ник уже используется!" if n in online_users or n == '📢' else None)

    -----------------------------------------------------------------
    Вывод сообщения о том, что пользователь присоединился к чату

    chat_msgs.append(('📢', f'`{nickname}` присоединился к чату!'))
    msg_box.append(put_markdown(f'📢 `{nickname}` присоединился к чату'))

    -----------------------------------------------------------------
    Если пользователь присоединился, то предоставляем возможность писать сообщения в чат

    while True:
        data = await input_group("🖂 Новое сообщение", [
            input(placeholder="Текст сообщения ...", name="msg"),
            actions(name="cmd", buttons=["Отправить", {'label': "Выйти из чата", 'type': 'cancel'}])
        ], validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)

        if data is None:
            break

        msg_box.append(put_markdown(f"🖂`{nickname}`: {data['msg']}"))
        chat_msgs.append((nickname, data['msg']))

    refresh_task.close()
    -----------------------------------------------------------------
    Реализуем выход из чата с возможностью переподключения

    online_users.remove(nickname)
    toast("Вы вышли из чата!")
    msg_box.append(put_markdown(f'📢 Пользователь `{nickname}` покинул чат!'))
    chat_msgs.append(('📢', f'Пользователь `{nickname}` покинул чат!'))

    put_buttons(['Перезайти'], onclick=lambda btn: run_js('window.location.reload()'))
    """
    global chat_msgs

    put_markdown("## ▶ Добро пожаловать в чат!\n")

    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)
    """Ввод имени пользователя и проверка на его индивидуальность"""
    nickname = await input("Войти в чат", required=True, placeholder="Ваше имя",
                           validate=lambda n: "Такой ник уже используется!" if n in online_users or n == '📢' else None)
    online_users.add(nickname)
    """Вывод сообщения о том, что пользователь присоединился к чату"""
    chat_msgs.append(('📢', f'`{nickname}` присоединился к чату!'))
    msg_box.append(put_markdown(f'📢 `{nickname}` присоединился к чату'))


    refresh_task = run_async(refresh_msg(nickname, msg_box))
    """Если пользователь присоединился, то предоставляем возможность писать сообщения в чат"""
    while True:
        data = await input_group("🖂 Новое сообщение", [
            input(placeholder="Текст сообщения ...", name="msg"),
            actions(name="cmd", buttons=["Отправить", {'label': "Выйти из чата", 'type': 'cancel'}])
        ], validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)

        if data is None:
            break

        msg_box.append(put_markdown(f"🖂`{nickname}`: {data['msg']}"))
        chat_msgs.append((nickname, data['msg']))

    refresh_task.close()

    """Реализуем выход из чата с возможностью переподключения"""
    online_users.remove(nickname)
    toast("Вы вышли из чата!")
    msg_box.append(put_markdown(f'📢 Пользователь `{nickname}` покинул чат!'))
    chat_msgs.append(('📢', f'Пользователь `{nickname}` покинул чат!'))

    put_buttons(['Перезайти'], onclick=lambda btn: run_js('window.location.reload()'))

print(main.__doc__)

async def refresh_msg(nickname, msg_box):
    """
    -----------------------------------------------------------------
    Работаем с сообщениями пользователей

    global chat_msgs
    last_idx = len(chat_msgs)

    Удаляем сообщения

    while True:
        await asyncio.sleep(1)

        for m in chat_msgs[last_idx:]:
            if m[0] != nickname:  # если нет сообщения от текущего пользователя
                msg_box.append(put_markdown(f"`{m[0]}`: {m[1]}"))

        # удалить просроченный
        if len(chat_msgs) > MAX_MESSAGES_COUNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)
    -----------------------------------------------------------------
    """
    global chat_msgs
    last_idx = len(chat_msgs)
    """Удаляем сообщения"""
    while True:
        await asyncio.sleep(1)

        for m in chat_msgs[last_idx:]:
            if m[0] != nickname:  # если нет сообщения от текущего пользователя
                msg_box.append(put_markdown(f"`{m[0]}`: {m[1]}"))

        # удалить просроченный
        if len(chat_msgs) > MAX_MESSAGES_COUNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)
print(refresh_msg.__doc__)
'''запускаем сервер'''
if __name__ == "__main__":
    start_server(main, debug=True, port=8080, cdn=False)
