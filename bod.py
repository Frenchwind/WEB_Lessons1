import vk_api
import json
import datetime


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():
    with open('config.json') as config_file:
        config = json.load(config_file)

    login, password = config['login'], config['password']
    club = config['club']

    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler
    )

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return


    vk = vk_session.get_api()
    # Используем метод wall.get
    response = vk.wall.get(count=5, offset=0)
    if response['items']:
        for i in response['items']:
            time = datetime.datetime.fromtimestamp(float(i['date']))
            print(time)
    print('-' * 20)

    response = vk.friends.get(fields="bdate, city")
    if response['items']:
        for i in response['items']:
            print(i)


if __name__ == '__main__':
    main()
