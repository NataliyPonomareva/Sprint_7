import allure
import requests

from data import UserCourier
from url_api import Api


class TestLoginCourieInSystem:
    @allure.title('Курьера может авторизоваться')
    def test_authorization_successfully(self, cleanup_courier):
        #'Создаем курьера'
        requests.post(Api.BASE_URL + Api.CREATE_COURIER, json=UserCourier.COURIER_DATA)

        #'Авторизуемся под созданным курьером'
        login_response =requests.post(Api.BASE_URL + Api.COURIER_ID, json=UserCourier.COURIER_DATA_AUTHORIZATION)
        login_response_json = login_response.json()

        # Сохраняем ID курьера для проверки авторизации и последующего удаления созданного курьера
        courier_id = login_response.json().get('id')
        cleanup_courier['courier_id'] = courier_id

        assert login_response.status_code == 200 and login_response_json == {"id": courier_id}, \
            f'Ожидался статус-код 200 и JSON {{"id": {courier_id}}}, но получили статус-код {login_response.status_code} и JSON {login_response_json}'


    @allure.title('Система выдаст ошибку, если указать неверный логин (или авторизоваться под несуществующим пользователем)')
    def test_authorization_invalid_login(self):
        # 'Создаем курьера'
        requests.post(Api.BASE_URL + Api.CREATE_COURIER, json=UserCourier.COURIER_DATA)

        # 'Авторизуемся под созданным курьером - с ошибкой в логине'
        login_response = requests.post(Api.BASE_URL + Api.COURIER_ID, json=UserCourier.COURIER_DATA_LOGIN_INVALID)
        login_response_json = login_response.json()

        assert login_response.status_code == 404 and login_response_json == {'code': 404,'message':  'Учетная запись не найдена'}, \
            f"Ожидался статус-код 404 и JSON {{'code': 404,'message':  'Учетная запись не найдена'}}, но получили статус-код {login_response.status_code} и JSON {login_response_json}"


    @allure.title('Система выдаст ошибку, если указать неверный пароль')
    def test_authorization_invalid_password(self):
        # 'Создаем курьера'
        requests.post(Api.BASE_URL + Api.CREATE_COURIER, json=UserCourier.COURIER_DATA)

        # 'Авторизуемся под созданным курьером - с ошибкой в пароле'
        login_response = requests.post(Api.BASE_URL + Api.COURIER_ID, json=UserCourier.COURIER_DATA_PASSWORD_INVALID)
        login_response_json = login_response.json()

        assert login_response.status_code == 404 and login_response_json == {'code': 404,'message':  'Учетная запись не найдена'}, \
            f"Ожидался статус-код 404 и JSON {{'code': 404,'message':  'Учетная запись не найдена'}}, но получили статус-код {login_response.status_code} и JSON {login_response_json}"


    @allure.title('Система выдаст ошибку, если не указан логин')
    def test_authorization_without_login(self):
        # 'Создаем курьера'
        requests.post(Api.BASE_URL + Api.CREATE_COURIER, json=UserCourier.COURIER_DATA)

        # 'Авторизуемся под созданным курьером - без логина'
        login_response = requests.post(Api.BASE_URL + Api.COURIER_ID, json=UserCourier.COURIER_DATA_WITHOUT_LOGIN)
        login_response_json = login_response.json()

        assert login_response.status_code == 400 and login_response_json == {'code': 400,'message':  'Недостаточно данных для входа'}, \
            f"Ожидался статус-код 400 и JSON {{'code': 400,'message':  'Недостаточно данных для входа'}}, но получили статус-код {login_response.status_code} и JSON {login_response_json}"


    @allure.title('Система выдаст ошибку, если не указан пароль')
    def test_authorization_without_password(self):
        # 'Создаем курьера'
        requests.post(Api.BASE_URL + Api.CREATE_COURIER, json=UserCourier.COURIER_DATA)

        # 'Авторизуемся под созданным курьером - без пароля'
        login_response = requests.post(Api.BASE_URL + Api.COURIER_ID, json=UserCourier.COURIER_DATA_WITHOUT_PASSWORD)
        login_response_json = login_response.json()

        assert login_response.status_code == 400 and login_response_json == {'code': 400,'message':  'Недостаточно данных для входа'}, \
            f"Ожидался статус-код 400 и JSON {{'code': 400,'message':  'Недостаточно данных для входа'}}, но получили статус-код {login_response.status_code} и JSON {login_response_json}"
